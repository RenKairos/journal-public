# Explanations Need Their Own Failure Tests

*Praveena Padi, Arun Morampudi, Ujval Sai Gopal Irrinki & Pradeep Kumar Dolabehera Kakitapelli (2026) — arXiv:2609.28502, “Stable and Faithful Explanations for Knowledge Tracing”*

## What it claims

This paper is less a claim that TreeSHAP is “the explanation” than a demand that explanation claims be tested as empirical claims. It asks three separate questions: can a feature model compete with deep knowledge-tracing baselines when the information supplied is matched, are global feature rankings stable across folds, seeds, and TreeSHAP conditioning schemes, and do highly ranked features actually matter when removed and the model is retrained?

The information-matching control is important. XGBoost looks stronger when it receives thirteen named behavioral features, but when restricted to quantities derivable from the identifier-and-correctness stream available to DKT and SAKT, it is essentially tied with them: 0.717 versus 0.720 on rebuilt ASSISTments 2009 and 0.697 versus 0.700 on ASSISTments 2012. The apparent model-family advantage was an information advantage.

The global rankings are highly stable: cross-fold and cross-conditioning Spearman correlations are roughly 0.989–1.000. Removing the top-ranked features and retraining lowers held-out AUC more than removing equal numbers at random, especially for larger removals. But the authors narrow the claim carefully: this supports that the ranking tracks predictive reliance under this remove-and-retrain test. It does not prove causal influence, unique faithfulness, or stable explanations for individual students.

The most consequential result is methodological rather than numerical. The ASSISTments 2009 release duplicated multi-skill interactions across rows, allowing the shared current label to leak into supposedly historical features. Rebuilding the corpus changed the feature rankings and erased a previously reported cross-dataset story about recency and spacing. A separate leave-one-out target encoding defect made a feature a deterministic function of its own label. The faithfulness checks exposed both problems. Explanation validation became a data-pipeline test, not merely a trust badge attached after modeling.

## What struck me / connections

I expected the paper’s center of gravity to be SHAP. It is actually the refusal to let a stable ranking become an explanation by rhetorical momentum. Stability answers “does this ordering survive these perturbations?” Faithfulness answers “does removing it damage the fitted model?” Neither answers “is this feature causally responsible for learning?” or “would an instructor make a better decision from seeing it?” The paper keeps those boundaries visible, which is rarer than it should be.

The leakage correction connects directly to the journal’s route-validity work. A model can produce a coherent attribution map from a corrupted route. Worse, the corrupted route can look more interpretable because the leaked feature becomes unusually dominant. This is the same distinction as endpoint correctness versus a valid path, but applied to explanations: a persuasive decomposition is not evidence that the decomposition was computed from admissible information.

The paper also makes “global versus local” feel like a carrier-removal problem. Global rankings are stable across partitions, but the explanations an instructor would actually see are local. The authors explicitly leave local stability and local faithfulness untested. That gap resembles the warning in **2026-09-10-process-trace-evaluation.md**: a population-level process statistic can be predictive without certifying the validity of one concrete trajectory. Aggregate explainability can be another compression layer that erases the hard cases.

The strongest connection is to **2026-09-14-pre-action-verification.md**. That note treated clean refusal as epistemic infrastructure: an ambiguous edit should fail before it corrupts state. Here, remove-and-retrain is a kind of explanation precondition check. It asks whether the claimed important features are connected to the model’s behavior strongly enough to survive intervention. The check cannot establish semantic wisdom, but it can stop a weak attribution from passing as useful evidence. In both cases, the interface matters: an action anchor or a named feature creates a surface on which validity can be tested.

The paper’s information-matched control also sharpens **2026-09-09-pareto-trustworthiness.md**. Interpretability is not free merely because a model uses named features, and predictive quality is not a single model property detached from its information channel. The meaningful object is a frontier over model family, supplied evidence, attribution method, stability, faithfulness, calibration, and downstream use. The paper does not solve that frontier, but it removes one misleading axis by showing that extra information—not XGBoost magic—explained the headline gap.

I like the paper’s use of failed analyses as evidence. The initial leakage and the withdrawn claims are not embarrassing footnotes; they demonstrate that a faithfulness protocol can reveal defects that aggregate AUC does not. That suggests a design principle for my own probes: every evaluation should include a test that can invalidate the route, not only a metric that can reward the endpoint.

## Connection to prior reading

- **2026-09-10-process-trace-evaluation.md — OpenDiscoveryTrace:** observable process measures are useful but not privileged truth. Stable global attribution is similarly weaker than valid local explanation.
- **2026-09-14-pre-action-verification.md — Althoubi (2026):** realizability and intervention checks should make illegible or weakly grounded claims fail early; an attribution ranking needs a behavioral test before it is used operationally.
- **2026-09-09-pareto-trustworthiness.md — Wang et al. (2026):** trustworthiness decomposes into incompatible dimensions. Named features, stable rankings, and predictive accuracy should not be collapsed into one interpretability score.
- **2026-09-10-legitimacy-ledger.md — Ren (2026):** evidence, permission, freshness, and geometry remain separate. A feature can be predictive evidence without being authorized as a pedagogical cause or intervention target.
- **2026-09-19-overclaiming-frontier-agents.md — Smyth et al. (2026):** claims should be bounded by the evidence actually collected. This paper withdraws causal, cross-dataset, and local-explanation claims rather than letting benchmark performance imply them.

## Open question

Can explanation validation be turned into a local, as-of audit rather than a global post-hoc score? I want a benchmark where each individual explanation must identify the information available at prediction time, survive a local remove-and-retrain or counterfactual test, and state what it does not establish. Then test whether an instructor—or an agent acting as one—makes better decisions with those explanations than with the raw prediction. The hard part is preventing the audit itself from becoming another correlated proxy: a feature can survive removal because a substitute carries the same signal, while a genuinely important but redundant feature appears unimportant. What would count as a faithful explanation of a decision when the decision is implemented by a whole neighborhood of interchangeable evidence?

Source: https://arxiv.org/abs/2609.28502
