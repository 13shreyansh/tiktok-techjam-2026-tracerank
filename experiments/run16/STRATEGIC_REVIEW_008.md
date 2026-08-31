# Run 16 fresh-context review — attempt 8

## Is the gain real enough to continue?

Yes. The fixed content fields improved early validation and its paired forward
window by more than 0.014 primary, improved both official metrics, and improved
all activity slices. This is far above seed noise and organizer epsilon.

## Leakage and overfitting audit

- The added values are label-free identities from the official item feature
  table. They are available for candidate scoring.
- The cache kept identical base row arrays and order. Training-only seen masks
  still map content values absent from the training window to unknown.
- The hypothesis and exact three fields were fixed before the attempt. No
  metadata subset or weight was chosen from the result.
- No row after April 28 is retained, and no public-test label was accessed.

## Next action

Run the unchanged content FM on middle and late shadows. Require both to improve
validation and forward by at least 0.002, with neither metric nor activity
slice materially worse. If they pass, run seeds 2026/2027/2028 on official
validation and form one fixed equal mean user-rank ensemble. Preserve the base
0.644227425 1K fallback until that ensemble is verified.
