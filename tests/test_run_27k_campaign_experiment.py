import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "run_27k_campaign_experiment.py"
SPEC = importlib.util.spec_from_file_location("run_27k_campaign_experiment", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class BenchmarkScopeTest(unittest.TestCase):
    def test_quarter_training_scope_is_explicitly_allowed(self) -> None:
        self.assertIn(
            "KuaiRand-27K quarter-training deterministic development sample",
            MODULE.ALLOWED_BENCHMARKS,
        )

    def test_half_training_scope_is_explicitly_allowed(self) -> None:
        self.assertIn(
            "KuaiRand-27K half-training deterministic development sample",
            MODULE.ALLOWED_BENCHMARKS,
        )

    def test_full_training_scope_is_explicitly_allowed(self) -> None:
        self.assertIn(
            "KuaiRand-27K full-training deterministic development sample",
            MODULE.ALLOWED_BENCHMARKS,
        )


if __name__ == "__main__":
    unittest.main()
