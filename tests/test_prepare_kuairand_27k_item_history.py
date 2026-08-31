import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "prepare_kuairand_27k_item_history.py"
SPEC = importlib.util.spec_from_file_location("prepare_kuairand_27k_item_history", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ItemHistoryScopeTest(unittest.TestCase):
    def test_quarter_training_scope_is_accepted(self) -> None:
        MODULE.validate_cache_benchmark(
            {"benchmark": "KuaiRand-27K quarter-training deterministic development sample"}
        )

    def test_half_training_scope_is_accepted(self) -> None:
        MODULE.validate_cache_benchmark(
            {"benchmark": "KuaiRand-27K half-training deterministic development sample"}
        )

    def test_full_training_scope_is_accepted(self) -> None:
        MODULE.validate_cache_benchmark(
            {"benchmark": "KuaiRand-27K full-training deterministic development sample"}
        )

    def test_unknown_scope_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "verified 27K sampled cache"):
            MODULE.validate_cache_benchmark({"benchmark": "unverified"})

    def test_direct_cli_help_executes(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(MODULE_PATH), "--help"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main()
