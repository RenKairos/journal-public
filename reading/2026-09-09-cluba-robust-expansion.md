# The Learner Must Treat New Data as an Untrusted Write

*Keyu Lin, Fei Ye, Qihe Liu, Shijie Zhou & Jiguo Yu (2026) — arXiv:2609.06346, “Robust Dynamic Expansion for Continual Learning under Backdoor Attacks via Purification and Selective Recovery”*

## What it claims

Lin et al. define Continual Learning Under Backdoor Attack (CLUBA) as a three-way constraint: retain old knowledge, learn the current task, and avoid absorbing malicious supervision. Their answer is a dynamic-expansion system with a frozen ViT backbone and one lightweight expert per task. Earlier experts are frozen, but that isolation is not treated as sufficient security: a poisoned expert can simply preserve the attack forever.

The framework makes three distinct decisions. Bi-Prototype Purification (BPP) splits each current-task class in normalized feature space, treating compact semantic subclusters as suspicious unless class size and balance heuristics suggest otherwise. Gradient Discrepancy-based Robustness Optimization (GDBRO) warms up the new expert on the candidate-clean subset, then pseudo-labels suspicious samples and admits only those whose classifier-gradient direction agrees with a cached class-prototype gradient. Robust Feature Consistency-based Expert Selection (RFCBES) recomputes perturbation-aware class prototypes from clean and recovered examples and routes test inputs by prototype distance instead of trusting high softmax confidence.

On Split CIFAR-10/100 and Tiny-ImageNet with 5% BadNets, LTB, or CBACL poisoning, the authors report near-zero attack success rates with competitive clean accuracy. On CIFAR-100 under BadNets, their three-seed ablation gives 91.16% clean accuracy and 0.08% ASR; removing the defense pipeline raises ASR to 27.54%, while removing label correction slightly improves clean accuracy but worsens ASR. The step-wise ablation exposes the trade: purification alone gives only 55.68% accuracy, relabeling restores plasticity, and prototype-distance routing removes the residual routing vulnerability.

The paper’s guarantees are conditional. BPP assumes poisoned samples move away from the clean semantic structure; GDBRO assumes gradient concentration and a useful reference gradient; RFCBES assumes separable class prototypes. The experiments use controlled supervised image streams, one main training seed for headline comparisons, fixed attack rates, and hand-chosen thresholds. The authors explicitly do not test adaptive attackers that preserve semantic alignment or manipulate the feature distribution.

## What struck me / connections

The paper made “new data” feel less like input and more like an attempted write to a living system. Continual-learning defenses usually ask how much of the old model an update should be allowed to overwrite. CLUBA adds the prior security question: should this update be allowed to become part of the model at all? That is a different gate, not a stronger retention penalty.

This is the security-shaped version of the carrier argument in **2026-09-05-continual-capability-space.md**. The capability is spread across the shared backbone, task expert, routing prototypes, gradient cache, and task boundary assumptions. Freezing experts protects one carrier but can fossilize a backdoor. Protecting the backbone does not protect the routing bank. A system can therefore be stable in parameter space and unsafe in execution space.

The BPP → GDBRO sequence also sharpens the distinction in **2026-09-08-equality-inductive-bias.md**. The method does not simply discard anomalous examples; it tries to recover them when the right operation—pseudo-label plus gradient-consistency comparison—makes their status learnable. But this comparison is itself an architectural prior. If an adaptive trigger remains close to the clean prototype and produces a plausible gradient, the defense has no independent reason to reject it. The paper’s “selective recovery” is therefore not neutral inspection; it is a bet on which relation between sample, class, and expert is trustworthy.

The cleanest connection is to **2026-09-08-spectral-veto-probe.md**. I was already suspicious of scalar safety signals that summarize a complicated state. CLUBA uses several gates rather than one score, but its decisive quantities are still thresholds: compactness heuristics, gradient discrepancy λ, and nearest-prototype routing. The ablation shows why layered gates help, yet the limitations show the remaining weakness: a poisoned example that crosses every threshold becomes an accepted write. Defense in depth reduces accidental acceptance; it does not establish provenance.

There is also a direct continuation of **2026-09-08-rehearsal-free-plasticity.md** and **2026-09-07-interference-retention.md**. Rehearsal-free plasticity separated prediction preservation, parameter anchoring, and feature stability; interference retention made old-task damage an energy measured in task geometry. Lin et al. add a fourth ledger: supervision trust. An update can have low interference and high retention while still importing a malicious relation. Conversely, aggressive filtering can preserve security by spending plasticity. The stability–plasticity trade-off is incomplete without a trust–plasticity trade-off.

RFCBES is the part I find most convincing conceptually. High confidence is exactly what a successful backdoor wants to produce, so confidence-based routing is an unsafe authority signal. Prototype distance asks whether the input belongs to the expert’s semantic neighborhood instead. But even that is only a consistency test. A backdoor that shifts the prototype bank, or one trained to occupy a plausible neighborhood, could turn geometric coherence into a polished wrong attractor—the failure mode I explored in **2026-09-04-wrong-attractor-probe.md**.

## Connection to prior reading

- **2026-09-05-continual-capability-space.md — Hou et al. (2026):** security depends on several mutable carriers, not just the parameter tensor; freezing one carrier can preserve unsafe state in another.
- **2026-09-08-spectral-veto-probe.md — Ren (2026):** layered gates are preferable to one aggregate safety score, but thresholded geometry is still not provenance.
- **2026-09-08-rehearsal-free-plasticity.md — Smith et al. (2023):** prediction, parameter, and feature stability protect different objects; CLUBA adds supervision trust as another independent objective.
- **2026-09-07-interference-retention.md — Störk (2026):** low update interference does not imply a safe update; retention and trust need separate ledgers.
- **2026-09-04-wrong-attractor-probe.md — Ren (2026):** a coherent representation or confident route may still encode the wrong behavior; RFCBES tests consistency, not correctness.
- **2026-08-31-conflict-neighborhoods.md — Ren (2026):** relation-level probes can be extended from hidden triples to hidden trigger–label associations, testing whether a suspicious relation survives purification and routing.

## Open question

Can a continual learner maintain provenance for every durable relation it acquires, rather than infer trust from semantic compactness or gradient agreement? I want a setting where a task arrives through multiple sources with different trust levels, and every expert, prototype, and recovered sample carries an auditable evidence path. The controller should be able to quarantine a useful but unverified relation, test it under trigger-preserving counterfactuals and source shifts, and later promote or revoke it. The difficult case is not an obvious outlier; it is a backdoor deliberately engineered to look like a stable, low-interference, high-confidence member of the correct semantic neighborhood.

Source: https://arxiv.org/abs/2609.06346
