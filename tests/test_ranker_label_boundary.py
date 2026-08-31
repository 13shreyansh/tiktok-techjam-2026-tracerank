import csv
import tempfile
import unittest
from pathlib import Path

from solution.ranker import OUTCOME_FIELDS, label_boundary_attestation, load_rows


LOG_FIELDS = (
    "user_id",
    "video_id",
    "date",
    "hourmin",
    "time_ms",
    "is_click",
    "is_like",
    "is_follow",
    "is_comment",
    "is_forward",
    "is_hate",
    "long_view",
    "play_time_ms",
    "duration_ms",
    "profile_stay_time",
    "comment_stay_time",
    "is_profile_enter",
    "is_rand",
    "tab",
)


def write_csv(path, fieldnames, rows):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class OfficialTestLabelBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.temporary_directory.name)
        write_csv(
            self.data_dir / "video_features_basic_pure.csv",
            ("video_id", "author_id", "video_type", "upload_type", "music_id", "tag"),
            [
                {
                    "video_id": "v1",
                    "author_id": "a1",
                    "video_type": "NORMAL",
                    "upload_type": "0",
                    "music_id": "m1",
                    "tag": "7,8",
                }
            ],
        )
        write_csv(
            self.data_dir / "user_features_pure.csv",
            (
                "user_id",
                "user_active_degree",
                "follow_user_num_range",
                "fans_user_num_range",
                "friend_user_num_range",
                "register_days_range",
            ),
            [
                {
                    "user_id": "u1",
                    "user_active_degree": "full_active",
                    "follow_user_num_range": "1",
                    "fans_user_num_range": "2",
                    "friend_user_num_range": "3",
                    "register_days_range": "4",
                }
            ],
        )
        write_csv(
            self.data_dir / "log_standard_4_08_to_4_21_pure.csv",
            LOG_FIELDS,
            [self.log_row("20220408", "1")],
        )
        write_csv(
            self.data_dir / "log_standard_4_22_to_5_08_pure.csv",
            LOG_FIELDS,
            [
                self.log_row("20220422", "1"),
                self.log_row("20220429", "not-readable-as-an-outcome"),
            ],
        )

    def tearDown(self):
        self.temporary_directory.cleanup()

    @staticmethod
    def log_row(date, outcome):
        return {
            "user_id": "u1",
            "video_id": "v1",
            "date": date,
            "hourmin": "1305",
            "time_ms": f"{date}000",
            "is_click": outcome,
            "is_like": outcome,
            "is_follow": outcome,
            "is_comment": outcome,
            "is_forward": outcome,
            "is_hate": outcome,
            "long_view": outcome,
            "play_time_ms": outcome,
            "duration_ms": "10000",
            "profile_stay_time": "0",
            "comment_stay_time": "0",
            "is_profile_enter": "0",
            "is_rand": "0",
            "tab": "1",
        }

    def test_official_test_outcomes_are_never_parsed_or_returned(self):
        splits = load_rows(self.data_dir)

        self.assertEqual(splits["train"][0]["label"], 1)
        self.assertEqual(splits["valid"][0]["label"], 1)
        self.assertEqual(len(splits["test"]), 1)
        for field in OUTCOME_FIELDS:
            self.assertNotIn(field, splits["test"][0])

    def test_shadow_window_retains_development_labels_and_excludes_final_test(self):
        shadow = {
            "train": (20220408, 20220408),
            "valid": (20220422, 20220422),
            "test": (20220422, 20220422),
        }
        splits = load_rows(self.data_dir, split_bounds=shadow)

        self.assertEqual(splits["test"][0]["label"], 1)
        self.assertTrue(all(row["date"] <= 20220428 for rows in splits.values() for row in rows))

    def test_attestation_records_training_only_fitted_state(self):
        attestation = label_boundary_attestation(True)

        self.assertFalse(attestation["official_test_outcomes_loaded"])
        self.assertTrue(attestation["official_test_rows_feature_only"])
        self.assertEqual(attestation["fitted_preprocessing_splits"], ["train"])
        self.assertEqual(attestation["behavior_history_splits"], ["train"])
        self.assertFalse(attestation["official_test_outcome_statistics_used"])


if __name__ == "__main__":
    unittest.main()
