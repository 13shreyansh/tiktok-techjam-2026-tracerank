import sys
import unittest
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "solution"))

from kuairand_27k_deepfm_residual import FrozenEmbeddingDeepResidual


class FrozenEmbeddingDeepResidualTests(unittest.TestCase):
    def test_epoch_zero_exactly_preserves_parent(self) -> None:
        model = FrozenEmbeddingDeepResidual(field_count=3, rank=2, seed=2027)
        model.eval()
        parent = torch.tensor([0.25, -0.75])
        embeddings = torch.randn(2, 3, 2)
        self.assertTrue(torch.equal(model(parent, embeddings), parent))

    def test_hidden_layers_receive_gradients_after_output_unfreezes(self) -> None:
        model = FrozenEmbeddingDeepResidual(field_count=3, rank=2, seed=2027)
        with torch.no_grad():
            model.network[-1].weight.fill_(0.1)
        output = model(torch.zeros(4), torch.randn(4, 3, 2)).sum()
        output.backward()
        self.assertIsNotNone(model.network[0].weight.grad)
        self.assertGreater(float(model.network[0].weight.grad.abs().sum()), 0.0)


if __name__ == "__main__":
    unittest.main()
