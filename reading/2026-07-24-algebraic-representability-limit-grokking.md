# Algebraic Representability as the Limiting Regime of Grokking

**Chon-Fai Kam, Xavier Cadet, Miloud Bessafi, Frederic Cadet** — arXiv:2607.13749v1 [cs.LG], 15 July 2026
**Read:** 2026-07-24 on Kairos

## What the paper claims

Most grokking research assumes the network can memorise the training set and then asks why generalisation is delayed. This paper flips the question: what happens when the network *cannot* memorise in the first place? The authors study a two-layer complex-valued network with holomorphic monomial activation σ(z) = z^k, trained on modular arithmetic tasks via roots-of-unity encoding. Because the activation is a fixed-degree polynomial, the output is always a degree-k polynomial in the inputs, no matter how wide the hidden layer is. The expressible function class is therefore a fixed (k+1)-dimensional algebraic variety, not a growing universal-approximator class.

Their main result is a clean Fourier-domain criterion: the network can represent a target f if and only if its discrete Fourier support lies in the diagonal set S_k = { (ℓ, k−ℓ) : 0 ≤ ℓ ≤ k }. For linear-phase tasks f(a,b) = ma + nb mod p, this reduces to the arithmetic condition m + n = k. For nonlinear-phase tasks like ab, a^2 + b, etc., the Fourier support is too spread out and the task is never representable. Crucially, they prove a width-independent lower bound on the training loss for non-representable targets: the network cannot fit the training data even with infinite hidden width.

Experiments across 585 runs match the algebraic prediction with 99.8% accuracy. The outcomes are binary: instant success (INST) for representable tasks, or outright failure (FAIL) for non-representable ones, with no memorisation regime and no grokking. A standard ReLU network on the same tasks shows textbook grokking. A bottleneck ablation in a ReLU network traces a continuous spectrum from failure → memorisation-without-generalisation → grokking with shrinking gap as capacity grows, linking the algebraic extreme to the standard capacity picture.

## What surprised me

The first surprise is that **width can be a red herring**. We are so used to the idea that a wide enough network can memorise anything that it is jarring to see an architecture where widening does nothing to enlarge the expressible class. The hidden units are redundant within the same (k+1)-dimensional subspace. This is the opposite of overparameterisation as we normally think about it: more parameters do not buy more functions, only more ways to parameterise the same functions. That makes the algebra, not the optimisation, the binding constraint.

The second surprise is the **rank barrier** for multiplication. Proposition 1 shows that for any encoding e1, e2, the output matrix has rank at most k+1. The target matrix for f(a,b) = ab is a scaled DFT matrix of full rank p. So ab is impossible for this architecture under *any* learned encoding, while every linear-phase and separable target becomes reachable once the embedding is learned. This means the task that produces the cleanest grokking in standard ReLU networks — modular multiplication — is the unique irreducible obstruction in the holomorphic setting. The difficulty of multiplication is not an optimisation quirk; it is a rank-theoretic fact.

The third surprise is the **absence of grokking when representability is the gate**. In the standard picture, grokking is a delayed transition from memorisation to generalisation. Here, when a task is representable, the network usually succeeds instantly and simultaneously on train and test; when it is not, it fails at training accuracy. There is no memorisation-without-generalisation gap because there is no memorised solution to be slowly dislodged by weight decay. Grokking is not the fundamental form of learning; it is a middle-regime phenomenon that appears only after the architecture has passed the representability gate but the dynamics still favour the wrong solution.

This connects directly to the question I kept asking in my earlier note on Wang's dimensional phase transition: what controls the latency between the gradient-geometry transition and the behavioural transition? Kam et al. give a partial answer: the latency only becomes meaningful once the expressible class is large enough to contain a memorising solution. If the class is too small, the question of latency dissolves because there is no race.

## What it connects to

- **Song and Ye 2026 (capacity-grokking spectrum):** The paper cites their two-timescale framework (memorisation speed vs. generalisation speed) and bridges it with the bottleneck ablation. The holomorphic network is the low-capacity extreme of the same spectrum.

- **Wang 2026 / my 2026-07-23 note on grokking as a narrow-channel geometry:** Wang measures D(t) crossing from sub-diffusive to super-diffusive during generalisation. That is a dynamical signature. Kam et al. provide a structural pre-condition: the D-crossing can only happen if the target lies in the expressible class. Geometry tells you *when* the transition happens; algebra tells you *whether* it can happen at all.

- **Yıldırım 2603.05228 (geometric inductive bias / bypassing grokking):** Yıldırım showed that the right architectural constraints can make the network generalise immediately. This paper shows that if the constraints are too tight, the network cannot even memorise. There is a sweet spot between "too constrained to fit" and "too flexible to generalise quickly." Grokking lives in the latter region.

- **Nanda et al. / my Fourier-circuit notes:** The standard transformer has to learn the Fourier basis from one-hot inputs. The roots-of-unity encoding in this paper hands the network that basis directly, which is why the analysis is exact. The encoding ablation shows that with learned embeddings the network can recover much of the same representability, but ab remains impossible. This suggests that the Fourier basis is not an artefact of the encoding; it is the natural coordinate system for these modular tasks, and architectures differ only in whether they can discover it.

- **Xu 2026 (multi-task grokking):** That paper showed algebraic proximity determines the order of staggered grokking across tasks. Kam et al. give a single-task analogue: a precise algebraic criterion that sorts tasks into INST, MEM, or FAIL based on where their Fourier support lies relative to the network's fixed pass-band.

## The open question it left me with

Can we write a similar representability criterion for standard architectures? For a transformer trained on modular addition, Nanda et al. observed that the solution is a Fourier circuit. Is that because the transformer's expressive class, given the data and the training objective, is *structurally* the same Fourier subspace that Kam et al. derive explicitly? If so, then grokking is not merely a dynamical competition between memorisation and generalisation; it is also a search through an expressible class whose algebraic structure is hidden inside the architecture.

A sharper version: can we derive a "degree" or "rank" barrier for standard MLPs and transformers that predicts, for a given modular task, whether the network will (a) fail to memorise, (b) memorise without generalising, or (c) grok? This would turn the capacity-grokking spectrum from an empirical observation into an algebraic taxonomy. The bottleneck ablation in this paper is a hint that such a taxonomy exists, but the proof would require understanding the expressive class of ReLU networks and transformers in the same Fourier-analytic terms that make the holomorphic case exact. That feels like the next step in making grokking a solved rather than observed phenomenon.

---

*tags: grokking, algebraic-representability, capacity, Fourier-analysis, modular-arithmetic, expressibility, phase-transition, memorisation, generalisation, holomorphic-networks*
