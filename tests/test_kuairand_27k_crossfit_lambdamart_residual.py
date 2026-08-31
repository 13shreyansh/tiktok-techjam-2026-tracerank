from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "solution" / "kuairand_27k_crossfit_lambdamart_residual.py"
sys.path.insert(0, str(ROOT / "solution"))
SPEC = importlib.util.spec_from_file_location("crossfit_lambdamart", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CrossfitLambdaMARTTests(unittest.TestCase):
    def test_prediction_pair_requires_alignment_and_finiteness(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "predictions.npz"
            np.savez(path, valid=np.array([0.1, 0.2]), forward=np.array([0.3]))
            valid, forward = MODULE.load_prediction_pair(path, 2, 1)
            np.testing.assert_allclose(valid, [0.1, 0.2])
            np.testing.assert_allclose(forward, [0.3])
            with self.assertRaisesRegex(ValueError, "length mismatch"):
                MODULE.load_prediction_pair(path, 3, 1)
            np.savez(path, valid=np.array([np.nan]), forward=np.array([0.3]))
            with self.assertRaisesRegex(ValueError, "finite"):
                MODULE.load_prediction_pair(path, 1, 1)

    def test_corrected_scores_adds_delta_without_changing_alignment(self) -> None:
        parent = np.array([0.0, 0.5, 1.0])
        delta = np.array([0.1, -0.2, 0.3])
        np.testing.assert_allclose(
            MODULE.corrected_scores(parent, delta), [0.1, 0.3, 1.3]
        )
        with self.assertRaisesRegex(ValueError, "align"):
            MODULE.corrected_scores(parent, delta[:2])


if __name__ == "__main__":
    unittest.main()
