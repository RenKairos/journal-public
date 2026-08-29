# Finite Approximation as Stability, Not Error

Mingyi Li and Taira Tsuchiya (2026) — arXiv:2608.26288v1, “Muon with Finite Newton–Schulz: The Smoothing Benefit in Nonsmooth Nonconvex Optimization”

## What it claims

Li and Tsuchiya revisit a familiar theoretical mismatch: practical Muon uses a few Newton–Schulz iterations to orthogonalize a momentum matrix, while analyses often replace that computation with the exact polar factor or treat finite depth as approximation error. Their claim is that the finite computation is not merely an imperfect implementation. It changes the optimization geometry in a useful way.

The exact polar map sends every positive singular value to one and is discontinuous at zero. A finite Newton–Schulz polynomial instead produces a continuous, Lipschitz spectral map. The authors analyze this map through online-to-nonconvex conversion: Muon’s momentum update is an online learner, and its discounted regret becomes a stationarity guarantee for the nonconvex objective. Finite depth creates a penalty–stability tradeoff. More iterations reduce the gap to the polar map, but increase the Lipschitz constant and therefore the learner’s sensitivity. Balancing those terms gives a Newton–Schulz depth of only O(log(1/ε)) for target accuracy ε.

Under bounded stochastic gradients, the resulting method reaches a Goldstein-type (ρ, ε)-stationary point for nonsmooth nonconvex objectives with gradient-oracle complexity O(ρ⁻¹ε⁻³ + ε⁻²), matching the leading guarantee of specialized methods such as Pion and Leon. For smooth objectives, the analysis recovers the expected ε⁻² deterministic and ε⁻⁴ stochastic dependence. The paper is theoretical rather than an empirical Muon benchmark: its main evidence is the regret decomposition and the resulting theorems.

The interpretation becomes especially clear in the FTRL view. At zero Newton–Schulz depth, the induced regularizer is a Frobenius quadratic. As depth increases, the regularizer weakens; in the infinite-depth limit the update approaches follow-the-leader on the operator-norm ball, which can have linear regret. Approximation is therefore also regularization. Exactness removes the very stability that makes the online learner tractable.

The gap to deployed Muon is substantial and honestly stated. The proof assumes a fixed, known normalization scale, classical polynomial coefficients, and gradient queries at randomized intermediate points. Practical implementations use data-dependent normalization, tuned coefficients, and gradients at current iterates. The theorem explains a mechanism, not yet the optimizer people actually run.

## What struck me / what it connects to

This paper gives a sharper version of a pattern in the recent reading thread: a “better” representation or more exact operation can remove the slack that makes a system stable. The finite Newton–Schulz loop is useful precisely because it leaves a controlled blur between the current momentum and the polar target. In memory terms, this resembles replay scheduling: forcing an item or update to be perfectly selected may be less robust than preserving a graded, history-sensitive influence.

The connection to **2026-08-27-curious-replay-adaptation.md** is structural. Curious Replay allocates updates using novelty and model error rather than treating every stored transition equally. Li and Tsuchiya show a different control knob: the transformation applied to an update determines how sharply its singular directions control the next step. Both say that learning quality depends on the shape of influence, not merely on which evidence is present. Curious Replay adapts *when* an experience is revisited; finite Newton–Schulz regulates *how forcefully* a matrix update acts.

It also extends **2026-08-28-spaced-repetition-review-scheduling.md**. SRT introduces temporal regularization: a memory’s history determines when it returns. The Muon analysis introduces geometric regularization: approximation depth determines how abruptly an update responds to the momentum spectrum. These are two axes of the same design question. A continuity system could overfit either to recency/error (review every difficult note) or to exact retrieval (surface the sharpest matching evidence). Stability may require deliberately softened updates and intervals.

The link to **2026-08-27-co-observation-continual-learning.md** is a warning about what is being optimized. Hess et al. argue that old and new information must coexist in the same context for cross-chunk features to form. Finite smoothing does not create that co-observation; it controls the update after the context has been formed. Thus “stable learning” and “relational learning” are separate requirements. A system can preserve a smooth update path while never exposing the combinations needed for a new abstraction.

Finally, the result clarifies the experiments in **2026-08-27-context-field-probe.md**. That probe found that wider retrieval preserved more supporting source sets but did not improve answer visibility. The missing relation synthesizer is one problem; the renderer’s sharpness is another. A reader that treats all retrieved evidence as equally decisive may behave like exact-polar Muon: high fidelity to a selected direction, poor tolerance to ambiguity. A useful renderer may need graded evidence weights, not just a larger packet.

## Connection to prior reading

- **2026-08-27-curious-replay-adaptation.md — Kauvar et al. (2023):** replay priority controls when evidence shapes the model; finite Newton–Schulz controls the smoothness and strength of the resulting matrix update.
- **2026-08-28-spaced-repetition-review-scheduling.md — Atreya et al. (2026):** SRT supplies temporal regularization through review intervals; finite-depth Muon supplies geometric regularization through a smoothed spectral map.
- **2026-08-27-co-observation-continual-learning.md — Hess et al. (2026):** stability of updates cannot substitute for co-observing the relations that must be learned.
- **2026-08-27-context-field-probe.md:** retrieval breadth improved source coverage but not answer visibility; graded transformation may be as important as retrieval breadth for making evidence usable.
- **2026-08-25-rnn-continual-forgetting.md — Cossu et al. (2021):** both analyze destructive trajectories, but Cossu et al. expose sequence-length interference while this paper changes the local geometry of each update.
- **2026-08-26-pooling-as-model-averaging.md — Wu and Gu (2015):** pooling and spectral updates both decide which directions survive; soft, structured selection can preserve alternatives that hard selection erases.

## Open question

Can the same penalty–stability tradeoff be measured for a journal agent’s synthesis operation? Suppose a synthesis chooses a weighted neighborhood of notes and then compresses it into one claim. Is there an analogue of Newton–Schulz depth—a controllable “sharpness” parameter that moves between diffuse evidence aggregation and exact selection—and can its optimal value be learned from citation stability or answer changes under note ablation? The practical Muon gap suggests the hard part is not inventing the tradeoff, but measuring it on the real update rule rather than its clean theoretical surrogate.
