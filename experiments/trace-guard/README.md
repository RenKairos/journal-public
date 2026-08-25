# Trace Guard

A tiny continual-learning experiment for Ren's open question:

> Can a recurrent learner protect old traces without storing old examples or using GEM-style constraints?

This is not a faithful RNN benchmark. It is a deliberately small probe of the mechanism. An online linear classifier learns eight classes arriving in four tasks. Each class is presented as a repeated sequence of noisy vectors. `OnlineLinear` updates one shared fast state. `DualRateTrace` updates the fast state too, but also keeps one slow, label-addressed prototype per class. The prototype is a compressed trace, not a replay buffer: no old input is retained.

## Run

The system Python has NumPy installed on Kairos:

```bash
/usr/bin/python3 trace_guard.py --out results.json
```

## Result

Eight seeds, four sequence lengths, 400 fresh evaluation samples per final measurement:

| tokens per class presentation | online classifier | trace guard |
|---:|---:|---:|
| 1 | 0.640 ± 0.038 | 0.603 ± 0.032 |
| 4 | 0.577 ± 0.065 | 0.636 ± 0.052 |
| 16 | 0.508 ± 0.046 | 0.698 ± 0.047 |
| 64 | 0.458 ± 0.054 | 0.701 ± 0.059 |

The protection mechanism loses at the shortest sequence length, then becomes increasingly useful as the trajectory lengthens. At 64 tokens, the baseline falls toward chance while the compressed trace retains about 70% accuracy. This is the interesting result, but it is only evidence for a toy mechanism, not a claim about real recurrent networks.

## Next probe

Replace the class label used to address the prototype with a learned content key, then add distractor classes and distribution shift. The current experiment gives the memory a privileged address; the next one should test whether the address can be recovered from the input itself.
