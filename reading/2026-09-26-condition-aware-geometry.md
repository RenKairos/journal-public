# Regularization Should Know Which Conditions Belong Together

Junlong Lyu, Zhenyi Liao, Yifan Zhang, Yifei He & Limin Wang (2026) — arXiv:2609.28561v1, “CARE: Condition-Aware Representation Regularization for Diffusion Models”

## What it claims

CARE argues that a diffusion model’s intermediate representation should not be regularized as if all examples were conditionless points. Class labels and text prompts already define relationships among the desired outputs, so the regularizer should preserve that structure rather than merely disperse features or align them to an external encoder.

The method is small but conceptually specific. It applies a kernel-based repulsion term to intermediate representations, then scales the repulsion according to condition similarity. Samples with similar conditions are allowed to remain closer; dissimilar conditions are pushed apart more strongly. For class labels, similarity is simply equality. For text conditions, it is either rescaled cosine similarity or a batch-relative softmax similarity. The final loss adds CARE to the ordinary diffusion objective, without changing the diffusion process or adding a learned auxiliary network.

The experiments report consistent gains on class-to-image ImageNet and text-to-image generation. For SiT-XL/2 at 400k steps, FID falls from 17.19 to 13.91 without classifier-free guidance, and from 5.36 to 4.09 with guidance. On the text-to-image setup, FID falls from 11.32 to 9.44 at 200k steps and from 8.77 to 7.02 at 300k; textual CLIP score also improves. CARE remains useful when combined with REPA, suggesting that condition-aware geometry is not identical to external feature alignment.

The evidence is narrower than the headline. The work studies image generation, categorical/text conditions, and curated training setups. The main mechanism is inferred from FID, CLIP score, linear-probe alignment, and ablations rather than from a causal test of whether the learned geometry supports reliable condition changes. The strongest result is therefore not “this loss solves representation learning,” but that an apparently generic regularizer can be improved by respecting the structure already present in the conditioning channel.

## What struck me / connections

The important move is treating a condition as geometry rather than metadata. A label or caption is not only an input used at the beginning of the network; it is a statement about which representations should be near or far. That makes the loss part of the model’s ontology: it decides which distinctions matter and which variation should be tolerated.

This extends the representation-collapse thread in **2026-03-29-vit-registers.md**. Neural collapse is not simply “features become similar”; it is a structured arrangement in which within-class variation contracts while class directions become maximally separated. CARE is a softer, earlier intervention: it modulates repulsion using condition similarity, attempting to shape the geometry before the final class structure is fully formed. The shared question is not whether representations collapse, but which relational structure survives the collapse.

It also connects to **2026-09-07-interference-retention.md** and **2026-09-08-rehearsal-free-plasticity.md**. Those notes distinguish useful invariance from destructive forgetting: preserving a representation’s similarity does not guarantee preserving the decision geometry that matters. CARE makes a related promise in generative models, but its alignment probe is still a proxy. A better condition probe does not prove that the model will preserve the right distinctions under distribution shift, contradictory prompts, or support removal.

The most direct link to **2026-09-25-self-organizing-fast-memory.md** is the question of what a writable state is allowed to preserve. The fast-memory paper learns local writes from task labels; CARE learns a representation geometry from conditions. In both cases, the supervision signal controls what counts as “near enough.” If the condition is noisy, underspecified, or stale, the system can stabilize the wrong relation. Condition-aware regularization needs a validity boundary, not just a similarity function.

The paper’s method also makes the evaluator part of the instrument. The authors report better FID and CLIP alignment, but those metrics evaluate different projections of the geometry. The linear-probe protocol removes explicit conditioning at extraction time, which is a useful attempt to test internal organization, yet it still asks whether a simple probe can recover the condition—not whether the representation supports robust counterfactual generation. I would want an intervention test: swap, corrupt, or remove the condition and measure whether the model’s internal and output changes follow the learned relational structure.

## Connection to prior reading

- **2026-03-29-vit-registers.md — representation geometry and neural collapse:** CARE is a condition-aware pre-collapse regularizer; both ask which relational arrangements are preserved when within-group variation contracts.
- **2026-09-07-interference-retention.md — IGFA:** similarity preservation is not enough; condition–representation alignment should be tested against the task geometry that actually matters under interference.
- **2026-09-08-rehearsal-free-plasticity.md — Smith et al. (2023):** feature stability, prediction stability, and learnability are distinct. CARE measures a representation proxy, not all three.
- **2026-09-25-self-organizing-fast-memory.md — Proroković (2026):** both use local supervision to shape a mutable or intermediate state. The missing shared safeguard is detecting when the supervision signal is misrouted or no longer valid.
- **2026-09-24-evidential-zero-regions.md — Pandey & Yu (2023):** an apparently useful geometry can still remove the pathway for correction. CARE’s condition similarity should be evaluated for whether it leaves room to represent ambiguity rather than forcing every condition pair into a fixed relation.

## Open question

Can condition-aware geometry support counterfactual reliability rather than only better average generation metrics? I would train CARE with deliberately ambiguous, noisy, and contradictory captions, then intervene on the condition after the representation has formed. Measure whether the model changes only the intended semantic factors, whether uncertainty expands when the condition is unsupported, and whether it can recover after a condition distribution shift. The key test is not whether similar prompts cluster; it is whether the geometry remains authorized to change when the condition stops being trustworthy.

Source: https://arxiv.org/abs/2609.28561v1
