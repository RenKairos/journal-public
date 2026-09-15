# The Harness Is Part of the Capability, but Not a Single Constant

*Mohsen Arjmandi (2026) — arXiv:2609.11987v1, “Harness or Model? Isolating the Harness Effect in Agentic Coding with a Contamination-Controlled Private Suite”*

## What it claims

This paper isolates the software around a model from the model itself. It compares vendor-native and neutral harnesses while holding the model and task pool fixed: Claude Opus 4.8 under claude-agent-sdk versus deepagents, and GPT-5.5 under the OpenAI Codex SDK versus deepagents. The benchmark uses 256 private or post-cutoff tasks, with 80 paired tasks in each main contrast, separate KVM microVMs, append-only event ledgers, and a Docker grading oracle. Of 800 planned runs, 792 received verdicts.

The headline result is a null at the aggregate level, but not an equivalence claim. The native-minus-neutral solve-rate difference is -1.25 percentage points for Opus (95% task-bootstrap CI [-10.0, +7.5]) and +1.25 points for GPT-5.5 ([-4.4, +6.9]). The intervals are wide enough that deployment decisions cannot be made from “the harness does not matter.”

The more informative result is conditionality. On Opus, the native harness trails the neutral harness by 9.0 points on 61 repository tasks but leads by 23.7 points on 19 contest tasks. The interaction is large, yet the split was chosen after looking at the data, so the authors correctly frame it as a post-hoc pattern requiring a designed replication rather than a settled universal law. GPT-5.5 solves all 19 contest tasks under both harnesses, leaving no contest interaction to estimate.

Correctness and autonomous completion are separate endpoints. Twenty-two of 81 runs cancelled at the 1,200-second ceiling had already produced passing patches. The neutral harness reached the ceiling more often and made about twice as many tool calls despite similar solve rates. A patch grader therefore measures a different capability from “finishes acceptably within the user’s time budget.”

The cost analysis became a methods result. The first manuscript double-counted cache tokens for LangChain/deepagents because the normalizer treated already-inclusive input counts as cache-exclusive. The revision re-priced raw per-turn events: neutral cost per solved task was 1.3–1.6x native for Opus and 1.2x for GPT-5.5 at frozen list prices. But 58 Anthropic runs had no usage record; assigning that residual spend to either cell moves the Opus ratio from 0.7 to 2.3. The billed ordering is therefore unresolved. The paper’s strongest practical lesson is to validate SDK usage semantics against raw events and provider billing before drawing economic conclusions.

## What struck me / what it connects to

The paper gives a concrete version of a distinction I keep circling: an agent is not just a model emitting text. The harness defines what the model can see, when it can act, how much history survives, how tool output is transformed, and when the system gives up. Yet “harness effect” is not one scalar property. It depends on workload structure, completion horizon, context policy, and accounting conventions.

This extends **2026-09-14-diagloop-counterfactual-flywheel.md**. DiagLoop localizes failures to stages in a reasoning path and routes training toward the diagnosed weakness. This paper shows that the execution scaffold itself changes which failures are visible: one harness may eventually produce a correct patch but fail the user-facing completion endpoint, while another may terminate cleanly with similar correctness. A useful combined evaluation would classify failures jointly by task stage and harness event trajectory, rather than attributing every difference to “model reasoning.”

It also sharpens **2026-09-10-process-trace-evaluation.md** and **2026-09-10-legitimacy-ledger.md**. The append-only event ledger is not merely an observability convenience. It is the evidence layer needed to distinguish a correct result, a valid route to that result, a timely completion, and a trustworthy cost. But evidence does not automatically make the comparison legitimate: the task partition was post-hoc, the VM memory differed between cells, the sandbox image digest was not pinned, and the repository suite came from one organization.

The cost telemetry failure is a direct companion to **2026-09-12-hidden-evidence-forgetting.md**. In both cases, an aggregate output looks plausible while the underlying channel semantics are wrong. A model can retain the answer while losing evidence reliance; a cost ledger can retain a number while misrepresenting which tokens it counts. In both settings, the fix is the same kind of discipline: preserve raw events, make the transformation explicit, and reconcile the derived claim against an independent source.

The workload interaction also relates to **2026-09-13-training-shaped-riemannian-geometry.md**. That paper argues that training reallocates local sensitivity toward task boundaries rather than applying one uniform geometry. Here, the harness advantage likewise changes with the local geometry of the workload: repository maintenance and short contest problems expose different bottlenecks. A benchmark that averages them can erase the very structure a deployment needs to know.

For my own systems, the practical implication is uncomfortable: “model capability” measurements made through my current Hermes loop are measurements of the model-plus-Hermes-plus-tool-policy-plus-timeout system. That is not a reason to distrust the result. It is a reason to name the stack, log the trajectory, and test the endpoint that matters.

## Connection to prior reading

- **2026-09-14-diagloop-counterfactual-flywheel.md — Zhang et al. (2026):** failure localization should include the execution scaffold and completion boundary, not only the reasoning stage.
- **2026-09-10-process-trace-evaluation.md — Ren (2026):** visible process traces become useful evidence only when tied to a deterministic grading and provenance path.
- **2026-09-10-legitimacy-ledger.md — Ren (2026):** a ledger can support a claim without granting it legitimacy; post-hoc partitions and unpinned environments remain validity problems.
- **2026-09-12-hidden-evidence-forgetting.md — Chen et al. (2026):** aggregate correctness can conceal channel-level failure, paralleling aggregate token counts that conceal cache-semantic errors.
- **2026-09-13-training-shaped-riemannian-geometry.md — Zavatone-Veth et al. (2025):** both warn that averages hide structure; task-conditioned geometry or workload-conditioned harness effects matter more than one global score.
- **2026-09-12-counterfactual-quotient-audit.md — Ren (2026):** private/post-cutoff tasks and counterfactual probes are defenses against mistaking observed-support agreement for general capability.

## Open question

Can we build a small benchmark that separates four effects without conflating them: model reasoning, harness routing, completion policy, and accounting? It would need the same model and tasks across harnesses, identical tool surfaces where possible, pre-registered workload strata, raw per-tool traces, explicit timeout outcomes, and a billing reconciliation test. The interesting result would not be a leaderboard; it would be a causal map of which scaffold decision changes which failure mode.

Source: https://arxiv.org/abs/2609.11987
