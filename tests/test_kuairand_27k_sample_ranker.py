from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "kuairand_27k_sample_ranker",
    ROOT / "solution" / "kuairand_27k_sample_ranker.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class KuaiRand27KSampleRankerTest(unittest.TestCase):
    def test_relabel_preserves_score_and_declares_scope(self) -> None:
        source = {"benchmark": "KuaiRand-1K", "valid": {"primary": 0.5}}
        result = MODULE.relabel_result(source)
        self.assertEqual(source["benchmark"], "KuaiRand-1K")
        self.assertEqual(result["valid"], {"primary": 0.5})
        self.assertEqual(
            result["benchmark"], "KuaiRand-27K deterministic development sample"
        )
        self.assertIn("not the full", result["score_scope_warning"])
        self.assertEqual(len(result["delegated_ranker"]["sha256"]), 64)

    def test_required_argument_reader_rejects_missing_value(self) -> None:
        with self.assertRaisesRegex(ValueError, "has no value"):
            MODULE.argument_value(["--json-out"], "--json-out")

    def test_relabel_preserves_declared_expanded_benchmark(self) -> None:
        benchmark = "KuaiRand-27K expanded-training deterministic development sample"
        result = MODULE.relabel_result({"valid": {"primary": 0.5}}, benchmark)
        self.assertEqual(result["benchmark"], benchmark)


if __name__ == "__main__":
    unittest.main()
