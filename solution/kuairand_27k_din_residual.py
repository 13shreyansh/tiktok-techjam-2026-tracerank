#!/usr/bin/env python3
"""Train a compact target-aware tag-history residual over an exact FM parent.

The parent checkpoint is frozen.  The residual sees only the candidate tag,
five strictly causal positive-history tags, tab, duration bucket, and time since
the last positive event.  Its final layer starts at zero, so epoch zero exactly
reproduces the supplied parent and is always available as rollback.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
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


class TagDINResidual(nn.Module):
    """Candidate-aware attention over the five most recent positive tags."""

    def __init__(self, tag_count: int, tab_count: int, seed: int) -> None:
        super().__init__()
        torch.manual_seed(seed)
        width = 16
        self.tag = nn.Embedding(tag_count + 1, width, padding_idx=0)
        self.tab = nn.Embedding(tab_count + 1, 4, padding_idx=0)
        self.duration = nn.Embedding(11, 4, padding_idx=0)
        self.recency = nn.Embedding(18, 4, padding_idx=0)
        for embedding in (self.tag, self.tab, self.duration, self.recency):
            nn.init.normal_(embedding.weight, mean=0.0, std=0.01)
            with torch.no_grad():
                embedding.weight[0].zero_()
        self.attention = nn.Sequential(
            nn.Linear(4 * width, 64),
            nn.PReLU(),
            nn.Linear(64, 1),
        )
        self.network = nn.Sequential(
            nn.Linear(4 * width + 4 + 4 + 4 + 2, 64),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(32, 1),
        )
        # Exact-parent initialization is part of the Run77 safety contract.
        nn.init.zeros_(self.network[-1].weight)
        nn.init.zeros_(self.network[-1].bias)

    def forward(
        self,
        parent_logit: torch.Tensor,
        candidate_tag: torch.Tensor,
        history_tags: torch.Tensor,
        tab: torch.Tensor,
        duration: torch.Tensor,
        recency: torch.Tensor,
    ) -> torch.Tensor:
        candidate = self.tag(candidate_tag)
        historical = self.tag(history_tags)
        mask = history_tags.ne(0)
        target = candidate[:, None, :].expand_as(historical)
        attention_input = torch.cat(
            [historical, target, historical - target, historical * target], dim=-1
        )
        attention_logits = self.attention(attention_input).squeeze(-1)
        attention_logits = attention_logits.masked_fill(~mask, -1e4)
        weights = torch.softmax(attention_logits, dim=1) * mask
        weights = weights / weights.sum(1, keepdim=True).clamp_min(1e-6)
        profile = (historical * weights[:, :, None]).sum(1)
        count = mask.sum(1).clamp_min(1).to(candidate.dtype)
        matches = ((history_tags == candidate_tag[:, None]) & mask).sum(1)
        match_fraction = matches.to(candidate.dtype) / count
        has_history = mask.any(1).to(candidate.dtype)
        dense = torch.cat(
            [
                candidate,
                profile,
                candidate * profile,
                torch.abs(candidate - profile),
                self.tab(tab),
                self.duration(duration),
                self.recency(recency),
                match_fraction[:, None],
                has_history[:, None],
            ],
            dim=1,
        )
        return parent_logit + self.network(dense).squeeze(1)


def encode_residual_inputs(
    rows: CachedRows,
    sequence: np.ndarray,
    duration_edges: np.ndarray,
    indices: np.ndarray,
) -> tuple[torch.Tensor, ...]:
    raw_tag = np.asarray(rows.tag[indices], dtype=np.int64)
    candidate = np.where(raw_tag >= 0, raw_tag + 1, 0)
    raw_history = np.asarray(sequence[indices, :5], dtype=np.int64)
    history = np.where(raw_history >= 0, raw_history + 1, 0)
    tab = np.asarray(rows.tab[indices], dtype=np.int64) + 1
    duration = np.searchsorted(
        duration_edges, np.asarray(rows.duration[indices], dtype=np.float32)
    ).astype(np.int64) + 1
    recency = np.asarray(sequence[indices, 10], dtype=np.int64) + 1
    return tuple(
        torch.from_numpy(value)
        for value in (candidate, history, tab, duration, recency)
    )


def load_parent(
    path: Path,
    encoder: Encoder,
    split_mode: str,
    seed: int,
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
    if not np.array_equal(checkpoint.get("field_dims"), encoder.field_dims):
        raise ValueError("parent field dimensions mismatch")
    if not np.array_equal(checkpoint.get("offsets"), encoder.offsets):
        raise ValueError("parent offsets mismatch")
    model = SparseFM(
        int(encoder.field_dims.sum()),
        32,
        encoder.offsets,
        seed,
        neutral_unknown_init=False,
    )
    with torch.no_grad():
        model.latent.weight.copy_(checkpoint["latent"])
        model.linear.weight.copy_(checkpoint["linear"])
    model.requires_grad_(False)
    model.eval()
    return model, checkpoint


def score(
    parent: SparseFM,
    residual: TagDINResidual,
    rows: CachedRows,
    encoder: Encoder,
    sequence: np.ndarray,
    indices: np.ndarray,
    batch_size: int,
) -> np.ndarray:
    output = np.empty(len(indices), dtype=np.float32)
    parent.eval()
    residual.eval()
    with torch.no_grad():
        for start in range(0, len(indices), batch_size):
            batch = indices[start : start + batch_size]
            fields = torch.from_numpy(encoder.encode(rows, batch))
            parent_logit = parent(fields)
            inputs = encode_residual_inputs(rows, sequence, encoder.duration_edges, batch)
            output[start : start + len(batch)] = residual(
                parent_logit, *inputs
            ).numpy()
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, required=True)
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
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    if args.epochs <= 0 or args.patience <= 0:
        raise ValueError("epochs and patience must be positive")
    started = time.time()
    torch.set_num_threads(args.threads)
    rows = CachedRows(args.cache_dir)
    bounds = SPLITS[args.split_mode]
    train_indices = rows.indices(bounds["train"])
    activity_reference_indices = rows.indices(bounds["train"], evaluation=True)
    valid_indices = rows.indices(bounds["valid"], evaluation=True)
    forward_indices = (
        rows.indices(bounds["forward"], evaluation=True)
        if "forward" in bounds
        else None
    )
    encoder = Encoder(
        rows, train_indices, "history_item_repeat", args.split_mode, 1, 1, False
    )
    sequence_manifest_path = args.cache_dir / "sequence_profile_manifest.json"
    sequence_manifest = json.loads(sequence_manifest_path.read_text())
    split_record = sequence_manifest.get("splits", {}).get(args.split_mode)
    if split_record is None:
        raise ValueError(f"no causal sequence archive for {args.split_mode}")
    sequence_path = args.cache_dir / split_record["path"]
    if sha256_path(sequence_path) != split_record["sha256"]:
        raise ValueError("causal sequence archive checksum mismatch")
    sequence = np.load(sequence_path, mmap_mode="r")
    if sequence.shape != (len(rows.user), 11):
        raise ValueError("causal sequence archive shape mismatch")
    parent, parent_checkpoint = load_parent(
        args.parent_checkpoint, encoder, args.split_mode, args.seed
    )
    residual = TagDINResidual(
        int(rows.manifest["tag_count"]), int(rows.manifest["tab_count"]), args.seed
    )
    parent_archive = np.load(args.parent_predictions)
    parent_valid = score(
        parent, residual, rows, encoder, sequence, valid_indices, args.predict_batch_size
    )
    if len(parent_archive["valid"]) != len(parent_valid):
        raise ValueError("parent validation prediction length mismatch")
    valid_parent_error = float(
        np.max(np.abs(parent_valid - np.asarray(parent_archive["valid"])))
    )
    if valid_parent_error > 1e-6:
        raise ValueError(f"epoch-zero parent mismatch: {valid_parent_error}")
    valid_users = np.asarray(rows.user[valid_indices], dtype=np.int32)
    valid_labels = np.asarray(rows.label[valid_indices], dtype=np.uint8)
    parent_metric = fast_evaluate(valid_users, valid_labels, parent_valid)
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
            with torch.no_grad():
                parent_logit = parent(fields)
            inputs = encode_residual_inputs(
                rows, sequence, encoder.duration_edges, batch
            )
            optimizer.zero_grad(set_to_none=True)
            output = residual(parent_logit, *inputs)
            loss = loss_fn(output, torch.from_numpy(labels[positions]))
            loss.backward()
            optimizer.step()
            losses.append(float(loss.detach()))
        valid_scores = score(
            parent, residual, rows, encoder, sequence, valid_indices, args.predict_batch_size
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
        parent, residual, rows, encoder, sequence, valid_indices, args.predict_batch_size
    )
    forward_scores = None
    forward_metric = None
    if forward_indices is not None:
        forward_scores = score(
            parent, residual, rows, encoder, sequence, forward_indices,
            args.predict_batch_size,
        )
        forward_metric = fast_evaluate(
            np.asarray(rows.user[forward_indices], dtype=np.int32),
            np.asarray(rows.label[forward_indices], dtype=np.uint8),
            forward_scores,
        )
    args.model_out.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "variant": "exact_parent_tag_din_residual",
            "state_dict": residual.state_dict(),
            "split_mode": args.split_mode,
            "seed": args.seed,
            "best_epoch": best_epoch,
            "parent_checkpoint_sha256": sha256_path(args.parent_checkpoint),
            "sequence_archive_sha256": split_record["sha256"],
        },
        args.model_out,
    )
    args.predictions_out.parent.mkdir(parents=True, exist_ok=True)
    prediction_record = {"valid": valid_scores.astype(np.float32)}
    if forward_scores is not None:
        prediction_record["forward"] = forward_scores.astype(np.float32)
    np.savez_compressed(args.predictions_out, **prediction_record)
    result = {
        "benchmark": rows.manifest["benchmark"],
        "variant": "exact_parent_tag_din_residual",
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
        "epoch_zero_parent_max_abs_error": valid_parent_error,
        "parent_checkpoint": str(args.parent_checkpoint),
        "parent_checkpoint_sha256": sha256_path(args.parent_checkpoint),
        "parent_predictions": str(args.parent_predictions),
        "parent_predictions_sha256": sha256_path(args.parent_predictions),
        "sequence_archive": str(sequence_path),
        "sequence_archive_sha256": split_record["sha256"],
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
            "history_length": 5,
            "tag_embedding_dim": 16,
            "hidden_dims": [64, 32],
            "dropout": 0.1,
        },
        "parent_best_epoch": parent_checkpoint.get("best_epoch"),
        "elapsed_seconds": time.time() - started,
        "public_test_evaluated": False,
        "score_scope_warning": rows.manifest["score_scope_warning"],
    }
    serializable = json.loads(json.dumps(result, default=str))
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(serializable, indent=2, sort_keys=True) + "\n")
    print("RESULT_JSON=" + json.dumps(serializable, sort_keys=True))


if __name__ == "__main__":
    main()
