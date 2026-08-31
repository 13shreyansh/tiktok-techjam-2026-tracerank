# Run 9: explicit deep-cross architecture audit

Run 9 tested one bounded DCN-V2-inspired hypothesis: add two parallel
full-rank cross layers to the existing target-aware history model, leaving the
data, split, seed, evaluator, optimizer, FM term, and deep tower unchanged.

The command succeeded, but the candidate was rejected. Validation moved from
0.616858721 to 0.616292357 (-0.000566363). Forward validation improved from
0.603960752 to 0.604613423 (+0.000652671), but all five activity/date slices
regressed, including -0.001339921 for high-activity users. The result did not
meet the predeclared +0.001 validation gate.

The single attempt used 215.64 wall seconds and 3,815,112,704 maximum resident
bytes. No public-test labels were evaluated. No layer, projection, width, or
learning-rate search followed the failure. The protected official-validation
fallback remains the exact Run 2 six-seed within-user rank ensemble at
0.605400885.
