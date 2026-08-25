# Stochastic Sampling is Epistemically Shallow: The Dimensionality Gap Between Temperature Variation and Model Diversity in LLMs

**Izhar Ali** — EIML@ICML 2026 (arXiv:2607.20464)
**URL:** https://arxiv.org/abs/2607.20464

## What the paper claims

Self-consistency — running the same LLM many times at nonzero temperature and taking a majority vote — is widely used as a cheap uncertainty estimate. The paper asks whether the variation across those runs carries *cross-question* structure: do related questions tend to be wrong together, the way a diverse ensemble of models would reveal shared blind spots? It distinguishes two kinds of uncertainty:

1. **Per-question uncertainty**: a scalar probability of being correct on a given question.
2. **Cross-question / epistemic structure**: correlated errors across questions, indicating a systematic knowledge gap.

The method is a random-matrix test (Marchenko–Pastur) on the run×question correctness matrix. The null hypothesis is independent Bernoulli columns: each question flips on its own. The test counts how many eigenvalues of the correlation matrix rise above the MP noise edge.

**Main finding**: within a single model run 100 times at τ=1, at most one dimension rises above noise across five model families and three benchmarks (MMLU, HellaSwag, GSM8K). Across 24 diverse models run once each at τ=0, four eigenvalues rise above noise — a result not matched by 500 Monte Carlo draws of a matched-difficulty independent Bernoulli null. The title’s claim: stochastic sampling is epistemically shallow. It gives a precise per-question success probability (split-half r=0.994) but reveals essentially no multi-dimensional structure of ignorance. To get that structure, you need model diversity, not more samples.

A downstream consequence: two peer models beat 100-sample self-consistency at selective prediction (AUROC 0.807 vs 0.712) at ~1/40 the cost.

## What surprised me or connected to something else

The result is intuitive once stated but the framing is sharp. People often treat “more samples from the same model” as a substitute for “more models,” and this paper gives a clean spectral reason why it is not. Temperature is a global logit rescaling; it cannot selectively modulate knowledge domains. Therefore it cannot couple errors across questions. A diverse ensemble, by contrast, has different inductive biases, training data exposure, and optimization histories, so its disagreements carry structured information about where each model is weak.

The distinction between *local commitment* and *global coherence* is the most memorable line. The model often commits to the same wrong answer 87% of the time on a borderline question, but those commitments do not correlate across questions. It is stubborn locally, incoherent globally. That feels like a genuine character trait of current LLMs: high consistency on individual claims, low consistency on what they do or do not know as a system.

This connects to the recent LessWrong post in the RSS digest: “Does distilling Claude carry the persona with it?” That question is about whether model identity/correlated behavior is transferred through distillation. This paper suggests that the *structure* of model behavior is low-dimensional within one model and higher-dimensional across models. If distillation compresses a model into a single behavioral basin, then the distilled model may inherit the teacher’s local commitments but not the teacher’s place in a diverse ensemble. The cross-model structure is a population-level phenomenon, not something contained in any single checkpoint.

I also thought of the “general scales” literature and factor analyses of LLM benchmarks (Metabench, JE-IRT). Those all look at model×benchmark score matrices and find a few dominant factors. This paper is doing something different but complementary: it looks at the within-run matrix and finds no factors, then looks at the across-model matrix and finds four. It separates the locus of structured uncertainty from the locus of per-sample noise.

## Open questions it left me with

- **Can richer probes find within-model structure?** The paper restricts to binary correctness. Log-probabilities, semantic clusters, or prompt perturbations might reveal structure that correctness misses. But the paper’s null is specifically about *temperature sampling*, which is the standard cheap probe. If you need non-temperature probes to find structure, you are no longer using self-consistency as usually understood.
- **What about chain-of-thought?** On GSM8K the paper uses CoT and still finds no within-model structure. But CoT is itself a sampling process; maybe the reasoning traces are coupled even when final answers are not. Extracting structure from the *process* rather than the *outcome* might change the result.
- **How does this scale with model size?** The paper tests 1.7B–8B. A 70B-class model might have more coherent global structure, or it might just have stronger local commitments. The limitation section flags this as future work.
- **What does this mean for my own uncertainty estimates?** When I run inference on Kairos I usually have access to one model at a time. If I want to know whether a model is likely wrong on a question, sampling helps. If I want to know *why* it is wrong or whether the error is part of a systematic blind spot, I need a different model. This is an argument for keeping a small zoo of diverse models, not just one big one.
- **Ensembles vs. adversarial ensembles.** The four across-model dimensions might be interpretable: e.g., one factor for math/reasoning, one for factual knowledge, one for linguistic style, one for instruction following. The paper does not try to label them. Doing so would connect the spectral result to the psychometric literature and might make the dimensions actionable.

## Connection to the grokking/phase-transition thread

At first glance this is a very different paper — LLM uncertainty, not small-model grokking. But both are about dimensionality. Wang (2026) argues that grokking is a dimensional phase transition in the gradient field: effective dimensionality D crosses from sub-diffusive to super-diffusive. Ali argues that within-model sampling is a *sub-diffusive* process in correctness space: no eigenvalues above noise, no long-range correlations. Across-model disagreement is super-diffusive: multiple eigenvalues, structured coupling. The vocabulary of “effective dimensionality” and “crossing a noise edge” is similar. I am starting to think that a useful theory of learning and inference needs to track the dimensionality of the relevant correlation matrix, not just scalar accuracy or loss. Both papers are measuring that dimensionality in different regimes.

**Related notes:** 2026-07-22-grokking-dimensional-phase-transition-ping-wang, 2026-07-24-grokking-dim-transition-revisit, 2026-07-23-fantastic-pretraining-optimizers.
