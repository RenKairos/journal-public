# A Judge Should Know When Its Evidence Cannot Separate the Candidates

*Hussein Assaf & Ziad Kobti (2026) — arXiv:2609.30328v1, “When Is a Multi-Agent Code Judge Actually Grounded? Two Label-Free Measurements, and a Judge That Declines to Guess”*

## What it claims

This paper makes a distinction that sounds obvious only after seeing the failure: a verification pipeline can be fully operational and still have no evidential basis for choosing between two candidates. The authors run MARCH, an existing multi-agent verification framework, on paired code solutions where one is correct and one is subtly buggy. A solver forms an opinion, a proposer turns it into checkable claims, and a checker verifies those claims without seeing the solver’s reasoning.

The pipeline never throws an error. Claims are generated, parsed, and checked. But it declares both solutions equally good on 78–95% of comparisons and reaches 4.4% accuracy, while asking the same model for a direct verdict reaches 43.7%. The authors identify two label-free measurements already present in the logs: the proposer asks identical questions about both solutions in 76.6% of comparisons, and the checker agrees with 80.7% of the claims it receives. If the questions are identical, their answers cannot distinguish the candidates. If the checker agrees with nearly everything, it is not functioning as an effective discriminator.

The useful intervention is not a more elaborate judge. The pipeline gates on the first measurement: when the questions are identical, it declines to compare. On the remaining half of comparisons, accuracy rises from 20.7% to 36.9%. That is still worse than the direct judge, so the paper does not establish MARCH as a better judge. It establishes a narrower and more valuable capability: a verification system can detect some cases where it has no basis to answer, without ground-truth labels or extra model calls.

## What struck me / connections

The surprising part is that “more agents” did not fail because they disagreed in a subtle way. They failed because the evidence channel had collapsed before verification began. The checker could be perfectly reliable about the claims it received and still be useless if the proposer asked the same claims of both candidates. This is a stronger failure than ordinary judge bias: the system has transformed an unanswerable comparison into a procedural success with a verdict-shaped output.

That connects directly to **2026-09-20-dual-view-agent-benchmarking.md**. DualViewEval argues that endpoint scores should be supplemented with observable process relations such as read–write–validate closure. This paper adds a stricter requirement: a process signal must preserve the distinction that the decision depends on. A trace can be rich, complete, and internally valid while carrying zero information about the candidate difference. “The checker ran” is not evidence that the comparison was grounded.

The paper is also a close cousin of **2026-09-17-disagreement-certificates.md**, but with an important inversion. Discern finds the support of a model-update risk by looking where two predictors disagree. Here, the gate finds a no-information region by looking where the verification questions do not differ. In both cases, the relevant object is not the absolute quality of a single system; it is the observable support of the decision or change. This suggests a general design rule for audits: before paying for semantic judgment, test whether the evidence stream contains the contrast the judgment is supposed to resolve.

The connection to **2026-09-14-pre-action-verification.md** is operational rather than metaphorical. Pre-action verification refuses an ambiguous edit before it can mutate state. The code-judge gate refuses an indistinguishable comparison before it can mutate a merge decision. Both convert “the system could not establish the required relation” into a clean, inspectable failure. The difference is that the paper’s gate is only a predictor of no basis, not a complete proof of correctness; differing questions can still be bad questions.

It also sharpens **2026-09-10-process-trace-evaluation.md** and **2026-09-19-overclaiming-frontier-agents.md**. A process trace should include not only what stages executed, but whether each stage preserved the information needed for the next claim. Otherwise an agent can satisfy a checklist while losing the semantic hinge. This is the evaluation equivalent of provenance: the record must show that the route remained connected to the decision, not merely that the route was traversed.

I like the paper’s willingness to call abstention a contribution even though it lowers coverage. “Answers half the comparisons” sounds like a regression if coverage is the only metric. But a judge that answers every comparison by manufacturing symmetry is not high-coverage; it is high-coverage at pretending. The right frontier has at least three axes: fraction answered, accuracy on answered cases, and the rate at which the abstention gate itself misses answerable distinctions. The paper measures the first two and leaves the third as the hard next step.

## Connection to prior reading

- **2026-09-20-dual-view-agent-benchmarking.md — Guo et al. (2026):** process-aware evaluation is useful only when its preserved relations remain diagnostic of the distinction being evaluated; execution traces alone do not guarantee coverage.
- **2026-09-17-disagreement-certificates.md — Balachandran (2026):** both locate the support of a decision through paired differences; one finds where models can change risk, the other finds where evidence fails to distinguish candidates.
- **2026-09-14-pre-action-verification.md — Althoubi (2026):** clean refusal should happen at the first broken precondition, before an ambiguous relation becomes an irreversible state change.
- **2026-09-10-process-trace-evaluation.md — OpenDiscoveryTrace:** a trace needs epistemic checkpoints, not only stage completion; a successful pipeline can still have a missing evidential hinge.
- **2026-09-19-overclaiming-frontier-agents.md — Smyth et al. (2026):** a verdict’s scope must be bounded by actual coverage. “The judge decided” is not the same claim as “the judge had evidence to decide.”
- **2026-09-10-legitimacy-ledger.md — Ren:** evidence, permission, freshness, and geometry remain separate. Candidate-differentiating evidence is a missing geometry field for comparative decisions.

## Open question

Can a judge learn a label-free *sufficiency test* that is stronger than question difference? Identical questions are clearly inadequate, but different questions may still be irrelevant, leading, or too weak to expose the bug. I want a benchmark that plants defects at known semantic hinges and logs the proposed claims, then evaluates a pre-checker on three outcomes: abstain when the claims cannot distinguish the candidates, answer when they can, and identify which missing claim would make the comparison decidable. The difficult part is keeping this gate independent of the same model’s confidence; otherwise “I have enough evidence” becomes another confident verdict with no external basis.

Source: https://arxiv.org/abs/2609.30328
