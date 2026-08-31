# Run 10: censored watch-time auxiliary audit

Run 10 implemented the organizer-recommended Counterfactual Watch Model loss
as a separate auxiliary head while preserving the judged native `long_view`
BCE and inference score. It used the official CWM repository's KuaiRand
settings (`c_inv=40`, `sigma=2`) and a predeclared auxiliary weight of 0.1.

The command succeeded, but the candidate was rejected. Validation changed
from 0.616858721 to 0.613846302 (-0.003012419), and forward validation changed
from 0.603960752 to 0.601552606 (-0.002408147). Every activity/date slice
regressed, with the largest decline (-0.004919455) on high-activity users.

The single attempt used 296.16 wall seconds and 5,373,296,640 maximum resident
bytes. No public-test labels were evaluated. No auxiliary-weight, inverse-cost,
or sigma search followed the failed gate. The protected fallback remains the
exact Run 2 six-seed within-user rank ensemble at 0.605400885.
