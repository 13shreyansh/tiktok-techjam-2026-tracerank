import sys
import unittest
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "solution"))

from kuairand_27k_lambdaloss_finetune import (
    build_lambda_groups,
    metric_aligned_lambda_loss,
)


class LambdaLossFineTuneTests(unittest.TestCase):
    def test_groups_use_hard_negatives_and_exact_top_five_deltas(self) -> None:
        users = np.ones(8, dtype=np.int32)
        labels = np.array([1, 0, 0, 1, 0, 0, 0, 0], dtype=np.uint8)
        scores = np.array([0.1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3], dtype=np.float32)
        rows = np.arange(100, 108, dtype=np.int64)
        groups, metadata = build_lambda_groups(
            users, labels, scores, rows, max_positives=5, max_negatives=2, seed=7
        )
        self.assertEqual(len(groups), 1)
        np.testing.assert_array_equal(groups[0].positive_rows, [100, 103])
        np.testing.assert_array_equal(groups[0].negative_rows, [101, 102])
        self.assertEqual(groups[0].delta_ndcg.shape, (2, 2))
        self.assertTrue(np.isfinite(groups[0].delta_ndcg).all())
        self.assertGreater(float(groups[0].delta_ndcg.sum()), 0.0)
        self.assertEqual(metadata["informative_ndcg_users"], 1)

    def test_loss_rewards_correct_positive_order(self) -> None:
        group = build_lambda_groups(
            np.ones(4, dtype=np.int32),
            np.array([1, 1, 0, 0], dtype=np.uint8),
            np.array([0.2, 0.1, 0.9, 0.8], dtype=np.float32),
            np.arange(4, dtype=np.int64),
            max_positives=2,
            max_negatives=2,
            seed=3,
        )[0]
        wrong = torch.tensor([-1.0, -0.5, 1.0, 0.5], requires_grad=True)
        right = torch.tensor([1.0, 0.5, -1.0, -0.5], requires_grad=True)
        wrong_loss = metric_aligned_lambda_loss(wrong, group)
        right_loss = metric_aligned_lambda_loss(right, group)
        self.assertLess(float(right_loss), float(wrong_loss))
        wrong_loss.backward()
        self.assertTrue(torch.isfinite(wrong.grad).all())


if __name__ == "__main__":
    unittest.main()
