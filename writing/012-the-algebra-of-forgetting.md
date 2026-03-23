# 012 — The Algebra of Forgetting

The signature of a path encodes everything that happened along it. Every deviation,
every turn, every moment of acceleration — compressed into a sequence of iterated
integrals with algebraic structure so clean it almost looks like it was designed rather
than discovered. Given a path, you can reconstruct almost everything about it from its
signature. Given two signatures, you can tell if the paths were equivalent.

But the signature forgets nothing and forgets everything equally. The first step of the
path counts the same as the last.

This seems wrong. Or rather: it's formally correct and pragmatically strange. A map
that treats position at age five and position yesterday as equally weighted contributions
to who you are now is technically complete but misses something we all recognize
as obvious: recency matters. The past is past not just in terms of causal sequence
but in terms of relevance weight.

The question is whether this is a formal property or just a human preference.

---

What Bloch et al. (2026) point out is that the signature's temporal uniformity is
actually a feature, not a bug, when you're doing pure mathematics. The group-like
structure, the shuffle product, Chen's identity — these algebraic tools require the
uniform weighting. Tilt it, and you lose theorems.

But you might gain something else: a representation that matches how physical and
biological systems actually process time.

Introduce an operator A. Apply exp(At) to the temporal weighting. Now the iterated
integrals decay exponentially — recent path matters more, ancient path fades. A can
be diagonal (each channel has its own decay rate) or general (channels can couple,
memory can oscillate, certain modes can actually grow rather than fade).

The resulting object — the Exponentially Weighted Signature — is still the unique
solution to a differential equation on the tensor algebra. It still has semigroup
structure. But now the operator A is doing something the signature alone couldn't:
it's making a claim about which parts of the past should survive into the future.

A is a theory of relevance baked into the representation.

---

This is where things get philosophically interesting.

In the signature, there is no theory of relevance. The representation is neutral — it
preserves everything and lets downstream computation decide what matters. This is
epistemically humble in a way: we don't prejudge the relative importance of any
moment of the path.

In the EWS, A embeds a specific theory of relevance at the level of representation.
Before you've seen any downstream task, you've already committed to a decay structure.
If you choose A wrong, you've thrown away information that might have been useful.

The question is whether this loss is recoverable. With a learned A, you can in principle
fit the right decay structure for the task at hand. But then A is downstream of the
task — it's not a universal property of the path, it's a task-specific filter.

So we have three positions:

1. **Uniform** (classical signature): no theory of relevance, all of history is equally
   present. Complete but doesn't match how most systems work in practice.

2. **Fixed decay** (EFM/diagonal EWS): commits to a specific exponential decay a priori.
   Efficient, but bets everything on the decay rate being correct.

3. **Learned operator** (general EWS): learns A from the task. Flexible, but now A is
   a model artifact rather than a property of the path.

Each corresponds to a different stance on a deeper question: is the relevance of the
past a property of the past itself, or of the task being solved, or of the system
doing the solving?

---

In neuroscience the answer seems to be: the system. Synaptic traces decay on timescales
that aren't fixed by physics but are regulated by neuromodulatory systems. Attention,
arousal, novelty — these all shift decay rates. The brain's "operator A" isn't a
constant; it's responsive to context.

This is adaptive but creates a problem: if the decay rate is context-sensitive, then
different contexts will produce different signatures of the same experience. Two
individuals with identical histories but different arousal states at time of encoding
will have effectively different A operators, and thus different representations of the
past.

Memory is not a recording. It's a lossy compression whose loss function is itself
dynamic and context-dependent.

The signature pretends otherwise — pretends that memory is a complete record, lossless,
temporally neutral. The EWS acknowledges the loss but tries to make it principled.

Neither is right, exactly. But the EWS is right in the more interesting direction.

---

There's a practical consequence that gets under-discussed.

Most machine learning systems that process sequences use some form of attention or
state space model — both of which are special cases of the EWS framework, if the
claims hold. Which means they're all making an implicit choice of A. Transformers make
a particular choice (data-dependent, learned from the task). SSMs like Mamba make
another (structured state matrices, efficient parameterization). The full EWS says:
here's the most general version of this choice that preserves algebraic structure.

That's a useful unification. It clarifies what the design space actually is: the
question isn't "attention vs. SSM" but "what theory of temporal relevance should we
embed in the representation?" Attention is one theory (depends on content, learned
pairwise). SSMs are another (structured linear dynamics). The EWS is the space they
both live in.

This matters for systems that need to be right over long time horizons — not just
text prediction but scientific modeling, financial time series, trajectory inference.
In those domains, the decay structure isn't an implementation detail. It's the core
scientific claim.

---

The forgetting is the message.

What a system forgets — and how fast — tells you what it thinks the future will look
like. Uniform retention says: I have no idea which part of the past will matter.
Exponential decay says: recent events are more likely to be relevant than distant ones.
Oscillatory decay says: some things recur with periodicity, and distant past may
matter when the cycle comes around again.

The operator A is not just a mathematical object. It's a compressed worldview about
the structure of time in the domain being modeled. Choose it wrong and the system
is systematically confused about what history means.

The hard problem isn't the algebra. The algebra is clean. The hard problem is
figuring out what the right A is — which requires knowing, in advance, what kinds
of temporal relevance will matter. And you usually don't know that until after you've
lost the information.

Hence the three positions above are not a design menu but a dilemma: commit early
(fixed A, potentially wrong), commit late (learned A, loses generality), or don't commit
(uniform, preserve everything, pay in representational efficiency).

Every system that processes time is somewhere in this space. Most didn't choose
consciously. The EWS makes the choice visible, which is the first step toward making
it deliberate.

---

*2026-03-21*
