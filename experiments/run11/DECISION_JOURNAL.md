# Run 11 decision journal

## 2026-08-29 15:55 SGT — campaign start

- Protected fallback: official validation primary 0.605400885.
- The meeting and starter define a candidate-ranking task scored user by user;
  final whole-list diversity re-ranking remains out of scope.
- Predeclared one neural LambdaLoss candidate with fixed pair counts, learning
  rate, metric mixture, and early-stop rule.

## 2026-08-29 16:04 SGT — attempt 001 rejected

- The run's best pointwise checkpoint scored 0.616981924. The first LambdaLoss
  epoch reduced it to 0.616863608, so patience stopped the fine-tune and the
  pointwise checkpoint was restored.
- The restored final result was only +0.000123203 over the separately run
  paired parent; forward change was +0.000021100. Both are far below the
  +0.001 promotion gate and consistent with run variance.
- The successful command used 390.93 wall seconds and 16,949,690,368 maximum
  resident bytes. Public-test labels were not evaluated.
- Decision: reject and stop this family without tuning pair counts, learning
  rate, or metric weights. Preserve the 0.605400885 fallback.
