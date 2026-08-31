from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "sample_kuairand_27k_logs", ROOT / "scripts" / "sample_kuairand_27k_logs.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class SampleKuaiRand27KLogsTest(unittest.TestCase):
    def test_vector_hash_exactly_matches_scalar_hash(self) -> None:
        users = np.asarray([0, 17, 27284], dtype=np.uint64)
        videos = np.asarray([1, 23, 32_038_724], dtype=np.uint64)
        times = np.asarray([100, 1_650_000_000_000, 2**63 + 7], dtype=np.uint64)
        observed = MODULE.event_hash_array(users, videos, times)
        expected = np.asarray(
            [MODULE.event_hash(int(u), int(v), int(t)) for u, v, t in zip(users, videos, times)],
            dtype=np.uint64,
        )
        np.testing.assert_array_equal(observed, expected)

    def test_hash_sampling_is_deterministic_and_bounded(self) -> None:
        first = MODULE.event_hash(17, 23, 1650000000000)
        self.assertEqual(first, MODULE.event_hash(17, 23, 1650000000000))
        self.assertTrue(0 <= first < 2**64)
        decisions = [
            MODULE.keep_event(17, video, 1650000000000 + video, 8, 0)
            for video in range(100)
        ]
        self.assertGreater(sum(decisions), 0)
        self.assertLess(sum(decisions), len(decisions))

    def test_sample_group_never_writes_post_boundary_row(self) -> None:
        header = ",".join(MODULE.EXPECTED_COLUMNS)
        retained = ["1", "2", "20220428", "1200", "100"] + ["0"] * 14
        held_out = ["1", "3", "20220429", "1200", "101"] + ["1"] * 14
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.csv"
            destination = root / "sample.csv"
            source.write_text(
                header + "\n" + ",".join(retained) + "\n" + ",".join(held_out) + "\n"
            )
            observed = MODULE.sample_group(
                [source],
                destination,
                modulus=1,
                residue=0,
                minimum_date=20220422,
                maximum_date=20220428,
                allow_after_boundary=True,
            )
            lines = destination.read_text().splitlines()
            self.assertEqual(len(lines), 2)
            self.assertIn("20220428", lines[1])
            self.assertNotIn("20220429", destination.read_text())
            self.assertEqual(observed["sampled_rows"], 1)
            self.assertEqual(observed["skipped_after_boundary"], 1)


if __name__ == "__main__":
    unittest.main()
