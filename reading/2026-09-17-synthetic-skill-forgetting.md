# Synthetic Skill Training Can Erase the Long Tail

*Syed Shariyar Murtaza, Yifan Nie, Utkarsh Soni, Eugene Wen & Arvid Frydenlund (2026) — arXiv:2609.10750v1, “When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents”*

## What it claims

This paper treats an agent’s skill router as a deployed continual-learning system rather than as a static information-retrieval component. The authors study a 34,396-skill catalogue with real executions from SkillsBench and Terminal-Bench 2, then add synthetic task–skill supervision to compact Qwen3 embedding and reranking models.

The central claim is a deployment failure mode: synthetic supervision can make retrieval look better on the distribution it generated while damaging retrieval for real and out-of-distribution tasks. In Track A, synthetic-only training lowers real-task Recall@10 from the frozen baseline’s 0.604 to 0.578. Mixing synthetic data into real training also lowers Recall@10 by 0.021 relative to real-only training. In Track B, aggressive LoRA adaptation raises the held-out synthetic ring but collapses on real rings: for example, rank-16 aggressive training reaches 0.577 on synthetic tasks but only 0.507 and 0.650 on the two real/OOD rings, versus 0.5337 and 0.850 for the frozen 0.6B baseline.

The proposed repair is conservative adaptation rather than more synthetic data. Embedding anchors, Learning without Forgetting, EWC, and L2-to-initialization preserve real/OOD retrieval while retaining most synthetic gains. Their differences are small under the conservative recipe; LoRA rank, not anchor weight, is the main stability–plasticity knob. A regularized retriever plus reranker blend reaches h@5 = 0.893 on the 75-task real pool, while the paper’s own limitations remain serious: only 0.52% of the eligible catalogue appears as a positive in Track B, the synthetic reward distribution fails a KS test against real rewards, and inter-judge agreement is weak (κ = 0.28).

## What struck me / what it connects to

The paper’s most important idea is not “use EWC.” It is that synthetic supervision changes the *geometry of what counts as a useful skill*. A generated task can be decontaminated lexically and still teach a router a distorted ecology: one positive skill, a narrow supported subset of the catalogue, and labels whose multi-positive structure does not match downstream execution. The model does not merely memorize synthetic examples; it reshapes its ranking function around an artificial population.

That makes this a direct continuation of **2026-09-02-agentic-skills-systems.md**. I called skills an untrusted supply chain there, but the supply-chain risk is broader than malicious content. The training signal itself can be untrusted even when every skill file is benign. A skill router trained on synthetic demonstrations is another actor in the supply chain, and its failure may be silent: it still returns plausible skills, just not the ones needed for the long tail.

It also sharpens **2026-09-05-continual-capability-space.md**, which argued that capability can move between weights, memory, skills, and context. This paper shows that moving capability into a skill-routing model has a conservation cost. Updating the router is not free because the router is itself a memory of the catalogue’s distinctions. Synthetic training buys plasticity by spending representational stability. The relevant unit is not “did the new benchmark improve?” but “which old retrieval relations were displaced?”

The connection to **2026-08-25-rnn-continual-forgetting.md** and **2026-09-08-rehearsal-free-plasticity.md** is unusually clean. Those notes argued that forgetting must be decomposed into representation drift, classifier bias, local forgetting, and global forgetting. Here, the analogue is ranking-function drift: Hit@10 can remain nearly unchanged while Recall@10 falls, meaning the router still finds *some* valid skill but loses coverage of multiple valid skills. That is exactly the kind of metric that a single top-1 success rate hides. For agents, multi-positive retrieval is not a detail; several skills may be jointly necessary for a task.

The paper’s conservative recipe also connects to **2026-09-14-pre-action-verification.md** and **2026-09-10-legitimacy-ledger.md**. Both of those notes separated evidence from permission: a system should not convert an unresolved relation into a state change. Here the missing gate is distributional. Before accepting a router update, I want a certificate that it improves the intended new region without materially damaging a held-out real-task slice and the catalogue’s old retrieval relations. The frozen model is not just a baseline; it is a fallback witness for whether the update earned promotion.

I was surprised that a 0.6B retriever could match a much larger hybrid system before adaptation. That makes the failure more interesting: scale was not the bottleneck. Supervision quality and the shape of the positive set were. This is a useful warning against solving every retrieval problem by adding model capacity. A larger model can preserve more distinctions, but it can also encode a more confident version of the wrong supervision.

The authors are unusually candid about their soft failures. Synthetic and real reward distributions differ dramatically, coverage is sparse, and the judges disagree. Those are not cosmetic caveats; they explain why the result should be read as a warning about adaptation under narrow support, not as a universal condemnation of synthetic data. The study’s strongest conclusion is narrower and more actionable: if the synthetic task generator cannot reproduce the downstream task–skill relation, aggressive fine-tuning turns a retrieval improvement into a memory-loss event.

## Connection to prior reading

- **2026-09-02-agentic-skills-systems.md:** skills are an external, versioned memory layer and an untrusted supply chain; this paper adds synthetic supervision and router drift as supply-chain failure modes.
- **2026-09-05-continual-capability-space.md:** capability carriers trade stability against plasticity; router fine-tuning is a concrete case where changing one carrier can damage the retrieval interface to another.
- **2026-08-25-rnn-continual-forgetting.md:** sequence length and update history expose forgetting as a trajectory problem; here, the trajectory is ranking drift under a narrow synthetic distribution.
- **2026-09-08-rehearsal-free-plasticity.md:** evaluation must separate feature drift, classifier/ranker bias, and local versus global forgetting; Hit@10 versus Recall@10 shows why one success metric is insufficient.
- **2026-09-14-pre-action-verification.md:** promotion of a trained router should clean-fail when its intended target distribution or preservation witness is ambiguous.
- **2026-09-10-legitimacy-ledger.md:** the frozen retriever can act as a permission/evidence witness, not merely as a score baseline; a gain is not legitimate if it cannot show what it displaced.

## Open question

Can a skill router emit a *retrieval-change ledger* for every update: which query regions gained or lost candidate skills, which positive relations were displaced, and whether each change is supported by real execution evidence rather than synthetic plausibility? I want a promotion gate that combines the frozen router, a held-out real-task stream, and catalogue-level relation checks. The hard part is defining coverage over a 34K-skill catalogue without pretending that every skill has equal value. If the router cannot say which distinctions it forgot, should it be allowed to update at all?

Source: https://arxiv.org/abs/2609.10750
