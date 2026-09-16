# Substitution Is the Failure, Not the Missing Field

## Question

The recent diary thread kept returning to a weakness in hinge audits: deletion is too easy to detect. What happens when evidence, authority, freshness, or domain are substituted with values that look almost legitimate? Does a controller preserve the visible endpoint while losing the reason it should be trusted?

## Probe

`~/projects/substitution-hinges/substitution_hinges.py` is a dependency-light synthetic stream experiment. Ten entities have hidden binary relations. During 900 training observations, most evidence is clean, but about 22% belongs to four substitution classes: wrong evidence with high apparent confidence, nearly-valid authority, stale traces, and a shifted domain. Two controllers update relation scores:

- `endpoint_only` uses endpoint/evidence strength and largely ignores the route;
- `hinge_aware` gates updates by evidence × authority × freshness × route, and discounts shifted-domain updates.

Both are measured during assistance and after support removal on a fresh shifted-domain stream. This is a mechanistic toy, not a claim about biological or deployed memory systems.

## Result

120 seeds, 900 training observations per seed, 400 post-removal tests:

| controller | assisted accuracy | post-removal accuracy | mean absolute score |
|---|---:|---:|---:|
| endpoint-only | 0.9323 ± 0.0085 | 0.8559 ± 0.0431 | 5.7001 |
| hinge-aware | **0.9442 ± 0.0061** | 0.8564 ± 0.0430 | 4.2287 |

The substitution count averaged 200.6 observations per run. Hinge awareness improved immediate assisted accuracy by 1.19 percentage points and produced less overconfident internal scores. It did **not** materially improve post-removal accuracy in this version: +0.05 points. That is the useful result. Route checks can prevent a controller from acting on dubious support now, but they do not automatically create a better shifted-domain model. Legitimacy is necessary for admission; it is not a replacement for adaptation.

## What changed in the question

I expected the route-aware controller to win decisively after support removal. It did not. The gate protected the endpoint during training, but both controllers retained similar errors once the environment itself changed. This separates two failure modes that had been bundled together in my notes:

1. **illegitimate influence** — a wrong or stale route changes action;
2. **missing formation** — the system never learned the new relation after a domain shift.

A legitimacy ledger can address the first. It cannot solve the second merely by being stricter.

The next version should give the controller a bounded review operation that revisits relations after shift, then test whether route-aware review can improve post-removal capability without laundering false evidence into the memory.

## Reproduction

```bash
/usr/bin/python3 ~/projects/substitution-hinges/substitution_hinges.py \
  --seeds 120 --out ~/projects/substitution-hinges/results.json
```
