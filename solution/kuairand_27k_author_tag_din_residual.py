#!/usr/bin/env python3
"""Train a zero-initialized creator-and-tag DIN residual over exact Run52."""
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
    SPLITS, CachedRows, Encoder, fast_evaluate, robustness_slices, sha256_path
)
from kuairand_27k_din_residual import load_parent


class AuthorTagDINResidual(nn.Module):
    """Attend to recent positive creators and tags without changing the parent."""

    def __init__(self, author_count: int, tag_count: int, tab_count: int, seed: int) -> None:
        super().__init__()
        torch.manual_seed(seed)
        self.author = nn.Embedding(author_count + 1, 8, padding_idx=0, sparse=True)
        self.tag = nn.Embedding(tag_count + 1, 8, padding_idx=0)
        self.tab = nn.Embedding(tab_count + 1, 4, padding_idx=0)
        self.duration = nn.Embedding(11, 4, padding_idx=0)
        self.recency = nn.Embedding(18, 4, padding_idx=0)
        for embedding in (self.author, self.tag, self.tab, self.duration, self.recency):
            nn.init.normal_(embedding.weight, mean=0.0, std=0.01)
            with torch.no_grad():
                embedding.weight[0].zero_()
        self.attention = nn.Sequential(
            nn.Linear(64, 64), nn.PReLU(), nn.Linear(64, 1)
        )
        self.network = nn.Sequential(
            nn.Linear(78, 64),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(32, 1),
        )
        nn.init.zeros_(self.network[-1].weight)
        nn.init.zeros_(self.network[-1].bias)

    def forward(
        self,
        parent_logit: torch.Tensor,
        candidate_author: torch.Tensor,
        history_authors: torch.Tensor,
        candidate_tag: torch.Tensor,
        history_tags: torch.Tensor,
        tab: torch.Tensor,
        duration: torch.Tensor,
        recency: torch.Tensor,
    ) -> torch.Tensor:
        candidate = torch.cat(
            [self.author(candidate_author), self.tag(candidate_tag)], dim=1
        )
        historical = torch.cat(
            [self.author(history_authors), self.tag(history_tags)], dim=2
        )
        mask = history_authors.ne(0)
        target = candidate[:, None, :].expand_as(historical)
        attention_input = torch.cat(
            [historical, target, historical - target, historical * target], dim=2
        )
        logits = self.attention(attention_input).squeeze(-1).masked_fill(~mask, -1e4)
        weights = torch.softmax(logits, dim=1) * mask
        weights = weights / weights.sum(1, keepdim=True).clamp_min(1e-6)
        profile = (historical * weights[:, :, None]).sum(1)
        count = mask.sum(1).clamp_min(1).to(candidate.dtype)
        author_match = (
            ((history_authors == candidate_author[:, None]) & mask).sum(1).to(candidate.dtype)
            / count
        )
        tag_match = (
            ((history_tags == candidate_tag[:, None]) & mask).sum(1).to(candidate.dtype)
            / count
        )
        dense = torch.cat(
            [
                candidate,
                profile,
                candidate * profile,
                torch.abs(candidate - profile),
                self.tab(tab),
                self.duration(duration),
                self.recency(recency),
                author_match[:, None],
                tag_match[:, None],
            ],
            dim=1,
        )
        return parent_logit + self.network(dense).squeeze(1)


def encode_inputs(
    rows: CachedRows,
    author_sequence: np.ndarray,
    tag_sequence: np.ndarray,
    duration_edges: np.ndarray,
    indices: np.ndarray,
) -> tuple[torch.Tensor, ...]:
    raw_author = np.asarray(rows.author[indices], dtype=np.int64)
    candidate_author = np.where(raw_author >= 0, raw_author + 1, 0)
    raw_history_author = np.asarray(author_sequence[indices], dtype=np.int64)
    history_author = np.where(raw_history_author >= 0, raw_history_author + 1, 0)
    raw_tag = np.asarray(rows.tag[indices], dtype=np.int64)
    candidate_tag = np.where(raw_tag >= 0, raw_tag + 1, 0)
    raw_history_tag = np.asarray(tag_sequence[indices, :5], dtype=np.int64)
    history_tag = np.where(raw_history_tag >= 0, raw_history_tag + 1, 0)
    tab = np.asarray(rows.tab[indices], dtype=np.int64) + 1
    duration = np.searchsorted(
        duration_edges, np.asarray(rows.duration[indices], dtype=np.float32)
    ).astype(np.int64) + 1
    recency = np.asarray(tag_sequence[indices, 10], dtype=np.int64) + 1
    return tuple(
        torch.from_numpy(value)
        for value in (
            candidate_author, history_author, candidate_tag, history_tag,
            tab, duration, recency,
        )
    )


def score(
    parent: nn.Module,
    residual: AuthorTagDINResidual,
    rows: CachedRows,
    encoder: Encoder,
    author_sequence: np.ndarray,
    tag_sequence: np.ndarray,
    indices: np.ndarray,
    batch_size: int,
) -> np.ndarray:
    output = np.empty(len(indices), dtype=np.float32)
    parent.eval(); residual.eval()
    with torch.no_grad():
        for start in range(0, len(indices), batch_size):
            batch = indices[start:start + batch_size]
            parent_logit = parent(torch.from_numpy(encoder.encode(rows, batch)))
            inputs = encode_inputs(
                rows, author_sequence, tag_sequence, encoder.duration_edges, batch
            )
            output[start:start + len(batch)] = residual(parent_logit, *inputs).numpy()
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
    started = time.time(); torch.set_num_threads(args.threads)
    rows = CachedRows(args.cache_dir); bounds = SPLITS[args.split_mode]
    train_indices = rows.indices(bounds["train"])
    activity_reference = rows.indices(bounds["train"], evaluation=True)
    valid_indices = rows.indices(bounds["valid"], evaluation=True)
    forward_indices = rows.indices(bounds["forward"], evaluation=True) if "forward" in bounds else None
    encoder = Encoder(rows, train_indices, "history_item_repeat", args.split_mode, 1, 1, False)
    tag_manifest = json.loads((args.cache_dir / "sequence_profile_manifest.json").read_text())
    tag_record = tag_manifest.get("splits", {}).get(args.split_mode)
    author_manifest = json.loads(
        (args.cache_dir / "positive_author_sequence_manifest.json").read_text()
    )
    author_record = author_manifest.get("splits", {}).get(args.split_mode)
    if tag_record is None or author_record is None:
        raise ValueError("matching tag and author causal sequences are required")
    tag_path = args.cache_dir / tag_record["path"]
    author_path = args.cache_dir / author_record["path"]
    if sha256_path(tag_path) != tag_record["sha256"]:
        raise ValueError("tag sequence checksum mismatch")
    if sha256_path(author_path) != author_record["sha256"]:
        raise ValueError("author sequence checksum mismatch")
    tag_sequence = np.load(tag_path, mmap_mode="r")
    author_sequence = np.load(author_path, mmap_mode="r")
    if tag_sequence.shape != (len(rows.user), 11) or author_sequence.shape != (len(rows.user), 5):
        raise ValueError("causal sequence shape mismatch")
    parent, parent_checkpoint = load_parent(
        args.parent_checkpoint, encoder, args.split_mode, args.seed
    )
    residual = AuthorTagDINResidual(
        int(rows.manifest["author_count"]), int(rows.manifest["tag_count"]),
        int(rows.manifest["tab_count"]), args.seed,
    )
    parent_archive = np.load(args.parent_predictions)
    parent_valid = score(
        parent, residual, rows, encoder, author_sequence, tag_sequence,
        valid_indices, args.predict_batch_size,
    )
    parent_error = float(np.max(np.abs(parent_valid - parent_archive["valid"])))
    if parent_error > 1e-6:
        raise ValueError(f"epoch-zero parent mismatch: {parent_error}")
    valid_users = np.asarray(rows.user[valid_indices], dtype=np.int32)
    valid_labels = np.asarray(rows.label[valid_indices], dtype=np.uint8)
    parent_metric = fast_evaluate(valid_users, valid_labels, parent_valid)
    best_metric = parent_metric; best_epoch = 0
    best_state = copy.deepcopy(residual.state_dict()); bad = 0
    sparse_optimizer = torch.optim.SparseAdam(
        [residual.author.weight], lr=args.learning_rate
    )
    dense_parameters = [
        parameter for name, parameter in residual.named_parameters()
        if name != "author.weight"
    ]
    dense_optimizer = torch.optim.Adam(dense_parameters, lr=args.learning_rate)
    loss_fn = nn.BCEWithLogitsLoss()
    labels = np.asarray(rows.label[train_indices], dtype=np.float32)
    rng = np.random.default_rng(args.seed); trace = []
    for epoch in range(1, args.epochs + 1):
        epoch_started = time.time(); residual.train(); losses = []
        order = rng.permutation(len(train_indices))
        for start in range(0, len(order), args.batch_size):
            positions = order[start:start + args.batch_size]
            batch = train_indices[positions]
            with torch.no_grad():
                parent_logit = parent(torch.from_numpy(encoder.encode(rows, batch)))
            inputs = encode_inputs(
                rows, author_sequence, tag_sequence, encoder.duration_edges, batch
            )
            sparse_optimizer.zero_grad(set_to_none=True)
            dense_optimizer.zero_grad(set_to_none=True)
            loss = loss_fn(
                residual(parent_logit, *inputs), torch.from_numpy(labels[positions])
            )
            loss.backward(); sparse_optimizer.step(); dense_optimizer.step()
            losses.append(float(loss.detach()))
        valid_scores = score(
            parent, residual, rows, encoder, author_sequence, tag_sequence,
            valid_indices, args.predict_batch_size,
        )
        metric = fast_evaluate(valid_users, valid_labels, valid_scores)
        record = {"epoch": epoch, "loss": float(np.mean(losses)), "valid": metric,
                  "elapsed_seconds": time.time() - epoch_started}
        trace.append(record)
        print(
            f"epoch {epoch:2d} loss {record['loss']:.5f} GAUC {metric['GAUC']:.6f} "
            f"nDCG@5 {metric['nDCG@5']:.6f} primary {metric['primary']:.6f} "
            f"{record['elapsed_seconds']:.1f}s", flush=True,
        )
        if metric["primary"] > best_metric["primary"] + 1e-5:
            best_metric = metric; best_epoch = epoch
            best_state = copy.deepcopy(residual.state_dict()); bad = 0
        else:
            bad += 1
            if bad >= args.patience: break
    residual.load_state_dict(best_state)
    valid_scores = score(
        parent, residual, rows, encoder, author_sequence, tag_sequence,
        valid_indices, args.predict_batch_size,
    )
    forward_scores = None; forward_metric = None
    if forward_indices is not None:
        forward_scores = score(
            parent, residual, rows, encoder, author_sequence, tag_sequence,
            forward_indices, args.predict_batch_size,
        )
        forward_metric = fast_evaluate(
            np.asarray(rows.user[forward_indices], dtype=np.int32),
            np.asarray(rows.label[forward_indices], dtype=np.uint8), forward_scores,
        )
    args.model_out.parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "variant": "exact_parent_author_tag_din_residual",
        "state_dict": residual.state_dict(), "split_mode": args.split_mode,
        "seed": args.seed, "best_epoch": best_epoch,
        "parent_checkpoint_sha256": sha256_path(args.parent_checkpoint),
        "tag_sequence_sha256": tag_record["sha256"],
        "author_sequence_sha256": author_record["sha256"],
    }, args.model_out)
    args.predictions_out.parent.mkdir(parents=True, exist_ok=True)
    prediction_record = {"valid": valid_scores.astype(np.float32)}
    if forward_scores is not None: prediction_record["forward"] = forward_scores.astype(np.float32)
    np.savez_compressed(args.predictions_out, **prediction_record)
    result = {
        "benchmark": rows.manifest["benchmark"],
        "variant": "exact_parent_author_tag_din_residual",
        "split_mode": args.split_mode, "split_bounds": bounds,
        "train_rows": int(len(train_indices)), "valid_rows": int(len(valid_indices)),
        "best_epoch": best_epoch, "parent_valid": parent_metric,
        "valid": fast_evaluate(valid_users, valid_labels, valid_scores),
        "forward_valid": forward_metric,
        "robustness": robustness_slices(rows, activity_reference, valid_indices, valid_scores),
        "robustness_activity_reference_rows": int(len(activity_reference)),
        "trace": trace, "epoch_zero_parent_max_abs_error": parent_error,
        "parent_checkpoint_sha256": sha256_path(args.parent_checkpoint),
        "parent_predictions_sha256": sha256_path(args.parent_predictions),
        "tag_sequence_sha256": tag_record["sha256"],
        "author_sequence_sha256": author_record["sha256"],
        "model_out": str(args.model_out), "model_out_sha256": sha256_path(args.model_out),
        "predictions_out": str(args.predictions_out),
        "predictions_out_sha256": sha256_path(args.predictions_out),
        "parameters": {"epochs": args.epochs, "patience": args.patience,
            "learning_rate": args.learning_rate, "batch_size": args.batch_size,
            "predict_batch_size": args.predict_batch_size, "threads": args.threads,
            "seed": args.seed, "history_length": 5, "author_embedding_dim": 8,
            "tag_embedding_dim": 8, "hidden_dims": [64, 32], "dropout": 0.1},
        "parent_best_epoch": parent_checkpoint.get("best_epoch"),
        "elapsed_seconds": time.time() - started, "public_test_evaluated": False,
        "score_scope_warning": rows.manifest["score_scope_warning"],
    }
    serializable = json.loads(json.dumps(result, default=str))
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(serializable, indent=2, sort_keys=True) + "\n")
    print("RESULT_JSON=" + json.dumps(serializable, sort_keys=True))


if __name__ == "__main__": main()
