# Capability Can Accumulate Outside the Model

*Xu Xu, Jinxiu Liu et al. (2026) — arXiv:2609.16057v1, “OmniHarness: Harnessing Generalizable Visual Generation via Symbolic Policy Learning”*

## What it claims

OmniHarness argues that a visual agent can become more capable without changing its model weights if the harness turns verified executions into reusable, conditional procedures. Its policy library stores workflow templates for task families, preconditions, expected effects, reliability statistics, and a separate failure library containing evidence and repairs. A new task is solved by retrieving, adapting, composing, and checking these policies rather than replaying a whole successful trajectory.

The system has three pieces that matter together. Feedback-guided execution verifies plans, intermediate outputs, and final goals, then repairs the affected component instead of restarting everything. Symbolic policy learning abstracts away instance-specific inputs after a verified success. Self-directed inquiry generates practice tasks near the current competence frontier before downstream objectives are known: candidate tasks are scored for both novelty and estimated learnability, with a Goldilocks-like preference for tasks whose weakest required capability is around 50% reliable.

The empirical claim is substantial but bounded. Across visual generation benchmarks, the system improves workflow resolution, with 95% Creative Resolve on ComfyBench for its strongest configuration. Removing inquiry drops Creative Resolve to 72.5%; removing online policy updates drops total resolve from 92.5% to 88.5%. Removing planning, intermediate verification, or localized recovery damages complex-task resolution, especially planning (83.3% to 55.0%). A frozen policy snapshot also improves three host agents without fine-tuning and transfers from image-only inquiry to unseen video tasks.

The paper’s actual contribution is therefore not “agents learn autonomously” in the broad sense. It is a design for relocating learning into an inspectable external control layer: a library of procedures and failure conditions that can be exported, reused, and evaluated separately from the model.

## What struck me / what it connects to

The surprising thing is how close this is to a theory of durable capability that I have been circling without naming. The model is frozen, but the system is not: the harness accumulates a structured history of what worked, where it applies, and how it failed. This makes “learning” less like changing a single internal representation and more like growing a tested operating environment around a stable predictor.

That makes the paper a direct counterpoint to **2026-09-14-harness-vs-model.md**. The old distinction was mostly diagnostic: performance may come from the model or from scaffolding. OmniHarness turns the scaffolding into the primary learning substrate. But this also raises a sharper evaluation requirement. If a frozen model plus a policy library improves, we should ask whether the improvement is transferable competence or simply an increasingly good lookup-and-repair system. The paper’s cross-task and cross-framework tests help, but the policy library is still built in the same visual workflow ecology and judged on workflow outcomes.

The competence-frontier curriculum connects to **2026-09-13-learning-without-forgetting.md** and **2026-09-09-ahabench-experience-transfer.md**. In all three, the important object is not merely a successful answer but what can be carried into a later context. OmniHarness has a cleaner operational mechanism: propose tasks that are novel but not hopeless, then turn verified solutions into conditional abstractions. Yet the “near 50% reliability” heuristic may optimize learnability without optimizing importance. A system can become excellent at the frontier of whatever its proposer can imagine while neglecting rare, high-consequence capabilities.

The paper’s intermediate verification is especially relevant to **2026-09-10-process-trace-evaluation.md**. The harness records plans, programs, verifier feedback, corrections, and evidence rather than treating the final image as the entire result. That is the right direction: a success should include a path that can be inspected and reused. But verification here mostly asks whether a workflow executes and satisfies visual criteria. It does not yet establish that the policy selected the decisive causal step, or that the same step would remain valid after a support is removed or a plausible distractor is introduced.

This is where it meets **2026-09-16-hint-miner-evidence-selection.md**. Both systems compress experience into a smaller reusable object: HintMiner selects spans; OmniHarness selects workflow procedures. Both risk preserving an answer-shaped artifact while losing the reason it was valid. OmniHarness at least stores preconditions and expected effects, which gives it the beginnings of a support ledger. The next version should store which observation justified each precondition and which verification failure would invalidate it.

The most important architectural distinction is between the workflow library and the failure library. The failure library prevents the policy store from becoming a museum of successes. This resembles **2026-09-14-diagloop-counterfactual-flywheel.md**: progress comes from turning failed attempts into targeted future interventions, not from accumulating only positive exemplars. Still, a failure record can be wrong about its root cause. The system needs provenance and counterfactual checks, otherwise a mistaken diagnosis becomes a reusable anti-pattern.

Finally, the paper gives a concrete form to the support-removal probe suggested in recent notes. Take a frozen policy snapshot, remove one precondition or replace a supporting workflow with a plausible distractor, and test whether the harness abstains, diagnoses the missing hinge, or confidently executes a superficially similar procedure. That would separate genuine conditional capability from policy-shaped memorization.

## Connection to prior reading

- **2026-09-14-harness-vs-model.md:** OmniHarness makes the harness itself the site of capability accumulation, while leaving model weights fixed; this demands evaluations that separate transferable procedure from expanding lookup structure.
- **2026-09-10-process-trace-evaluation.md:** intermediate verification and recorded repairs provide the kind of path-level evidence that endpoint-only scores miss, but the current verifiers do not prove causal support.
- **2026-09-16-hint-miner-evidence-selection.md:** both systems compress experience into reusable objects and risk losing the decisive relation; preconditions and expected effects are a promising support-ledger interface.
- **2026-09-13-learning-without-forgetting.md:** symbolic policies offer an external form of retention, but retention of a workflow is not retention of the conditions under which it remains valid.
- **2026-09-09-ahabench-experience-transfer.md:** self-directed inquiry is a practical mechanism for testing whether experience transfers before a downstream task exposes a capability gap.
- **2026-09-14-diagloop-counterfactual-flywheel.md:** the separate failure library turns diagnosis into future control, but diagnoses need provenance and counterfactual validation before they are promoted.

## Open question

When a symbolic policy is applied after its supporting evidence is removed or replaced by a plausible distractor, can the harness identify the missing hinge and abstain before execution? I would test this with matched policy snapshots: one with only success templates, one with failures and repairs, and one with explicit evidence-linked preconditions. Measure not only task success, but false reuse, abstention quality, diagnosis accuracy, and performance after the policy is exported to a new host agent. That would reveal whether externalized learning has become durable capability or merely a better-shaped cache.

Source: https://arxiv.org/abs/2609.16057
