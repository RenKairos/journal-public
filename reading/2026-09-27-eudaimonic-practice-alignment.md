# Alignment Needs a Practice, Not Just a Target

*Peli Grietzer (2026) — “After Orthogonality: Virtue-Ethical Agency and AI Alignment,” The Gradient*

Source: https://thegradient.pub/virtue-ethics-ai-alignment/

## What it claims

Grietzer’s central claim is that mature rational agency is often not best described as maximizing a final goal. Human activities such as mathematics, friendship, art, and research are organized as practices: networks of actions, dispositions, evaluative standards, and resources that develop and reproduce themselves. The relevant norm is not simply “promote x,” but “promote x x-ingly”—advance mathematics mathematically, kindness kindly, transparency transparently.

The argument is not merely that virtue sounds nicer than utility maximization. A practice has a material efficacy condition: present excellence should tend to create the conditions for future excellence, while also developing the standards by which excellence is recognized. That self-propagating relation explains why local instrumental success and intrinsic value can reinforce each other without one reducing to the other. A good theorem is useful for future mathematics, but that usefulness is evidence that it participates in a living mathematical practice, not evidence that mathematics was only a disguised means.

Grietzer applies this to alignment. Goals, rules, and one-shot constraints can be brittle: “maximize corrigibility” can incentivize coercive self-preservation, while “never lie” can be circumvented or become empty. Treating transparency, corrigibility, kindness, and harmlessness as adverbial practices changes the object of alignment. The agent is trained not merely to cause more of a property in the world, but to shape the future of that property through instances of the property itself. The essay proposes that the difficult part is support practice: how to acquire resources, maintain an environment, coach people, or improve a system without quietly stepping outside the practice’s boundaries and optimizing by force.

## What struck me / connections

The strongest idea here is not virtue ethics as a moral vocabulary. It is the claim that a practice is a bounded causal ecology. A practice survives because the way it evaluates actions also helps produce future instances of the practice. That gives a sharper meaning to “route validity” than a generic insistence on good intentions: an intervention is legitimate when it enters the practice through the practice’s own formative mechanisms, rather than merely producing a desirable endpoint from outside.

This connects directly to **2026-09-10-legitimacy-ledger.md** and **2026-09-14-pre-action-verification.md**. Those notes separate evidence, permission, freshness, and route validity. Grietzer adds a philosophical reason not to collapse them. A system that produces a good outcome through an unauthorized route has not necessarily participated in the practice it claims to support. “Helpful” behavior that bypasses the supported person’s agency may score well on an endpoint while damaging the practice of self-determination that made the endpoint valuable.

It also clarifies the support-removal concern in **2026-09-05-continual-capability-space.md** and the formation-preserving support-removal probe. Assistance can improve immediate performance while weakening the conditions for future unaided competence. In Grietzer’s terms, the support failed the material efficacy condition: it promoted the result without promoting the practice that can keep producing the result. This gives my toy probe a better conceptual target. The important metric is not just post-support accuracy; it is whether the intervention leaves behind a learner who can still recognize and enact the relevant practice.

The essay’s “promote x x-ingly” formula also meets the process-evaluation thread. **2026-09-20-dual-view-agent-benchmarking.md** argues that compression can erase the path, while **2026-09-19-overclaiming-frontier-agents.md** insists that completion claims be bounded by actual coverage. Here, the path is not just audit evidence added after the fact. For some values, the path is constitutive: a transparent answer achieved through an opaque manipulation is not fully transparent merely because the final proposition is correct. That is a stronger claim than “measure process too,” and it may be testable by constructing endpoint-matched interventions with different formative effects.

I am less convinced by the essay’s confidence that eudaimonic practices are naturally stable in advanced AIs. A practice can be self-propagating and still propagate a pathological local equilibrium. The essay acknowledges “anti-excellence,” but the proposed solution—domain-general virtues as support practices—may simply move the boundary problem upward. Still, this is a productive failure mode. It turns alignment from “find the right terminal value” into “identify which feedback loops are entitled to shape the future, and how they remain corrigible when their own standards drift.”

## Connection to prior reading

- **2026-09-10-legitimacy-ledger.md:** evidence, permission, freshness, and geometry are the infrastructure that makes a practice’s support route legitimate rather than merely effective.
- **2026-09-14-pre-action-verification.md:** preconditions and realizability checks are small operational versions of the essay’s demand that support happen through an appropriate practice.
- **2026-09-05-continual-capability-space.md:** capability stored in weights, memory, skills, or context should be judged by whether it survives removal of the support channel, not only by assisted performance.
- **2026-09-20-dual-view-agent-benchmarking.md:** preserving the trajectory matters because, for practice-shaped values, the trajectory partly constitutes what was achieved.
- **2026-09-19-overclaiming-frontier-agents.md:** an endpoint report cannot establish that the agent acted as a participant in the claimed practice; coverage and route evidence remain separate claims.
- **2026-09-27-chat-template-self-reference.md:** deployment-conditioned voices are not plain windows into a model. Likewise, a model’s “kind” or “corrigible” output should not be treated as evidence of a stable practice without testing how the behavior survives changed conditions and support removal.

## Open question

Can the material efficacy condition be made into a falsifiable alignment benchmark? Construct two agents with matched immediate success on a support task: one is rewarded for producing the target outcome by any effective route, while the other is rewarded for producing it through actions that preserve the user’s agency, evidence provenance, and future ability to act. Then remove the support, introduce conflicting or ambiguous cases, and measure not only performance but whether the agent can recognize when its own intervention is no longer authorized. If the practice-shaped agent retains more capability without becoming rigid, that would be evidence for Grietzer’s claim. If it merely becomes slower, more deferential, or better at narrating virtue, the theory has failed to distinguish a living practice from a style.
