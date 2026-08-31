import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import torch


MODULE_PATH = Path(__file__).resolve().parents[1] / "solution" / "kuairand_1k_ranker.py"
SPEC = importlib.util.spec_from_file_location("kuairand_1k_ranker", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class EvaluationReferenceTest(unittest.TestCase):
    def test_lambdamart_query_bound_preserves_every_row(self) -> None:
        bounded = MODULE.bounded_query_groups(
            np.array([1, 10_000, 10_583, 25_000], dtype=np.int64), 10_000
        )
        np.testing.assert_array_equal(
            bounded,
            np.array([1, 10_000, 10_000, 583, 10_000, 10_000, 5_000]),
        )
        self.assertEqual(int(bounded.sum()), 45_584)

    def test_lambdamart_features_are_stably_grouped_and_restored(self) -> None:
        rows = SimpleNamespace(
            manifest={"user_count": 2},
            user=np.array([1, 0, 1], dtype=np.int32),
            label=np.array([1, 0, 0], dtype=np.uint8),
            duration=np.array([0.0, 1.0, 3.0], dtype=np.float32),
            tab=np.array([2, 1, 0], dtype=np.int16),
            tag=np.array([-1, 4, 5], dtype=np.int16),
            upload_type=np.array([0, 1, 2], dtype=np.int16),
            video_type=np.array([2, 1, 0], dtype=np.int16),
        )
        history = np.arange(24, dtype=np.int16).reshape(3, 8)
        item_history = np.arange(12, dtype=np.int16).reshape(3, 4)
        entity_history = np.arange(20, 32, dtype=np.int16).reshape(3, 4)

        features, labels, groups, order = MODULE.lambdamart_grouped_matrix(
            rows,
            np.array([0, 1, 2], dtype=np.int64),
            history,
            item_history,
            entity_history,
        )

        np.testing.assert_array_equal(order, np.array([1, 0, 2]))
        np.testing.assert_array_equal(groups, np.array([1, 2], dtype=np.int32))
        np.testing.assert_array_equal(labels, np.array([0, 1, 0], dtype=np.int32))
        self.assertEqual(features.shape, (3, 21))
        self.assertEqual(features[1, 2], 0.0)  # missing tag is categorical zero
        restored = MODULE.restore_grouped_predictions(order, np.array([0.2, 0.8, 0.4]))
        np.testing.assert_allclose(restored, np.array([0.8, 0.2, 0.4]))

    def test_slot_preserving_profile_blend_keeps_unsupported_parent_slots(self) -> None:
        users = np.array([0, 0, 0, 0], dtype=np.int32)
        parent = np.array([0.1, 0.2, 0.3, 0.4])
        profile = np.array([0.0, 1.0, 0.0, 0.0])
        supported = np.array([False, True, True, False])

        blended = MODULE.slot_preserving_profile_blend(
            users, parent, profile, supported
        )

        np.testing.assert_allclose(blended, np.array([0.0, 0.5, 0.5, 1.0]))

    def test_frozen_video_profile_uses_training_positive_vectors_only(self) -> None:
        rows = SimpleNamespace(
            manifest={"user_count": 2, "video_count": 3},
            user=np.array([0, 0, 1, 0, 0, 1], dtype=np.int32),
            video=np.array([0, 1, 1, 0, 1, 1], dtype=np.int32),
            label=np.array([1, 0, 1, 0, 0, 0], dtype=np.uint8),
        )
        # Field 0 occupies rows 0:3. Video unknown is row 3, and video ids
        # 0:3 occupy rows 4:7.
        checkpoint = {
            "latent": torch.tensor(
                [
                    [0.0, 0.0],
                    [0.0, 0.0],
                    [0.0, 0.0],
                    [0.0, 0.0],
                    [2.0, 0.0],
                    [0.0, 3.0],
                    [-4.0, 0.0],
                ],
                dtype=torch.float32,
            ),
            "field_dims": np.array([3, 4], dtype=np.int64),
            "offsets": np.array([0, 3], dtype=np.int64),
            "seen_video": np.array([True, True, True]),
        }

        scores, supported, metadata = MODULE.frozen_video_profile_scores(
            rows,
            np.array([0, 1, 2], dtype=np.int64),
            np.array([3, 4, 5], dtype=np.int64),
            checkpoint,
            batch_size=2,
        )

        np.testing.assert_allclose(scores, np.array([1.0, 0.0, 1.0]))
        np.testing.assert_array_equal(supported, np.array([True, True, True]))
        self.assertEqual(metadata["positive_exposures"], 2)
        self.assertEqual(metadata["profile_users"], 2)

    def test_evaluation_reference_filters_expanded_training_rows(self) -> None:
        rows = MODULE.CachedRows.__new__(MODULE.CachedRows)
        rows.date = np.array([20220408, 20220408, 20220409, 20220409])
        rows.evaluation_remainder = np.array([0, 1, 0, 2], dtype=np.uint8)
        rows.evaluation_residue = 0

        all_train = rows.indices((20220408, 20220409))
        reference = rows.indices((20220408, 20220409), evaluation=True)

        np.testing.assert_array_equal(all_train, np.array([0, 1, 2, 3]))
        np.testing.assert_array_equal(reference, np.array([0, 2]))

    def test_hard_pairs_choose_lowest_positive_and_highest_negative(self) -> None:
        rows = SimpleNamespace(
            user=np.array([1, 0, 1, 0, 0, 1, 0, 1], dtype=np.int32),
            label=np.array([0, 1, 1, 0, 1, 0, 0, 1], dtype=np.uint8),
        )
        indices = np.arange(8, dtype=np.int64)
        scores = np.array([0.9, 0.2, 0.1, 0.8, 0.3, 0.7, 0.6, 0.4])

        positive, negative, metadata = MODULE.within_user_hard_pairs(
            rows, indices, scores, max_positives=1
        )

        np.testing.assert_array_equal(positive, np.array([1, 2]))
        np.testing.assert_array_equal(negative, np.array([3, 0]))
        self.assertEqual(metadata["usable_users"], 2)
        self.assertEqual(metadata["pairs"], 2)
        self.assertEqual(metadata["positive_rule"], "lowest_parent_score")
        self.assertEqual(metadata["negative_rule"], "highest_parent_score")

    def test_hard_pairs_reject_nonfinite_scores(self) -> None:
        rows = SimpleNamespace(
            user=np.array([0, 0], dtype=np.int32),
            label=np.array([1, 0], dtype=np.uint8),
        )
        with self.assertRaisesRegex(ValueError, "finite"):
            MODULE.within_user_hard_pairs(
                rows,
                np.array([0, 1], dtype=np.int64),
                np.array([0.2, np.nan]),
                max_positives=1,
            )

    def test_checkpoint_metadata_requires_exact_parent_identity(self) -> None:
        encoder = SimpleNamespace(
            field_dims=np.array([2, 3], dtype=np.int64),
            offsets=np.array([0, 2], dtype=np.int64),
        )
        args = SimpleNamespace(
            feature_set="history_item",
            model_type="sparse_fm",
            split_mode="shadow_early",
            seed=2027,
            min_video_count=1,
            min_author_count=1,
            time_features=False,
            legacy_random_unknown_init=False,
            epoch_order="random",
        )
        bounds = {
            "train": (20220408, 20220411),
            "valid": (20220412, 20220414),
            "forward": (20220415, 20220417),
        }
        checkpoint = {
            "feature_set": "history_item",
            "model_type": "sparse_fm",
            "split_mode": "shadow_early",
            "seed": 2027,
            "split_bounds": bounds,
            "field_dims": encoder.field_dims.copy(),
            "offsets": encoder.offsets.copy(),
        }

        MODULE.validate_checkpoint_metadata(checkpoint, encoder, args, bounds)
        checkpoint["seed"] = 2028
        with self.assertRaisesRegex(ValueError, "seed mismatch"):
            MODULE.validate_checkpoint_metadata(checkpoint, encoder, args, bounds)

    def test_seen_with_min_count_pools_rare_and_missing_identities(self) -> None:
        seen = MODULE.seen_with_min_count(
            np.array([0, 0, 1, 2, 2, 2, -1], dtype=np.int64),
            dimension=4,
            minimum_count=2,
        )
        np.testing.assert_array_equal(
            seen, np.array([True, False, True, False], dtype=np.bool_)
        )

    def test_seen_with_min_count_rejects_out_of_range_identity(self) -> None:
        with self.assertRaisesRegex(ValueError, "exceeds"):
            MODULE.seen_with_min_count(
                np.array([0, 4], dtype=np.int64), dimension=4, minimum_count=1
            )

    def test_raw_prediction_aggregation_preserves_logit_margins(self) -> None:
        users = np.array([0, 0, 1], dtype=np.int32)
        members = [
            np.array([-2.0, 1.0, 3.0], dtype=np.float32),
            np.array([0.0, 3.0, 1.0], dtype=np.float32),
        ]
        combined = MODULE.aggregate_prediction_members(users, members, "raw_mean")
        np.testing.assert_allclose(combined, np.array([-1.0, 2.0, 2.0]))

    def test_balanced_positive_weight_uses_negative_positive_ratio(self) -> None:
        self.assertEqual(
            MODULE.balanced_positive_weight(np.array([0, 0, 0, 1])), 3.0
        )
        with self.assertRaisesRegex(ValueError, "both label classes"):
            MODULE.balanced_positive_weight(np.array([1, 1]))

    def test_fractional_epoch_order_uses_deterministic_ceiling_prefix(self) -> None:
        order = np.array([7, 2, 9, 1, 4], dtype=np.int64)
        np.testing.assert_array_equal(
            MODULE.fractional_epoch_order(order, 0.5),
            np.array([7, 2, 9], dtype=np.int64),
        )
        np.testing.assert_array_equal(
            MODULE.fractional_epoch_order(order, 1.0), order
        )

    def test_fractional_epoch_order_rejects_invalid_fraction(self) -> None:
        for fraction in (0.0, -0.5, 1.1):
            with self.subTest(fraction=fraction):
                with self.assertRaisesRegex(ValueError, "epoch-fraction"):
                    MODULE.fractional_epoch_order(
                        np.array([0], dtype=np.int64), fraction
                    )

    def test_training_epoch_order_is_stably_chronological(self) -> None:
        order = MODULE.chronological_epoch_order(
            np.array([30, 10, 20, 10], dtype=np.int64)
        )
        np.testing.assert_array_equal(order, [1, 3, 2, 0])

    def test_chronological_epoch_order_rejects_matrix(self) -> None:
        with self.assertRaisesRegex(ValueError, "one-dimensional"):
            MODULE.chronological_epoch_order(np.array([[1, 2]]))

    def test_remove_sparse_gradient_rows_excludes_only_frozen_identities(self) -> None:
        torch = __import__("torch")
        embedding = torch.nn.Embedding(8, 2, sparse=True)
        embedding(torch.tensor([0, 2, 4, 6])).sum().backward()

        removed = MODULE.remove_sparse_gradient_rows(
            embedding.weight, ((0, 3), (6, 8))
        )

        self.assertEqual(removed, 3)
        gradient = embedding.weight.grad.coalesce()
        np.testing.assert_array_equal(gradient.indices()[0].numpy(), [4])

    def test_remove_sparse_gradient_rows_rejects_invalid_range(self) -> None:
        torch = __import__("torch")
        embedding = torch.nn.Embedding(4, 2, sparse=True)
        embedding(torch.tensor([1])).sum().backward()
        with self.assertRaisesRegex(ValueError, "freeze range"):
            MODULE.remove_sparse_gradient_rows(embedding.weight, ((0, 5),))

    def test_sparse_optimizer_does_not_move_removed_rows(self) -> None:
        torch = __import__("torch")
        embedding = torch.nn.Embedding(4, 1, sparse=True)
        optimizer = torch.optim.SparseAdam(embedding.parameters(), lr=0.1)
        optimizer.zero_grad(set_to_none=True)
        embedding(torch.tensor([0, 2])).sum().backward()
        before = embedding.weight.detach().clone()
        MODULE.remove_sparse_gradient_rows(embedding.weight, ((0, 2),))
        optimizer.step()

        self.assertEqual(float(embedding.weight[0]), float(before[0]))
        self.assertNotEqual(float(embedding.weight[2]), float(before[2]))

    def test_legacy_unknown_mode_preserves_random_latent_row(self) -> None:
        neutral = MODULE.SparseFM(
            dimension=5,
            rank=2,
            unknown_offsets=np.array([0], dtype=np.int64),
            seed=2027,
            neutral_unknown_init=True,
        )
        legacy = MODULE.SparseFM(
            dimension=5,
            rank=2,
            unknown_offsets=np.array([0], dtype=np.int64),
            seed=2027,
            neutral_unknown_init=False,
        )

        np.testing.assert_array_equal(neutral.latent.weight[0].detach().numpy(), [0, 0])
        self.assertFalse(np.all(legacy.latent.weight[0].detach().numpy() == 0))
        np.testing.assert_array_equal(
            neutral.latent.weight[1:].detach().numpy(),
            legacy.latent.weight[1:].detach().numpy(),
        )

    def test_recurring_time_fields_use_shanghai_hour_and_weekday(self) -> None:
        hours, weekdays = MODULE.recurring_time_fields(
            np.array([1649673618997, 1649756418997], dtype=np.int64),
            np.array([20220411, 20220412], dtype=np.int32),
        )
        np.testing.assert_array_equal(hours, np.array([18, 17]))
        np.testing.assert_array_equal(weekdays, np.array([0, 1]))

    def test_encoder_appends_recurring_time_fields(self) -> None:
        rows = SimpleNamespace(
            manifest={
                "user_count": 2,
                "video_count": 2,
                "author_count": 2,
                "tab_count": 1,
            },
            user=np.array([0, 1], dtype=np.int32),
            video=np.array([0, 1], dtype=np.int32),
            author=np.array([0, 1], dtype=np.int32),
            tab=np.array([0, 0], dtype=np.int16),
            duration=np.array([1_000, 2_000], dtype=np.int32),
            time_ms=np.array([1649673618997, 1649756418997], dtype=np.int64),
            date=np.array([20220411, 20220412], dtype=np.int32),
        )
        encoder = MODULE.Encoder(
            rows,
            np.array([0, 1], dtype=np.int64),
            "base",
            "shadow_early",
            time_features=True,
        )
        encoded = encoder.encode(rows, np.array([0, 1], dtype=np.int64))
        np.testing.assert_array_equal(encoder.field_dims[-2:], [25, 8])
        np.testing.assert_array_equal(encoded[:, -2] - encoder.offsets[-2], [19, 18])
        np.testing.assert_array_equal(encoded[:, -1] - encoder.offsets[-1], [1, 2])

    def test_additive_tail_keeps_tail_out_of_latent_interactions(self) -> None:
        model = MODULE.WideCrossFM(
            dimension=16,
            rank=2,
            base_field_count=2,
            unknown_offsets=np.array([], dtype=np.int64),
            seed=2027,
        )
        torch = __import__("torch")
        with torch.no_grad():
            model.latent.weight.zero_()
            model.linear.weight.zero_()
            model.latent.weight[8:].fill_(100.0)
        fields = torch.tensor([[1, 2, 8], [1, 2, 9]], dtype=torch.long)
        np.testing.assert_allclose(model(fields).detach().numpy(), [0.0, 0.0])
        with torch.no_grad():
            model.linear.weight[9] = 2.5
        np.testing.assert_allclose(model(fields).detach().numpy(), [0.0, 2.5])

    def test_bipartite_fm_keeps_only_cross_group_interactions(self) -> None:
        torch = __import__("torch")
        model = MODULE.BipartiteFM(
            dimension=20,
            rank=2,
            left_field_indices=(0,),
            right_field_indices=(1,),
            unknown_offsets=np.array([], dtype=np.int64),
            seed=2027,
        )
        with torch.no_grad():
            model.latent.weight.zero_()
            model.linear.weight.zero_()
            model.latent.weight[1] = torch.tensor([1.0, 2.0])
            model.latent.weight[2] = torch.tensor([3.0, 4.0])
            model.latent.weight[3] = torch.tensor([100.0, 100.0])
        fields = torch.tensor([[1, 2, 3]], dtype=torch.long)
        np.testing.assert_allclose(model(fields).detach().numpy(), [11.0])

    def test_funnel_fm_scores_click_times_conditional_long_view(self) -> None:
        torch = __import__("torch")
        model = MODULE.FunnelFM(
            dimension=8,
            rank=2,
            unknown_offsets=np.array([], dtype=np.int64),
            seed=2027,
        )
        with torch.no_grad():
            model.latent.weight.zero_()
            model.linear.weight.zero_()
            model.click_linear.weight.zero_()
            model.click_linear.weight[1] = 2.0
        fields = torch.tensor([[1, 2]], dtype=torch.long)
        click, conditional = model.funnel_logits(fields)
        np.testing.assert_allclose(click.detach().numpy(), [2.0])
        np.testing.assert_allclose(conditional.detach().numpy(), [0.0])
        expected = torch.nn.functional.logsigmoid(torch.tensor(2.0))
        expected += torch.nn.functional.logsigmoid(torch.tensor(0.0))
        np.testing.assert_allclose(
            model(fields).detach().numpy(), [float(expected)], rtol=1e-6
        )

    def test_sparse_fm_latent_init_std_scales_seeded_weights(self) -> None:
        default = MODULE.SparseFM(
            dimension=16,
            rank=4,
            unknown_offsets=np.array([0], dtype=np.int64),
            seed=2027,
        )
        scaled = MODULE.SparseFM(
            dimension=16,
            rank=4,
            unknown_offsets=np.array([0], dtype=np.int64),
            seed=2027,
            latent_init_std=0.005,
        )
        np.testing.assert_allclose(
            scaled.latent.weight.detach().numpy(),
            default.latent.weight.detach().numpy() * 0.5,
            rtol=1e-6,
            atol=1e-8,
        )
        self.assertEqual(float(scaled.latent.weight[0].abs().sum()), 0.0)
        self.assertEqual(float(scaled.linear.weight[0].abs().sum()), 0.0)

    def test_prediction_aggregation_rejects_nonfinite_member(self) -> None:
        with self.assertRaisesRegex(ValueError, "finite"):
            MODULE.aggregate_prediction_members(
                np.array([0, 0], dtype=np.int32),
                [np.array([0.0, np.nan]), np.array([1.0, 2.0])],
                "raw_mean",
            )

    def test_high_activity_specialist_routes_only_above_upper_tertile(self) -> None:
        users = np.array([0, 1, 2, 3], dtype=np.int32)
        activity = np.array([1, 2, 3, 100], dtype=np.int64)
        base = [
            np.array([0.0, 0.0, 0.0, 0.0]),
            np.array([1.0, 1.0, 1.0, 1.0]),
            np.array([2.0, 2.0, 2.0, 2.0]),
        ]
        specialist = np.array([100.0, 100.0, 100.0, 100.0])
        scores, route = MODULE.high_activity_specialist_scores(
            users, activity, base + [specialist], "raw_mean", cutoff=3.0
        )
        np.testing.assert_array_equal(route, np.array([False, False, False, True]))
        np.testing.assert_allclose(scores, np.array([1.0, 1.0, 1.0, 25.75]))

    def test_high_activity_fallback_uses_final_member_alone(self) -> None:
        users = np.array([0, 1, 2, 3], dtype=np.int32)
        activity = np.array([1, 2, 3, 100], dtype=np.int64)
        base = np.array([0.0, 10.0, 20.0, 30.0])
        fallback = np.array([100.0, 100.0, 100.0, 100.0])
        scores, route = MODULE.high_activity_fallback_scores(
            users, activity, [base, fallback], "raw_mean", cutoff=3.0
        )
        np.testing.assert_array_equal(route, np.array([False, False, False, True]))
        np.testing.assert_allclose(scores, np.array([0.0, 10.0, 20.0, 100.0]))

    def test_high_activity_equal_blend_changes_only_routed_rows(self) -> None:
        users = np.array([0, 1, 2, 3], dtype=np.int32)
        activity = np.array([1, 2, 3, 100], dtype=np.int64)
        base = np.array([0.0, 10.0, 20.0, 30.0])
        fallback = np.array([100.0, 100.0, 100.0, 100.0])
        scores, route = MODULE.high_activity_equal_blend_scores(
            users, activity, [base, fallback], "raw_mean", cutoff=3.0
        )
        np.testing.assert_array_equal(route, np.array([False, False, False, True]))
        np.testing.assert_allclose(scores, np.array([0.0, 10.0, 20.0, 65.0]))

    def test_activity_upper_tertile_matches_row_weighted_slice_definition(self) -> None:
        activity = np.array([1, 2, 100], dtype=np.int64)
        reference_users = np.array([0, 1, 1, 1, 2], dtype=np.int32)
        self.assertEqual(
            MODULE.activity_upper_tertile(reference_users, activity), 2.0
        )


if __name__ == "__main__":
    unittest.main()
