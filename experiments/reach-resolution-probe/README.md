# Reach–Resolution Probe

A small dependency-free experiment growing out of Ren's September 20, 2026 journal question: can effective epistemic reach and nuisance-aware resolution be evaluated separately?

## Question

If an agent learns to reach a new diagnostic, does that automatically mean it can make safer structural claims? Competing mechanisms:

1. Averages/utility can select an aliasing measurement that looks excellent under benign calibration contexts.
2. A nuisance-aware policy should prefer an explicitly noisy but nuisance-robust measurement, accepting unresolved cases when the route cannot be reached.

## Protocol

There are two hidden worlds (`m=0/1`) and an unobserved nuisance state `z=0..7`.

- `alias`: observes `m xor parity(z)`. Calibration overweights even `z` (80%); evaluation gives odd `z` the hard tail (60%). It always returns a singleton, but the same nuisance-blind decoder is wrong on the odd tail.
- `direct`: observes `m` with 18% measurement noise, costs the full budget, and is reachable with probability 0.25 (unlearned) or 0.90 (learned).
- If `direct` is not reached, the policy returns an explicit two-candidate set instead of fabricating a singleton.

Policies choose once from 80 calibration trials: `average` follows average calibration accuracy, `robust` compares a hard-tail lower bound, and `reach-only` switches on a reach threshold. Each condition has 200 independent seeds and 400 evaluation episodes per seed.

## Actual result

The full run was executed with:

```bash
/usr/bin/python3 reach_resolution.py --seeds 200 --episodes 400 --out results.json
```

| policy / reach | selected direct | resolution | accuracy on resolved | mean candidate set | false exclusion | hard-tail false exclusion |
|---|---:|---:|---:|---:|---:|---:|
| average / 0.25 | 41% | 0.693 | 0.575 | 1.307 | 0.372 | 0.607 |
| robust / 0.25 | 100% | 0.252 | 0.824 | 1.748 | 0.044 | 0.044 |
| reach-only / 0.25 | 0% | 1.000 | 0.400 | 1.000 | 0.600 | 1.000 |
| average / 0.90 | 36% | 0.965 | 0.551 | 1.035 | 0.443 | 0.702 |
| robust / 0.90 | 100% | 0.900 | 0.822 | 1.100 | 0.161 | 0.161 |
| reach-only / 0.90 | 100% | 0.900 | 0.822 | 1.100 | 0.161 | 0.161 |

“Selected direct” is averaged over seeds; the other columns are episode-level averages. The robust low-reach policy looks less capable if resolution means singleton output, but it is much safer: it refuses to settle most cases and nearly eliminates false exclusions. The average policy preserves more apparent resolution by selecting the alias often, but its hard-tail claims are wrong 61–70% of the time. Reaching the direct experiment helps only when the policy also evaluates its nuisance robustness; reach alone does not define safe resolution.

## Interpretation

The interesting result is not that robust wins a synthetic benchmark. It is the separation itself:

- reach is a prerequisite, not a certificate;
- high resolution can be counterfeit when nuisance context changes the meaning of an observation;
- explicit ambiguity is a measurable behavior, not a failure to hide behind a guess;
- improving reach from 0.25 to 0.90 helps the robust policy substantially, but its residual error is the direct sensor's noise, not a vanished uncertainty contract.

The alias calibration is deliberately privileged and the evaluator knows the hidden tail. This is a toy mechanism sketch, not evidence about production agents. It omits learned experiment generation, adaptive multi-step budgets, and nuisance-contract estimation.

## Next discriminating probe

Replace the fixed odd/even nuisance contract with several held-out contracts and let the agent choose among three reachable diagnostics. The key test is whether a policy can learn a reusable procedure for identifying which ambiguity remains validly resolvable without receiving the hidden relation list or hard-tail labels.
