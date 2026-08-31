#!/usr/bin/env python3
"""Training-only audit of causal positive and strict-skip Pure histories."""
from __future__ import annotations

import argparse
import collections
import csv
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--history-length", type=int, default=20)
    args = parser.parse_args()

    source = args.data_dir / "log_standard_4_08_to_4_21_pure.csv"
    metadata = args.data_dir / "video_features_basic_pure.csv"
    tags = {}
    with metadata.open(newline="") as handle:
        for row in csv.DictReader(handle):
            tags[row["video_id"]] = row["tag"] or "UNK"

    rows = []
    frequency = collections.Counter()
    covered_users = collections.defaultdict(set)
    with source.open(newline="") as handle:
        for source_index, row in enumerate(csv.DictReader(handle)):
            duration = max(float(row["duration_ms"]), 1.0)
            play_time = float(row["play_time_ms"])
            watch_ratio = min(play_time / duration, 1.0)
            user = row["user_id"]
            values = {
                "long_view": int(row["long_view"]),
                "click": int(row["is_click"]),
                "like": int(row["is_like"]),
                "follow": int(row["is_follow"]),
                "comment": int(row["is_comment"]),
                "forward": int(row["is_forward"]),
                "hate": int(row["is_hate"]),
            }
            for name, value in values.items():
                frequency[name] += value
                if value:
                    covered_users[name].add(user)
            strict_skip = (
                values["long_view"] == 0
                and values["click"] == 0
                and watch_ratio <= 0.05
            )
            frequency["strict_skip_005"] += int(strict_skip)
            if strict_skip:
                covered_users["strict_skip_005"].add(user)
            rows.append(
                (
                    user,
                    int(row["time_ms"]),
                    source_index,
                    row["video_id"],
                    tags.get(row["video_id"], "UNK"),
                    values["long_view"],
                    values["click"],
                    watch_ratio,
                )
            )

    rows.sort(key=lambda value: (value[0], value[1], value[2]))
    positive = collections.defaultdict(
        lambda: (
            collections.deque(maxlen=args.history_length),
            collections.deque(maxlen=args.history_length),
        )
    )
    skipped = collections.defaultdict(
        lambda: (
            collections.deque(maxlen=args.history_length),
            collections.deque(maxlen=args.history_length),
        )
    )
    signal = collections.defaultdict(lambda: [0, 0])
    for user, _, _, video, tag, long_view, click, watch_ratio in rows:
        signal["all"][0] += 1
        signal["all"][1] += long_view
        positive_videos, positive_tags = positive[user]
        skipped_videos, skipped_tags = skipped[user]
        positive_tag_match = tag in positive_tags
        conditions = {
            "positive_video_match": video in positive_videos,
            "positive_tag_match": positive_tag_match,
            "strict_skip_video_match": video in skipped_videos,
            "strict_skip_tag_match": tag in skipped_tags,
            "strict_skip_tag_only": tag in skipped_tags and not positive_tag_match,
        }
        for name, matched in conditions.items():
            if matched:
                signal[name][0] += 1
                signal[name][1] += long_view
        if long_view:
            positive_videos.append(video)
            positive_tags.append(tag)
        if long_view == 0 and click == 0 and watch_ratio <= 0.05:
            skipped_videos.append(video)
            skipped_tags.append(tag)

    users = {row[0] for row in rows}
    base = signal["all"][1] / signal["all"][0]
    result = {
        "source": str(source),
        "scope": "training rows only; causal histories; no validation or test file read",
        "rows": len(rows),
        "users": len(users),
        "history_length": args.history_length,
        "event_frequency": {
            name: {
                "rows": count,
                "row_rate": count / len(rows),
                "users": len(covered_users[name]),
                "user_coverage": len(covered_users[name]) / len(users),
            }
            for name, count in sorted(frequency.items())
        },
        "causal_signal": {
            name: {
                "rows": count,
                "long_view": positives,
                "long_view_rate": positives / count,
                "delta_vs_base": positives / count - base,
            }
            for name, (count, positives) in sorted(signal.items())
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
