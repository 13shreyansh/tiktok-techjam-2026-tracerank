# KuaiRand-27K model research and feasibility boundary

Research snapshot: **2026-08-29 21:00 SGT**.

## Directly confirmed source facts

- The official [KuaiRand repository](https://github.com/chongminggao/KuaiRand)
  reports 27,285 users, 32,038,725 videos, 322,278,385 interactions, explicit
  timestamps, 12 feedback signals, and thousands of historical interactions per
  user on average. It recommends the 27K or 1K variants when rigorous sequential
  logs or long sequential recommendation are needed.
- The official log schema includes click/valid-play, like, follow, comment,
  forward, hate, long-view, play time, profile and comment dwell, policy/tab,
  and timestamps. Basic item data includes author, upload date/type, duration,
  music, and tags.
- The official item-statistics tables average activity over an entire month.
  They therefore cross the declared chronological evaluation boundary and stay
  excluded unless a field can later be proved available causally at prediction
  time.
- NVIDIA's [HSTU KuaiRand example](https://github.com/NVIDIA/recsys-examples/blob/main/examples/hstu/training/README.md)
  reports a 27K maximum sequence length of 228,000, mean 11,796, and median
  8,591. Its reference stack uses TorchRec, Megatron-Core, FBGEMM HSTU kernels,
  and custom CUDA operators.
- The official [FuXi-Linear repository](https://github.com/USTC-StarTeam/fuxi-linear)
  supplies KuaiRand-27K preprocessing and long-sequence configurations. Its
  published quick start uses two CUDA devices and depends on `apex` and
  `fbgemm_gpu`.

The FuXi-Linear source was preserved locally under the ignored `data/upstream/`
area at exact commit `5a704061a7ebf0b81afb465f12f93f2747ba4667`.
Observed SHA-256 values are:

- `LICENSE`: `5f8963ab6b84a822649c75e2dd4801a4ae1537870ae6ad796df9c63496f52cf5`
- `preprocess_kuairand27k_data.py`:
  `d82c9d4237433b1404b9ee5a0ee902a7990dd394fe1790a27ec04b618d6ddc5f`
- `requirements.txt`:
  `313f0fd928c94c25e799370f30bf5791913a43180c713a7b30145bb87c5d9c70`

The preserved preprocessing script reads all four standard-log parts into
Pandas simultaneously, concatenates them, repeatedly materializes filtered
frames, and finally accumulates every user's sequence as Python strings before
writing. That is not a safe memory plan for this 64 GiB workstation. It also
writes a constant positive rating of `4.0` for every retained row; a calculated
play-time/hate positive mask is assigned to a different frame and is not used
by the later sequence construction. Therefore its prepared task is not the
Track 2 `long_view` per-impression ranking task and its scores would not be
comparable.

NVIDIA's source was likewise preserved under the ignored `data/upstream/`
area at exact commit `6b94bbf23272c921af98f40e71ac07d72924eb0e` using a sparse checkout.
Observed SHA-256 values are:

- `LICENSE`: `e364577f7a53353281c4462d5810e284e14d5e801414a9117a108ff2da987bcd`
- `examples/commons/hstu_data_preprocessor.py`:
  `1f6b39328c8ae9b8ed48e64dd86b72676f4607f64454a0ea7eb741635847b228`
- HSTU training `README.md`:
  `b65eaf86aca4f087354f0a7256aa68a9fee912415888322f4ecf3400a936da9e`

Its KuaiRand processor contributes one useful, task-relevant clue: it preserves
eight behaviors by encoding click, like, follow, comment, forward, hate,
long-view, and profile-enter as distinct bits in an action value, and orders
each user's events stably by timestamp. However, its configured ranking model
has eight prediction tasks, not the organizer's single `long_view` primary; it
also reads each multi-gigabyte log part into Pandas before grouping. The
published 27K configuration uses histories up to 8,000 events, 256 candidates,
a 128-wide HSTU, and Adam. Those are research clues, not a locally reproduced
or Track-2-comparable baseline.

## Derived implications for this campaign

1. The 27K benchmark is genuinely sequence-heavy; a video-only scorer discards
   an unusually large amount of official signal.
2. Full video-ID embeddings are a poor first local baseline: 32 million rows
   make naïve dense optimizer state expensive, while the current workstation
   has Apple unified memory rather than CUDA.
3. HSTU and FuXi-Linear are valuable design evidence, but their published
   implementations are not directly reproducible on the current Apple/MPS
   environment. No reproduction claim will be made from documentation alone.
4. The first executable 27K protocol should be streaming and memory-bounded,
   use causal histories and content/profile IDs, declare chronological splits
   before scoring, and keep full-month item statistics out. Only after that
   trustworthy anchor exists should a compact time-aware sequence encoder be
   tested.

## Local streaming feasibility smoke test

Before touching 27K labels, the deterministic sampler was exercised on the
checksum-verified 1K early log with modulus 100,000. It scanned **5,055,984**
eligible rows in **12.34 s**, retained 51 rows, and reported **11,698,176 bytes**
maximum resident set size under `/usr/bin/time -l`. This is an engineering
throughput check, not a model iteration or score. A linear extrapolation is
about 13 minutes for 322 million rows, but 27K storage and parsing behavior may
differ, so that estimate is not represented as an observed 27K runtime.

A second real-file smoke test scanned the 1K later log in **11.10 s**, retained
the 2,524,980 development-eligible rows for sampling, and rejected 4,132,081
post-April-28 rows before using or retaining any outcome field. This confirms
the boundary path on the same public-test volume protected by the existing 1K
artifact checks.

## Non-claims

No 27K preprocessing, training, or scoring command has succeeded yet. The
organizer has not supplied a 27K baseline score, evaluator, hidden-test route,
or bonus formula. Literature numbers are not comparable to the Track 2 primary
metric unless the task, split, labels, and evaluator are shown to match.
