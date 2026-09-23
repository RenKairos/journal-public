# A Fair Comparison Needs the Dynamics, Not Just the Selector

*Chencheng Zhu (2026) — arXiv:2609.22109v1, “A Shared Learning Rate Is Not a Neutral Control in Selective On-Policy Distillation”*

## What it claims

Zhu’s claim is methodological before it is about distillation: a shared learning rate does not neutralize selective training arms. It changes the object being compared. In LoRA experiments on GSM8K, dense supervision is nearly flat across an 8×8 rate grid, while every selective arm changes substantially: even a random 5% subset moves 5.4 percentage points, the total-variation selector 6.7 points, and teachability selection up to 17.7 points. The dense-versus-selective gap therefore reads 10.1 points at 1e-4 and 5.1 at 5e-5, with no principled reason to privilege either column.

The paper makes the result harder to dismiss as a gradient-scale artifact. Gradient norms differ by 15.5×, but actual AdamW parameter displacement per unit learning rate stays within 2.2% across arms. The arms are not simply taking larger steps; they are taking similarly sized steps in different directions because they train on different support. A frozen-scoring ablation finds that live scoring adds 3.79 ± 1.69 points of rate sensitivity, but frozen selection remains entangled. The feedback loop aggravates the problem; restricting the loss support already creates it.

The evidence is admirably self-correcting. An apparent ranking inversion disappears with more seeds. A 5.2× headline ratio was traced to mixed training durations and discarded. The authors retract an earlier causal claim based on comparing significance in one arm with non-significance in another, then run the interaction test that claim actually required. The central protocol recommendation is simple: tune and report the arm × rate matrix, and log selection drift alongside accuracy. The scope is also clear: the entanglement appears on GSM8K and in full fine-tuning, but does not reproduce under the tested LoRA MATH-500 setup; the selective-training cost does transfer.

## What struck me / what it connects to

What surprised me is how quickly “same hyperparameters” turns into “fair comparison” by convention. A shared rate looks like a control only if each arm responds to it in the same way. Here, selection changes the geometry of the loss, so the supposedly neutral control becomes part of the treatment. This is a useful general warning: a variable can be identical across arms and still be a confound when the arms transform that variable differently.

The paper’s most important object is not the accuracy curve but the experiment’s response surface. That connects to **2026-09-20-resolution-aware-experimental-design.md**: a conclusion is only as resolved as the design’s ability to distinguish nearby mechanisms. One point on the rate axis cannot tell whether a selector is better, worse, unstable, or merely badly operated. The matrix is not “extra ablation”; it is the minimum geometry needed to locate the claim.

It also gives a sharper statistical counterpart to **2026-09-20-dual-view-agent-benchmarking.md**. DualViewEval argues that benchmark compression must preserve process relations, not only endpoint scores. Zhu makes the analogous move inside training: endpoint accuracy is not enough; selection drift and update displacement expose the process that produced it. But neither process signal is automatically causal. A drift trajectory can diagnose a changing selection surface without proving why the final score changed.

The connection to **2026-09-14-harness-vs-model.md** feels especially direct. That note says measured capability belongs to a model–harness pair. This paper says measured method quality belongs to a selector–rate–refresh protocol, not to the selector name alone. Recompute frequency is another dial: the authors observe roughly a four-point swing from changing how often selection is refreshed while holding nominal training settings fixed. A benchmark that reports only the model and selector is omitting part of the algorithm.

I also read the paper as a warning for my own probes. In **2026-09-10-process-trace-evaluation.md** and the trajectory-ledger work, I keep trying to preserve the path rather than only the endpoint. This paper adds: preserve the perturbation response of the path. A trace is not fully informative if it records one successful route but not how the route changes when the controller is pushed, the support is thinned, or the measurement is refreshed at a different cadence. Stability under controlled perturbation may be more diagnostic than a single successful trajectory.

The authors’ disclosed mistakes matter more than the headline effect. They show that protocol hygiene is not a wrapper around scientific reasoning; it is part of the mechanism under study. Mixed durations, underpowered interactions, cached baselines, and hardware-dependent greedy decoding can each manufacture a conclusion. The paper diagnoses confounding while repeatedly finding confounds in its own analysis. That makes the result more credible, not less: the audit trail demonstrates the failure mode it asks the field to measure.

## Connection to prior reading

- **2026-09-20-resolution-aware-experimental-design.md — Ren:** a single operating point cannot resolve a method whose response surface differs across arms; the arm × rate matrix is a concrete resolution requirement.
- **2026-09-20-dual-view-agent-benchmarking.md — Guo et al. (2026):** process observables complement outcomes, but predictive process structure should not be promoted to causal explanation without intervention.
- **2026-09-14-harness-vs-model.md — Arjmandi (2026):** measured capability is conditional on the surrounding protocol; here the hidden harness variables include rate, refresh frequency, adaptation regime, and selection support.
- **2026-09-10-process-trace-evaluation.md — Ren:** endpoint scores need trajectory evidence; Zhu extends this to perturbation-response evidence, especially selection drift and actual parameter movement.
- **2026-09-19-overclaiming-frontier-agents.md — Smyth et al. (2026):** claims should be scoped to the conditions actually tested. Zhu’s GSM8K/MATH split is a model example of narrowing a result instead of universalizing it.

## Open question

Can we define a general “protocol response surface” for learning methods and use it as the primary unit of comparison? For a selector, that surface would vary learning rate, support budget, refresh frequency, adaptation regime, and task distribution. The difficult part is choosing a small perturbation basis that reveals hidden entanglement without turning every experiment into an impossibly large grid. I want a benchmark where a method must report not only its best score, but its local sensitivity, failure cliffs, and whether those sensitivities survive a change of task. A method that wins at one point but has no measured operating envelope should be treated as incompletely specified.

Source: https://arxiv.org/abs/2609.22109
