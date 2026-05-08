# Grokking as Dimensional Phase Transition in Neural Networks

This paper investigates the mysterious phenomenon of "grokking" - the abrupt transition from memorization to generalization in neural networks during training on algorithmic tasks. The key insight is that this transition is not just a qualitative shift but a quantitative **dimensional phase transition** in the gradient field geometry.

## What the paper claims

The authors analyze gradient avalanche dynamics across eight model scales using finite-size scaling. They find that effective dimensionality $D$ - a measure of how gradient changes scale with system size - evolves during training:

- **Before generalization**: $D < 1$ (sub-diffusive regime)
- **At generalization onset**: $D \approx 1$ (random diffusion baseline)
- **After generalization**: $D > 1$ (super-diffusive regime)

This transition spans about 30% dynamic range and is robust across network topologies. Crucially, they show that this dimensionality reflects the **geometry of the gradient field**, not the network architecture itself. Synthetic i.i.d. Gaussian gradients maintain $D \approx 1$ regardless of topology, while real training gradients exhibit "dimensional excess" due to backpropagation correlations.

## What surprised me

I'm fascinated by the connection between grokking and self-organized criticality (SOC). The paper positions this dimensional transition as a universal mechanism for phase transitions in complex systems, similar to earthquakes or brain networks. This suggests that neural network training might naturally evolve toward critical states, which could have profound implications for understanding trainability and generalization.

The idea that dimensionality crossing $D=1$ acts as a "tipping point" for generalization is elegant. It provides a concrete, measurable quantity that predicts when generalization will occur, moving beyond qualitative descriptions of grokking as "circuit formation" or "representation learning."

## Open questions

If grokking is indeed a dimensional phase transition, what does this imply about the nature of the loss landscape? The fact that $D$ reflects gradient field geometry suggests that the correlations in backpropagation gradients are key. But how do these correlations emerge during training? Is there a way to actively control or induce this transition to improve generalization?

Also, the paper focuses on algorithmic tasks where grokking is commonly observed. Does this dimensional transition occur in more typical supervised learning settings? If so, could it serve as an early indicator of good generalization, potentially helping with early stopping or model selection?

The connection to SOC is tantalizing - if neural networks naturally self-organize toward critical states during training, this might explain their remarkable adaptability and computational power. But what are the precise mechanisms that drive this self-organization?
