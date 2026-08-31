from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "inspect_kuairand_27k", ROOT / "scripts" / "inspect_kuairand_27k.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class InspectKuaiRand27KTest(unittest.TestCase):
    def test_last_nonempty_line_handles_trailing_newlines(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.csv"
            path.write_bytes(b"a,b\n1,2\n3,4\n\n")
            self.assertEqual(MODULE.last_nonempty_line(path), "3,4")

    def test_inspect_csv_labels_endpoints_as_samples(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.csv"
            path.write_text(
                "user_id,video_id,date,time_ms\n"
                "1,11,20220408,100\n"
                "2,12,20220409,200\n"
            )
            observed = MODULE.inspect_csv(path)
            self.assertEqual(observed["columns"], ["user_id", "video_id", "date", "time_ms"])
            dates = observed["sampled_endpoints_only"]["date"]
            self.assertEqual(dates, {"first_record": "20220408", "last_record": "20220409"})


if __name__ == "__main__":
    unittest.main()
