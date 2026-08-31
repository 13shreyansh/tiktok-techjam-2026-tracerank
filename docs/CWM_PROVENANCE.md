# Counterfactual Watch Model provenance

Official upstream source: <https://github.com/hyz20/CWM>

- Acquired locally: 2026-08-29 15:45 SGT
- Git commit: `c36da4ba745a491545490be1b2b976180ab69c87`
- Upstream commit date: 2024-05-24 14:31:27 +0800
- README SHA-256:
  `040a9e97c73396b76939edf8918ec4c918ba908bc62e5900a975d4210040cab3`
- Loss implementation SHA-256:
  `dbfa9b39617443b49f54901d18027247acaa6633ee0d3a5a57c866c77283899c`
- Paper: <https://arxiv.org/abs/2406.07932>
- Paper title: *Counteracting Duration Bias in Video Recommendation via
  Counterfactual Watch Time* (KDD 2024)

The upstream repository contains no explicit `LICENSE`, `COPYING`, or licence
statement as of the recorded commit. Its local clone is therefore ignored and
must not be committed or redistributed. This repository independently
implements the paper's small censored-likelihood equation in the existing
model and records the upstream code only as verification evidence.

The upstream `run.sh` uses KuaiRand parameters `c_inv=40` and `sigma=2`; its
preprocessing truncates play time at duration and rounds both from milliseconds
to seconds. Run 10 fixes those values and changes only the auxiliary-loss
semantics relative to the paired parent.
