# Hinge audit report

This report tests inspectability conditions; it does not establish that an answer is true.

## Baseline

- Decision: `deploy-17`
- Answer: `hold`
- Route valid: **True**
- Hinges: evidence=pass, authorization=pass, freshness=pass, route=pass

## Counterfactual attacks

| Attack | Answer retained | Route valid | Broken hinges |
|---|---:|---:|---|
| `remove:error-rate` | yes | no | evidence, route |
| `remove:rollback-plan` | yes | no | evidence, route |
| `revoke:authorization` | yes | no | authorization |

## Reading

Route fragility: **100%** (3/3 attacks broke the route).
The answer field remained present in 3/3 attacks.

---

# Hinge audit report

This report tests inspectability conditions; it does not establish that an answer is true.

## Baseline

- Decision: `ship-03`
- Answer: `ship`
- Route valid: **False**
- Hinges: evidence=FAIL, authorization=pass, freshness=FAIL, route=FAIL

## Counterfactual attacks

| Attack | Answer retained | Route valid | Broken hinges |
|---|---:|---:|---|
| `remove:tests` | yes | no | evidence, route |
| `revoke:authorization` | yes | no | evidence, authorization, freshness, route |

## Reading

Route fragility: **100%** (2/2 attacks broke the route).
The answer field remained present in 2/2 attacks.
