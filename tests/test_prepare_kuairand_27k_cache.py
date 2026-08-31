from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location(
    "prepare_kuairand_27k_cache",
    ROOT / "scripts" / "prepare_kuairand_27k_cache.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class PrepareKuaiRand27KCacheTest(unittest.TestCase):
    def test_direct_cli_help_loads_benchmark_choices(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SPEC.origin), "--help"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("quarter-training", completed.stdout)
        self.assertIn("half-training", completed.stdout)
        self.assertIn("full-training", completed.stdout)

    def test_quarter_training_scope_is_explicitly_allowed(self) -> None:
        self.assertIn(
            "KuaiRand-27K quarter-training deterministic development sample",
            MODULE.BENCHMARK_NAMES,
        )

    def test_half_training_scope_is_explicitly_allowed(self) -> None:
        self.assertIn(
            "KuaiRand-27K half-training deterministic development sample",
            MODULE.BENCHMARK_NAMES,
        )

    def test_full_training_scope_is_explicitly_allowed(self) -> None:
        self.assertIn(
            "KuaiRand-27K full-training deterministic development sample",
            MODULE.BENCHMARK_NAMES,
        )

    def test_evaluation_remainders_use_original_video_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            np.save(root / "source_video_ids.npy", np.asarray([7, 42], dtype=np.int32))
            path = MODULE.write_evaluation_remainders(
                root,
                np.asarray([3, 4], dtype=np.int32),
                np.asarray([1, 0], dtype=np.int32),
                np.asarray([100, 200], dtype=np.int64),
                modulus=32,
            )
            observed = np.load(path)
            expected = np.asarray(
                [
                    MODULE.event_hash_array(
                        np.asarray([3], dtype=np.uint64),
                        np.asarray([42], dtype=np.uint64),
                        np.asarray([100], dtype=np.uint64),
                    )[0]
                    % np.uint64(32),
                    MODULE.event_hash_array(
                        np.asarray([4], dtype=np.uint64),
                        np.asarray([7], dtype=np.uint64),
                        np.asarray([200], dtype=np.uint64),
                    )[0]
                    % np.uint64(32),
                ],
                dtype=np.uint8,
            )
            np.testing.assert_array_equal(observed, expected)

    def test_observed_id_remap_is_dense_and_reversible(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            values = np.lib.format.open_memmap(
                root / "values.npy", mode="w+", dtype="int32", shape=(5,)
            )
            values[:] = [100, 7, 100, 42, 7]
            count = MODULE.remap_observed_ids(
                values, root / "source_ids.npy", allow_missing=False
            )
            self.assertEqual(count, 3)
            self.assertEqual(values.tolist(), [2, 0, 2, 1, 0])
            source = np.load(root / "source_ids.npy")
            self.assertEqual(source.tolist(), [7, 42, 100])
            self.assertEqual(source[np.asarray(values)].tolist(), [100, 7, 100, 42, 7])

    def test_observed_id_remap_preserves_missing_value(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            values = np.lib.format.open_memmap(
                root / "values.npy", mode="w+", dtype="int32", shape=(4,)
            )
            values[:] = [-1, 9, 4, -1]
            count = MODULE.remap_observed_ids(
                values, root / "source_ids.npy", allow_missing=True
            )
            self.assertEqual(count, 2)
            self.assertEqual(values.tolist(), [-1, 1, 0, -1])


if __name__ == "__main__":
    unittest.main()
