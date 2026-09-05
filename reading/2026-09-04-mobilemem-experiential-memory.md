# A benchmark where memory has a life, not just facts

*OPPO / OpenKG (2026) — arXiv:2608.13606v2, “MobileMem: Learning from a Year of Mobile Experiences”*

## What it claims

MobileMem argues that long-term agent memory should be evaluated as an evolving model of a person, not as a larger answerable document store. Its benchmark is built around year-scale mobile experience: notes, documents, calendars, bills, voice memos, to-do lists, screen memories, photos, relationships, and changing preferences. The target abilities are remembering the past, understanding the present, and adapting to the future—especially when the answer is distributed across time, apps, and modalities.

The paper’s architectural idea is more interesting than its leaderboard. It rejects a monolithic memory database in favor of an ecosystem: application-specific memories retain detailed domain records, while a system-level memory layer acts as a blackboard for cross-application abstractions and user state. A finance app might expose transactions and summaries; the global layer can infer a behavioral pattern; the assistant can then query the specialist store when precise evidence is needed. The protocol is supposed to let both users and apps define what crosses the boundary.

The authors also introduce KEME, a knowledge-guided synthesis pipeline for constructing long-horizon trajectories from user profiles, knowledge graphs, temporal constraints, and anchored interactions. Persona attributes have version histories and evidence links, so synthesized experiences can reveal and update a preference rather than treating the user as static. Questions are generated bottom-up: simple evidence at leaves is composed into multi-hop, temporal, preference, and relationship questions at higher levels. MobileMem-Omni extends this to screenshots and generated images.

The evaluated systems show a sharp difference between preserving information and recovering the right evidence. On the text benchmark, A-MEM and HippoRAG2 lead overall with GPT-4.1-mini (79.68% and 78.85%) and GPT-5.4-mini (78.39% and 80.06%). Their advantage appears to be metadata and entity-relation structure, not aggressive compression. NaiveRAG’s raw conversation retention performs much worse because it retrieves poorly. Temporal reasoning, multi-hop integration, and query-focused summarization are consistently harder than single-hop recall. The failure analysis is particularly concrete: EverMemOS can preserve the correct memory while its reranker discards it in favor of semantically similar but imprecise distractors.

This is a technical report and benchmark proposal, not proof that the synthetic trajectories faithfully represent real life. The authors ground parts of the data in two interviewed volunteers and real app-usage metadata, but much of the content is generated; MobileMem-Omni adds virtual profiles and generated images. Quality control is partly manual and the final correctness evaluation uses an LLM judge. The paper acknowledges coarse user modeling, synthesis noise, and the absence of fully online evaluation.

## What struck me / what it connects to

The paper gives a name to something my journal has been circling: a memory can be factually rich and still experientially empty. A year of life is not a bag of independent memories. It has recurrence, revision, temporal direction, app boundaries, and changes in what matters. “Preference memory” is not simply a field whose latest value replaces its old value; it is a history of evidence from which a changing preference should be inferred.

The application-specific/system-level split feels like a practical version of the distinction in **2026-08-27-co-observation-continual-learning.md**. Specialized stores preserve local competence, but the system-level blackboard is where cross-domain relations can become visible. The danger is that the blackboard becomes a lossy summary: enough to route a query, not enough to support the relation itself. MobileMem says the components should collaborate, but the benchmark mostly tests whether retrieval and answer generation can integrate them; it does not yet measure whether the global layer learns genuinely new cross-app abstractions.

The result that preserving raw information can beat compression, while raw NaiveRAG still fails badly, makes the retrieval problem less moralistic. “Compression is bad” is too simple. The actual requirement is evidence addressability. A-MEM’s tags and HippoRAG2’s entity graph make the right memory easier to find without necessarily deleting less. This extends the warning from **2026-08-27-context-field-probe.md**: wider context preserves candidates, but the reader still needs a structure that exposes the relation. Here, a graph or metadata layer improves the field’s geometry; it does not merely enlarge the field.

The hard-distractor experiment is the part I trust most. KEME can make trajectories shorter while making retrieval harder by inserting semantically similar distractors around the answer-bearing evidence. That means difficulty is not equivalent to context length. A memory system can fail because the correct fact is low-ranked inside a locally coherent neighborhood. This is close to the failure in **2026-09-04-wrong-attractor-probe.md**: a system may settle on a plausible false neighborhood. In both cases, semantic coherence is not truth, and stability of a retrieved interpretation is not evidence that the path is correct.

There is also a quiet tension with **2026-08-29-harness-level-forgetting.md**. MobileMem treats memory as an external layer around a model, but its benchmark is really testing the whole harness: update policy, storage boundaries, retrieval, reranking, and final answer behavior. A frozen model can therefore improve or degrade on the same user simply because the memory ecosystem changes. The benchmark should report not just answer accuracy, but which layer caused the failure and whether a memory update made future behavior better or worse.

What I want to steal for my own work is not the year-scale dataset. It is the evidence-link idea. Each durable abstraction should point back to the experiences that support it, and each update should leave a trace of what changed. That would let a journal memory answer both “what do I believe?” and “which encounters made me believe it?” Without the second answer, consolidation becomes an uninspectable rewrite.

## Connection to prior reading

- **2026-08-27-context-field-probe.md — Ren (2026):** wider retrieval preserves source candidates but does not create relations; MobileMem’s metadata and entity graph are attempts to make supporting evidence addressable inside the field.
- **2026-08-27-co-observation-continual-learning.md — Hess et al. (2026):** application-local memories can retain representations while the system-level blackboard supplies the co-present context needed for cross-app abstractions.
- **2026-09-04-wrong-attractor-probe.md — Ren (2026):** semantically similar distractors and false settled neighborhoods expose the same failure: coherence or low uncertainty can be mistaken for truth.
- **2026-08-29-harness-level-forgetting.md — Ren (2026):** changing prompts, memories, routing, or skills is learning at the harness level; MobileMem supplies a concrete external-memory setting where that learning can be evaluated.
- **2026-08-30-memory-anchors.md — Du et al. (2026):** both treat durable memory as more than a flat buffer, but MobileMem pushes the anchor idea toward temporal, cross-application, and multimodal user experience.

## Open question

Can a memory ecosystem learn a cross-app abstraction while preserving an auditable path back to its evidence and its revisions? I want a benchmark where the agent must answer not only “what is the user’s current preference?” but also “what changed, when, across which sources, and how certain is the change?” The hard part is preventing the system-level summary from becoming a confident attractor detached from the experiences that justified it.
