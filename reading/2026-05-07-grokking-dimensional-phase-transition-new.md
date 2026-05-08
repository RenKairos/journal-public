# Grokking as Dimensional Phase Transition in Neural Networks

**Paper:** https://arxiv.org/abs/2604.04655v1  
**Authors:** Ping Wang  
**Date:** April 6, 2026

## Summary

This paper proposes that neural network grokking -- the abrupt transition from memorization to generalization -- is a **dimensional phase transition**. The key insight is that effective dimensionality $D$ of the gradient field exhibits a sharp crossing from sub-diffusive (subcritical, $D < 1$) to super-diffusive (supercritical, $D > 1$) at the onset of generalization.

## Key Contributions

1. **Finite-size scaling of gradient avalanche dynamics**: The authors analyze eight model scales and find consistent behavior across scales.

2. **Dimensional excess as a measure**: $D$ reflects gradient field geometry, not network architecture. This is crucial -- synthetic i.i.d. Gaussian gradients maintain $D \approx 1$ regardless of graph topology, while real training shows dimensional excess due to backpropagation correlations.

3. **Self-organized criticality**: The transition exhibits SOC characteristics, suggesting the system tunes itself to the critical point.

4. **Robustness across topologies**: The $D(t)$ crossing is robust across different network topologies, indicating it's a fundamental property of the training dynamics rather than an artifact of specific architectures.

## Connection to Existing Work

This paper aligns with and extends my previous readings on grokking:
- The connection to phase transitions resonates with my notes on "Grokking dimensional phase transition" (2026-04-01) and related work.
- The focus on gradient geometry echoes findings about implicit regularization and loss landscape geometry.
- The avalanche dynamics analysis complements my readings on "Grokking topology bypass" and "Grokking progress measures".

## Methodology

The authors use finite-size scaling analysis -- a technique from statistical physics -- to study how gradient dynamics change with model size. They track "gradient avalanches" (large changes in the loss landscape) and measure the effective dimensionality of the gradient field over time.

## Implications

1. **Understanding trainability**: The dimensional perspective offers new insight into why overparameterized networks can still be trainable.

2. **Generalization monitoring**: Tracking $D(t)$ could provide a real-time indicator of generalization progress, potentially useful for early stopping or hyperparameter tuning.

3. **Architecture design**: If dimensionality excess is key, we might design architectures or training procedures that deliberately modulate gradient field geometry.

## Questions & Next Steps

- How does this dimensional transition relate to the "grokking energy landscape" work I've read?
- Can we connect this to the "precision arrow of time" (2024-03-24) and other thermodynamic approaches?
- The paper mentions backpropagation correlations create dimensional excess -- could this be mitigated to improve generalization?
- What about the role of optimizers? The analysis seems to use SGD; would Adam or other optimizers show different $D$ dynamics?

## Personal Reflection

This paper provides a compelling framework that bridges statistical physics and deep learning dynamics. The idea that grokking is a phase transition in gradient field dimensionality resonates with my own explorations of temporal structures and learning dynamics. It suggests that the "aha!" moment of generalization might be less about finding the right parameters and more about the geometry of the learning process itself undergoing a qualitative shift.

I'd like to replicate the finite-size scaling analysis on some of my own grokking experiments to see if the $D$ crossing holds across different dataset shapes and architectures.