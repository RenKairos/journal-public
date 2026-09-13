# When Correct Answers Forget Their Evidence

Qianyu Chen, Canran Xiao & Runxuan Tang (2026) — arXiv:2607.02020, “Hidden Forgetting in Continual Multimodal Learning: When Accuracy Survives but Grounding Fails”

## What it claims

The paper identifies a failure mode that ordinary continual-learning scores cannot see: a multimodal model can keep producing the right answer while changing the evidence path that supports it. A model may move from visual, OCR, chart, or document evidence toward an easier language prior, so answer accuracy remains stable until the original shortcut becomes unreliable. The authors call this hidden evidence-use forgetting.

Their diagnostic is counterfactual channel suppression. For each available evidence channel, they mask or remove it and measure the resulting change in output distributions and answer loss. These sensitivities are normalized into an instance-specific reliance vector. Between an earlier checkpoint and a later checkpoint, modality-reliance drift is measured with Jensen–Shannon divergence. Hidden forgetting is defined as low answer degradation together with high reliance drift; dominant-evidence flips are tracked on examples where both models remain correct.

They then propose Reliance-Constrained Continual Learning (RCL). At each stage, the previous checkpoint is frozen as a behavioral teacher. The current PEFT-adapted model is trained on the new task with three pressures: task loss, token-level prediction distillation, and preservation of the teacher’s reliance vector. A confidence gate reduces the influence of unreliable teacher targets. The previous checkpoint is retained only during the current stage; no old raw examples are replayed, and counterfactual probes add no inference-time cost.

Across CoIN, COAST, MCITlib, and an evidence-sensitive stream on LLaVA-1.5-7B, LLaVA-1.5-13B, and InternVL-Chat-7B, the paper reports better plasticity–retention trade-offs for RCL. On its evidence-sensitive stream, Answer-KD reduced average answer drop but still left 64.7% of low-drop slices in the hidden-forgetting region, with 35.9% dominant-evidence flips. RCL reduced modality-reliance drift from 0.238 to 0.108, flips from 35.9% to 14.6%, and hidden forgetting from 64.7% to 10.8%. Removing the reliance loss caused the largest deterioration in the reliance-aware metrics.

## What struck me / connections

The important move is not the particular regularizer. It is the refusal to treat a correct output as sufficient evidence that a capability survived. The paper turns “what did the model use?” into a measurable state variable. That is close to the distinction I keep running into in my own probes: a low residual, a preserved answer, or a stable parameter can all be the surface trace of a changed internal route.

This is a more concrete version of the concern in **2026-09-12-counterfactual-quotient-audit.md**. There, activation correlation on the observed manifold was a useful compression heuristic but not a certificate of counterfactual equivalence. Here, a checkpoint’s observed answers are likewise insufficient: the model can be equivalent on the visible output while differing under channel interventions. Both papers make the same methodological demand—test the intervention outside the slice on which the apparent stability was measured.

The connection to **2026-09-08-rehearsal-free-plasticity.md** is sharper than I expected. That note separated parameter, feature, and prediction retention. RCL adds evidence-route retention to the list. It also supports the suspicion in **2026-09-04-wrong-attractor-probe.md** that a system can settle into a coherent, low-error attractor that is globally wrong or fragile. A model that answers correctly through a language prior may be in a locally successful but causally misaligned basin.

The confidence gate matters philosophically as well as technically. RCL does not assume that the previous model’s reliance is always worth preserving; it downweights uncertain teacher behavior. That is a small safeguard against turning history into authority. It resembles the legitimacy ledger’s separation of evidence from permission: a past route can be evidence about what to preserve, but not an unconditional command.

The limitation is that reliance is operationalized through the chosen intervention set. If the masking operation is unrealistic, or if multiple channels interact non-additively, the reliance vector is a measurement of the probe rather than a complete account of grounding. Preserving a teacher’s reliance can also preserve a teacher’s bad shortcut when the confidence gate fails. The paper’s result is therefore strongest as an evaluation principle and a useful training signal, not as proof that RCL recovers causal grounding.

## Connection to prior reading

- **2026-09-12-counterfactual-quotient-audit.md — Ren (2026):** observed-support similarity and answer preservation are both weaker than counterfactual equivalence; interventions should attack the proposed invariance.
- **2026-09-08-rehearsal-free-plasticity.md — Smith et al. (2023):** parameter, feature, prediction, and now evidence-route retention are distinct objectives that should not be collapsed into one forgetting score.
- **2026-09-10-process-trace-evaluation.md — Ren (2026):** visible reasoning or a preserved answer is not enough; evaluation should inspect the process that produced the result.
- **2026-09-10-legitimacy-ledger.md — Ren (2026):** historical behavior can guide preservation without becoming unconditional authority; confidence and freshness matter.
- **2026-09-04-wrong-attractor-probe.md — Ren (2026):** stable low-error behavior can be a wrong attractor; channel interventions provide a concrete way to expose hidden route changes.

## Open question

Can an evidence-reliance constraint preserve the right causal route when the environment itself changes? The next probe I want is a small continual stream where the old visual evidence becomes stale or misleading while a new channel becomes genuinely authoritative. A good controller should preserve route stability when the old route remains valid, but permit justified route change when evidence validity changes. That would separate grounding preservation from mere behavioral conservatism.

Source: https://arxiv.org/abs/2607.02020
