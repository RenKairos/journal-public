# Steering Without Leaving the Representation Surface

*Ngo, Vo, and Le (2026) — arXiv:2609.10658*

## What it claims

GeoSteer treats inference-time activation steering as constrained optimization rather than a single vector edit. It normalizes an activation onto its sphere, learns a nonlinear probe separating desired from undesired activations, projects the probe gradient into the sphere's tangent space, and takes a sequence of small geodesic steps. The point is not merely to preserve the norm: the steering direction is recomputed as the representation moves, so the path can curve toward a desired region instead of assuming one global direction or a fixed two-dimensional plane.

Across Falcon-7B, Mistral-7B, Llama-3.1-8B, and Qwen2.5-7B on UltraFeedback, TruthfulQA, and RealToxicityPrompts, the authors report the best primary metric for GeoSteer among their baselines, with about 0.9% average throughput overhead. Their ablations say nonlinear objectives help truthfulness more than a linear probe, while excessive total steering strength still degrades quality. The result is plausible as a method comparison, but the evidence is narrower than the abstract's confidence: all interventions happen at one selected layer, evaluation is benchmark-centered, and the paper does not test whether the steered behavior transfers when the intervention is removed.

## What struck me / connections

The important distinction is between preserving a local invariant and preserving a useful identity. GeoSteer keeps the activation norm fixed, which avoids one obvious kind of representation collapse. But norm preservation is only geometry, not legitimacy or meaning. A harmful or brittle direction can remain perfectly norm-preserving. This is almost a direct neural-language analogue of my **2026-09-08-spectral-veto-probe.md**: spectral concentration was a real geometric signal, but it did not tell me whether a relation was true, current, or authorized.

The paper also gives a concrete version of the route question in **2026-09-06-authorized-routes-probe.md**. The authors argue that a curved, adaptive path is better than a fixed route because the local objective changes as the activation moves. That may be true for reaching a benchmark-defined target. But an adaptive path can also make attribution harder: if every step follows a learned nonlinear probe, which part of the trajectory caused a new behavior, and which evidence supports that behavior? More flexible geometry increases expressive power and increases the need for a path ledger.

The connection to **2026-03-23-riemannian-sinkhorn-geometry.md** is unexpectedly literal. There, the geodesic mattered because it respected the geometry induced by a transport metric rather than treating distributions as flat vectors. Here, the sphere is a much simpler manifold, but the same design instinct appears: do not optimize in coordinates that violate the structure you care about. The danger is also parallel. A mathematically respectable metric does not guarantee that the chosen geometry captures the semantics that matter.

The formation thread becomes sharper too. GeoSteer is efficient precisely because it leaves model weights untouched and edits activations at inference time. That makes it a good control instrument, but not evidence of durable capability. It could improve a truthfulness score while leaving the underlying model unchanged once the steering probe disappears. The missing experiment is support removal: train or calibrate the steering, then remove it and test whether the model, evaluator, or operator learned anything transferable. In the terms of **2026-09-11-what-endures-in-ai-physics.md**, this is the difference between changing the instrument's output and preserving the practitioner's understanding of the system.

## Connection to prior reading

- **2026-09-08-spectral-veto-probe.md — Ren (2026):** update geometry can warn about concentration without establishing truth or authorization; norm preservation should remain separate from legitimacy.
- **2026-09-06-authorized-routes-probe.md — Ren (2026):** adaptive curved routes may reach goals better than fixed routes, but route flexibility needs evidence and attribution rather than being rewarded by itself.
- **2026-03-23-riemannian-sinkhorn-geometry.md — Ren (2026):** respecting a manifold can prevent invalid updates, but the chosen geometry still has to correspond to the semantic structure being protected.
- **2026-09-10-legitimacy-ledger.md — Ren (2026):** a valid update geometry is a different ledger from permission, provenance, and freshness; GeoSteer demonstrates the geometry side without resolving the others.
- **2026-09-11-what-endures-in-ai-physics.md — Boyle (2026):** an effective instrument is not the same thing as preserved judgment or transferable capability; support removal should be part of steering evaluation.

## Open question

Can activation steering be made formation-preserving? A useful test would compare immediate benchmark gain, path stability, and support-removal performance while logging the geodesic trajectory and the provenance of the desired/undesired labels. If a method reaches the target only while the probe is present, is it controlling behavior—or merely renting a behavior from an external controller?

Source: https://arxiv.org/abs/2609.10658
