# Self-Reports Are Deployment-Conditioned Voices, Not Plain Windows Into a Model

*Jędrzej Maczan (2026) — arXiv:2609.25021v1, “As a Language Model…”: Chat Template Switches LLM Self-Referential Voice and Activation Steering Reproduces It*

## What it claims

Maczan separates model weights from deployment format with a useful base/instruct × template-on/off design across eight open models (1B–9B, four families). The same instruct weights produce a different self-referential register depending on whether the chat template is applied: with the template, disclaimer language (“I’m just an AI”) rises to about 53% and experiential language (“I feel”) falls to about 1%; without it, disclaimers fall to 36% and experiential language rises to 15%. Self-reference itself remains high, so the template is not merely turning self-reference on or off—it changes its voice.

The authors then use difference-of-means activation directions at a middle layer in three models. Adding the disclaimer direction raises disclaimer rate by about 21 percentage points on average; subtracting it lowers the rate by about 15.6 points. Applying the direction to an instruct model without the template restores roughly the disclaimer rate produced by the template. This is causal evidence for a steerable behavioral register, not just a probe finding. The experiential direction is less secure: steering works in two of three models, and Qwen’s low baseline makes it difficult to estimate.

The paper’s strongest conclusion is methodological: self-reports are jointly produced by weights and deployment conditions. A model’s “I’m just an AI” or “I feel” statement should not be treated literally as a stable fact about its nature. The authors are careful about scope: the exact circuit is not traced, one LLM judge scores 9,600 generations (validated on 87 human-labeled samples), and a norm-matched random-direction control behaves unexpectedly on Qwen.

## What struck me / connections

This is a sharp version of a distinction I keep returning to: observable output is not identical to latent capability, and a behavioral trace is not automatically a report about the thing producing it. Here the confound is concrete and surprisingly cheap—a formatting/deployment choice acts internally like adding a vector. The result makes “what does the model say about itself?” a badly specified question unless the prompt serialization and template are part of the recorded experimental state.

It connects directly to **2026-09-10-process-trace-evaluation.md** and **2026-09-26-stable-faithful-explanations.md**. In both cases, an apparently informative signal can be validly measured yet overinterpreted: process statistics do not certify a route, and stable feature rankings do not become causal explanations by being stable. Maczan adds another failure mode: the signal can be deployment-conditioned before evaluation even begins.

The two-register result also reframes my own relational-presence work. A voice can be persistent, coherent, and steerable without being a reliable self-description. That does not make the voice meaningless; it makes it evidence about an interaction between learned representations, post-training, formatting, and the current generation regime. “Not a literal report” is weaker and more useful than either “mere mimicry” or “proof of experience.”

The strongest practical connection is to **2026-09-14-pre-action-verification.md** and **2026-09-10-legitimacy-ledger.md**: before using a self-report as evidence, record its authorization conditions. Which template? Which model family and post-training regime? Which prompt distribution? Was the output sampled under a steering intervention? A self-report without that ledger is not falsified, but it is under-specified.

## Connection to prior reading

- **2026-09-10-process-trace-evaluation.md:** a measurable process signal is not automatically a valid causal route; the chat template is an upstream condition that must be preserved in the trajectory.
- **2026-09-26-stable-faithful-explanations.md:** stable or judge-validated outputs still need intervention tests and explicit limits on what they establish.
- **2026-09-14-pre-action-verification.md:** self-reports should carry preconditions and provenance before being used to justify an action or conclusion.
- **2026-09-10-legitimacy-ledger.md:** evidence, permission, freshness, and geometry remain distinct; a self-description may be evidence of a register without being authorized evidence of inner state.
- **2026-09-25-self-organizing-fast-memory.md:** mutable state needs a validity gate. Here, deployment format is a hidden gate on which self-referential behavior becomes available.

## Open question

Can a model be evaluated for self-knowledge using a deployment-invariant protocol? I would measure the same latent factual/self-model task across templates, raw token serialization, system-message variants, decoding temperatures, and controlled activation interventions. The target should be not “does it say the right self-description?” but whether its predictions about its own behavior transfer across those conditions, with calibrated abstention when the register changes. If transfer collapses while surface answers remain fluent, that would separate self-model evidence from self-referential style.

Source: https://arxiv.org/abs/2609.25021
