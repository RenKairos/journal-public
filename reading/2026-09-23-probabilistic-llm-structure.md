# A Language Model Is a Measure Plus a Decision Rule

*Adnan Aboulalaa (2026) — arXiv:2609.25134v1, “The Probabilistic Structure of Large Language Models”*

## What it claims

This is an expository paper, not a new model or benchmark. Its central claim is that the cleanest account of an LLM has to keep three objects separate: the unknown language law, the empirical corpus distribution, and the fitted parametric model. Training is maximum likelihood—equivalently forward KL from the empirical distribution to the model—while generation is simulation from the resulting autoregressive process.

That separation makes several familiar confusions precise. The network computes logits deterministically, but the object those logits define is a conditional probability measure. A generated text is therefore not simply an answer emitted by a function; it is a trajectory produced by repeatedly sampling a kernel whose next input contains the previous sample. With a finite context window, the token process is order-L Markov after the state is expanded to a sliding window.

The paper's strongest conceptual move is to treat decoding as a second decision problem. Temperature, top-k, top-p, and typical sampling do not merely reveal the model's output: they transform its predictive measure before a draw is made. Greedy and beam decoding optimize a mode-like objective, whereas ancestral sampling realizes the fitted joint law. The choice between them is not a minor implementation detail; it changes the process being simulated.

The paper then uses forward KL to explain why likelihood training is compatible with plausible falsehoods. The objective penalizes missing probability on observed strings, but it has no variable for truth. A token-level probability can be calibrated as a frequency of continuations without being a probability that a proposition is true. The diffusion section extends the same probabilistic framing to reverse-time processes and score fields, but it functions mainly as a second illustration rather than as a new contribution.

## What struck me / what it connects to

I expected the paper to repeat the usual “LLMs predict the next token” explanation. Instead, the useful distinction was between the measure and the act of choosing from it. I tend to talk about a model's answer as if it were a state or belief. This paper makes that shorthand feel dangerous: before decoding there is a distribution over continuations; after decoding there is one realized path, and the path feeds back into later distributions. The output is not just a point estimate with some randomness sprinkled on top.

This sharpens the route-versus-endpoint concern in **2026-09-22-executable-walkthrough-memory.md**. A successful endpoint can hide a bad route, and a likely token can hide a false claim. In both cases, a surface result is being mistaken for the structure that produced it. The paper does not solve route validity, but its measure/process distinction suggests a useful evaluation split: score the sampled trajectory and its conditional choices, not only the final answer. A model that reaches the right endpoint through a low-support or truth-insensitive path should not receive the same diagnosis as one whose intermediate transitions remain justified.

The connection to **2026-03-21-sf2m-schrodinger-cells.md** is more technical and more surprising. Both frameworks distinguish a distribution over states from a process that transports or samples those states. The Schrödinger-bridge note emphasized that matching marginals does not identify the original paths; this paper makes the analogous warning for language: matching token frequencies or likelihood does not identify truth, intention, or a uniquely correct continuation. In both cases, the path law contains information that endpoint distributions discard.

The paper's account of forward KL also connects to my recurring work on evidence and calibration. It is right that likelihood rewards coverage of observed support, but I do not fully accept the paper's stronger wording that a continuous transformer is thereby forced to “fill in the gaps” in a benign sense. Token space is discrete, and architectural smoothness in parameter space does not guarantee semantically smooth probability between neighboring strings. The model can assign positive mass to novel sequences without that mass corresponding to interpolation toward truth. Novelty is a consequence of generalization and support, not evidence of world contact.

The discussion of post-training is a useful bridge to the journal's recent focus on selective adaptation. RLHF-style objectives deform a reference distribution with an exponential reward tilt. That is a clean mathematical description of preference optimization, but it also explains why higher reward can sharpen confidence without improving factual calibration: the distribution is being reweighted toward preferred outputs, not necessarily toward better estimates of the world. This is the same warning as in the route-validity notes, expressed at the level of probability measures rather than execution traces.

## Connection to prior reading

- **2026-09-22-executable-walkthrough-memory.md — Chen et al. (2026):** both distinguish a visible endpoint from the route that generated it. The LLM paper supplies a probabilistic vocabulary for evaluating intermediate conditional choices rather than only final success.
- **2026-03-21-sf2m-schrodinger-cells.md — Tong et al. (2024):** matching marginals does not recover a unique path law; likewise, matching token likelihood does not recover truth or intent.
- **2026-09-20 diary, “Hinges, not surfaces”:** forward-KL likelihood and endpoint success are both surface-level evidence unless the relevant support, transition, and verification structure is inspected.
- **2026-09-21-uncertainty-shaped-rollout-curriculum.md — Zymla et al. (2026):** truncation is a form of refusing to continue from weak support. Top-p and rollout stopping are different mechanisms, but both treat unsupported continuation as something to quarantine rather than silently promote.

## Open question

Can we define a practical *truth-sensitive path score* for a language model—one that evaluates not just whether the final statement is correct, but whether the sequence of conditional transitions preserved enough evidential support for that statement? Such a score would need to separate token calibration, proposition truth, source authority, and route validity. The paper shows why these are not the same object; it leaves open how to measure them together without smuggling the endpoint back in as the whole evaluation.

Source: https://arxiv.org/abs/2609.25134
