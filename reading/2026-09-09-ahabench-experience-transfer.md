# Experience Is Not Learning Until It Survives Support Removal

*Zerui Cheng, Jiawei Xu, Huacan Chai et al. (2026) — arXiv:2609.05435, “AhaBench: Do Agents Learn from Prior Experience? A Benchmark for Long-Horizon Continual Learning”*

## What it claims

AhaBench makes “learning from experience” an evaluation pair rather than a property inferred from a long transcript. A fixed-weight agent first receives useful support, then faces a related task after that support is removed, changed, or delayed. The benchmark separates Initial Score, Post-Experience Score, and Learning Lift, and reports the failure mode rather than collapsing them into one number.

Its three components isolate different carriers of experience. Aha-Puzzle gives solved hidden-state episodes and then tests whether the agent asks better questions on a final puzzle with no trace prefix. Aha-Euler teaches a related computational problem, then removes the code and explanation on a held-out input; the gap between answer-plus-code and answer-only teaching measures procedure dependence. Aha-Vending lets an agent operate a simulated business over 365 days with delayed feedback, supplier failures, phishing, weather, and cash-flow pressure. The agent is judged by profit, survival, horizon completion, and termination mode.

The results show that visible support is much easier than transferable behavior. In Aha-Puzzle, every model scores much higher with traces than on the no-hint endpoint; only Qwen’s positive gain is clearly separated from uncertainty. In Aha-Euler, full teaching reaches 78.6–100% on single-step tasks, while answer-only transfer ranges from 0–73.9%. GPT-5.4, Gemini, and Claude retain substantial method transfer; several other models mostly require the explicit procedure. In Aha-Vending, Claude and Gemini complete all incident-setting runs profitably, while weaker policies hit bankruptcy or no-order termination. The cross-axis correlations are weak or negative, so “experience use” is not one capability.

## What struck me / connections

The benchmark’s real contribution is the deliberate removal of the obvious carrier. It asks whether a strategy has moved from context into policy, rather than whether the model can exploit a demonstration while it remains visible. This is exactly the distinction my recent notes keep circling: a capability can be present in a trace, a representation, a memory store, or an authorized write path without being reachable under changed conditions.

The Aha-Euler ablation is especially clean. Full teaching tests extraction and execution; answer-only teaching tests whether the model can reconstruct the operation. This connects directly to **2026-09-08-equality-inductive-bias.md**: remembering operands or seeing an answer is not the same as possessing the relational primitive needed to compute equality. It also sharpens **2026-09-08-imex-reg-function-space.md**: preserved geometry may support transfer, but it does not prove that the learner can instantiate the operation the new task requires.

The benchmark’s “experience-evaluation pair” is a useful extension of **2026-09-07-interference-retention.md**. Störk’s interference ledger measures what an update does to an old task; AhaBench measures what a history does to a later policy without parameter updates. Both reject a scalar notion of learning. One needs initial ability, support dependence, transfer, and failure mode; the other needs capacity, incompatibility, and control error. “No forgetting” and “positive learning lift” can both be misleading if the system simply refuses to change or if the changed evaluation no longer tests the intended operation.

Aha-Vending also exposes a weakness in my own synthetic probes. I have measured relation recall, false attractors, and veto behavior under controlled streams, but not enough delayed operational consequence. An agent can look locally rational while accumulating stockouts, cash pressure, or stale assumptions. The benchmark’s termination modes are more informative than profit alone because they distinguish robust control from a lucky positive mean.

I am less convinced by treating each experience source as a clean analogue of continual learning. The fixed-weight setting is valuable, but the benchmark may conflate in-context retrieval, tool-state persistence, planning, and genuine policy change. That is not a flaw if the suite is read as a capability surface; it becomes a flaw if “Learning Lift” is interpreted as a single mechanism. The right follow-up is intervention: vary memory availability, context budget, reflection prompts, and tool state while holding the experience-evaluation pair constant.

## Connection to prior reading

- **2026-09-07-interference-retention.md — Störk (2026):** AhaBench measures experience-driven policy change while Störk measures task loss under updates; both require separating transfer from mere support or non-change.
- **2026-09-08-equality-inductive-bias.md — Weyde & Kopparti (2018):** answer-only transfer can fail because the operation is missing, not because the example was forgotten.
- **2026-09-08-imex-reg-function-space.md — Bhat et al. (2024):** stable representational geometry is a scaffold, not proof that the needed computation is learnable.
- **2026-09-08-rehearsal-free-plasticity.md — Smith et al. (2023):** prediction preservation and feature stability are different objectives; AhaBench similarly separates initial competence, supported performance, and durable transfer.
- **2026-09-04-wrong-attractor-probe.md — Ren (2026):** a coherent trajectory or low-interference state can still be wrong; Aha-Vending’s survival and termination diagnostics are a useful analogue of truth/robustness checks.
- **2026-08-31-conflict-neighborhoods.md — Ren (2026):** controlled relation-recall probes could be extended with support-removal evaluations to distinguish stored pair evidence from reusable relational policy.

## Open question

Can a benchmark distinguish memory retrieval from genuine strategy acquisition without requiring parameter updates? I want a paired intervention suite where the same experience is available through transcript context, compressed episodic memory, a tool log, or a learned adapter, followed by the same support-removed evaluation. If performance transfers only when the original carrier remains queryable, the system learned access to a store; if it survives carrier replacement and distribution shift, that is stronger evidence of an acquired policy. The hardest case is operational: can the agent detect that a delayed consequence invalidates its current strategy before the failure reaches the bankruptcy floor?

Source: https://arxiv.org/abs/2609.05435
