import unittest

from solution.ranker import (
    STRICT_SKIP_WATCH_RATIO,
    bounded_user_groups,
    build_causal_history_transformer,
    build_task_protected_extraction,
    copeland_rank_consensus,
    encode_causal_history,
    hard_attention_profile,
    is_secondary_history_event,
    is_strict_skip_history_event,
    masked_attention_profile,
    restore_grouped_scores,
    sequence_history_indices,
    within_user_percentile_rank,
)


class SequenceHistoryOrderTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"user": "a", "time_ms": 30},
            {"user": "b", "time_ms": 5},
            {"user": "a", "time_ms": 10},
            {"user": "a", "time_ms": 20},
            {"user": "b", "time_ms": 5},
        ]

    def test_source_order_reproduces_raw_traversal(self):
        self.assertEqual(sequence_history_indices(self.rows, "source"), [0, 1, 2, 3, 4])

    def test_causal_order_sorts_within_user_and_stabilizes_ties(self):
        self.assertEqual(sequence_history_indices(self.rows), [2, 3, 0, 1, 4])

    def test_unknown_order_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "unknown sequence history order"):
            sequence_history_indices(self.rows, "wrong")

    def test_strict_skip_requires_all_three_negative_conditions(self):
        row = {
            "label": 0,
            "click": 0,
            "play_time": 500.0,
            "duration": 10_000.0,
        }
        self.assertEqual(STRICT_SKIP_WATCH_RATIO, 0.05)
        self.assertTrue(is_strict_skip_history_event(row))
        for changed in (
            {"label": 1},
            {"click": 1},
            {"play_time": 501.0},
        ):
            candidate = row | changed
            self.assertFalse(is_strict_skip_history_event(candidate))

    def test_strict_skip_handles_zero_duration_without_division_error(self):
        row = {"label": 0, "click": 0, "play_time": 0.0, "duration": 0.0}
        self.assertTrue(is_strict_skip_history_event(row))

    def test_secondary_engagement_history_excludes_click_only_and_hate(self):
        base = {
            "click": 0,
            "like": 0,
            "follow": 0,
            "comment": 0,
            "forward": 0,
            "hate": 0,
        }
        self.assertFalse(is_secondary_history_event(base, "engagement"))
        for action in ("like", "follow", "comment", "forward"):
            self.assertTrue(is_secondary_history_event(base | {action: 1}, "engagement"))
        self.assertFalse(is_secondary_history_event(base | {"click": 1}, "engagement"))
        self.assertFalse(is_secondary_history_event(base | {"hate": 1}, "engagement"))
        self.assertTrue(is_secondary_history_event(base | {"click": 1}, "click"))
        self.assertFalse(is_secondary_history_event(base, "none"))
        with self.assertRaisesRegex(ValueError, "unknown secondary history event"):
            is_secondary_history_event(base, "unknown")

    def test_task_protected_extraction_has_finite_dual_outputs_and_gradients(self):
        import torch

        torch.manual_seed(7)
        model = build_task_protected_extraction(12, 16, 0.0)
        values = torch.randn(5, 12)
        long_view, click = model(values)
        self.assertEqual(tuple(long_view.shape), (5,))
        self.assertEqual(tuple(click.shape), (5,))
        self.assertTrue(torch.isfinite(long_view).all())
        self.assertTrue(torch.isfinite(click).all())
        (long_view.square().mean() + click.square().mean()).backward()
        self.assertTrue(all(parameter.grad is not None for parameter in model.parameters()))

    def test_causal_history_transformer_handles_padding_and_empty_rows(self):
        import torch

        torch.manual_seed(11)
        position, encoder = build_causal_history_transformer(16, 4, 0.0)
        historical = torch.randn(2, 4, 16, requires_grad=True)
        mask = torch.tensor([[False, True, True, True], [False, False, False, False]])
        encoded = encode_causal_history(encoder, position, historical, mask)
        self.assertEqual(tuple(encoded.shape), (2, 4, 16))
        self.assertTrue(torch.isfinite(encoded).all())
        self.assertTrue(torch.equal(encoded[1], torch.zeros_like(encoded[1])))
        encoded[0].square().mean().backward()
        self.assertTrue(torch.isfinite(historical.grad).all())

    def test_masked_attention_profile_is_finite_for_recent_and_empty_history(self):
        import torch

        historical = torch.tensor(
            [
                [[1.0, 0.0], [2.0, 0.0], [3.0, 0.0]],
                [[4.0, 0.0], [5.0, 0.0], [6.0, 0.0]],
            ]
        )
        logits = torch.zeros(2, 3)
        mask = torch.tensor([[False, True, True], [False, False, False]])
        profile = masked_attention_profile(historical, logits, mask)
        self.assertTrue(torch.isfinite(profile).all())
        torch.testing.assert_close(profile[0], torch.tensor([2.5, 0.0]))
        torch.testing.assert_close(profile[1], torch.zeros(2))

    def test_hard_attention_profile_selects_best_valid_and_zeros_empty(self):
        import torch

        historical = torch.tensor(
            [
                [[1.0, 0.0], [2.0, 0.0], [3.0, 0.0]],
                [[4.0, 0.0], [5.0, 0.0], [6.0, 0.0]],
            ]
        )
        logits = torch.tensor([[9.0, 2.0, 7.0], [3.0, 2.0, 1.0]])
        mask = torch.tensor([[False, True, True], [False, False, False]])
        profile = hard_attention_profile(historical, logits, mask)
        torch.testing.assert_close(profile[0], historical[0, 2])
        torch.testing.assert_close(profile[1], torch.zeros(2))

    def test_crossfit_rank_and_group_helpers_preserve_alignment(self):
        import numpy as np

        users = np.asarray(["b", "a", "b", "a"])
        scores = np.asarray([0.8, 0.1, 0.2, 0.9])
        np.testing.assert_allclose(
            within_user_percentile_rank(users, scores),
            [1.0, 0.0, 0.0, 1.0],
        )
        order = np.argsort(users, kind="stable")
        self.assertEqual(bounded_user_groups(users[order]).tolist(), [2, 2])
        np.testing.assert_allclose(
            restore_grouped_scores(order, [10.0, 20.0, 30.0, 40.0]),
            [30.0, 10.0, 40.0, 20.0],
        )

    def test_bounded_groups_split_only_oversized_users(self):
        import numpy as np

        users = np.asarray(["a"] * 5 + ["b"] * 2)
        self.assertEqual(bounded_user_groups(users, maximum=3).tolist(), [3, 2, 2])

    def test_copeland_consensus_uses_member_majority_with_user_isolation(self):
        import numpy as np

        users = np.asarray(["a", "a", "a", "b"])
        members = np.asarray(
            [
                [1.0, 0.5, 0.0, 0.4],
                [1.0, 0.5, 0.0, 0.8],
                [0.0, 0.5, 1.0, 0.2],
            ]
        )
        scores = copeland_rank_consensus(members, users)
        self.assertGreater(scores[0], scores[1])
        self.assertGreater(scores[1], scores[2])
        self.assertEqual(scores[3], 0.0)

    def test_copeland_consensus_fails_on_misalignment(self):
        import numpy as np

        with self.assertRaisesRegex(ValueError, "not aligned"):
            copeland_rank_consensus(np.zeros((3, 2)), ["a"])


if __name__ == "__main__":
    unittest.main()
