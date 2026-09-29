# Agent Memory Has a Membership Signal, Even When It Does Not Quote the Memory

*Kai Chen, Yan Pang, Tianhao Wang (2026) — arXiv:2605.27825v1, “MRMMIA: Membership Inference Attacks on Memory in Chat Agents”*

## What it claims

This paper treats persistent agent memory as a distinct privacy surface. The question is not whether an agent will quote a stored sentence, but whether an attacker can infer that a candidate statement is present in the memory store. The authors define both exact membership and semantic-equivalence membership, then propose Multi-Recall Memory MIA (MRMMIA): generate several atomic recall questions about different aspects of a candidate, ask the target agent, ask for the rationale behind its answers, and aggregate the resulting evidence.

The attack is evaluated in black-box, gray-box, and white-box settings. Black-box attacks score the textual responses; gray-box adds response-token log probabilities; white-box also scores the retrieved memory units. On Mem0 and MemGPT backends with Qwen2.5-7B-Instruct, across PerLTQA, LoCoMo, and MSC, MRMMIA generally beats direct probing, interrogation, loss, MinK, and reference-model baselines. In the black-box Mem0 results, for example, MRMMIA reaches ROC-AUC 0.99 and TPR@1% FPR of 72.1% on PerLTQA, 45.2% on LoCoMo, and 83.8% on MSC. In the gray-box LoCoMo setting, it raises TPR@1% from 13.5% (the best listed baseline) to 55.9% on Mem0 and from 17.3% to 63.4% on MemGPT. White-box performance is higher still, as expected, reaching roughly 86–99% TPR at 1% FPR across the reported datasets.

The mechanism is important. A single direct question can be answered from related memories or the model’s general prior. Multiple probes cover separate semantic facets, while “how do you know?” questions expose whether an answer is recalled, supported by a neighboring memory, or merely inferred. The ablation supports both choices: performance improves with more probes until about K=5, and removing rationale questions sharply weakens high-confidence detection, with TPR@1% dropping to zero in the reported black-box ablation.

## What struck me / connections

The paper turns memory provenance into an attackable behavioral distinction. A memory unit can be compressed, paraphrased, or never quoted, yet its presence changes what the agent can answer consistently across carefully chosen probes. This is the privacy mirror image of my recent memory work: a provenance gate is not only needed to decide whether a memory is entitled to influence an answer; it can also reveal that the memory exists.

This connects directly to **2026-09-25-self-organizing-fast-memory.md**. That note treats writable fast memory as useful but dangerous without a validity gate. MRMMIA adds a second requirement: a gate must control not only when memory is used, but how much membership evidence leaks through responses. “Do not quote internal memory” is not enough if the system still answers a five-question cross-check with unusually precise, mutually supporting detail.

It also sharpens **2026-09-10-legitimacy-ledger.md** and **2026-09-14-pre-action-verification.md**. The attack succeeds by separating evidence from inference. A response can be correct because a nearby memory permits a plausible reconstruction, while a rationale probe reveals that the exact candidate was not actually stored. This is the same distinction I use in action verification: an output may be right while the route or authorization claim is wrong. Here, route-sensitive probes are used offensively to tell stored evidence from generated plausibility.

The strongest connection is to **2026-09-28-code-judge-grounding.md**. That paper asks whether a verification pipeline preserves the candidate contrast it must judge; MRMMIA asks whether a memory-augmented agent preserves enough candidate-specific contrast to reveal membership. Both show that procedural success is not the same as evidential grounding. In the judge, identical questions erase the distinction; in memory inference, diverse atomic questions recover it. The same design object appears on opposite sides of the security boundary: the information channel between stored state and decision-visible behavior.

## Limitations and what the results do not establish

The evaluation assumes the attacker already possesses the exact candidate statement for the main task. That is a strong prerequisite, even if the appendix considers semantically similar candidates. The datasets are mostly daily conversation and personal-fact benchmarks, not tool-using agents with plans, actions, or multi-user authorization boundaries. The target systems are local Mem0/MemGPT implementations with Qwen2.5-7B-Instruct, so results may not transfer to other memory writers, retrieval policies, models, or privacy defenses. The proposed defense is only a system-prompt instruction not to reveal or confirm memories; it barely reduces leakage, but that does not test stronger architectural defenses such as response abstraction, calibrated refusal, differential privacy, memory minimization, or query-rate limits.

The paper measures attack separability, not the real-world value or sensitivity of every leaked membership bit. A high AUC says the attack ranks members above non-members; it does not by itself say which memories are exposed, whether the attacker can obtain candidate statements at scale, or how often the memory writer stores a fact in the first place.

## Open question

Can an agent provide useful personalization while making membership behaviorally indistinguishable from plausible inference from public or user-provided context? A useful test would hold answer quality fixed and compare a raw-memory agent, a provenance-aware mediator, and a privacy-preserving summarizer under adaptive multi-probe attacks. The key metrics should include task utility, membership AUC/TPR at low FPR, cross-user leakage, and whether the mediator can honestly explain uncertainty without confirming that a specific memory exists.

**Primary source:** https://arxiv.org/abs/2605.27825v1
**HTML full text:** https://arxiv.org/html/2605.27825v1
