#!/usr/bin/env python3
"""Fine-tune exact Run52 with the organizer-primary-aligned LambdaLoss."""
from __future__ import annotations

import argparse
import gc
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from kuairand_1k_ranker import (
    SPLITS,
    CachedRows,
    Encoder,
    SparseFM,
    fast_evaluate,
    predict,
    robustness_slices,
    sha256_path,
)


@dataclass(frozen=True)
class LambdaGroup:
    """One bounded user list with exact parent-rank nDCG swap weights."""

    positive_rows: np.ndarray
    negative_rows: np.ndarray
    positive_total: int
    delta_ndcg: np.ndarray


def build_lambda_groups(
    users: np.ndarray,
    labels: np.ndarray,
    parent_scores: np.ndarray,
    row_indices: np.ndarray,
    max_positives: int,
    max_negatives: int,
    seed: int,
) -> tuple[list[LambdaGroup], dict[str, object]]:
    """Build deterministic hard-negative groups without leaking evaluation rows."""
    users = np.asarray(users, dtype=np.int32)
    labels = np.asarray(labels, dtype=np.uint8)
    parent_scores = np.asarray(parent_scores, dtype=np.float32)
    row_indices = np.asarray(row_indices, dtype=np.int64)
    if not (len(users) == len(labels) == len(parent_scores) == len(row_indices)):
        raise ValueError("LambdaLoss source arrays must have identical lengths")
    if max_positives <= 0 or max_negatives <= 0:
        raise ValueError("LambdaLoss row caps must be positive")
    if not np.isfinite(parent_scores).all():
        raise ValueError("LambdaLoss parent scores must be finite")

    grouped_order = np.argsort(users, kind="stable")
    grouped_users = users[grouped_order]
    grouped_labels = labels[grouped_order]
    grouped_scores = parent_scores[grouped_order]
    grouped_rows = row_indices[grouped_order]
    starts = np.r_[0, np.flatnonzero(grouped_users[1:] != grouped_users[:-1]) + 1]
    ends = np.r_[starts[1:], len(grouped_users)]
    rng = np.random.default_rng(seed)
    groups: list[LambdaGroup] = []
    informative_ndcg = 0
    selected_positive_rows = 0
    selected_negative_rows = 0
    for start, end in zip(starts, ends):
        group_labels = grouped_labels[start:end]
        positive_local = np.flatnonzero(group_labels == 1)
        negative_local = np.flatnonzero(group_labels == 0)
        if not len(positive_local) or not len(negative_local):
            continue
        selected_positive = positive_local
        if len(selected_positive) > max_positives:
            selected_positive = np.sort(
                rng.choice(selected_positive, size=max_positives, replace=False)
            )
        negative_order = np.argsort(
            -grouped_scores[start:end][negative_local], kind="stable"
        )
        selected_negative = negative_local[negative_order[:max_negatives]]

        parent_order = np.argsort(-grouped_scores[start:end], kind="stable")
        ranks = np.empty(len(parent_order), dtype=np.int64)
        ranks[parent_order] = np.arange(len(parent_order), dtype=np.int64)
        discounts = np.zeros(len(parent_order), dtype=np.float64)
        top = ranks < 5
        discounts[top] = 1.0 / np.log2(ranks[top].astype(np.float64) + 2.0)
        ideal_count = min(len(positive_local), 5)
        ideal_ranks = np.arange(ideal_count, dtype=np.float64)
        ideal_dcg = float((1.0 / np.log2(ideal_ranks + 2.0)).sum())
        delta = np.abs(
            discounts[selected_positive, None]
            - discounts[selected_negative][None, :]
        ) / max(ideal_dcg, 1e-12)
        delta = delta.astype(np.float32)
        if float(delta.sum()) > 0.0:
            informative_ndcg += 1
        groups.append(
            LambdaGroup(
                positive_rows=grouped_rows[start:end][selected_positive].copy(),
                negative_rows=grouped_rows[start:end][selected_negative].copy(),
                positive_total=int(len(positive_local)),
                delta_ndcg=delta,
            )
        )
        selected_positive_rows += len(selected_positive)
        selected_negative_rows += len(selected_negative)
    metadata = {
        "source_rows": int(len(users)),
        "users": int(len(starts)),
        "usable_users": int(len(groups)),
        "informative_ndcg_users": int(informative_ndcg),
        "selected_positive_rows": int(selected_positive_rows),
        "selected_negative_rows": int(selected_negative_rows),
        "max_positives_per_user": int(max_positives),
        "max_negatives_per_user": int(max_negatives),
        "positive_rule": "seeded_uniform_without_replacement",
        "negative_rule": "highest_exact_parent_score",
        "rank_reference": "complete_exact_parent_scored_training_user_list",
    }
    return groups, metadata


def metric_aligned_lambda_loss(
    scores: torch.Tensor, groups: list[LambdaGroup]
) -> torch.Tensor:
    """Equal organizer-primary proxy: positive-weighted AUC plus user nDCG@5."""
    auc_numerator = scores.new_zeros(())
    positive_total = 0
    ndcg_losses: list[torch.Tensor] = []
    offset = 0
    for group in groups:
        positive_count = len(group.positive_rows)
        negative_count = len(group.negative_rows)
        size = positive_count + negative_count
        group_scores = scores[offset : offset + size]
        offset += size
        positive_scores = group_scores[:positive_count]
        negative_scores = group_scores[positive_count:]
        pair_loss = F.softplus(
            -(positive_scores[:, None] - negative_scores[None, :])
        )
        auc_numerator = auc_numerator + group.positive_total * pair_loss.mean()
        positive_total += group.positive_total
        delta = torch.from_numpy(group.delta_ndcg).to(
            device=scores.device, dtype=scores.dtype
        )
        delta_sum = delta.sum()
        if float(delta_sum.detach()) > 0.0:
            ndcg_losses.append((delta * pair_loss).sum() / delta_sum)
    if offset != len(scores) or positive_total <= 0:
        raise ValueError("LambdaLoss score/group alignment failure")
    auc_loss = auc_numerator / positive_total
    ndcg_loss = (
        torch.stack(ndcg_losses).mean()
        if ndcg_losses
        else auc_loss.new_zeros(())
    )
    return 0.5 * auc_loss + 0.5 * ndcg_loss


def load_exact_parent(
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
    if checkpoint.get("legacy_random_unknown_init") not in {None, True}:
        raise ValueError("parent checkpoint uses neutral unknown initialization")
    if not np.array_equal(checkpoint.get("field_dims"), encoder.field_dims):
        raise ValueError("parent field dimensions mismatch")
    if not np.array_equal(checkpoint.get("offsets"), encoder.offsets):
        raise ValueError("parent offsets mismatch")
    if checkpoint["latent"].ndim != 2 or checkpoint["latent"].shape[1] != 32:
        raise ValueError("parent is not rank 32")
    model = SparseFM(
        int(encoder.field_dims.sum()),
        32,
        encoder.offsets,
        seed,
        neutral_unknown_init=False,
    )
    if checkpoint["latent"].shape != model.latent.weight.shape:
        raise ValueError("parent latent shape mismatch")
    if checkpoint["linear"].shape != model.linear.weight.shape:
        raise ValueError("parent linear shape mismatch")
    with torch.no_grad():
        model.latent.weight.copy_(checkpoint["latent"])
        model.linear.weight.copy_(checkpoint["linear"])
    return model, checkpoint


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--split-mode", choices=tuple(SPLITS), required=True)
    parser.add_argument("--parent-checkpoint", type=Path, required=True)
    parser.add_argument("--parent-predictions", type=Path, required=True)
    parser.add_argument("--learning-rate", type=float, default=0.00002)
    parser.add_argument("--batch-users", type=int, default=64)
    parser.add_argument("--max-positives", type=int, default=5)
    parser.add_argument("--max-negatives", type=int, default=20)
    parser.add_argument("--predict-batch-size", type=int, default=262144)
    parser.add_argument("--threads", type=int, default=16)
    parser.add_argument("--seed", type=int, default=2027)
    parser.add_argument("--model-out", type=Path, required=True)
    parser.add_argument("--predictions-out", type=Path, required=True)
    args = parser.parse_args()
    if args.learning_rate <= 0:
        raise ValueError("learning rate must be positive")
    if min(
        args.batch_users,
        args.max_positives,
        args.max_negatives,
        args.predict_batch_size,
        args.threads,
    ) <= 0:
        raise ValueError("batch, cap, and thread settings must be positive")

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
    model, parent_checkpoint = load_exact_parent(
        args.parent_checkpoint, encoder, args.split_mode, args.seed
    )
    with np.load(args.parent_predictions) as archive:
        if not {"valid", "forward"}.issubset(archive.files):
            raise ValueError("parent prediction archive lacks valid/forward arrays")
        stored_parent_valid = np.asarray(archive["valid"], dtype=np.float32)
        stored_parent_forward = np.asarray(archive["forward"], dtype=np.float32)
    epoch_zero_valid = predict(
        model, rows, encoder, valid_indices, args.predict_batch_size
    )
    epoch_zero_forward = predict(
        model, rows, encoder, forward_indices, args.predict_batch_size
    )
    if len(stored_parent_valid) != len(epoch_zero_valid):
        raise ValueError("parent validation prediction length mismatch")
    if len(stored_parent_forward) != len(epoch_zero_forward):
        raise ValueError("parent forward prediction length mismatch")
    parent_error = max(
        float(np.max(np.abs(epoch_zero_valid - stored_parent_valid))),
        float(np.max(np.abs(epoch_zero_forward - stored_parent_forward))),
    )
    if parent_error > 1e-6:
        raise ValueError(f"epoch-zero parent mismatch: {parent_error}")

    valid_users = np.asarray(rows.user[valid_indices], dtype=np.int32)
    valid_labels = np.asarray(rows.label[valid_indices], dtype=np.uint8)
    forward_users = np.asarray(rows.user[forward_indices], dtype=np.int32)
    forward_labels = np.asarray(rows.label[forward_indices], dtype=np.uint8)
    parent_valid = fast_evaluate(valid_users, valid_labels, epoch_zero_valid)
    parent_forward = fast_evaluate(
        forward_users, forward_labels, epoch_zero_forward
    )
    parent_robustness = robustness_slices(
        rows, activity_reference_indices, valid_indices, epoch_zero_valid
    )
    parent_latent = model.latent.weight.detach().clone()
    parent_linear = model.linear.weight.detach().clone()

    train_scores = predict(
        model, rows, encoder, train_indices, args.predict_batch_size
    )
    groups, group_metadata = build_lambda_groups(
        np.asarray(rows.user[train_indices], dtype=np.int32),
        np.asarray(rows.label[train_indices], dtype=np.uint8),
        train_scores,
        train_indices,
        args.max_positives,
        args.max_negatives,
        args.seed + 104729,
    )
    del train_scores
    gc.collect()
    if not groups:
        raise ValueError("LambdaLoss produced no usable user groups")

    optimizer = torch.optim.SparseAdam(
        [model.latent.weight, model.linear.weight], lr=args.learning_rate
    )
    rng = np.random.default_rng(args.seed + 130363)
    epoch_started = time.time()
    group_order = rng.permutation(len(groups))
    losses: list[float] = []
    model.train()
    for start in range(0, len(group_order), args.batch_users):
        batch_groups = [groups[index] for index in group_order[start : start + args.batch_users]]
        batch_rows = np.concatenate(
            [
                rows_part
                for group in batch_groups
                for rows_part in (group.positive_rows, group.negative_rows)
            ]
        )
        fields = torch.from_numpy(encoder.encode(rows, batch_rows))
        optimizer.zero_grad(set_to_none=True)
        scores = model(fields)
        loss = metric_aligned_lambda_loss(scores, batch_groups)
        if not torch.isfinite(loss):
            raise ValueError("LambdaLoss became non-finite")
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))

    candidate_valid_scores = predict(
        model, rows, encoder, valid_indices, args.predict_batch_size
    )
    candidate_forward_scores = predict(
        model, rows, encoder, forward_indices, args.predict_batch_size
    )
    candidate_valid = fast_evaluate(
        valid_users, valid_labels, candidate_valid_scores
    )
    candidate_forward = fast_evaluate(
        forward_users, forward_labels, candidate_forward_scores
    )
    candidate_robustness = robustness_slices(
        rows, activity_reference_indices, valid_indices, candidate_valid_scores
    )
    selected = bool(candidate_valid["primary"] > parent_valid["primary"] + 1e-5)
    if selected:
        final_valid_scores = candidate_valid_scores
        final_forward_scores = candidate_forward_scores
        best_epoch = 1
    else:
        with torch.no_grad():
            model.latent.weight.copy_(parent_latent)
            model.linear.weight.copy_(parent_linear)
        final_valid_scores = epoch_zero_valid
        final_forward_scores = epoch_zero_forward
        best_epoch = 0

    args.model_out.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "variant": "primary_aligned_lambdaloss_finetune",
            "latent": model.latent.weight.detach(),
            "linear": model.linear.weight.detach(),
            "field_dims": encoder.field_dims,
            "offsets": encoder.offsets,
            "feature_set": "history_item_repeat",
            "split_bounds": bounds,
            "split_mode": args.split_mode,
            "seed": args.seed,
            "model_type": "sparse_fm",
            "legacy_random_unknown_init": True,
            "best_epoch": best_epoch,
            "parent_checkpoint_sha256": sha256_path(args.parent_checkpoint),
        },
        args.model_out,
    )
    args.predictions_out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.predictions_out,
        valid=final_valid_scores.astype(np.float32),
        forward=final_forward_scores.astype(np.float32),
    )
    final_valid = fast_evaluate(valid_users, valid_labels, final_valid_scores)
    final_forward = fast_evaluate(
        forward_users, forward_labels, final_forward_scores
    )
    final_robustness = robustness_slices(
        rows, activity_reference_indices, valid_indices, final_valid_scores
    )
    result = {
        "benchmark": rows.manifest["benchmark"],
        "variant": "primary_aligned_lambdaloss_finetune",
        "split_mode": args.split_mode,
        "split_bounds": bounds,
        "train_rows": int(len(train_indices)),
        "valid_rows": int(len(valid_indices)),
        "best_epoch": best_epoch,
        "parent_valid": parent_valid,
        "parent_forward_valid": parent_forward,
        "parent_robustness": parent_robustness,
        "valid": final_valid,
        "forward_valid": final_forward,
        "robustness": final_robustness,
        "candidate_epoch": {
            "epoch": 1,
            "loss": float(np.mean(losses)),
            "valid": candidate_valid,
            "forward_valid": candidate_forward,
            "robustness": candidate_robustness,
            "selected": selected,
            "elapsed_seconds": time.time() - epoch_started,
        },
        "group_metadata": group_metadata,
        "robustness_activity_reference_rows": int(len(activity_reference_indices)),
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
            "epochs": 1,
            "learning_rate": args.learning_rate,
            "batch_users": args.batch_users,
            "max_positives": args.max_positives,
            "max_negatives": args.max_negatives,
            "predict_batch_size": args.predict_batch_size,
            "threads": args.threads,
            "seed": args.seed,
            "auc_weight": 0.5,
            "ndcg_at_5_weight": 0.5,
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
