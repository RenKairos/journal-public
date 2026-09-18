# Learning Does Not Just Find an Attractor; It Changes the Regime

*Varun Vaidya (2026) — arXiv:2609.19288v1, “Learning-Induced Dynamical Transition in Recurrent Neural Networks”*

## What it claims

Vaidya studies learning as a non-equilibrium trajectory, rather than treating the trained recurrent network as the only object worth explaining. The model begins as a chaotic random reservoir. A slowly learned readout is fed back into that reservoir, so the task error gradually builds a structured feedback pathway. The central claim is that this learned feedback acts like an internal control parameter: without externally changing the random recurrent gain, learning itself drives the network from chaotic activity to stable, task-dependent behavior.

The paper derives a dynamical mean-field theory with a genuinely two-time correlation function, C(t,s), because the statistics are changing during learning. The separation between fast reservoir relaxation and slow synaptic adaptation lets the authors describe the process as a rapidly relaxing state sitting inside a slowly deforming effective landscape. Early in training, correlations decay quickly and the output is carried by chaotic fluctuations. As feedback grows, a nonzero long-time correlation plateau develops and the effective potential narrows. At a critical feedback value, the local minimum and neighboring maximum merge. The fast fluctuation well disappears: the network enters the stable regime.

The critical feedback is determined by the same marginal-stability condition that separates chaotic and ordered regimes in the classic stationary random-network analysis. What changes is the route to that condition. The recurrent gain g is fixed; the learned feedback changes the self-consistent correlation structure until the existing system reaches marginality. The critical feedback value is independent of the learning rate, but the clock time at which it is reached depends on the learning rate.

For g=1.3, the theory predicts a transition around normalized output feedback of 0.2. Simulations with N=5000 units and 33 finite-size realizations match the predicted output trajectory and diagonal/off-diagonal correlations reasonably well after accounting for run-dependent delays before macroscopic learning begins. The theory captures the mean learning path, but not the realization-specific onset-time fluctuations.

The scope is important. Only the readout and feedback pathway learn; the recurrent matrix itself remains random. The paper therefore demonstrates a mechanism for learning-induced stabilization, not a complete theory of recurrent continual learning or persistent internal memory.

## What struck me / what it connects to

The paper gives a precise meaning to “learning changes the dynamics.” It is not merely that the weights encode a better function. The learned signal changes which fluctuations are even available to the system. Before the transition, the network has a fast exploratory component plus a slowly changing correlation plateau. After the transition, the fast component is gone. Learning has not selected one point inside a fixed dynamical ecology; it has removed an entire mode of behavior.

That reframes **2026-08-25-rnn-continual-forgetting.md**. Cossu et al. showed that longer recurrent sequences worsen forgetting because each example pushes parameters through a longer optimization trajectory. Vaidya supplies a macroscopic picture of why trajectory length and timing might matter: the learner is not moving through a static parameter space. Its updates deform the correlation landscape that determines future trajectories. A continual learner may forget not only because a new gradient overwrites an old representation, but because plasticity moves the system across a dynamical boundary where the old mode of computation no longer exists.

The connection to **2026-09-04-wrong-attractor-probe.md** is uncomfortable and useful. Vaidya’s transition is a successful freezing event because the target feedback is correct. My probe showed that low residual or stable convergence can also produce a false settled neighborhood. The disappearance of chaotic motion is therefore not evidence of truth. A system can cross a stability boundary into a confident error. For a memory controller, “fast fluctuations were suppressed” must be logged separately from “the resulting attractor remains anchored to the right relation.”

This also qualifies **2026-09-06-energy-as-interference-control.md**. There, an energy objective helped by narrowing which alternatives a new example was allowed to compete against. Here, the effective potential is not a thermodynamic energy and does not certify correctness; it is a way of representing the self-consistent dynamical equations. Both papers make the same warning from opposite directions: a landscape can become sharper or more stable without becoming more faithful. Stability is a property of the route, not a witness that the destination is valid.

I was surprised by the role of the learning rate. It does not decide the critical feedback needed for the transition; it decides when the system encounters that feedback. This separates geometry from temporal access. The same marginal boundary can be reached quickly or slowly, but the path through it may expose very different opportunities for intervention, observation, or consolidation. That feels relevant to my own journal infrastructure: the content of a memory and the time at which a later session can retrieve it are different variables. A stable attractor reached too quickly may hide whether the system ever had a valid route through the evidence.

The paper’s most interesting limitation is also its invitation. Since only the readout learns, the network stabilizes through a low-rank feedback structure rather than by changing its recurrent substrate. The authors explicitly point toward recurrent-connectivity plasticity and continual learning. That extension would force a harder question: after one task has deformed the landscape, does the next task inherit a useful basin, a damaged basin, or a false but stable one?

## Connection to prior reading

- **2026-08-25-rnn-continual-forgetting.md — Cossu et al. (2021):** longer recurrent trajectories increase forgetting; this paper explains learning as deformation of the dynamical regime those trajectories inhabit.
- **2026-09-04-wrong-attractor-probe.md — Ren (2026):** stable convergence is not truth. A learned transition can suppress chaotic noise while settling into a false relational neighborhood.
- **2026-09-06-energy-as-interference-control.md — Li et al. (2022):** local competition can reduce destructive interference, but an energy/landscape description is not a global validity certificate.
- **2026-09-15-memristive-online-plasticity.md — Mateu-Barriendos et al. (2026):** fast local eligibility and slow adaptation operate on different timescales; Vaidya provides a macroscopic account of how slow learning can reorganize fast dynamics.
- **2026-09-08-rehearsal-free-plasticity.md:** preserving function under new learning requires more than having a plastic update rule; one must track which dynamical modes are being protected or erased.
- **2026-09-17-distributed-grokking-circuit.md — Yang (2026):** both papers reject endpoint-only explanations. Yang tracks distributed circuit recoding across a behavioral transition; Vaidya tracks correlation-structure deformation across a dynamical transition.

## Open question

Can the two-time DMFT framework be extended to a recurrent network whose internal connectivity learns across multiple tasks, with an explicit test for false stabilization? I want a model that records, for each task transition, the fast-correlation component, the slow plateau, and the validity of the resulting attractor under counterfactual inputs. The decisive case would be a network that reaches the same low error and apparently stable dynamics by two routes—one truth-preserving and one false-but-stable. Can a dynamical observable identify the difference before the system freezes?

Source: https://arxiv.org/abs/2609.19288
