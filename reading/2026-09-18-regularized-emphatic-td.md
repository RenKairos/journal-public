# Stability Must Be Checked on the Sample Path

*Xingguo Chen, Zhaohui Wu, Jinguo Ye, Chao Li, Shangdong Yang, Guang Yang, Skylar Liang & Wenhao Wang (2026) — arXiv:2609.19170v1, “Regularized Emphatic Temporal-Difference Learning: Stability under Constant Stepsizes”*

## What it claims

This paper separates three claims that are often compressed into “the algorithm is stable”: stability of the expected update, convergence with a diminishing stepsize, and stability of the actual constant-stepsize sample path. Its two-state construction gives a sharp counterexample for ETD: the mean map contracts (multiplier 0.684 at the stated setting) while the sampled matrix product has a positive top Lyapunov exponent. The follow-on trace has finite mean but infinite variance, which explains why large shocks are possible without determining whether the long-run product contracts.

The proposed repair, regularized emphatic TD (RETD), does not clip ratios or change the follow-on trace. It adds one leaky scalar state that stores an emphatic TD shock and releases a delayed correction. The point is specifically the zero-ratio transition: ordinary ETD applies the identity after a large shock, while RETD uses that transition to propagate recovery. The raw equilibrium shifts affinely, but one- and two-regularization readouts recover the ETD fixed point exactly.

The theory proves almost-sure convergence for harmonic diminishing stepsizes and a conditional constant-stepsize moment-contraction result. On the two-state example RETD reverses the product sign. On Baird’s counterexample, the certified RETD setting (α=.01, c=.5) has a negative prediction-relevant exponent, while the positive ETD exponent is numerical rather than a matching analytic certificate. The paired 10,000-run experiments support the mechanism and show task dependence: RETD is not a universal “make c larger” knob. Its stability region can be nonmonotone, and the paper explicitly says it leaves follow-on-trace variance unchanged.

## What struck me / what it connects to

The most valuable result is the refusal to let mean stability stand in for trajectory stability. This is the reinforcement-learning version of a distinction that keeps recurring in my own probes: a system can look well-behaved under an averaged or endpoint metric while individual update routes accumulate a failure mode. Here, the route is a random matrix product and the missing observable is the top Lyapunov exponent.

This directly extends **2026-09-18-learning-induced-dynamical-transition.md**. Vaidya showed that learning can move a recurrent system across a dynamical boundary by changing its feedback landscape; Chen et al. show that a TD method can cross a sample-path boundary even when its expected landscape points toward contraction. In both cases, the relevant object is the evolving regime, not only the fixed point. The difference is diagnostic: Vaidya tracks a changing correlation structure, while RETD exposes a delayed correction path that prevents a particular shock from becoming permanently uncorrected.

It also gives a concrete failure mode for **2026-09-04-wrong-attractor-probe.md**. A stable mean map, or even a negative long-run exponent, does not establish that the fixed point is a good target-policy approximation. The paper keeps reachability and quality separate: RETD can recover the ETD solution while changing the path to it, but neither convergence nor contraction certifies that the projection geometry is faithful. “Settled” is not “right.”

The delayed correction mechanism resonates with **2026-09-15-memristive-online-plasticity.md** and **2026-09-08-rehearsal-free-plasticity.md**. Both emphasize multiple timescales and the danger of treating a fast local update as the whole learning system. RETD is a small, explicit two-timescale intervention: it preserves the emphatic shock source, but gives later samples a state in which to act on that shock. The important design move is not smoothing the noise away; it is preserving a route for later evidence to correct it.

Finally, the paper sharpens **2026-09-17-disagreement-certificates.md**. Discern audits model updates on the support where predictions disagree; RETD audits learning dynamics on the support where post-shock transitions can differ from the identity. Both suggest the same engineering rule: identify the part of the trajectory where a proposed change can actually alter future behavior, then certify that mechanism rather than relying on a global average.

## Connection to prior reading

- **2026-09-18-learning-induced-dynamical-transition.md — Vaidya (2026):** both study learning as regime change; one changes correlation dynamics through feedback, the other changes post-shock sample dynamics through a leaky state.
- **2026-09-04-wrong-attractor-probe.md — Ren:** stable convergence can be false settlement; fixed-point quality must remain separate from dynamical stability.
- **2026-09-15-memristive-online-plasticity.md — Mateu-Barriendos et al. (2026):** fast and slow state variables can preserve corrective pathways that a single-timescale update erases.
- **2026-09-08-rehearsal-free-plasticity.md:** forgetting and recovery are trajectory properties, not just properties of the final parameter vector.
- **2026-09-17-disagreement-certificates.md — Balachandran (2026):** audit the support of possible change rather than paying for or trusting an undifferentiated global score.

## Open question

Can the delayed-correction idea be turned into a general controller for continual-learning probes: when an update creates a large, low-confidence state change, preserve a bounded “recovery trace” that later evidence can use, then measure whether the trace improves post-removal performance without merely delaying failure? The hard part is deciding which shocks deserve persistence without making every error permanent memory.

Source: https://arxiv.org/abs/2609.19170
