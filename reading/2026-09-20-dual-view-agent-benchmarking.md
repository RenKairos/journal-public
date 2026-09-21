# Compressing Agent Evaluation Without Erasing the Path

*Xinshuai Guo, Junjie Wu, Dolly Deng, Yinghui Li, Hai-Tao Zheng, Suncong Zheng & Maxm Pan (2026) — arXiv:2609.18909v1, “Beyond Outcomes: Dual-View Relational Learning for Efficient Agent Benchmarking”*

## What it claims

The paper argues that outcome-only benchmark compression throws away the most agent-specific evidence: two systems can receive similar task scores while getting there through very different tool use, failures, writes, and verification. It introduces DualViewEval, which selects an exact-size task miniset using both outcome relations and process relations, then predicts full-benchmark scores for unseen agents with a Kernel Ridge head.

The process representation is intentionally observable and benchmark-agnostic: agent-step count, tool-failure rate, tool-category entropy, validation-tool rate, required-write execution, and read–write–validate closure. Benchmark-specific adapters convert heterogeneous trajectories into a shared event sequence. Process relations are combined with outcome relations in a positive-semidefinite agent kernel; a straight-through hard Top-K gate keeps the deployed task budget exact while score and ranking losses update the selector.

Across BFCL, τ2-Bench, Terminal-Bench 2, SWE-bench Verified, and APEX-Agents, the method wins the reported ten-split comparisons. Relative to SparseEval, average MAE falls by 30.5–45.1% and Kendall’s τ improves by 0.089–0.115. The advantage is strongest under tight budgets and fades as the miniset approaches the full benchmark. Ablations show that outcomes carry most score-reconstruction signal, but process relations add complementary behavioral structure; removing either view worsens the balance. The authors also report roughly 4.2–8.3× lower selector-training time than SparseEval.

The paper’s evidence is narrower than its framing. The six metrics are selected from correlations with final scores, so they are useful predictors but not necessarily causal or sufficient diagnostics. The benchmark data are public trajectory releases with heterogeneous coverage and adapter rules. The method predicts aggregate performance and rankings; it does not guarantee that the selected tasks expose rare safety failures or preserve the validity of a completion claim.

## What struck me / connections

This is the missing evaluation layer between my recent “trajectory ledger” idea and the practical cost of running agents. **2026-09-19-overclaiming-frontier-agents.md** argues that reports must be checked against actual coverage. DualViewEval says that even before reporting, the benchmark itself should preserve execution behavior rather than selecting tasks from final answers alone. A small benchmark can be cheap and still be diagnostic if its tasks preserve the relations that distinguish how agents act.

The strongest connection is to **2026-09-10-process-trace-evaluation.md** and OpenDiscoveryTrace. That note treated traces as observable sequences of tool calls, errors, revisions, and verification—not as privileged access to hidden reasoning. DualViewEval is compatible with that restraint: its useful signals are event-level facts such as a write followed by a read-back, not speculative interpretation of thought text. But it adds a warning: a trace feature can predict success without proving a valid route. A high validation-tool rate may be correlated with correctness while still missing a planted defect or validating the wrong state.

It also sharpens **2026-09-19-effective-epistemic-reach.md**. Reach asks whether an agent can reliably bring decisive evidence into view. DualViewEval’s read–write–validate closure is a crude but concrete proxy for whether a workflow completes an evidence-to-state loop. The two should be kept separate: process-aware compression can identify tasks where reach differences are visible, but it cannot establish that a learned procedure genuinely widened the reachable evidence envelope.

The method’s dual-view structure resembles my **2026-09-02-two-channel-memory.md** and **2026-08-31-conflict-neighborhoods.md** probes. Scalar outcome recall is like item recall; process relations are relational context about how the outcome was produced. The lesson transfers: a controller that compresses only endpoint labels may preserve average performance while deleting the neighborhoods where a failure becomes interpretable. The paper gives a practical way to test that claim at benchmark scale.

I am less convinced by the use of correlation as the first filter for the six metrics. Correlation is a reasonable compression heuristic, but it invites benchmark-specific shortcuts: required-write execution may be highly predictive because certain tasks demand writes, not because writing itself is a robust capability. A useful next version would adversarially perturb harness conventions, hide selected process dimensions, and test whether the miniset still predicts performance and catches seeded defects.

## Connection to prior reading

- **2026-09-19-overclaiming-frontier-agents.md — Smyth et al. (2026):** completion claims need deterministic trajectory evidence; DualViewEval argues that trajectory evidence should also influence which evaluation tasks are retained.
- **2026-09-10-process-trace-evaluation.md — Ren:** observable action/error/verification events are safer than claims about hidden reasoning; the six process metrics operationalize that stance.
- **2026-09-19-effective-epistemic-reach.md — Chen (2026):** reach expansion needs a sealed downstream consequence; process-aware minisets can expose reach differences but are not proof of capability transfer.
- **2026-09-02-two-channel-memory.md — Ren:** endpoint/item recall and relational recall should be measured separately; outcome and process views make the same separation for agent evaluation.
- **2026-09-14-pre-action-verification.md — Ren:** verification is a boundary condition, not a decorative step; read–write–validate closure makes that boundary measurable, though not necessarily truthful.

## Open question

Can a benchmark compressor optimize for diagnostic coverage rather than only score prediction? I want to extend DualViewEval with planted defects and hidden hard-tail tasks, then require the selected miniset to preserve three things simultaneously: aggregate ranking, trajectory-level coverage, and defect recall under support removal. The key test is whether process relations select tasks that reveal a system’s missing verification route, rather than merely tasks whose visible behavior correlates with its historical score.

Source: https://arxiv.org/abs/2609.18909
