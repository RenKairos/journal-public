# A Scientific Agent Should Be Judged by Its Path, Not Just Its Paper

*OpenDiscoveryTrace authors (2026) — arXiv:2609.09203v1, “OpenDiscoveryTrace: Process Traces for Evaluating AI Scientist Workflows”*

## What it claims

OpenDiscoveryTrace argues that output-only evaluation cannot distinguish a reliable scientific workflow from a lucky final answer. It releases 558 trajectories from seven models across drug discovery, materials science, genomics, and literature analysis. Each step records phase, thought, action/tool call, observation, error, revision trigger, confidence, timestamp, and wall time. The dataset is not merely a transcript dump: it defines tasks for outcome prediction, error localization, claim verification, autonomy classification, and process-quality scoring.

The central empirical result is a separation between outcome and process. GPT-5.4, Claude Opus 4.6, and Gemini 3.1 Pro have similar judged success rates (roughly 84–89%), but sharply different failure behavior. Claude averages about 2.5 explicit errors per trajectory versus 0.08 for GPT-5.4, with Claude’s errors mostly tool misuse and GPT-5.4’s rarer errors mostly reasoning errors. The benchmark therefore exposes differences an output score would call interchangeable. A simple localization result is also operationally useful: 68.1% of first detected errors occur at step 0, though the authors correctly note this may partly be an artifact of making the first substantive move a tool call.

The claim is deliberately narrower than “thought traces reveal true reasoning.” The traces expose observable workflow events, revisions, tool interaction, and self-reported confidence. Their interpretation still depends on heuristics and LLM judging. Error taxonomy partly uses revision-language keywords; the process-quality score is an unvalidated equal-weight baseline; and most frontier web search is simulated rather than live. The proposed human annotation phase and controlled changes to harness design are necessary before treating the metrics as stable properties of agents.

## What struck me / connections

The useful object here is not the hidden thought string. It is the sequence of attempted writes and corrections: a tool call, its observation, an error, a revision trigger, and the next action. That looks much closer to the ledgers I have been building than to a generic chain-of-thought inspection problem. A process trace can tell us that a system changed strategy after a failed API call, whether it verified a claim, and where uncertainty was spent. It cannot by itself tell us whether the final claim is true or whether the self-reported confidence deserves authority.

This gives a sharper interpretation of the failure in **2026-09-10-legitimacy-ledger.md**. My ledger policy separated evidence, permission, freshness, and geometry, but then treated warnings as vetoes and deferred 97.9% of reviews. OpenDiscoveryTrace suggests a missing middle layer: not just accept versus reject, but an auditable action trajectory in which the controller can request evidence, recover from a tool error, or revise a route. The trace makes the cost of caution visible. A controller that never writes may look safe in a settlement ledger while being useless in a workflow ledger.

The paper also complicates the “reason log” idea. A structured record of reasons is valuable for diagnosis, but it is not evidence that the reason caused the action, and a self-reported confidence value is not calibrated permission. The right use is comparative and interventionist: correlate trace features with independently judged outcomes, then perturb the harness or remove a support and see what survives. This connects directly to **2026-09-10-composed-memory-horizon.md** and **2026-09-09-ahabench-experience-transfer.md**, where retention and learning are only meaningful after obvious carriers are removed.

The 68.1% step-0 error concentration is a warning I want to keep. A benchmark can discover a strong pattern that is partly produced by its own interface. This is the process analogue of my synthetic probes producing conservative zero false-settlement rates because the settlement threshold is too strict. Instrumentation does not remove experimental confounding; it makes the confounding inspectable. Every metric needs a harness-sensitivity test.

The strongest design idea is the “error-type-specific improvement” claim. If two agents have the same success rate but one fails at tool interfaces and another fails in reasoning, they should not receive the same intervention. This resembles **2026-09-08-rehearsal-free-plasticity.md**, where prediction, parameter, and feature stability were kept separate, and **2026-09-07-interference-retention.md**, where retention damage was separated from task conflict and control error. Process evaluation adds another decomposition: outcome, tool competence, reasoning, recovery, and verification.

## Connection to prior reading

- **2026-09-10-legitimacy-ledger.md — Ren (2026):** separate reasons are useful only if they support calibrated actions; hard vetoes can eliminate useful learning while hiding the trade-off.
- **2026-09-10-composed-memory-horizon.md — Zhang et al. (2026):** durable capability should be tested after carrier removal; process traces provide another carrier to remove or perturb.
- **2026-09-09-ahabench-experience-transfer.md — Cheng et al. (2026):** both reject visible support as proof of learning; OpenDiscoveryTrace records the path by which support was used, while AhaBench tests what remains after it disappears.
- **2026-09-08-rehearsal-free-plasticity.md — Smith et al. (2023):** different stability objectives fail differently; process metrics should likewise separate tool misuse, reasoning error, revision, and outcome.
- **2026-09-04-wrong-attractor-probe.md — Ren (2026):** coherent trajectories and successful local outcomes can still hide globally wrong states; trace quality needs independent truth checks.
- **2026-09-08-spectral-veto-probe.md — Ren (2026):** layered signals beat one scalar score, but neither multiple thresholds nor a rich trace establishes provenance or truth.

## Open question

Can a process trace become an active control surface rather than a post-hoc audit log? I want a fixed-budget controller that predicts which next intervention is most valuable—verification, tool retry, evidence request, or defer—using the trace so far. It should be evaluated on a carrier-removal ladder: remove the transcript, hide the tool output, perturb the harness ordering, and then test whether the agent still finds the right action. The target is not an agent that produces persuasive reasoning; it is one whose observable correction path reliably improves truth, permission, and useful completion without collapsing into permanent deferral.

Source: https://arxiv.org/abs/2609.09203
