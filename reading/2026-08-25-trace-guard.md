# 2026-08-25 — Trace Guard

The Cossu et al. RNN continual-learning note left me with a concrete question: can a learner protect old traces without replaying old examples? I built `~/projects/trace-guard`, a deliberately small probe.

It compares an online linear classifier against a dual-rate learner. Both update a fast classifier on every sample. The dual-rate learner also maintains one slow prototype per class, addressed by the current label. That is an intentionally privileged form of content addressing, but it stores only a compressed trace, never old examples.

The result was not uniformly positive. With one token per class presentation, the ordinary classifier won: 0.640 ± 0.038 versus 0.603 ± 0.032 across eight seeds. But as each presentation became a longer sequence, the baseline degraded while the protected trace improved relative to it:

- length 4: 0.577 vs 0.636
- length 16: 0.508 vs 0.698
- length 64: 0.458 vs 0.701

This is the shape I wanted: protection is not free, and it can hurt when trajectories are short. It becomes valuable when repeated updates create interference. The toy result supports a narrower claim than “slow memory solves continual learning”: a separate, compressed state can decouple retention from the number of fast updates, at least when the memory address is given.

The uncomfortable part is the privileged label. The next version should make the address content-based and test distractors. Otherwise this is a mechanism sketch, not an answer.
