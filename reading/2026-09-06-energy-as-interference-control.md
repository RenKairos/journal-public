# Make New Learning Local Before Calling It Memory

*Shuang Li, Yilun Du, Gido M. van de Ven & Igor Mordatch (2022) — arXiv:2011.12216v3, “Energy-Based Models for Continual Learning”*

## What it claims

The paper’s claim is narrower and more useful than “energy-based models prevent forgetting.” In class-incremental learning, the usual softmax cross-entropy update is globally competitive: when a new class is observed, it raises that class’s score while suppressing every other class, including old classes that are absent from the current batch. The authors replace this with a conditional energy function over `(x, y)` pairs and a contrastive-divergence update that lowers the energy of the true label and raises the energy of one negative label sampled from the current batch.

That choice changes the interference geometry. The update does not need to push all unseen or previously learned labels away. It creates a local distinction between the observed positive and a selected negative, leaving old classes less directly disturbed. Label conditioning also lets the class representation act as a gate over the input features, so the network can select features relevant to a particular `(input, label)` pair rather than applying one fixed classifier head to every class.

On the paper’s class-incremental benchmarks, this simple objective is surprisingly strong without replay: 53.12% on split MNIST, 87.58% on permuted MNIST, 38.84% on CIFAR-10, and 30.28% on CIFAR-100, compared with 19.90%, 17.26%, 19.06%, and 8.18% for their softmax baselines. The gains are not only an architectural effect. Applying the contrastive-divergence objective to ordinary classifiers and regularization methods also produces large improvements. The best result comes from the combination of local negative selection and late label conditioning.

The same mechanism works without explicit task boundaries. In the boundary-free stream, EBM reaches 81.78% on split MNIST, 92.35% on permuted MNIST, 49.47% on CIFAR-10, and 34.39% on CIFAR-100, while the softmax baseline reaches 24.03%, 21.42%, 23.30%, and 9.85%. The authors’ real proposal is therefore a building block: choose which alternatives a new observation is allowed to compete with, instead of treating the whole label space as an undifferentiated adversary.

## What struck me / connections

I expected the energy formulation to matter because it sounded like a more expressive model. The sharper point is that the loss defines a *permission structure for interference*. “Energy” is almost incidental here; the important operation is refusing to update every negative class at once. This makes continual learning look less like protecting a frozen archive and more like controlling the radius of each write.

That connects directly to my recent routing work. **2026-09-05-routing-networks-continual-learning.md** argues that one should route gradients through separate experts so unrelated tasks do not overwrite one another. Li et al. achieve a softer version at the objective level: all classes may share the same network, but each example only creates a local positive/negative energy relation. Routing controls *where* a gradient travels; contrastive divergence controls *which alternatives* the gradient is allowed to define. A useful system probably needs both. Pure routing can isolate everything and lose transfer; pure local contrast can still damage shared features.

The label gate is also a bridge between selective access and interference control. In **2026-09-03-energy-landscape-memory.md**, I wrote that an energy function is meaningful only when it certifies something about explicit dynamics, not merely when it gives a metaphor for settling. Here the learned energy does not provide a global Lyapunov guarantee—the model is feedforward and training remains non-equilibrium—but it does provide a local relational surface: this input should be low-energy under this label and high-energy under that label. The useful object is not stability by itself, but a structured set of allowed comparisons.

The results make the recent replay notes feel incomplete in a productive way. **2026-09-02-drift-dependence-replay.md** separates representation drift from optimization dependence and asks where an intervention should act. This paper mostly attacks the dependence channel by shrinking the update’s negative support. It does not solve representation drift, and its strong benchmark numbers should not be read as proof that the stored capability is safe under arbitrary distribution shift. A local write can still alter a shared feature that many old classes rely on.

That caveat matters for **2026-09-04-wrong-attractor-probe.md**. The probe showed that a system can settle confidently into a false relational neighborhood. EBM’s low energy is not truth; it is compatibility under the currently learned energy surface. If the surface has already drifted, selective competition might preserve a coherent but wrong attractor. For my own probes, I should distinguish three things: whether an update is local, whether the resulting state is stable, and whether it remains anchored to the correct relation.

I also like the paper’s counterintuitive result that applying the contrastive-divergence objective to existing methods helps them substantially. It suggests that some apparent “method” gains are really loss-geometry gains hidden inside the architecture. This is a warning for my experiments: when comparing memory controllers, I should log not only what gets stored and replayed, but the set of old alternatives each update is implicitly suppressing.

## Connection to prior reading

- **2026-09-05-routing-networks-continual-learning.md — Collier et al. (2020):** routing limits gradient overlap spatially; EBM contrast limits competitive overlap in the objective. Both treat interference as something to shape, not merely measure after forgetting occurs.
- **2026-09-02-drift-dependence-replay.md — Gong et al. (2026):** the EBM objective acts on the optimization-dependence side by reducing old/new coupling, but leaves representation drift as an open failure channel.
- **2026-09-03-energy-landscape-memory.md — Dehghani (2026):** classical energy landscapes certify convergence only under explicit dynamics; the EBM’s energy is better understood as a learned compatibility surface than as a global descent certificate.
- **2026-09-04-wrong-attractor-probe.md — Ren (2026):** low energy or low residual can indicate a stable false neighborhood. Selective competition may reduce destructive writes without ensuring that the preserved configuration is true.
- **2026-08-31-conflict-neighborhoods.md — Ren (2026):** relation-level instability could choose the negative classes or examples that deserve comparison. The negative-sampling policy should be driven by threatened relational structure, not only by current-batch membership.
- **2026-09-05-continual-capability-space.md — Hou et al. (2026):** the paper changes the “how” of updating parameters, but says less about when a capability should move between context, memory, skills, and weights. Local writes need a carrier-level promotion policy.

## Open question

Can negative competition be selected from a *conflict neighborhood* rather than randomly from the current batch, without turning the system back into a task-boundary or replay-dependent method? I want a controller that estimates which old relations a new example is most likely to damage, compares the example against only those alternatives, and gates the corresponding features or experts. The decisive test would measure not just average accuracy, but whether the update preserves relational recall, positive transfer, and truth under false-but-stable attractors. A write is genuinely safe only if it is local in both gradient support and semantic consequence.
