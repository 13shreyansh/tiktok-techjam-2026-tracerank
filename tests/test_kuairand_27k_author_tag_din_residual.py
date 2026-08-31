import sys
import unittest
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "solution"))

from kuairand_27k_author_tag_din_residual import AuthorTagDINResidual


class AuthorTagDINResidualTests(unittest.TestCase):
    def test_epoch_zero_preserves_parent(self):
        model = AuthorTagDINResidual(20, 10, 3, 2027).eval()
        parent = torch.tensor([0.3, -0.4])
        output = model(
            parent, torch.tensor([1, 2]),
            torch.tensor([[1, 2, 0, 0, 0], [2, 3, 4, 0, 0]]),
            torch.tensor([1, 2]),
            torch.tensor([[1, 2, 0, 0, 0], [2, 3, 4, 0, 0]]),
            torch.tensor([1, 2]), torch.tensor([1, 2]), torch.tensor([1, 2]),
        )
        self.assertTrue(torch.equal(output, parent))

    def test_empty_history_is_finite(self):
        model = AuthorTagDINResidual(20, 10, 3, 2027)
        output = model(
            torch.zeros(1), torch.ones(1, dtype=torch.long),
            torch.zeros((1, 5), dtype=torch.long), torch.ones(1, dtype=torch.long),
            torch.zeros((1, 5), dtype=torch.long), torch.ones(1, dtype=torch.long),
            torch.ones(1, dtype=torch.long), torch.ones(1, dtype=torch.long),
        )
        self.assertTrue(torch.isfinite(output).all())


if __name__ == "__main__": unittest.main()
