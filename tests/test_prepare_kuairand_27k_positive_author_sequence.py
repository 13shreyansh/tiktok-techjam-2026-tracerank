import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from prepare_kuairand_27k_positive_author_sequence import update_recent


class PositiveAuthorSequenceTests(unittest.TestCase):
    def test_stable_newest_first_update(self):
        recent = np.asarray([8, 7, 6, 5, 4], dtype=np.int32)
        update_recent(recent, np.asarray([9, 10], dtype=np.int32))
        np.testing.assert_array_equal(recent, [10, 9, 8, 7, 6])

    def test_empty_update_preserves_history(self):
        recent = np.asarray([3, 2, 1, -1, -1], dtype=np.int32)
        update_recent(recent, np.asarray([], dtype=np.int32))
        np.testing.assert_array_equal(recent, [3, 2, 1, -1, -1])


if __name__ == "__main__":
    unittest.main()
