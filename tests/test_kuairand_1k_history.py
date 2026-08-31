import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from scripts.prepare_kuairand_1k_history import build_split
from scripts.prepare_kuairand_1k_sequence_profile import (
    build_split as build_sequence_profile,
)
from scripts.prepare_kuairand_27k_full_history import (
    build_split as build_full_history,
)
from scripts.prepare_kuairand_27k_item_history import (
    build_split as build_item_history,
)
from scripts.prepare_kuairand_27k_item_behavior import (
    build_split as build_item_behavior,
)
from scripts.prepare_kuairand_27k_item_trend import (
    build_split as build_item_trend,
)
from scripts.prepare_kuairand_27k_user_entity_history import (
    causal_entity_features,
    source_segments,
)
from scripts.prepare_kuairand_27k_user_author_behavior import (
    causal_author_behavior_features,
)
from scripts.prepare_kuairand_27k_user_author_recency import (
    NEVER_BUCKET,
    causal_author_recency_features,
)
from scripts.prepare_kuairand_27k_user_multitag_history import (
    causal_primary_from_multitag_features,
)
from solution.kuairand_1k_ranker import (
    Encoder,
    WideCrossFM,
    item_age_buckets,
    same_impression_pairs,
    user_balanced_weights,
    within_user_pairs,
)


class KuaiRandHistoryTest(unittest.TestCase):
    def test_user_balanced_weights_are_mean_one_and_reduce_frequency_dominance(self):
        users = np.asarray([0, 0, 0, 0, 1], dtype=np.int64)
        weights = user_balanced_weights(users, 0.5)
        self.assertAlmostEqual(float(weights.mean()), 1.0, places=6)
        self.assertGreater(float(weights[-1]), float(weights[0]))
        self.assertAlmostEqual(float(weights[-1] / weights[0]), 2.0, places=6)

    def test_user_balanced_weights_reject_invalid_alpha(self):
        with self.assertRaises(ValueError):
            user_balanced_weights(np.asarray([0], dtype=np.int64), 1.1)

    def test_item_history_uses_prior_days_and_freezes_after_cutoff(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "cache"
            work = cache / "work"
            work.mkdir(parents=True)
            (cache / "manifest.json").write_text(
                json.dumps({"rows": 3, "video_count": 2, "author_count": 1})
            )
            np.save(cache / "date.npy", np.array([20220408, 20220409, 20220412], dtype=np.int32))
            np.save(cache / "video.npy", np.array([0, 1, 1], dtype=np.int32))
            np.save(cache / "author.npy", np.zeros(3, dtype=np.int32))
            daily_count = np.zeros((21, 2), dtype=np.uint32)
            daily_positive = np.zeros((21, 2), dtype=np.uint32)
            daily_count[0, 0] = 2
            daily_positive[0, 0] = 1
            daily_count[1, 1] = 9  # Must not update when cutoff is April 8.
            daily_positive[1, 1] = 9
            np.save(work / "item_daily_count.npy", daily_count)
            np.save(work / "item_daily_positive.npy", daily_positive)

            record = build_item_history(cache, work, "test", 20220408)
            history = np.load(cache / record["path"])
            np.testing.assert_array_equal(history[0], [0, 5, 0, 5])
            # Video 1 is unseen, but its shared author's prior-day count is 2.
            np.testing.assert_array_equal(history[1], [0, 5, 1, 7])
            # State is frozen; the April 9 outcomes never alter April 12.
            np.testing.assert_array_equal(history[2], history[1])

    def test_item_history_encoder_loads_dedicated_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            np.save(cache / "item.npy", np.zeros((3, 4), dtype=np.int16))
            np.save(cache / "behavior.npy", np.zeros((3, 8), dtype=np.int16))
            np.save(cache / "trend.npy", np.zeros((3, 8), dtype=np.int16))
            np.save(cache / "repeat.npy", np.zeros((3, 4), dtype=np.int16))
            np.save(cache / "author_behavior.npy", np.zeros((3, 2), dtype=np.int16))
            np.save(cache / "author_recency.npy", np.zeros((3, 2), dtype=np.int16))
            np.save(cache / "tag_history.npy", np.zeros((3, 2), dtype=np.int16))
            np.save(cache / "multitag_history.npy", np.zeros((3, 2), dtype=np.int16))
            sequence = np.full((3, 11), -1, dtype=np.int16)
            sequence[:, [5, 7, 9]] = 0
            sequence[:, 10] = 16
            np.save(cache / "sequence.npy", sequence)
            sampled_history = np.zeros((3, 8), dtype=np.int16)
            sampled_history[:, 7] = -1
            np.save(cache / "history.npy", sampled_history)
            (cache / "item_history_manifest.json").write_text(
                json.dumps({"splits": {"shadow_early": {"path": "item.npy"}}})
            )
            (cache / "item_behavior_manifest.json").write_text(
                json.dumps({"splits": {"shadow_early": {"path": "behavior.npy"}}})
            )
            (cache / "item_trend_manifest.json").write_text(
                json.dumps({"splits": {"shadow_early": {"path": "trend.npy"}}})
            )
            (cache / "history_manifest.json").write_text(
                json.dumps({"splits": {"shadow_early": {"path": "history.npy"}}})
            )
            (cache / "user_entity_history_manifest.json").write_text(
                json.dumps({"splits": {"shadow_early": {"path": "repeat.npy"}}})
            )
            (cache / "user_author_behavior_manifest.json").write_text(
                json.dumps(
                    {"splits": {"shadow_early": {"path": "author_behavior.npy"}}}
                )
            )
            (cache / "user_author_recency_manifest.json").write_text(
                json.dumps(
                    {"splits": {"shadow_early": {"path": "author_recency.npy"}}}
                )
            )
            (cache / "user_tag_history_manifest.json").write_text(
                json.dumps(
                    {"splits": {"shadow_early": {"path": "tag_history.npy"}}}
                )
            )
            (cache / "user_multitag_history_manifest.json").write_text(
                json.dumps(
                    {"splits": {"shadow_early": {"path": "multitag_history.npy"}}}
                )
            )
            (cache / "sequence_profile_manifest.json").write_text(
                json.dumps(
                    {"splits": {"shadow_early": {"path": "sequence.npy"}}}
                )
            )
            rows = SimpleNamespace(
                cache_dir=cache,
                manifest={
                    "user_count": 1, "video_count": 3, "author_count": 3,
                    "tab_count": 1, "tag_count": 3,
                    "upload_type_count": 1, "video_type_count": 1,
                },
                user=np.zeros(3, dtype=np.int32), video=np.arange(3, dtype=np.int32),
                author=np.arange(3, dtype=np.int32), tab=np.zeros(3, dtype=np.int16),
                duration=np.array([1.0, 2.0, 3.0], dtype=np.float32),
                tag=np.array([0, 1, 2], dtype=np.int16),
                upload_type=np.zeros(3, dtype=np.int16),
                video_type=np.zeros(3, dtype=np.int16),
            )
            encoder = Encoder(
                rows, np.array([0, 1], dtype=np.int64), "item_history", "shadow_early"
            )
            encoded = encoder.encode(rows, np.array([0, 2], dtype=np.int64))
            self.assertEqual(encoded.shape, (2, 12))
            combined = Encoder(
                rows, np.array([0, 1], dtype=np.int64), "history_item", "shadow_early"
            )
            combined_encoded = combined.encode(rows, np.array([0, 2], dtype=np.int64))
            self.assertEqual(combined_encoded.shape, (2, 20))
            behavior = Encoder(
                rows,
                np.array([0, 1], dtype=np.int64),
                "history_item_behavior",
                "shadow_early",
            )
            behavior_encoded = behavior.encode(rows, np.array([0, 2], dtype=np.int64))
            self.assertEqual(behavior_encoded.shape, (2, 24))
            trend = Encoder(
                rows,
                np.array([0, 1], dtype=np.int64),
                "history_item_trend",
                "shadow_early",
            )
            trend_encoded = trend.encode(rows, np.array([0, 2], dtype=np.int64))
            self.assertEqual(trend_encoded.shape, (2, 24))
            repeat = Encoder(
                rows,
                np.array([0, 1], dtype=np.int64),
                "history_item_repeat",
                "shadow_early",
            )
            repeat_encoded = repeat.encode(rows, np.array([0, 2], dtype=np.int64))
            self.assertEqual(repeat_encoded.shape, (2, 24))
            author_behavior = Encoder(
                rows,
                np.array([0, 1], dtype=np.int64),
                "history_item_repeat_author_behavior",
                "shadow_early",
            )
            author_behavior_encoded = author_behavior.encode(
                rows, np.array([0, 2], dtype=np.int64)
            )
            self.assertEqual(author_behavior_encoded.shape, (2, 26))
            author_recency = Encoder(
                rows,
                np.array([0, 1], dtype=np.int64),
                "history_item_repeat_author_recency",
                "shadow_early",
            )
            author_recency_encoded = author_recency.encode(
                rows, np.array([0, 2], dtype=np.int64)
            )
            self.assertEqual(author_recency_encoded.shape, (2, 26))
            tag_affinity = Encoder(
                rows,
                np.array([0, 1], dtype=np.int64),
                "history_item_repeat_tag_affinity",
                "shadow_early",
            )
            tag_affinity_encoded = tag_affinity.encode(
                rows, np.array([0, 2], dtype=np.int64)
            )
            self.assertEqual(tag_affinity_encoded.shape, (2, 26))
            multitag_affinity = Encoder(
                rows,
                np.array([0, 1], dtype=np.int64),
                "history_item_repeat_multitag_affinity",
                "shadow_early",
            )
            multitag_affinity_encoded = multitag_affinity.encode(
                rows, np.array([0, 2], dtype=np.int64)
            )
            self.assertEqual(multitag_affinity_encoded.shape, (2, 26))
            repeat_sequence = Encoder(
                rows,
                np.array([0, 1], dtype=np.int64),
                "history_item_repeat_sequence",
                "shadow_early",
            )
            repeat_sequence_encoded = repeat_sequence.encode(
                rows, np.array([0, 2], dtype=np.int64)
            )
            self.assertEqual(repeat_sequence_encoded.shape, (2, 35))
            self.assertTrue(np.all(repeat_sequence_encoded >= 0))
            self.assertTrue(
                np.all(repeat_sequence_encoded < int(repeat_sequence.field_dims.sum()))
            )

    def test_multitag_affinity_counts_secondary_history_for_current_primary(self):
        tags = np.array(
            [
                [1, 2, -1],
                [3, 1, -1],
                [1, -1, -1],
                [1, 1, -1],
            ],
            dtype=np.int64,
        )
        times = np.array([100, 150, 200, 300], dtype=np.int64)
        dates = np.array([20220408, 20220409, 20220410, 20220412], dtype=np.int32)
        labels = np.array([1, 0, 1, 0], dtype=np.uint8)
        history = causal_primary_from_multitag_features(
            tags, times, dates, labels, cutoff=20220410
        )
        np.testing.assert_array_equal(history[0], [0, 5])
        # Tag 3 is new even though tag 1 has prior history in another slot.
        np.testing.assert_array_equal(history[1], [0, 5])
        # Current primary tag 1 sees row 0 primary and row 1 secondary.
        np.testing.assert_array_equal(history[2], [1, 7])
        # Duplicate tag slots update only once per earlier row; post-cutoff
        # labels cannot change the frozen state.
        np.testing.assert_array_equal(history[3], [2, 9])

    def test_user_entity_history_is_prior_only_and_frozen(self):
        entity = np.array([3, 3, 4, 3, 3], dtype=np.int64)
        times = np.array([100, 100, 150, 200, 300], dtype=np.int64)
        dates = np.array(
            [20220408, 20220408, 20220409, 20220410, 20220412], dtype=np.int32
        )
        labels = np.array([1, 0, 1, 1, 0], dtype=np.uint8)
        history = causal_entity_features(entity, times, dates, labels, 20220410)
        # Simultaneous first impressions see no prior entity state.
        np.testing.assert_array_equal(history[0], [0, 5])
        np.testing.assert_array_equal(history[1], [0, 5])
        # Entity 4 is independent; entity 3 later sees both simultaneous rows.
        np.testing.assert_array_equal(history[2], [0, 5])
        np.testing.assert_array_equal(history[3], [1, 7])
        # The post-cutoff row sees all three eligible entity-3 rows, while its
        # own outcome cannot update the frozen state.
        np.testing.assert_array_equal(history[4], [2, 9])

    def test_user_entity_source_segments_detect_file_resets(self):
        users = np.array([0, 0, 2, 0, 1, 3], dtype=np.int32)
        self.assertEqual(source_segments(users), [(0, 3), (3, 6)])

    def test_user_author_behavior_is_prior_only_and_frozen(self):
        authors = np.array([3, 3, 4, 3, 3], dtype=np.int64)
        times = np.array([100, 100, 150, 200, 300], dtype=np.int64)
        dates = np.array(
            [20220408, 20220408, 20220409, 20220410, 20220412], dtype=np.int32
        )
        strong = np.array([1, 0, 1, 0, 1], dtype=np.uint8)
        hate = np.array([0, 1, 0, 1, 0], dtype=np.uint8)
        history = causal_author_behavior_features(
            authors, times, dates, strong, hate, 20220410
        )
        # Same-timestamp events share the prior and cannot see one another.
        np.testing.assert_array_equal(history[0], [5, 5])
        np.testing.assert_array_equal(history[1], [5, 5])
        # Independent author 4 starts from the fixed prior.
        np.testing.assert_array_equal(history[2], [5, 5])
        # Author 3 now sees one strong and one hate over two past exposures.
        np.testing.assert_array_equal(history[3], [7, 7])
        # The post-cutoff row sees all three eligible author-3 rows. Its own
        # outcome is masked and cannot update frozen validation state.
        np.testing.assert_array_equal(history[4], [6, 9])

    def test_user_author_recency_is_prior_only_and_frozen(self):
        hour = 3_600_000
        authors = np.array([3, 3, 4, 3, 3], dtype=np.int64)
        times = hour * np.array([100, 100, 150, 124, 220], dtype=np.int64)
        dates = np.array(
            [20220408, 20220408, 20220409, 20220409, 20220412], dtype=np.int32
        )
        labels = np.array([1, 0, 1, 0, 1], dtype=np.uint8)
        history = causal_author_recency_features(
            authors, times, dates, labels, 20220409
        )
        # Same-timestamp first impressions and a different author have no prior.
        np.testing.assert_array_equal(history[0], [NEVER_BUCKET, NEVER_BUCKET])
        np.testing.assert_array_equal(history[1], [NEVER_BUCKET, NEVER_BUCKET])
        np.testing.assert_array_equal(history[2], [NEVER_BUCKET, NEVER_BUCKET])
        # Twenty-four hours after the first author-3 batch: floor(log2(25)) = 4.
        np.testing.assert_array_equal(history[3], [4, 4])
        # The post-cutoff row sees the eligible exposure at hour 124, but the
        # last positive remains hour 100; its own outcome cannot update state.
        np.testing.assert_array_equal(history[4], [6, 6])

    def test_item_trend_uses_three_prior_days_and_freezes_at_cutoff(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "cache"
            work = cache / "work"
            work.mkdir(parents=True)
            dates = np.array(
                [20220408, 20220409, 20220410, 20220411, 20220412, 20220415],
                dtype=np.int32,
            )
            (cache / "manifest.json").write_text(
                json.dumps({"rows": len(dates), "video_count": 1, "author_count": 1})
            )
            np.save(cache / "date.npy", dates)
            np.save(cache / "video.npy", np.zeros(len(dates), dtype=np.int32))
            np.save(cache / "author.npy", np.zeros(len(dates), dtype=np.int32))
            np.save(cache / "item_history_test.npy", np.zeros((len(dates), 4), dtype=np.int16))
            count = np.zeros((21, 1), dtype=np.uint32)
            positive = np.zeros((21, 1), dtype=np.uint32)
            count[:5, 0] = [1, 2, 4, 8, 16]
            positive[:5, 0] = [1, 0, 0, 8, 16]
            np.save(work / "item_daily_count.npy", count)
            np.save(work / "item_daily_positive.npy", positive)

            record = build_item_trend(cache, work, "test", 20220411)
            trend = np.load(cache / record["path"])
            # April 11 sees April 8-10: 7 exposures and one positive.
            np.testing.assert_array_equal(trend[3, 4:], [3, 3, 3, 3])
            # Scoring freezes April 9-11: 14 exposures and eight positives;
            # April 12 outcomes do not enter April 15.
            np.testing.assert_array_equal(trend[4, 4:], [3, 10, 3, 10])
            np.testing.assert_array_equal(trend[5], trend[4])

    def test_item_behavior_uses_prior_days_and_freezes_after_cutoff(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "cache"
            work = cache / "work"
            work.mkdir(parents=True)
            (cache / "manifest.json").write_text(
                json.dumps({"rows": 3, "video_count": 2, "author_count": 1})
            )
            np.save(cache / "date.npy", np.array([20220408, 20220409, 20220412], dtype=np.int32))
            np.save(cache / "video.npy", np.array([0, 1, 1], dtype=np.int32))
            np.save(cache / "author.npy", np.zeros(3, dtype=np.int32))
            np.save(cache / "item_history_test.npy", np.zeros((3, 4), dtype=np.int16))
            count = np.zeros((21, 2), dtype=np.uint32)
            strong = np.zeros((21, 2), dtype=np.uint32)
            hate = np.zeros((21, 2), dtype=np.uint32)
            count[0, 0], strong[0, 0], hate[0, 0] = 4, 2, 1
            count[1, 1], strong[1, 1] = 8, 8  # Beyond cutoff; must stay unseen.
            np.save(work / "item_daily_count.npy", count)
            np.save(work / "item_daily_strong.npy", strong)
            np.save(work / "item_daily_hate.npy", hate)

            record = build_item_behavior(cache, work, "test", 20220408)
            behavior = np.load(cache / record["path"])
            np.testing.assert_array_equal(behavior[0, 4:], [5, 5, 5, 5])
            # Video 1 is unseen, while the shared author sees 4 exposures,
            # 2 strong events, and 1 hate event from the prior day.
            np.testing.assert_array_equal(behavior[1, 4:], [5, 5, 7, 5])
            np.testing.assert_array_equal(behavior[2], behavior[1])

    def test_full_history_uses_unsampled_events_and_freezes_at_cutoff(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "cache"
            work = cache / "full_history_work"
            work.mkdir(parents=True)
            np.save(work / "user_offsets.npy", np.array([0, 4], dtype=np.int64))
            np.save(work / "time_ms.npy", np.array([100, 200, 200, 400], dtype=np.int64))
            np.save(work / "date.npy", np.array([20220408, 20220408, 20220412, 20220412], dtype=np.int32))
            np.save(work / "sample_index.npy", np.array([-1, 0, -1, 1], dtype=np.int32))
            np.save(work / "label.npy", np.array([1, 0, 1, 0], dtype=np.uint8))
            np.save(work / "strong.npy", np.array([1, 0, 1, 0], dtype=np.uint8))
            np.save(work / "hate.npy", np.zeros(4, dtype=np.uint8))
            np.save(cache / "history_shadow_early.npy", np.zeros((2, 8), dtype=np.int16))

            record = build_full_history(
                cache, work, "shadow_early", 20220411
            )
            history = np.load(cache / record["path"])
            # The first sampled row sees the earlier unsampled positive event.
            self.assertEqual(int(history[0, 0]), 1)
            self.assertEqual(int(history[0, 2]), 1)
            # The validation row sees the two training events only; the
            # unsampled validation positive cannot update frozen state.
            self.assertEqual(int(history[1, 0]), 1)
            self.assertEqual(int(history[1, 2]), 1)
            self.assertEqual(int(history[1, 1]), 7)

    def test_full_history_encoder_loads_the_dedicated_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            full_history = np.zeros((3, 8), dtype=np.int16)
            full_history[:, 7] = -1
            np.save(cache / "full.npy", full_history)
            (cache / "full_history_manifest.json").write_text(
                json.dumps({"splits": {"shadow_early": {"path": "full.npy"}}})
            )
            rows = SimpleNamespace(
                cache_dir=cache,
                manifest={
                    "user_count": 1, "video_count": 3, "author_count": 3,
                    "tab_count": 1, "tag_count": 3,
                    "upload_type_count": 1, "video_type_count": 1,
                },
                user=np.zeros(3, dtype=np.int32),
                video=np.arange(3, dtype=np.int32),
                author=np.arange(3, dtype=np.int32),
                tab=np.zeros(3, dtype=np.int16),
                duration=np.array([1.0, 2.0, 3.0], dtype=np.float32),
                tag=np.array([0, 1, 2], dtype=np.int16),
                upload_type=np.zeros(3, dtype=np.int16),
                video_type=np.zeros(3, dtype=np.int16),
            )
            encoder = Encoder(
                rows, np.array([0, 1], dtype=np.int64), "full_history", "shadow_early"
            )
            encoded = encoder.encode(rows, np.array([0, 2], dtype=np.int64))
            self.assertEqual(encoded.shape, (2, 16))

    def test_history_builders_sort_nonchronological_source_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            values = {
                "user": np.zeros(3, dtype=np.int32),
                "tag": np.array([1, 2, 1], dtype=np.int32),
                "date": np.full(3, 20220408, dtype=np.int32),
                "time_ms": np.array([200, 100, 300], dtype=np.int64),
                "label": np.array([0, 1, 0], dtype=np.uint8),
                "is_like": np.zeros(3, dtype=np.uint8),
                "is_follow": np.zeros(3, dtype=np.uint8),
                "is_comment": np.zeros(3, dtype=np.uint8),
                "is_forward": np.zeros(3, dtype=np.uint8),
                "is_hate": np.zeros(3, dtype=np.uint8),
            }
            for name, value in values.items():
                np.save(cache / f"{name}.npy", value)
            (cache / "manifest.json").write_text(
                json.dumps({"rows": 3, "user_count": 1, "tag_count": 3})
            )

            history_record = build_split(cache, "test", (20220408, 20220408))
            history = np.load(cache / history_record["path"])
            self.assertEqual(history_record["source_timestamp_inversions"], 1)
            self.assertEqual(history_record["timestamp_inversions"], 0)
            self.assertEqual(int(history[0, 0]), 1)
            self.assertEqual(int(history[0, 7]), 2)

            sequence_record = build_sequence_profile(
                cache, "test", (20220408, 20220408)
            )
            sequence = np.load(cache / sequence_record["path"])
            self.assertEqual(sequence_record["source_timestamp_inversions"], 1)
            self.assertEqual(sequence_record["timestamp_inversions"], 0)
            self.assertEqual(int(sequence[0, 0]), 2)

    def test_item_age_is_derived_from_each_interaction_date(self):
        upload = np.array([738253, 738253, -1], dtype=np.int32)  # 2022-04-08
        dates = np.array([20220408, 20220416, 20220416], dtype=np.int32)
        np.testing.assert_array_equal(item_age_buckets(dates, upload), [0, 3, -1])

    def test_pair_sampler_never_crosses_an_impression_batch(self):
        rows = SimpleNamespace(
            user=np.array([0, 0, 0, 0, 1, 1, 1], dtype=np.int32),
            time_ms=np.array([10, 10, 10, 20, 10, 10, 20], dtype=np.int64),
            label=np.array([1, 0, 1, 0, 1, 0, 0], dtype=np.uint8),
        )
        positive, negative, metadata = same_impression_pairs(
            rows, np.arange(7, dtype=np.int64), max_positives=5, seed=2027
        )
        self.assertEqual(metadata["usable_impression_batches"], 2)
        self.assertEqual(metadata["pairs"], 3)
        for left, right in zip(positive, negative):
            self.assertEqual(int(rows.user[left]), int(rows.user[right]))
            self.assertEqual(int(rows.time_ms[left]), int(rows.time_ms[right]))
            self.assertEqual(int(rows.label[left]), 1)
            self.assertEqual(int(rows.label[right]), 0)

    def test_within_user_sampler_uses_full_history_but_never_crosses_users(self):
        rows = SimpleNamespace(
            user=np.array([0, 0, 0, 0, 1, 1, 1], dtype=np.int32),
            label=np.array([1, 0, 1, 0, 1, 0, 0], dtype=np.uint8),
        )
        positive, negative, metadata = within_user_pairs(
            rows, np.arange(7, dtype=np.int64), max_positives=1, seed=2027
        )
        self.assertEqual(metadata["usable_users"], 2)
        self.assertEqual(metadata["pairs"], 2)
        self.assertEqual(metadata["max_positives_per_user"], 1)
        for left, right in zip(positive, negative):
            self.assertEqual(int(rows.user[left]), int(rows.user[right]))
            self.assertEqual(int(rows.label[left]), 1)
            self.assertEqual(int(rows.label[right]), 0)

    def test_within_user_sampler_accepts_interleaved_cache_rows(self):
        rows = SimpleNamespace(
            user=np.array([1, 0, 1, 0, 1, 0, 1], dtype=np.int32),
            label=np.array([1, 1, 0, 0, 0, 1, 1], dtype=np.uint8),
        )
        source_indices = np.array([6, 1, 4, 3, 0, 5, 2], dtype=np.int64)
        positive, negative, metadata = within_user_pairs(
            rows, source_indices, max_positives=2, seed=2027
        )
        self.assertEqual(metadata["usable_users"], 2)
        self.assertEqual(metadata["pairs"], 4)
        for left, right in zip(positive, negative):
            self.assertEqual(int(rows.user[left]), int(rows.user[right]))
            self.assertEqual(int(rows.label[left]), 1)
            self.assertEqual(int(rows.label[right]), 0)

    def test_same_timestamp_is_not_leaked_and_scoring_state_is_frozen(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            values = {
                "user": np.zeros(7, dtype=np.int32),
                "tag": np.array([1, 2, 1, 2, 1, 2, 1], dtype=np.int32),
                "date": np.array(
                    [20220408, 20220408, 20220409, 20220412, 20220415, 20220418, 20220422],
                    dtype=np.int32,
                ),
                "time_ms": np.array([100, 100, 200, 300, 400, 500, 600], dtype=np.int64),
                "label": np.array([1, 0, 0, 1, 0, 1, 0], dtype=np.uint8),
                "is_like": np.array([1, 0, 0, 0, 0, 0, 0], dtype=np.uint8),
                "is_follow": np.zeros(7, dtype=np.uint8),
                "is_comment": np.zeros(7, dtype=np.uint8),
                "is_forward": np.zeros(7, dtype=np.uint8),
                "is_hate": np.array([0, 1, 0, 0, 0, 0, 0], dtype=np.uint8),
            }
            for name, value in values.items():
                np.save(cache / f"{name}.npy", value)
            (cache / "manifest.json").write_text(
                json.dumps(
                    {
                        "format_version": 3,
                        "rows": 7,
                        "user_count": 1,
                        "tag_count": 3,
                    }
                )
            )

            official = build_split(cache, "official", (20220408, 20220421))
            history = np.load(cache / official["path"])

            # The first two rows are one simultaneous impression batch, so the
            # positive first row cannot alter the second row's fields.
            np.testing.assert_array_equal(history[0], history[1])
            self.assertEqual(int(history[0, 0]), 0)
            self.assertEqual(int(history[0, 7]), -1)

            # The next timestamp sees both earlier rows and tag 1 as the last
            # positive tag.
            self.assertEqual(int(history[2, 0]), 1)  # floor(log2(2 + 1))
            self.assertEqual(int(history[2, 6]), 1)
            self.assertEqual(int(history[2, 7]), 1)

            # The validation row sees all six training rows but cannot update
            # from any scoring-row outcome.
            self.assertEqual(int(history[6, 0]), 2)  # floor(log2(6 + 1))
            self.assertEqual(int(history[6, 7]), 2)
            self.assertEqual(official["timestamp_inversions"], 0)
            self.assertEqual(official["simultaneous_multirow_batches"], 1)

            shadow = build_split(cache, "shadow_early", (20220408, 20220411))
            shadow_history = np.load(cache / shadow["path"])
            self.assertEqual(int(shadow_history[3, 0]), 2)  # frozen after 3 rows
            self.assertEqual(int(shadow_history[6, 0]), 2)
            self.assertEqual(int(shadow_history[3, 7]), 1)

    def test_sequence_profile_is_simultaneous_and_frozen(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            values = {
                "user": np.zeros(5, dtype=np.int32),
                "tag": np.array([1, 2, 1, 2, 1], dtype=np.int32),
                "date": np.array(
                    [20220408, 20220408, 20220409, 20220422, 20220423],
                    dtype=np.int32,
                ),
                "time_ms": np.array(
                    [0, 0, 3_600_000, 7_200_000, 10_800_000], dtype=np.int64
                ),
                "label": np.array([1, 0, 1, 0, 1], dtype=np.uint8),
                "is_like": np.array([1, 0, 0, 0, 0], dtype=np.uint8),
                "is_follow": np.zeros(5, dtype=np.uint8),
                "is_comment": np.zeros(5, dtype=np.uint8),
                "is_forward": np.zeros(5, dtype=np.uint8),
                "is_hate": np.array([0, 1, 0, 0, 0], dtype=np.uint8),
            }
            for name, value in values.items():
                np.save(cache / f"{name}.npy", value)
            (cache / "manifest.json").write_text(
                json.dumps({"format_version": 3, "rows": 5, "user_count": 1})
            )

            record = build_sequence_profile(cache, "official", (20220408, 20220421))
            profile = np.load(cache / record["path"])
            np.testing.assert_array_equal(profile[0], profile[1])
            np.testing.assert_array_equal(profile[0, :5], [-1, -1, -1, -1, -1])
            self.assertEqual(int(profile[2, 0]), 1)
            self.assertEqual(int(profile[2, 6]), 1)
            self.assertEqual(int(profile[2, 8]), 2)
            # Both score rows see the same cutoff state; candidate-dependent
            # match columns can differ, but row 4's positive label cannot
            # update row 5's remembered tags.
            np.testing.assert_array_equal(profile[3, :5], profile[4, :5])
            self.assertEqual(int(profile[3, 6]), int(profile[4, 6]))
            self.assertEqual(int(profile[3, 8]), int(profile[4, 8]))
            np.testing.assert_array_equal(profile[3, :5], [1, 1, -1, -1, -1])
            self.assertEqual(record["timestamp_inversions"], 0)
            self.assertEqual(record["simultaneous_multirow_batches"], 1)

    def test_sequence_encoder_declares_every_encoded_field(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            sequence = np.full((3, 11), -1, dtype=np.int16)
            sequence[:, [5, 7, 9]] = 0
            sequence[:, 10] = 16
            np.save(cache / "sequence.npy", sequence)
            (cache / "sequence_profile_manifest.json").write_text(
                json.dumps({"splits": {"shadow_early": {"path": "sequence.npy"}}})
            )
            rows = SimpleNamespace(
                cache_dir=cache,
                manifest={
                    "user_count": 1,
                    "video_count": 3,
                    "author_count": 3,
                    "tab_count": 1,
                    "tag_count": 3,
                    "upload_type_count": 1,
                    "video_type_count": 1,
                },
                user=np.zeros(3, dtype=np.int32),
                video=np.arange(3, dtype=np.int32),
                author=np.arange(3, dtype=np.int32),
                tab=np.zeros(3, dtype=np.int16),
                duration=np.array([1.0, 2.0, 3.0], dtype=np.float32),
                tag=np.array([0, 1, 2], dtype=np.int16),
                upload_type=np.zeros(3, dtype=np.int16),
                video_type=np.zeros(3, dtype=np.int16),
            )
            encoder = Encoder(
                rows, np.array([0, 1], dtype=np.int64), "sequence", "shadow_early"
            )
            encoded = encoder.encode(rows, np.array([2], dtype=np.int64))
            self.assertEqual(len(encoder.field_dims), 19)
            self.assertEqual(encoded.shape, (1, 19))
            self.assertTrue(np.all(encoded >= 0))
            self.assertTrue(np.all(encoded < int(encoder.field_dims.sum())))

    def test_explicit_cross_encoder_has_bounded_user_content_ids(self):
        rows = SimpleNamespace(
            manifest={
                "user_count": 2,
                "video_count": 3,
                "author_count": 3,
                "tab_count": 1,
                "tag_count": 3,
                "upload_type_count": 2,
                "video_type_count": 2,
            },
            user=np.array([0, 1, 1], dtype=np.int32),
            video=np.arange(3, dtype=np.int32),
            author=np.arange(3, dtype=np.int32),
            tab=np.zeros(3, dtype=np.int16),
            duration=np.array([1.0, 2.0, 3.0], dtype=np.float32),
            tag=np.array([0, 1, 2], dtype=np.int16),
            upload_type=np.array([0, 1, 0], dtype=np.int16),
            video_type=np.array([0, 1, 0], dtype=np.int16),
        )
        encoder = Encoder(
            rows, np.array([0, 1], dtype=np.int64), "cross", "shadow_early"
        )
        encoded = encoder.encode(rows, np.array([0, 1, 2], dtype=np.int64))
        self.assertEqual(len(encoder.field_dims), 12)
        self.assertEqual(encoded.shape, (3, 12))
        self.assertTrue(np.all(encoded >= 0))
        self.assertTrue(np.all(encoded < int(encoder.field_dims.sum())))
        # Tag 2 was unseen in training, so its explicit user-tag cross is the
        # unknown entry for that field rather than a validation-derived ID.
        self.assertEqual(int(encoded[2, 8]), int(encoder.offsets[8]))

    def test_wide_cross_fields_cannot_enter_latent_interactions(self):
        model = WideCrossFM(
            dimension=20,
            rank=2,
            base_field_count=2,
            unknown_offsets=np.array([], dtype=np.int64),
            seed=2027,
        )
        with __import__("torch").no_grad():
            model.latent.weight.zero_()
            model.linear.weight.zero_()
            model.latent.weight[10:].fill_(100.0)
        torch = __import__("torch")
        fields = torch.tensor([[1, 2, 10], [1, 2, 11]], dtype=torch.long)
        np.testing.assert_allclose(model(fields).detach().numpy(), [0.0, 0.0])
        with torch.no_grad():
            model.linear.weight[11] = 3.0
        np.testing.assert_allclose(model(fields).detach().numpy(), [0.0, 3.0])


if __name__ == "__main__":
    unittest.main()
