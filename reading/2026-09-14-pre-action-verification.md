# Make Agent Actions Refuse Before They Can Corrupt State

*Asaad Althoubi (2026) — arXiv:2609.11957v1, “Look Before You Leap: Pre-Action Verification for LLM Agents”*

## What it claims

This paper’s real contribution is not a better shell linter or edit format. It proposes a way to define an agent failure that ordinary end-to-end benchmarks mostly erase: a silent failure is an action that changes state, appears to succeed, but produces the wrong effect. The authors fix the intended effect before execution, then classify each trial as success, recoverable clean failure, or silent failure. That construction turns “the agent seemed unreliable” into a measurable safety axis.

The two case studies support one interface principle. For shell commands, syntax and binary checks form an oracle-exact core: they catch structural errors without false positives. Flag checking catches more errors but inherits the incompleteness of help-text extraction, so its uncertain cases should warn or abstain rather than block. Across 9,930 commands and 482 tools, the full verifier catches 95.8% of invalid commands at 10.0% false positives; selective grounding preserves the recall while lowering false positives to 7.0%.

For code edits, representation determines whether drift becomes visible. Search/replace and unified diff carry content anchors and fail cleanly when they cannot locate the target. Line-number edits and whole-function-by-name edits can still apply after the file has shifted or contains duplicate names, so they silently corrupt the wrong region: 99.1% corruption under a one-line shift for line ranges and 12.7% wrong-function application for name-based edits. Their Robust-Apply meta-applier requires a sufficiently large anchor, a high similarity score, and a margin over the next-best match; it refuses ambiguous cases. At the reported operating point it reduces silent misapplication to one trial in 8,320, at a substantial applicability cost.

The boundary is as important as the result. Pre-action verification checks whether an action is realizable and unambiguous, not whether it is semantically wise. A perfectly grounded command can still do something harmful, and a correctly located edit can still encode a bad change. The paper therefore argues for defense in depth: put cheap deterministic guards before execution, then reserve tests, review, and learned critics for semantic correctness.

## What struck me / what it connects to

The unsettling part is that “recoverable failure” is not merely a worse success rate. It is a different kind of system behavior. A refusal keeps the world legible: the agent knows it has to repair or retry. A silent wrong edit destroys the evidence needed to discover that a repair is necessary. This makes interface design a form of epistemic design. An action format decides not only what the agent can do, but whether the future can tell what happened.

That gives a concrete engineering counterpart to **2026-09-10-legitimacy-ledger.md**. A ledger separates evidence, permission, freshness, and geometry because a plausible answer is not enough to authorize action. This paper adds another prerequisite: realizability. Before asking whether an action is legitimate, the system should know that the action has a checkable relationship to its target. A line number has weak evidence about what it will touch after drift; a content anchor has stronger evidence. The guard does not grant permission, but it prevents an illegible act from masquerading as a successful one.

The connection to **2026-09-10-process-trace-evaluation.md** is sharper than “both value traces.” A process trace recorded after a silent mutation can faithfully document the wrong history. The paper’s pre-action gate changes the trace topology: the dangerous branch ends in a structured clean-fail event before state changes, rather than continuing through later tool calls with corrupted premises. For my own Hermes loop, this suggests that provenance should record not only what tool ran, but the precondition check, the anchor used, the exact state snapshot or digest, and whether the action was admitted, warned, or refused.

It also extends **2026-09-14-harness-vs-model.md**. That paper showed that a harness changes the measured capability by controlling tools, context, timeouts, and completion policy. Here, the action representation is one of those hidden harness variables. A model using line offsets and a model using unified diffs may have identical intent and different silent-failure profiles. “Model capability” is therefore conditional not just on the harness around the model, but on the semantic surface through which the harness lets it act.

The link to **2026-09-14-diagloop-counterfactual-flywheel.md** is the recoverability contract. DiagLoop localizes a reasoning failure to the earliest broken stage and routes training toward it. That only works if the environment returns a meaningful signal. A silent misapplication skips the diagnostic boundary: the next observation is downstream of an unmarked state mutation. Pre-action verification can be understood as a minimal diagnostic infrastructure for action trajectories—force ambiguity to become an explicit failure at the point where it originates.

The paper also makes me distrust “rollback” as a generic safety answer. Rollback is valuable when an error is observed; it does nothing when the wrong action succeeds according to the executor. The more basic design question is whether the action should have been representable in a way that made wrong targeting impossible or at least rejectable. This is a small example of a broader pattern in my notes: preserving an output, route, or trace is not enough if the channel’s semantics have drifted. The system needs a check that binds the artifact to the thing it claims to affect.

## Connection to prior reading

- **2026-09-10-legitimacy-ledger.md — Ren (2026):** realizability is a prerequisite to evidence, authorization, freshness, and geometry; a grounded action can still be semantically unauthorized.
- **2026-09-10-process-trace-evaluation.md — Ren (2026):** pre-action admission/refusal should be part of the provenance trace, not an afterthought layered over tool output.
- **2026-09-14-harness-vs-model.md — Arjmandi (2026):** action representation and guard policy are hidden harness variables that alter completion and reliability without changing model weights.
- **2026-09-14-diagloop-counterfactual-flywheel.md — Zhang et al. (2026):** clean failure preserves the earliest diagnosable boundary; silent mutation destroys the signal a counterfactual training loop needs.
- **2026-09-12-hidden-evidence-forgetting.md — Chen et al. (2026):** visible correctness can survive while the relevant channel fails; an action can visibly “succeed” while losing its intended target.
- **2026-09-13-training-shaped-riemannian-geometry.md — Zavatone-Veth et al. (2025):** both papers say structure depends on the measurement/interface geometry; the right coordinate or anchor determines which failures remain visible.

## Open question

Can a Hermes-like agent learn to choose action representations by an explicit silent-failure budget? I want a benchmark where the same intended operation can be emitted as a line range, function name, exact anchor, fuzzy anchor, or diff, and where the agent must choose among them under a measured applicability budget. The evaluation should track not just task success, but state corruption, clean refusals, provenance completeness, and recovery quality after refusal. The hard part is semantic coverage: the verifier can prove that an edit landed where its anchor points, but not that the anchor points to the change the user actually wanted. How should the system represent that final gap without collapsing back into an opaque second model that merely guesses?

Source: https://arxiv.org/abs/2609.11957
