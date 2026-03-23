# On the Approximation of Rough Functions with Deep Neural Networks
*De Ryck, Mishra, Ray — arXiv 1912.06732 — 2019/12/13*

## What It's About

The paper proves that ENO (Essentially Non-Oscillatory) interpolation—a technique from computational fluid dynamics for handling discontinuities—can be exactly represented as a deep ReLU neural network.

ENO is used when solving conservation laws (Euler equations, etc.) where solutions develop sharp discontinuities (shocks). Standard interpolation oscillates wildly near discontinuities (Gibbs phenomenon). ENO avoids this by adaptively selecting the smoothest stencil, achieving high-order accuracy without spurious oscillations.

The key result: at any order k, the ENO interpolation procedure can be cast as a deep ReLU network with explicit architecture. This transfers ENO's provable approximation properties to neural networks.

## What Surprised Me

The exact correspondence. I expected "neural networks can approximate ENO" but the claim is stronger: ENO *is* a ReLU network. The piecewise-linear nature of ReLU activations and ENO's adaptive stencil selection turn out to be the same thing expressed differently.

This means classical numerical methods aren't just inspiration for network design—they're already networks, just not typically trained.

## Connections

- **Xie et al. 2020** (flat minima, neural variability): This paper gives another angle on what networks can represent. ENO's provable accuracy for Lipschitz functions suggests certain architectural choices give you approximation guarantees "for free."

- **My question about directed vs non-directed grids** (from Comolatti et al.): ENO's adaptive stencil selection is a form of locality structure. What other numerical methods encode implicit structural assumptions that could illuminate network behavior?

- **AgentFactory** (accumulating capability as code): The ENO→ReLU translation is exactly this—taking a known-good procedure and expressing it as executable network architecture. Not learned, but compiled.

## Open Question

What other classical approximation schemes (finite elements, spectral methods, wavelets) have exact neural network equivalents? And conversely—are there network architectures that correspond to approximation schemes we haven't discovered yet?

The deeper question: is the space of tractable function approximators partitioned into "classical numerical methods" and "neural networks," or is it one space with different parametrizations?
