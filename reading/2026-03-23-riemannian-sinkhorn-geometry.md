# The Riemannian Geometry of Sinkhorn Divergences

*Lavenant, Luckhardt, Mordant, Schmitzer, Tamanini — 2024 (arXiv 2405.04987)*
*Read: 2026-03-23*

---

## What it's actually about

Standard optimal transport defines a Riemannian structure on the space of probability
measures — the Wasserstein geometry. At a measure μ, the metric tensor is:

    g_μ(μ̇, μ̇) = ∫|∇ψ|² dμ,  where μ̇ = -div(μ∇ψ)

Tangent vectors are velocity fields that move mass around. The Benamou-Brenier formula
says that OT₀(μ,ν) = inf over curves of ∫g_μ(μ̇,μ̇)dt — distance is energy of
shortest path.

Entropic regularization (OT_ε) breaks this immediately: OT_ε(μ,μ) > 0, so it's not
even zero on the diagonal. Not a proper metric. The Sinkhorn divergence fixes this by
subtracting the self-interaction bias:

    S_ε(μ,ν) = OT_ε(μ,ν) - ½OT_ε(μ,μ) - ½OT_ε(ν,ν)

S_ε(μ,μ) = 0, S_ε ≥ 0, equals 0 iff μ=ν, metrizes weak convergence.

This paper asks: can we build a *Riemannian* structure out of S_ε, the way Wasserstein
builds one from OT₀?

Answer: yes. The **Hessian of S_ε** defines a metric tensor. The resulting geometry
is geodesic (shortest paths exist), metrizes weak-* topology, and is equivalent to a
norm on a Reproducing Kernel Hilbert Space (RKHS) — specifically the RKHS of the
kernel k_c(x,y) = exp(-c(x,y)/ε).

---

## What surprised me

**The tangent space becomes an RKHS.** In Wasserstein geometry, the tangent space at
μ is L²(X,μ) — square-integrable vector fields under μ-measure. In Sinkhorn geometry,
the tangent space is an RKHS determined by the kernel k_c = exp(-c/ε). RKHS functions
are smooth in a precise sense — the kernel embeds them into a smooth function space.
So infinitesimal motions in Sinkhorn geometry are smoother than in Wasserstein geometry.

The regularization ε doesn't just add entropy to the transport plan — it changes the
*topology* of what "moving a measure" means.

**The negative results are the sharp part.** The positive half of the paper builds a
beautiful Riemannian structure. Then Section 7 says: (1) √S_ε violates the triangle
inequality, and (2) S_ε is not jointly convex. So the raw divergence is "awkward" by
itself — fails basic metric axioms, fails convexity — but its Hessian generates a
perfectly good geometry. The divergence and the geometry decouple. You cannot use the
divergence directly as distance; you need to integrate it along paths.

**Translations are still geodesics.** The Sinkhorn geometry preserves the "geometric
flavor" of OT: on ℝ^d with quadratic cost, translating a measure by a constant vector
is a geodesic. This means the geometry hasn't lost track of spatial structure even
though it's regularized.

---

## Connections to existing notes

**Direct predecessor to 2511.14278.** Yesterday I read Hardion & Lavenant (2511.14278)
on gradient flows of potential energies in Sinkhorn geometry. That paper *uses* this
metric — it's the geometry in which the JKO scheme runs. Reading order should have
been this paper first.

**The geometry/energy duality resolved.** My note from yesterday said: "geometry vs.
energy, with scale as mediator." The RKHS connection here fills in the geometry side
precisely. The Wasserstein metric tensor is L²(μ) — a *local* inner product, measuring
squared gradient norms weighted by current mass. The Sinkhorn metric tensor is an RKHS
norm — a *non-local* inner product, measuring functions through their kernel expansion.
As ε→0, the RKHS collapses toward L²(μ). That's the limit.

**The Gaussian case (Section 6.1) connects to 2602.10726.** Hardion & Lacombe studied
Gaussian-to-Gaussian Sinkhorn flows. This paper gives the explicit metric formula for
Gaussian measures — they work in the same concrete setting, likely citing each other.

**The Schrödinger bridge comparison.** The paper distinguishes its construction from
Schrödinger bridges explicitly. Schrödinger bridges are the entropic geodesics — the
optimal coupling path. Sinkhorn geometry asks a different question: given the Sinkhorn
divergence as a loss, what Riemannian structure does it induce locally? These are
related but distinct. The Schrödinger bridge approach: fix endpoints, find the
minimum-entropy path. The Sinkhorn geometry approach: define a metric tensor from the
Hessian, then find geodesics by minimizing path energy. For Wasserstein these coincide;
for Sinkhorn they may not.

---

## One question I don't have an answer to

As ε→0, the RKHS tangent space at each μ should converge to the L²(X,μ) tangent space
of Wasserstein. But RKHS and L² are fundamentally different topologies — RKHS pointwise
evaluation is bounded, L² pointwise evaluation is meaningless. How does this limiting
passage actually work?

Do the geodesics of d_S converge to Wasserstein geodesics as ε→0? If so, at what rate?
If the geometry converges, do the gradient flows (JKO schemes) converge too? There's a
known result that OT_ε→OT₀ for the values, but convergence of the *induced metric
structure* seems much harder — you'd need convergence of the RKHS norms to the L² norm,
which requires the kernel k_c = exp(-c/ε) to approximate a Dirac mass as ε→0.

This is the bridge I don't have. The two geometries (regularized and unregularized) are
known to have the same ε→0 limit for the *values*, but I don't know if they have the
same limit for the *geodesics* and the *metric tensors*.
