#!/usr/bin/env python3
"""Train a shallow nonlinear residual over frozen Run52 field embeddings."""
from __future__ import annotations

import argparse
import copy
import json
import time
from pathlib import Path

import numpy as np
import torch
from torch import nn

from kuairand_1k_ranker import (
    SPLITS,
    CachedRows,
    Encoder,
    SparseFM,
    fast_evaluate,
    robustness_slices,
    sha256_path,
)


class FrozenEmbeddingDeepResidual(nn.Module):
    """Standard compact DeepFM tower with exact-zero residual initialization."""

    def __init__(self, field_count: int, rank: int, seed: int) -> None:
        super().__init__()
        torch.manual_seed(seed)
        self.network = nn.Sequential(
            nn.Linear(field_count * rank, 32),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(16, 1),
        )
        nn.init.zeros_(self.network[-1].weight)
        nn.init.zeros_(self.network[-1].bias)

    def forward(
        self, parent_logit: torch.Tensor, embeddings: torch.Tensor
    ) -> torch.Tensor:
        return parent_logit + self.network(embeddings.flatten(start_dim=1)).squeeze(1)


def load_parent(
    path: Path, encoder: Encoder, split_mode: str, seed: int
) -> tuple[SparseFM, dict[str, object]]:
    checkpoint = torch.load(path, map_location="cpu", weights_only=False)
    if not isinstance(checkpoint, dict):
        raise ValueError("parent checkpoint must contain a dictionary")
    expected = {
        "feature_set": "history_item_repeat",
        "model_type": "sparse_fm",
        "split_mode": split_mode,
        "seed": seed,
    }
    for key, value in expected.items():
        if checkpoint.get(key) != value:
            raise ValueError(
                f"parent checkpoint {key} mismatch: {checkpoint.get(key)!r} != {value!r}"
            )
    # Run52 predates serialization of this flag.  Its exact stored prediction
    # archive is reproduced below before training; an explicit neutral-mode
    # checkpoint is never compatible with the protected parent.
    if checkpoint.get("legacy_random_unknown_init") not in {None, True}:
        raise ValueError("parent checkpoint uses neutral unknown initialization")
    if not np.array_equal(checkpoint.get("field_dims"), encoder.field_dims):
        raise ValueError("parent field dimensions mismatch")
    if not np.array_equal(checkpoint.get("offsets"), encoder.offsets):
        raise ValueError("parent offsets mismatch")
    parent = SparseFM(
        int(encoder.field_dims.sum()),
        32,
        encoder.offsets,
        seed,
        neutral_unknown_init=False,
    )
    with torch.no_grad():
        parent.latent.weight.copy_(checkpoint["latent"])
        parent.linear.weight.copy_(checkpoint["linear"])
    parent.requires_grad_(False)
    parent.eval()
    return parent, checkpoint


def parent_inputs(
    parent: SparseFM, fields: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor]:
    """Compute one frozen parent logit and its aligned field embeddings."""
    with torch.no_grad():
        embeddings = parent.latent(fields)
        summed = embeddings.sum(dim=1)
        interactions = 0.5 * (
            (summed * summed).sum(dim=1)
            - (embeddings * embeddings).sum(dim=(1, 2))
        )
        parent_logit = parent.linear(fields).sum(dim=1).squeeze(1) + interactions
    return parent_logit, embeddings


def score(
    parent: SparseFM,
    residual: FrozenEmbeddingDeepResidual,
    rows: CachedRows,
    encoder: Encoder,
    indices: np.ndarray,
    batch_size: int,
) -> np.ndarray:
    output = np.empty(len(indices), dtype=np.float32)
    residual.eval()
    with torch.no_grad():
        for start in range(0, len(indices), batch_size):
            batch = indices[start : start + batch_size]
            fields = torch.from_numpy(encoder.encode(rows, batch))
            parent_logit, embeddings = parent_inputs(parent, fields)
            output[start : start + len(batch)] = residual(
                parent_logit, embeddings
            ).numpy()
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--split-mode", choices=tuple(SPLITS), required=True)
    parser.add_argument("--parent-checkpoint", type=Path, required=True)
    parser.add_argument("--parent-predictions", type=Path, required=True)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--patience", type=int, default=1)
    parser.add_argument("--learning-rate", type=float, default=0.001)
    parser.add_argument("--batch-size", type=int, default=65536)
    parser.add_argument("--predict-batch-size", type=int, default=262144)
    parser.add_argument("--threads", type=int, default=16)
    parser.add_argument("--seed", type=int, default=2027)
    parser.add_argument("--model-out", type=Path, required=True)
    parser.add_argument("--predictions-out", type=Path, required=True)
    args = parser.parse_args()
    if args.epochs <= 0 or args.patience <= 0:
        raise ValueError("epochs and patience must be positive")
    if args.batch_size <= 0 or args.predict_batch_size <= 0 or args.threads <= 0:
        raise ValueError("batch sizes and threads must be positive")

    started = time.time()
    torch.set_num_threads(args.threads)
    rows = CachedRows(args.cache_dir)
    bounds = SPLITS[args.split_mode]
    train_indices = rows.indices(bounds["train"])
    activity_reference_indices = rows.indices(bounds["train"], evaluation=True)
    valid_indices = rows.indices(bounds["valid"], evaluation=True)
    forward_indices = rows.indices(bounds["forward"], evaluation=True)
    encoder = Encoder(
        rows, train_indices, "history_item_repeat", args.split_mode, 1, 1, False
    )
    parent, parent_checkpoint = load_parent(
        args.parent_checkpoint, encoder, args.split_mode, args.seed
    )
    residual = FrozenEmbeddingDeepResidual(len(encoder.field_dims), 32, args.seed)

    with np.load(args.parent_predictions) as archive:
        if not {"valid", "forward"}.issubset(archive.files):
            raise ValueError("parent prediction archive lacks valid/forward arrays")
        stored_parent_valid = np.asarray(archive["valid"], dtype=np.float32)
        stored_parent_forward = np.asarray(archive["forward"], dtype=np.float32)
    epoch_zero_valid = score(
        parent, residual, rows, encoder, valid_indices, args.predict_batch_size
    )
    if len(stored_parent_valid) != len(epoch_zero_valid):
        raise ValueError("parent validation prediction length mismatch")
    if len(stored_parent_forward) != len(forward_indices):
        raise ValueError("parent forward prediction length mismatch")
    parent_error = float(np.max(np.abs(epoch_zero_valid - stored_parent_valid)))
    if parent_error > 1e-6:
        raise ValueError(f"epoch-zero parent mismatch: {parent_error}")

    valid_users = np.asarray(rows.user[valid_indices], dtype=np.int32)
    valid_labels = np.asarray(rows.label[valid_indices], dtype=np.uint8)
    parent_metric = fast_evaluate(valid_users, valid_labels, epoch_zero_valid)
    best_metric = parent_metric
    best_epoch = 0
    best_state = copy.deepcopy(residual.state_dict())
    optimizer = torch.optim.Adam(residual.parameters(), lr=args.learning_rate)
    loss_fn = nn.BCEWithLogitsLoss()
    labels = np.asarray(rows.label[train_indices], dtype=np.float32)
    rng = np.random.default_rng(args.seed)
    trace: list[dict[str, object]] = []
    bad = 0
    for epoch in range(1, args.epochs + 1):
        epoch_started = time.time()
        residual.train()
        order = rng.permutation(len(train_indices))
        losses: list[float] = []
        for start in range(0, len(order), args.batch_size):
            positions = order[start : start + args.batch_size]
            batch = train_indices[positions]
            fields = torch.from_numpy(encoder.encode(rows, batch))
            parent_logit, embeddings = parent_inputs(parent, fields)
            optimizer.zero_grad(set_to_none=True)
            output = residual(parent_logit, embeddings)
            loss = loss_fn(output, torch.from_numpy(labels[positions]))
            loss.backward()
            optimizer.step()
            losses.append(float(loss.detach()))
        valid_scores = score(
            parent, residual, rows, encoder, valid_indices, args.predict_batch_size
        )
        metric = fast_evaluate(valid_users, valid_labels, valid_scores)
        record = {
            "epoch": epoch,
            "loss": float(np.mean(losses)),
            "valid": metric,
            "elapsed_seconds": time.time() - epoch_started,
        }
        trace.append(record)
        print(
            f"epoch {epoch:2d} loss {record['loss']:.5f} "
            f"GAUC {metric['GAUC']:.6f} nDCG@5 {metric['nDCG@5']:.6f} "
            f"primary {metric['primary']:.6f} {record['elapsed_seconds']:.1f}s",
            flush=True,
        )
        if metric["primary"] > best_metric["primary"] + 1e-5:
            best_metric = metric
            best_epoch = epoch
            best_state = copy.deepcopy(residual.state_dict())
            bad = 0
        else:
            bad += 1
            if bad >= args.patience:
                break

    residual.load_state_dict(best_state)
    valid_scores = score(
        parent, residual, rows, encoder, valid_indices, args.predict_batch_size
    )
    forward_scores = score(
        parent, residual, rows, encoder, forward_indices, args.predict_batch_size
    )
    forward_metric = fast_evaluate(
        np.asarray(rows.user[forward_indices], dtype=np.int32),
        np.asarray(rows.label[forward_indices], dtype=np.uint8),
        forward_scores,
    )
    args.model_out.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "variant": "frozen_embedding_deepfm_residual",
            "state_dict": residual.state_dict(),
            "split_mode": args.split_mode,
            "seed": args.seed,
            "best_epoch": best_epoch,
            "parent_checkpoint_sha256": sha256_path(args.parent_checkpoint),
        },
        args.model_out,
    )
    args.predictions_out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.predictions_out,
        valid=valid_scores.astype(np.float32),
        forward=forward_scores.astype(np.float32),
    )
    result = {
        "benchmark": rows.manifest["benchmark"],
        "variant": "frozen_embedding_deepfm_residual",
        "split_mode": args.split_mode,
        "split_bounds": bounds,
        "train_rows": int(len(train_indices)),
        "valid_rows": int(len(valid_indices)),
        "best_epoch": best_epoch,
        "parent_valid": parent_metric,
        "valid": fast_evaluate(valid_users, valid_labels, valid_scores),
        "forward_valid": forward_metric,
        "robustness": robustness_slices(
            rows, activity_reference_indices, valid_indices, valid_scores
        ),
        "robustness_activity_reference_rows": int(len(activity_reference_indices)),
        "trace": trace,
        "epoch_zero_parent_max_abs_error": parent_error,
        "parent_checkpoint": str(args.parent_checkpoint),
        "parent_checkpoint_sha256": sha256_path(args.parent_checkpoint),
        "parent_predictions": str(args.parent_predictions),
        "parent_predictions_sha256": sha256_path(args.parent_predictions),
        "model_out": str(args.model_out),
        "model_out_sha256": sha256_path(args.model_out),
        "predictions_out": str(args.predictions_out),
        "predictions_out_sha256": sha256_path(args.predictions_out),
        "parameters": {
            "epochs": args.epochs,
            "patience": args.patience,
            "learning_rate": args.learning_rate,
            "batch_size": args.batch_size,
            "predict_batch_size": args.predict_batch_size,
            "threads": args.threads,
            "seed": args.seed,
            "field_count": int(len(encoder.field_dims)),
            "embedding_dim": 32,
            "hidden_dims": [32, 16],
            "dropout": 0.1,
        },
        "parent_best_epoch": parent_checkpoint.get("best_epoch"),
        "elapsed_seconds": time.time() - started,
        "public_test_evaluated": False,
        "score_scope_warning": rows.manifest["score_scope_warning"],
    }
    serializable = json.loads(json.dumps(result, default=str))
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(serializable, indent=2, sort_keys=True) + "\n")
    print("RESULT_JSON=" + json.dumps(serializable, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
