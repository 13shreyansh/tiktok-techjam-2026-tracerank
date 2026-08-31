#!/usr/bin/env python3
"""Fit a chronological out-of-fold LambdaMART correction to a frozen parent."""
from __future__ import annotations

import argparse
import gc
import json
import time
from pathlib import Path

import numpy as np

from kuairand_1k_ranker import (
    LAMBDAMART_CATEGORICAL_FEATURES,
    LAMBDAMART_FEATURE_NAMES,
    SPLITS,
    CachedRows,
    bounded_query_groups,
    fast_evaluate,
    lambdamart_dense_features,
    load_declared_split_array,
    restore_grouped_predictions,
    robustness_slices,
    sha256_path,
    within_user_percentile_rank,
)


FEATURE_NAMES = (*LAMBDAMART_FEATURE_NAMES, "parent_within_user_rank")
CATEGORICAL_FEATURES = LAMBDAMART_CATEGORICAL_FEATURES


def load_prediction_pair(
    path: Path, valid_rows: int, forward_rows: int
) -> tuple[np.ndarray, np.ndarray]:
    """Load one aligned finite valid/forward prediction pair."""
    with np.load(path) as archive:
        if not {"valid", "forward"}.issubset(archive.files):
            raise ValueError(f"prediction archive lacks valid/forward arrays: {path}")
        valid = np.asarray(archive["valid"], dtype=np.float64)
        forward = np.asarray(archive["forward"], dtype=np.float64)
    if valid.ndim != 1 or len(valid) != valid_rows:
        raise ValueError(f"validation prediction length mismatch: {len(valid)} != {valid_rows}")
    if forward.ndim != 1 or len(forward) != forward_rows:
        raise ValueError(
            f"forward prediction length mismatch: {len(forward)} != {forward_rows}"
        )
    if not np.isfinite(valid).all() or not np.isfinite(forward).all():
        raise ValueError("parent predictions must be finite")
    return valid, forward


def split_sidecars(
    cache_dir: Path, split_mode: str
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Load the three audited causal feature sidecars for one split."""
    return (
        load_declared_split_array(cache_dir, "history_manifest.json", split_mode, 8),
        load_declared_split_array(
            cache_dir, "item_history_manifest.json", split_mode, 4
        ),
        load_declared_split_array(
            cache_dir, "user_entity_history_manifest.json", split_mode, 4
        ),
    )


def parent_aware_features(
    rows: CachedRows,
    indices: np.ndarray,
    sidecars: tuple[np.ndarray, np.ndarray, np.ndarray],
    parent_scores: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Return frozen dense features and the aligned within-user parent rank."""
    indices = np.asarray(indices, dtype=np.int64)
    parent_scores = np.asarray(parent_scores, dtype=np.float64)
    if parent_scores.ndim != 1 or len(parent_scores) != len(indices):
        raise ValueError("parent scores do not align with requested rows")
    if not np.isfinite(parent_scores).all():
        raise ValueError("parent scores must be finite")
    users = np.asarray(rows.user[indices], dtype=np.int64)
    parent_rank = within_user_percentile_rank(users, parent_scores)
    base = lambdamart_dense_features(rows, indices, *sidecars)
    features = np.empty((len(indices), len(FEATURE_NAMES)), dtype=np.float32)
    features[:, :-1] = base
    features[:, -1] = parent_rank.astype(np.float32)
    if not np.isfinite(features).all():
        raise ValueError("parent-aware features must be finite")
    return features, parent_rank


def grouped_parent_aware_matrix(
    rows: CachedRows,
    indices: np.ndarray,
    sidecars: tuple[np.ndarray, np.ndarray, np.ndarray],
    parent_scores: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Group rows stably by user and align features, labels, and init scores."""
    indices = np.asarray(indices, dtype=np.int64)
    users = np.asarray(rows.user[indices], dtype=np.int64)
    order = np.argsort(users, kind="stable")
    features, parent_rank = parent_aware_features(
        rows, indices[order], sidecars, np.asarray(parent_scores)[order]
    )
    ordered_users = users[order]
    raw_groups = np.bincount(
        ordered_users, minlength=int(rows.manifest["user_count"])
    )
    groups = bounded_query_groups(raw_groups[raw_groups > 0], 10_000)
    if int(groups.sum()) != len(indices):
        raise ValueError("group sizes do not cover every meta row")
    labels = np.asarray(rows.label[indices[order]], dtype=np.int32)
    return features, labels, groups, order, parent_rank


def corrected_scores(parent_rank: np.ndarray, tree_delta: np.ndarray) -> np.ndarray:
    """Add the learned tree correction to a frozen within-user parent rank."""
    parent_rank = np.asarray(parent_rank, dtype=np.float64)
    tree_delta = np.asarray(tree_delta, dtype=np.float64)
    if parent_rank.ndim != 1 or tree_delta.ndim != 1 or len(parent_rank) != len(
        tree_delta
    ):
        raise ValueError("parent rank and tree correction must align")
    result = parent_rank + tree_delta
    if not np.isfinite(result).all():
        raise ValueError("corrected scores must be finite")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--model-out", type=Path, required=True)
    parser.add_argument("--predictions-out", type=Path, required=True)
    parser.add_argument("--split-mode", choices=("shadow_early",), required=True)
    parser.add_argument("--stack-split-mode", choices=("stack_early",), required=True)
    parser.add_argument("--stack-parent-predictions", type=Path, required=True)
    parser.add_argument("--target-parent-predictions", type=Path, required=True)
    parser.add_argument("--threads", type=int, default=16)
    parser.add_argument("--seed", type=int, default=2027)
    args = parser.parse_args()
    if args.threads <= 0:
        raise ValueError("threads must be positive")

    import lightgbm as lgb

    started = time.time()
    cache_dir = args.cache_dir.resolve()
    rows = CachedRows(cache_dir)
    stack_bounds = SPLITS[args.stack_split_mode]
    target_bounds = SPLITS[args.split_mode]
    meta_train_indices = rows.indices(stack_bounds["valid"], evaluation=True)
    meta_valid_indices = rows.indices(stack_bounds["forward"], evaluation=True)
    target_valid_indices = rows.indices(target_bounds["valid"], evaluation=True)
    target_forward_indices = rows.indices(target_bounds["forward"], evaluation=True)
    activity_reference_indices = rows.indices(target_bounds["train"], evaluation=True)

    stack_parent_train, stack_parent_valid = load_prediction_pair(
        args.stack_parent_predictions, len(meta_train_indices), len(meta_valid_indices)
    )
    target_parent_valid, target_parent_forward = load_prediction_pair(
        args.target_parent_predictions,
        len(target_valid_indices),
        len(target_forward_indices),
    )
    stack_sidecars = split_sidecars(cache_dir, args.stack_split_mode)
    target_sidecars = split_sidecars(cache_dir, args.split_mode)

    (
        meta_train_features,
        meta_train_labels,
        meta_train_groups,
        meta_train_order,
        meta_train_parent_rank_grouped,
    ) = grouped_parent_aware_matrix(
        rows,
        meta_train_indices,
        stack_sidecars,
        stack_parent_train,
    )
    (
        meta_valid_features,
        meta_valid_labels,
        meta_valid_groups,
        meta_valid_order,
        meta_valid_parent_rank_grouped,
    ) = grouped_parent_aware_matrix(
        rows,
        meta_valid_indices,
        stack_sidecars,
        stack_parent_valid,
    )
    train_dataset = lgb.Dataset(
        meta_train_features,
        label=meta_train_labels,
        group=meta_train_groups,
        init_score=meta_train_parent_rank_grouped,
        feature_name=list(FEATURE_NAMES),
        categorical_feature=list(CATEGORICAL_FEATURES),
        free_raw_data=True,
    )
    valid_dataset = lgb.Dataset(
        meta_valid_features,
        label=meta_valid_labels,
        group=meta_valid_groups,
        init_score=meta_valid_parent_rank_grouped,
        feature_name=list(FEATURE_NAMES),
        categorical_feature=list(CATEGORICAL_FEATURES),
        reference=train_dataset,
        free_raw_data=True,
    )
    parameters = {
        "objective": "lambdarank",
        "metric": "ndcg",
        "ndcg_eval_at": [5],
        "lambdarank_truncation_level": 5,
        "learning_rate": 0.05,
        "num_leaves": 31,
        "min_data_in_leaf": 1000,
        "max_bin": 63,
        "feature_fraction": 1.0,
        "bagging_fraction": 1.0,
        "bagging_freq": 0,
        "verbosity": 1,
        "num_threads": args.threads,
        "seed": args.seed,
        "data_random_seed": args.seed,
        "feature_fraction_seed": args.seed,
        "bagging_seed": args.seed,
        "deterministic": True,
        "force_col_wise": True,
    }
    booster = lgb.train(
        parameters,
        train_dataset,
        num_boost_round=200,
        valid_sets=[valid_dataset],
        valid_names=["meta_valid"],
        callbacks=[lgb.early_stopping(20), lgb.log_evaluation(10)],
    )
    best_iteration = int(booster.best_iteration or 200)
    meta_train_query_count = int(len(meta_train_groups))
    meta_valid_query_count = int(len(meta_valid_groups))

    meta_valid_delta_grouped = booster.predict(
        meta_valid_features, num_iteration=best_iteration, raw_score=True
    )
    meta_valid_delta = restore_grouped_predictions(
        meta_valid_order, meta_valid_delta_grouped
    )
    meta_valid_users = np.asarray(rows.user[meta_valid_indices], dtype=np.int32)
    meta_valid_labels_original = np.asarray(
        rows.label[meta_valid_indices], dtype=np.uint8
    )
    meta_valid_parent_rank = within_user_percentile_rank(
        meta_valid_users, stack_parent_valid
    )
    meta_valid_scores = corrected_scores(meta_valid_parent_rank, meta_valid_delta)
    meta_parent_metrics = fast_evaluate(
        meta_valid_users, meta_valid_labels_original, meta_valid_parent_rank
    )
    meta_corrected_metrics = fast_evaluate(
        meta_valid_users, meta_valid_labels_original, meta_valid_scores
    )

    del train_dataset, valid_dataset, meta_train_features, meta_train_labels
    del meta_train_groups, meta_train_order, meta_train_parent_rank_grouped
    del meta_valid_features, meta_valid_labels, meta_valid_groups
    del meta_valid_parent_rank_grouped
    gc.collect()

    target_valid_features, target_valid_parent_rank = parent_aware_features(
        rows, target_valid_indices, target_sidecars, target_parent_valid
    )
    target_valid_delta = booster.predict(
        target_valid_features, num_iteration=best_iteration, raw_score=True
    )
    target_valid_scores = corrected_scores(
        target_valid_parent_rank, target_valid_delta
    )
    target_valid_users = np.asarray(rows.user[target_valid_indices], dtype=np.int32)
    target_valid_labels = np.asarray(rows.label[target_valid_indices], dtype=np.uint8)
    target_parent_metrics = fast_evaluate(
        target_valid_users, target_valid_labels, target_valid_parent_rank
    )
    target_metrics = fast_evaluate(
        target_valid_users, target_valid_labels, target_valid_scores
    )
    target_robustness = robustness_slices(
        rows,
        activity_reference_indices,
        target_valid_indices,
        target_valid_scores,
    )
    del target_valid_features
    gc.collect()

    target_forward_features, target_forward_parent_rank = parent_aware_features(
        rows, target_forward_indices, target_sidecars, target_parent_forward
    )
    target_forward_delta = booster.predict(
        target_forward_features, num_iteration=best_iteration, raw_score=True
    )
    target_forward_scores = corrected_scores(
        target_forward_parent_rank, target_forward_delta
    )
    target_forward_users = np.asarray(
        rows.user[target_forward_indices], dtype=np.int32
    )
    target_forward_labels = np.asarray(
        rows.label[target_forward_indices], dtype=np.uint8
    )
    target_forward_parent_metrics = fast_evaluate(
        target_forward_users, target_forward_labels, target_forward_parent_rank
    )
    target_forward_metrics = fast_evaluate(
        target_forward_users, target_forward_labels, target_forward_scores
    )

    args.model_out.parent.mkdir(parents=True, exist_ok=True)
    booster.save_model(str(args.model_out), num_iteration=best_iteration)
    importance = booster.feature_importance(
        importance_type="gain", iteration=best_iteration
    )
    args.predictions_out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.predictions_out,
        valid=target_valid_scores.astype(np.float32),
        forward=target_forward_scores.astype(np.float32),
        meta_valid=meta_valid_scores.astype(np.float32),
    )
    result = {
        "benchmark": rows.manifest["benchmark"],
        "variant": "chronological_crossfit_parent_aware_lambdamart_residual",
        "split_mode": args.split_mode,
        "split_bounds": target_bounds,
        "stack_split_mode": args.stack_split_mode,
        "stack_split_bounds": stack_bounds,
        "feature_names": list(FEATURE_NAMES),
        "categorical_feature_indices": list(CATEGORICAL_FEATURES),
        "parameters": parameters,
        "maximum_boost_rounds": 200,
        "early_stopping_rounds": 20,
        "best_epoch": best_iteration,
        "best_iteration": best_iteration,
        "meta_train_rows": int(len(meta_train_indices)),
        "meta_valid_rows": int(len(meta_valid_indices)),
        "meta_train_queries": meta_train_query_count,
        "meta_valid_queries": meta_valid_query_count,
        "maximum_query_rows": 10_000,
        "meta_valid_parent": meta_parent_metrics,
        "meta_valid": meta_corrected_metrics,
        "target_parent_valid": target_parent_metrics,
        "valid": target_metrics,
        "target_parent_forward": target_forward_parent_metrics,
        "forward_valid": target_forward_metrics,
        "robustness": target_robustness,
        "robustness_activity_reference_rows": int(len(activity_reference_indices)),
        "stack_parent_predictions": str(args.stack_parent_predictions),
        "stack_parent_predictions_sha256": sha256_path(
            args.stack_parent_predictions
        ),
        "target_parent_predictions": str(args.target_parent_predictions),
        "target_parent_predictions_sha256": sha256_path(
            args.target_parent_predictions
        ),
        "model_out": str(args.model_out),
        "model_out_sha256": sha256_path(args.model_out),
        "predictions_out": str(args.predictions_out),
        "predictions_out_sha256": sha256_path(args.predictions_out),
        "feature_importance_gain": {
            name: float(value) for name, value in zip(FEATURE_NAMES, importance)
        },
        "lightgbm_version": lgb.__version__,
        "elapsed_seconds": time.time() - started,
        "public_test_evaluated": False,
        "score_scope_warning": (
            "Metrics describe a fixed deterministic 1/32 development sample, "
            "not the full KuaiRand-27K benchmark or organizer hidden test."
        ),
    }
    serializable = json.loads(json.dumps(result, default=str))
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(serializable, indent=2, sort_keys=True) + "\n")
    print("RESULT_JSON=" + json.dumps(serializable, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
