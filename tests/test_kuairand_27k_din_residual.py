import sys
import unittest
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "solution"))

from kuairand_27k_din_residual import TagDINResidual


class TagDINResidualTests(unittest.TestCase):
    def test_epoch_zero_exactly_preserves_parent(self):
        model = TagDINResidual(tag_count=69, tab_count=15, seed=2027)
        model.eval()
        parent = torch.tensor([0.2, -0.7])
        candidate = torch.tensor([2, 3])
        history = torch.tensor([[1, 2, 0, 0, 0], [4, 5, 6, 7, 8]])
        output = model(
            parent,
            candidate,
            history,
            torch.tensor([1, 2]),
            torch.tensor([1, 2]),
            torch.tensor([1, 2]),
        )
        self.assertTrue(torch.equal(output, parent))

    def test_empty_history_is_finite(self):
        model = TagDINResidual(tag_count=69, tab_count=15, seed=2027)
        output = model(
            torch.zeros(3),
            torch.tensor([1, 2, 3]),
            torch.zeros((3, 5), dtype=torch.long),
            torch.ones(3, dtype=torch.long),
            torch.ones(3, dtype=torch.long),
            torch.ones(3, dtype=torch.long),
        )
        self.assertTrue(torch.isfinite(output).all())

    def test_attention_receives_gradients_after_output_unfreezes(self):
        model = TagDINResidual(tag_count=69, tab_count=15, seed=2027)
        with torch.no_grad():
            model.network[-1].weight.fill_(0.1)
        output = model(
            torch.zeros(2),
            torch.tensor([2, 3]),
            torch.tensor([[1, 2, 3, 0, 0], [3, 4, 5, 6, 0]]),
            torch.tensor([1, 2]),
            torch.tensor([1, 2]),
            torch.tensor([1, 2]),
        ).sum()
        output.backward()
        self.assertIsNotNone(model.attention[0].weight.grad)
        self.assertGreater(float(model.attention[0].weight.grad.abs().sum()), 0.0)


if __name__ == "__main__":
    unittest.main()
