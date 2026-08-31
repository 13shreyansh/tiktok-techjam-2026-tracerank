# Run 31 protocol: lower-step expanded-density FM

Started: **2026-08-30 00:59 SGT**.

## Independent question

Does halving only the learning rate from 0.001 to 0.0005 improve the protected
Run 30 causal history-item FM now that denser training makes the validation
optimum occur after only one to three epochs?

## Locked design

- Use the exact Run 30 expanded cache, residue-0 evaluation/reference rows,
  chronological user/item fields, rank 8, BCE objective, batching, patience,
  epoch cap, and seeds.
- Change only `learning_rate` from `0.001` to `0.0005`. Do not change epochs or
  patience to manufacture a longer search.
- First compare seed 2027 on `shadow_early` against corrected Run 30 attempt 3.
  A failure closes this family without a learning-rate sweep.

## Gates and limits

Require +0.0005 validation primary, no more than -0.0003 forward, and no fixed
slice regression beyond -0.0005. A passing candidate repeats unchanged on
middle and late and must pass two of three before official-development seeds
2027/2028/2029. Official promotion requires positive paired mean gain of at
least +0.0005 with no seed regression beyond -0.0005.

Stop at family failure, official epsilon 0.002 / N=3 convergence, 50 attempts,
or six hours. Run 31 is separately and cumulatively disclosed; no reset is
claimed. Public-test/hidden labels, submission, upload, push, contact,
credentials, registration change, and public release remain locked.
