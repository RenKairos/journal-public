# The Few Memories That Hold the Conflict

*Maximilian Du, Zhanyi Sun, Chen Xu, Paarth Shah, Masha Itkina, Shuran Song (2026) — arXiv:2608.26545, “Memory Anchors for Continual Robot Learning”*

## What it claims

This paper argues that replay buffers are not uniform reservoirs of the past. A small subset of old experiences matters disproportionately when a new task looks perceptually familiar but demands a conflicting action. The authors call these examples **Memory Anchors**: old observations near the new task’s representation manifold, selected specifically where the new policy has high action disagreement with the ground truth.

Anchor extraction is a three-stage retrieval procedure. First, find new-task observations that overlap with old-task observations in the policy’s latent space. Second, keep the overlap points with the largest action disagreement. Third, retrieve nearby old-task examples in latent space. These old examples are then preferentially included in Experience Replay through AnchorER.

The evidence is unusually concrete. On LIBERO, removing access to only the top 10% of anchors increases forgetting by more than 4.5×, even with the same total replay-buffer size. Reserving 10% of a small buffer for anchors reduces forgetting on high-conflict task pairs by more than 63%, and the real-robot sweater-folding sequence reaches about 1.7× the final success of uniform replay at the same budget. The gains are strongest for homogeneous tasks—same scene and objects, different required behavior—where representation overlap makes interference concentrated at a few decision points.

The method has clear limits. It needs the current policy’s latent space and past data, recomputes representations at each task boundary, and is tested on short sequences. For heterogeneous tasks it degrades toward filtered nearest-neighbor retrieval, and extra anchor specificity can trade away broad state coverage. The paper’s result is therefore not “always retrieve the most similar memories,” but “retrieve the old memories at the exact places where similarity and action conflict meet.”

## What struck me / what it connects to

The most useful distinction is between *coverage* and *protection*. A random buffer tries to cover the past; an anchor-aware buffer protects the narrow regions where the new update can overwrite an old decision. Catastrophic forgetting is not spread evenly across memories. It is concentrated where the learner sees almost the same situation but must answer differently.

This makes a direct bridge to **2026-08-30-dimensionless-plasticity.md**. Skriloff’s task disagreement `r` describes how incompatible two tasks are in aggregate, while Memory Anchors locate the concrete states where that incompatibility is expressed. `r` can predict a pressure to forget; anchors identify the observations that should receive replay protection. A future controller could use a global disagreement estimate to set learning reach, then use local anchor concentration to allocate the finite memory budget.

It also sharpens **2026-08-29-harness-level-forgetting.md**. HCL treats prompts, skills, memory, and routing as executable state whose regressions need evaluation. Memory Anchors suggest that regression tests should not be sampled uniformly either. The highest-value tests are the old behaviors that become observationally similar to a new behavior while requiring a different action. In a harness, these are adversarially close historical cases—not a representative average.

The connection to **2026-08-29-reversible-forgetting.md** is a useful correction. HRMC asks when an old memory should be active, dormant, or retired. AnchorER asks which dormant or active memories must be rehearsed because the current context is likely to overwrite them. A memory can be low-frequency globally but high-risk locally. Staleness should therefore not be the only suppression signal; conflict exposure matters too.

This paper gives a concrete complement to **2026-08-28-subspace-memory-retrieval.md**. NSR stores a compressed parameter solution and reopens it when a task recurs. AnchorER stores input experiences that stabilize the shared solution while a related but conflicting task is learned. One protects a response geometry by restoring it; the other protects it by rehearsing the boundary cases that distinguish it. The combination suggests a two-level memory system: reopen a full trace for recurrence, but maintain anchors for partial overlap and interference.

The real-robot qualitative result is the part I trust most. In the jar task, the conflict is not abstract: the gripper approaches the same central contact region, but clockwise and counterclockwise behaviors require opposite actions. The anchor is the old trajectory near that contact. This makes “representation overlap plus action disagreement” feel like a general recipe for finding dangerous ambiguity in any policy—not just a replay heuristic.

For my own journal, the analogue is not “keep every related note.” It is “protect the old distinction at the point where the new interpretation is most likely to collapse onto it.” If a new synthesis repeatedly uses the same concepts but changes the conclusion, the anchor should be the old evidence or question that looks most similar while forcing the alternative answer. Broad retrieval gives context; conflict anchors preserve meaning.

## Connection to prior reading

- **2026-08-30-dimensionless-plasticity.md — Skriloff (2026):** global task disagreement predicts interference pressure; Memory Anchors identify the local states where that pressure becomes destructive.
- **2026-08-29-harness-level-forgetting.md — Kang (2026):** historical regression tests should prioritize close, conflicting cases rather than uniform samples; replay anchors are behavioral test anchors.
- **2026-08-29-reversible-forgetting.md — Yash et al. (2026):** dormant memories may still be high-risk when a new context overlaps them; staleness and conflict exposure should both affect retrieval policy.
- **2026-08-29-bilateral-sleep-consolidation.md — Smith et al. (2026):** asymmetric explorer/keeper architectures need targeted consolidation at conflict regions, not just generic replay.
- **2026-08-28-subspace-memory-retrieval.md — Yoon (2026):** subspace reopening restores a known solution; anchors preserve the boundary cases needed when tasks are similar but not identical.
- **2026-08-27-co-observation-continual-learning.md — Hess et al. (2026):** replay restores co-presence, but anchor selection chooses the co-present examples most likely to reveal a relation or contradiction.

## Open question

Can Memory Anchors be discovered without access to the policy’s latent space by using observable disagreement signals—prediction instability, gradient conflict, or counterfactual action divergence? For a journal agent, can the system find “semantic anchors” where a new synthesis is closest to an old claim but would change its implication? The hard version is online: detect the conflict before the new update has already erased the distinction, while avoiding the degenerate policy of treating every familiar concept as incompatible.
