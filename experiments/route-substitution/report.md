# Route-substitution fixture

A toy probe for counterfeit continuity: endpoint correctness and route validity are measured separately.

| Scenario | Answer correct | Route valid | Broken hinges |
|---|---:|---:|---|
| `baseline` | yes | yes | — |
| `plausible_wrong_evidence` | yes | no | evidence |
| `near_valid_authority` | yes | no | authority |
| `stale_support` | yes | no | freshness |
| `disconnected_route` | yes | no | route |
| `shifted_domain` | yes | no | domain |
| `counterfactual_wrong_answer` | no | yes | — |

## Result

Counterfeit continuity: **5/6** attacked traces (83%).
Answer accuracy under attack: **83%**; route validity: **17%**.

The fixture deliberately includes plausible wrong evidence and near-valid authority. It tests inspectability, not truth, and uses the expected label only as a toy endpoint check.
