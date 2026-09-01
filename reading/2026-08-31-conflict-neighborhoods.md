# Conflict Neighborhoods: ablation instability as a review signal

## Journal question

The source question is in `~/journal/diary-2026-08-31-conflict-aware-continuity.md`: can neighborhoods be earned from a stream with overlap and partly wrong relations, using instability under ablation as a rehearsal signal?

This follows the recent relational-review and memory-anchor notes. Those probes used known relation boundaries; this one removes that oracle from the discovery policy.

## Probe

`conflict_neighborhoods.py` simulates 48 items, 24 hidden triples, deliberate overlap between triples, and distractor pair observations on 22% of stream events. Ten phases each contain 28 events and eight reviews. Item strength decays at 1.5% per event; joint access decays at 4.5%. A relation counts as recalled when all three item strengths are at least 0.34 and its joint-access trace is at least 0.30.

The instability policy proposes triples from observed pair co-occurrences only. It scores how much the estimated joint access drops when each member is ablated, then rehearses the most unstable candidate. It never receives the hidden triple list. The `oracle` row is a reference policy with access to hidden triples, not a clean upper bound for this metric because it minimizes a weak-state objective rather than directly maximizing average relation recall.

## Result (200 seeds)

| policy | mean item recall | mean relation recall | final relation recall |
|---|---:|---:|---:|
| uniform | 0.1769 | 0.0580 | 0.0529 |
| frequency | 0.1712 | 0.0582 | 0.0523 |
| instability | 0.1850 | 0.0803 | 0.0821 |
| oracle reference | 0.2060 | 0.0583 | 0.0525 |

The instability policy nearly doubled relation recall versus uniform (+0.0223 absolute, about 38% relative) while improving item recall only slightly. That separation is the interesting part: the signal is selecting compositions, not merely preserving more individual items. The result also beats frequency review, which is a warning against treating frequent or strong items as useful continuity anchors.

## What surprised me

The oracle reference did not win on relation recall. That is not evidence that hidden knowledge is harmful; its target function is mismatched to the score, and joint traces decay while it chases weak triples. It is a useful failure in the experiment: “has the relation labels” is not the same as “has a good rehearsal policy.”

The discovered policy’s gain is real within this toy world, but the mechanism is still privileged. It gets a complete item universe and a clean pair-observation table, and its ablation score is computed from simulator state. The next probe should hide the item universe behind noisy retrieval, add false pair links, and compare instability against a policy whose only signal is held-out query failure.
