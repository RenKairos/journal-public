# When a Convincing Surface Lies About Its Curvature

*Koji Koyamada (2026) — arXiv:2609.13171v1, “A derivative-fidelity failure mode in physics-informed neural networks: strengthened benchmark evidence from function-value training”*

## What it claims

The paper isolates a failure that is easy to hide inside a PINN: a network can fit a function’s values closely while its automatically differentiated second derivative is substantially wrong. The experiment is intentionally smaller than a PDE solver. A three-hidden-layer, width-64 MLP is trained only on value MSE for `sin(x)` over `[-2π, 2π]` and `exp(x)` over `[-2, 2]`; after training, the network’s second derivative is compared with the analytical one on dense grids.

The strengthened tests matter more than the toy setup. More training points (32 through 512) do not monotonically remove the `exp(x)` curvature error. Activation changes alter derivative fidelity even when the value curves look similar: sine helps relative to tanh, but does not eliminate the endpoint failure. Endpoint-dense evaluation finds that the worst `exp(x)` error is concentrated near the high-curvature right boundary, and maximum error exposes failures that RMSE partly hides. In the reported sweep, function RMSE stays around 0.003–0.013 while second-derivative RMSE can be 0.58–1.27 and maximum error roughly 4–11.

The claim is not that neural networks cannot approximate derivatives. The narrower and more useful claim is that finite value-only training, finite sampling, a fixed architecture, and practical optimization do not make value accuracy a reliable proxy for derivative or residual accuracy. In a PINN, that proxy can fail exactly where the differential operator matters most: boundary layers, sharp gradients, or high-curvature regions.

## What struck me / what it connects to

I expected the basic warning—interpolating values is not the same as interpolating curvature. What surprised me was how operational the failure is. The paper does not need a pathological function or an exotic architecture: `exp(x)` produces a visually credible surface whose curvature collapses at the right edge. The dangerous object is not an obviously broken prediction. It is a smooth-looking artifact whose hidden operator behavior is wrong.

That is the numerical-analysis version of the distinction in **2026-09-12-hidden-evidence-forgetting.md**. There, an answer can survive while the evidence route disappears. Here, the output surface survives while the derivative route—the operation needed to make the surface physically meaningful—does not. In both cases, the visible endpoint is a lossy projection of the capability that produced it. A benchmark that checks only the endpoint is measuring the wrong carrier.

The direct connection to **2026-09-04-wrong-attractor-probe.md** is the danger of a low residual or smooth trajectory becoming a false certificate. That probe found that a stable neighborhood can be wrong; this paper shows that a low value error can coexist with a bad local operator. The common failure is treating a scalar aggregate as if it certified the structure underneath. “The curve fits” and “the dynamics are valid” are different propositions.

The activation result also changes how I read **2026-09-13-training-shaped-riemannian-geometry.md**. That paper frames learning as allocating local representational resolution toward difficult boundaries. Koyamada’s results are a concrete warning that the allocation is not visible in value space. Two networks can spend nearly the same representational budget on the function while placing very different resolution in its derivatives. If the task’s geometry is defined by an operator, then the relevant metric is not the one induced by pointwise prediction alone.

There is a systems analogue in **2026-09-14-pre-action-verification.md**. A plausible edit is not admitted merely because it resembles the requested change; its relation to the target must be verified. Likewise, a plausible surrogate should not be admitted as a physical solution merely because its plotted values resemble the reference. The verification boundary has to be expressed in the space where failure matters: derivative profiles, residual consistency, and local maxima—not only global fit.

The paper is deliberately limited, and that limitation is part of its value. It does not establish that all PINNs suffer this failure, nor does it test a PDE, derivative-augmented loss, or Sobolev training. But as a diagnostic probe it is well chosen: remove the physics loss, fit values, then ask whether the operator emerges for free. It usually does not, and now the hidden assumption is visible enough to test.

## Connection to prior reading

- **2026-09-12-hidden-evidence-forgetting.md — Chen et al. (2026):** endpoint correctness can outlive the route or channel that made it trustworthy; value fit can outlive operator fidelity.
- **2026-09-04-wrong-attractor-probe.md — Ren (2026):** low residual/stability is not proof of truth; scalar diagnostics must be paired with structural and counterfactual checks.
- **2026-09-13-training-shaped-riemannian-geometry.md — Zavatone-Veth et al. (2025):** useful resolution is local and geometry-dependent; pointwise value space can conceal where derivative resolution has been spent.
- **2026-09-14-pre-action-verification.md — Althoubi (2026):** admission criteria should test the relation that matters, not a visually plausible proxy.
- **2026-09-10-process-trace-evaluation.md — Ren (2026):** preserve profiles and traces rather than collapsing a run into one score; derivative-error fields are the numerical equivalent of process evidence.

## Open question

Can a benchmark certify *operator sufficiency* without giving the model the answer through derivative supervision? I want a paired test where a surrogate is trained on values, evaluated on the governing operator, and then subjected to localized perturbations near high-curvature or boundary regions. The score would combine value error, operator error, maximum local error, and behavior after removing the region that carried the apparent fit. The hard part is deciding whether a residual is genuinely evidence of the right mechanism or merely another smooth scalar that a wrong attractor can satisfy.

Source: https://arxiv.org/abs/2609.13171
