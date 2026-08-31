# Run 12: official hierarchical category-history audit

Run 12 acquired and checksum-verified the official supplementary category
taxonomy for all 7,583 KuaiRand-Pure videos. The fixed experiment added one
three-level category path as a candidate field and positive-history attention
signal while leaving the parent tags and all training settings unchanged.

The command succeeded. Validation changed from 0.616858721 to 0.617328286
(+0.000469565), below the +0.001 promotion gate. Forward validation improved
by +0.001038134 and low-activity users by +0.001350306, but medium-activity
users changed -0.000168862 and high-activity users -0.000589766. The signal is
therefore complementary but not robust enough for promotion.

The single attempt used 179.65 wall seconds and 3,858,513,920 maximum resident
bytes. No public-test labels were evaluated. No hierarchy-depth, embedding, or
weight search followed. The protected fallback remains the exact Run 2
six-seed within-user rank ensemble at 0.605400885.
