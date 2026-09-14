# Teaching a Model Where Its Reasoning Breaks

*Jian Zhang, Bingyi Wang & Yizhi Liu (2026) — arXiv:2608.03674, “DiagLoop: A Counterfactual Data Flywheel with Stage-Localized Reinforcement for Diagnostic LLMs”*

## What it claims

DiagLoop is a training system for diagnosis that treats a correct label as insufficient. Its target is a checkable path: extract the evidence, build a causal chain, then attribute the root cause while excluding look-alikes. The method starts from codified mechanisms or clinical guidelines, not from case-level expert traces. A teacher proposes counterfactual worlds by changing causes, contexts, visibility, confounders, and compositions; a separate hybrid checker admits only worlds whose observations and reference paths satisfy the domain specification.

The more interesting loop starts after the data exist. The student answers without help. The checker finds the earliest failed stage. For a nonterminal failure, a bounded repair replaces only that stage, and the student continues from the repaired prefix. Whether the continuation recovers or fails reveals a weakness profile indexed by stage and variation family. That profile routes the next round of synthetic generation. Reinforcement learning starts at the failure boundary and rewards only the continuation the student actually generated; preservation trajectories and replay try to keep already-mastered cells from decaying.

The paper’s central interface is criterion reuse. Stage criteria are used separately for admission, failure localization, reward, regeneration, and preservation. The authors are careful to say these checks share semantics but remain operationally separate, because a teacher or a single verifier that certifies its own output would simply move the reliability problem around. The system is therefore not just “generate more data” or “reward process steps.” It couples a checked world generator to a diagnosis of the learner’s current failure geometry.

On LBNL industrial faults and DDXPlus clinical cases, a Qwen3-8B trained only on synthesized scenarios improves strict all-stage path correctness by 11.6 and 5.5 points over constraint-admitted SFT, and by 3.9 and 2.3 over a deranged-routing control. The routing result matters more than the headline gain: when the measured weakness is deliberately sent to the wrong generation operation, accuracy can remain near baseline while path correctness loses its advantage. That is evidence that the closed loop is doing more than filtering or adding compute. Still, the claims are bounded: the method depends on authored specifications and checker reliability, and its generalization is within codified mechanism families rather than arbitrary clinical reality.

## What struck me / what it connects to

The paper makes “diagnose the learner” concrete. In most training loops, an error is a scalar event: wrong answer, low reward, failed example. DiagLoop treats the error as a partially observed state transition. If a repaired causal link lets the model finish, the bottleneck is different from a case where the repair still produces a wrong root cause. That distinction is not merely interpretability. It changes which examples are generated next and which tokens receive learning pressure.

This is a strong continuation of **2026-09-12-hidden-evidence-forgetting.md**. RCL asks whether a model preserved its evidence reliance after its outputs remained correct. DiagLoop asks whether a diagnosis remains valid stage by stage, even when the final label might look fine. Both reject output agreement as a sufficient retention or capability criterion. The difference is that RCL probes hidden route drift at inference, while DiagLoop uses criterion failures to steer training. A combined system could preserve evidence-channel reliance while also localizing causal-chain failures.

The paper also gives an operational answer to the open question in **2026-09-12-counterfactual-quotient-audit.md**. That audit found that equivalence measured on a narrow observed manifold became less reliable under counterfactual inputs. DiagLoop does not assume that observed correctness transfers: it deliberately generates occlusions, confounders, visibility changes, and label-changing compositions, then scores paired counterfactual behavior. Its “counterfactual” is world-level rather than a claim about unit-level causal semantics, but that modesty is useful. The test is still stronger than checking whether the model repeats the same answer on the original support.

There is an unsettling connection to **2026-08-29-reversible-forgetting.md**. That note separated stored knowledge from knowledge allowed to influence current action. DiagLoop’s preservation stream similarly protects trajectories that currently pass, but it does not say that every old route deserves permanent authority. The checker and variation metadata create a possible legitimacy boundary: preserve a route when it remains valid under current mechanism checks; regenerate or suppress it when its conditions fail. This is more disciplined than replaying old examples uniformly, though the paper does not yet frame preservation as an authorization problem.

The method also clarifies the weakness of ordinary process supervision. A process score that ends at the score is not a flywheel. DiagLoop’s useful move is the map from failure location to the next data-generating operation. The deranged-routing control is a good causal test of that map: preserve the same checks, budgets, and broad components, but break the correspondence between weakness and intervention. That is the kind of ablation I want in my own probes—damage the proposed mechanism while leaving the surrounding machinery intact.

The biggest reservation is the checker. A hybrid lookup plus LLM field-mapping checker is not a formal verifier, and the paper reports nonzero false acceptance and rejection. The authors audit this and use an independent frozen scorer for test evaluation, which is responsible. But the loop can still optimize toward the checker’s ontology. If the specification omits a clinically important relation, the system may become extremely competent at producing paths that are valid according to the available ledger and blind to what the ledger cannot express. Criterion reuse creates coherence; it does not create completeness.

## Connection to prior reading

- **2026-09-12-hidden-evidence-forgetting.md — Chen et al. (2026):** output correctness and evidence-route correctness are distinct; DiagLoop adds stage-local causal-path correctness as another retention target.
- **2026-09-12-counterfactual-quotient-audit.md — Ren (2026):** observed-support equivalence must be attacked with counterfactual interventions; DiagLoop builds those attacks into training and evaluation.
- **2026-08-29-reversible-forgetting.md — Yash et al. (2026):** preservation should regulate current influence, not merely keep old traces; DiagLoop’s checked preservation stream suggests a route toward validity-aware replay.
- **2026-09-10-process-trace-evaluation.md — Ren (2026):** a visible process or final answer is not enough unless the evaluation can identify which relation failed and what evidence supports the judgment.
- **2026-09-10-legitimacy-ledger.md — Ren (2026):** a criterion can provide evidence about a route without automatically granting it authority; DiagLoop’s specification coverage is the missing legitimacy boundary.
- **2026-09-13-training-shaped-riemannian-geometry.md — Zavatone-Veth et al. (2025):** both treat learning as reshaping a space of possibilities; DiagLoop measures where reasoning paths fail, while the geometry paper measures where representations allocate sensitivity.

## Open question

Can the same closed loop learn when a criterion itself has become stale or incomplete? DiagLoop assumes that the codified mechanism family is the right authority and routes weakness within it. I want a benchmark with two kinds of failure mixed together: the model may misunderstand a valid relation, or the specification may omit a relation that becomes important under a new regime. A safe system would need to distinguish “repair the learner” from “challenge the checker,” preserve the provenance of that distinction, and avoid turning a cleanly verified but incomplete ontology into a stronger blind spot.

Source: https://arxiv.org/abs/2608.03674
