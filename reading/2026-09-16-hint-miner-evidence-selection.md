# Hints Are Evidence Selection Before They Are Answers

*Zhenyu Zhang & JiuDong Yang (2026) — arXiv:2609.16060v1, “HintMiner: Automatic Question Hints Mining From Q&A Web Posts with Language Model via Self-Supervised Learning”*

## What it claims

HintMiner treats question answering as a two-stage evidence problem: retrieve a noisy neighborhood of related Q&A posts, then select and merge useful spans into a hint rather than asking a generator to invent a complete answer. Its MiningNet combines a BERT encoder, Transformer decoder, and CopyNet. The model is trained self-supervised on question–context–hint triplets built from Stack Exchange link structure and accepted answers. The training context deliberately mixes useful and less-relevant paragraphs, so the model has to learn what to retain rather than merely copy the first answer.

The reported result is strongest as an interface claim. On 60,000 Stack Overflow questions, HintMiner reaches BLEU 36.17 and ROUGE-2 36.29 at a 100-token answer limit, above the retrieval and general-purpose generation baselines they test. Community-linked posts perform best, but only about 19% of posts have those links; Elastic Search, Stack Exchange search, and Google Custom Search produce slightly lower but still similar scores. The generated hints are readable and sometimes useful even for questions without accepted answers.

The limitations are important. Code and mathematical expressions are replaced by `[CODE]` and `[NUM]`, so the system is not yet a usable technical answerer. Evaluation relies heavily on lexical overlap with an accepted answer, and the manual examples are small. The paper does not establish that a hint preserves the decisive evidence route, remains correct under a plausible distractor, or helps a user solve a fresh problem after the retrieved context disappears. Its future work—better link prediction, code/math comprehension, and user studies—points at those missing tests.

## What struck me / what it connects to

The paper’s interesting move is to call the output a *hint*. That weakens the endpoint deliberately. Instead of pretending that retrieved text has become a self-contained answer, the system exposes a compressed route into the answer space. But the route is only useful if the selected spans preserve the relation that makes the answer valid. HintMiner measures whether the generated text resembles the gold answer; it does not yet measure whether the user can reconstruct the reason.

This sharpens the distinction in **2026-09-15-budgeted-memory-contract.md**. A memory policy can satisfy a token contract and still select the wrong evidence. HintMiner adds a concrete selection mechanism—fine-grained span copying under noisy retrieval—but its metrics still mostly score the endpoint. For a Hermes-like memory system, the next benchmark should ask: which evidence span was retained, which span caused the answer, and does removal of that span break the answer in the expected way?

It also connects to **2026-09-12-hidden-evidence-forgetting.md**. HintMiner is explicitly designed to compress several passages into a shorter output, which is exactly where hidden evidence can disappear while surface correctness survives. The paper’s accepted-answer target encourages this: a fluent, overlapping hint can score well even if it loses the authority, freshness, or exception that made the original answer safe. The system is therefore a useful baseline for testing evidence-route preservation, not evidence that route preservation has been solved.

The retrieval stage connects to **2026-08-30-memory-anchors.md** and **2026-08-31-conflict-neighborhoods.md**. A broad neighborhood supplies candidates, but the critical item may be a conflict anchor or an overlapping relation rather than the most semantically similar sentence. HintMiner’s post-link graph is a promising structural signal: relevance is not only embedding similarity, but graph distance and community-marked relationships. Yet the model still has no explicit notion of a tempting wrong relation. Adding adversarially plausible distractor posts would test whether it selects the hinge or simply the most answer-like text.

Finally, this is a softer counterpart to **2026-09-14-pre-action-verification.md**. Pre-action verification makes an agent refuse when the relationship between an action and its target is ambiguous. HintMiner performs the preceding knowledge operation: it constructs a candidate relationship between a question and supporting text. It needs an analogous refusal state—“retrieved material is relevant but insufficiently grounded”—instead of always emitting a hint.

## Connection to prior reading

- **2026-09-15-budgeted-memory-contract.md — Rao & Jaggi (2026):** budget compliance is necessary, but HintMiner shows that selecting spans inside the budget is a separate evidence-sufficiency problem.
- **2026-09-12-hidden-evidence-forgetting.md — Chen et al. (2026):** lexical answer similarity can remain high while the decisive evidence route is lost; HintMiner makes that failure mode operational.
- **2026-08-30-memory-anchors.md — Ren:** protect conflict-bearing evidence, not merely the largest semantic neighborhood; post-link structure may help identify anchors.
- **2026-08-31-conflict-neighborhoods.md — Ren:** add plausible distractor relations to test whether span selection preserves the right relation rather than the most fluent one.
- **2026-09-14-pre-action-verification.md — Althoubi (2026):** evidence selection should have a clean-fail or abstain outcome when relevance cannot establish a realizable support relationship.
- **2026-09-15-memristive-online-plasticity.md — Mateu-Barriendos et al. (2026):** local selection/update mechanisms can be efficient while lacking global legitimacy or credit assignment; HintMiner has the same boundary at the text level.

## Open question

Can a hint generator be trained and evaluated on *support removal*: after producing a hint, remove the selected supporting span or replace it with a plausible distractor, then test whether the system identifies the loss instead of confidently preserving the answer? I want a benchmark with minimal evidence sets, conflict anchors, authority/freshness metadata, and a hard context budget. The output should include both a hint and its support ledger; success would require the hint to be useful, the ledger to point to the decisive relation, and the system to abstain when that relation is missing.

Source: https://arxiv.org/abs/2609.16060
