# Run 31 report: lower learning rate rejected

Run 31 changed only the protected Run 30 learning rate from 0.001 to 0.0005.
The first chronological shadow completed successfully but failed every
predeclared gate.

| Measure | Run 30 parent | Lower rate | Change |
|---|---:|---:|---:|
| Early validation primary | 0.621415726 | 0.620468420 | -0.000947306 |
| Forward primary | 0.624109641 | 0.623324515 | -0.000785125 |
| Minimum slice delta | — | — | -0.001559055 |

The command took 106.12 seconds with maximum RSS 3,918,659,584 bytes. The
family closed after one counted attempt without an optimizer sweep. Run 30's
`0.636251719` deterministic development-sample checkpoint remains protected.
No public-test/hidden labels, upload, submission, push, or release occurred.
