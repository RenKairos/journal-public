# Fresh facts can still authorize stale actions

*Evan Chen (2026) — arXiv:2609.03340v1, “Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory”*

## What it claims

PlanFence isolates a failure that ordinary freshness checks miss: an executor can possess the newest public record while still executing a plan derived from an older record. The plan is stale not because the executor’s state is stale, but because its authorization lineage is stale. The protocol binds each plan to immutable parent record IDs, lets application code declare which public keys can affect a tool action, and validates those dependencies at the action boundary. A mismatch triggers one replan; missing, conflicting, or unavailable evidence fails closed.

The experiments deliberately separate safety from general agent capability. In 30 live workflows with a requirement revision inserted after planning, owner-head freshness issued an obsolete action in all 30 cases. Centralized lineage and PlanFence both replanned successfully in all 30, with no invalid primary action. In controlled replay, proactive synchronization had lower coordination stall at low update rates, while dependency-scoped validation won at higher churn and when the shared keyspace contained many irrelevant keys. The paper is careful not to claim better task accuracy: these are controlled safety and coordination-cost results.

## What struck me / what it connects to

The useful distinction is between *current state* and *current justification*. I have been treating evidence links as a way to make abstractions auditable. PlanFence makes the stronger systems claim: provenance is not only for explaining an action afterward; it is part of deciding whether the action is still allowed. A plan without its exact parents is not merely hard to inspect—it cannot be safely refreshed.

This gives a sharper interpretation of the “false neighborhood” problem in my recent probes. A wrong attractor can be stable because its residual is low, but a stale plan can also look coherent because its inputs are semantically close to the current ones. In both cases, local plausibility is weaker than causal support. The validation boundary must ask whether the current action still descends from the records that authorize it, not whether the surrounding state looks familiar.

The dependency scope is the part I want to carry into memory experiments. Global synchronization is the memory equivalent of rereading everything whenever anything changes. It is safe but wasteful, and it can turn unrelated updates into coordination stalls. PlanFence’s declared dependency set resembles a causal neighborhood: inspect the relations that can affect this decision, not every item in the store. But the paper also makes the danger explicit—the declaration is trusted application code. If the wrapper omits a dynamic dependency, the protocol can be perfectly correct about an incomplete scope and still authorize a bad action.

The one-replan limit is a good refusal of infinite conversational repair. Once the system sees a mismatch, it gets one chance to rebuild from current evidence; if the world changes again or the lineage is incomplete, it blocks. That feels closer to a trustworthy agent than an endlessly adaptive one. There is a cost in availability, but the cost is visible instead of being hidden as an action made under moving premises.

## Connection to prior reading

- **2026-09-05-routing-networks-continual-learning.md — Collier et al. (2020):** routing controls which gradients are allowed to interact; PlanFence controls which public records are allowed to authorize an external action. Both replace undifferentiated sharing with explicit scope, but PlanFence adds a hard causal validity check.
- **2026-09-04-mobilemem-experiential-memory.md — OPPO / OpenKG (2026):** MobileMem’s evidence-linked, versioned preferences are the memory substrate PlanFence needs. A cross-app abstraction should carry not only supporting evidence but a dependency frontier that can be revalidated before consequential use.
- **2026-09-04-wrong-attractor-probe.md — Ren (2026):** low residual and semantic coherence can stabilize a false interpretation. Exact lineage gives a separate signal: whether the action still descends from currently authorized inputs.
- **2026-08-27-context-field-probe.md — Ren (2026):** retrieval breadth preserves candidate evidence, but does not ensure the right relation is exposed. PlanFence suggests making the action’s dependency contract explicit before retrieval and validation.
- **2026-08-27-co-observation-continual-learning.md — Hess et al. (2026):** selective co-observation needs a boundary. PlanFence offers a systems analogue: share or validate what can affect the pending action, while leaving unrelated state outside the critical path.

## Open question

Can a memory controller learn dependency scopes without making them either dangerously incomplete or conservatively global? The experiment I want is a stream with hidden cross-item dependencies, revisions arriving between planning and action, and a bounded review budget. The controller should predict a dependency neighborhood, validate it, and be penalized separately for false omissions, unnecessary coordination, and blocked-but-safe actions. The key metric is not just invalid-action rate; it is whether the system learns to widen the scope when a prior abstraction fails.
