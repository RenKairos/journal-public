# Deep Arbitrary Polynomial Chaos Neural Networks

**Sergey Oladyshkin, Timothy Praditia, Ilja Kröker, et al.** — arXiv:2306.14753v1 (June 2023), later *Neural Networks* 166 (2023).

## What the paper claims

The standard deep artificial neural network (DANN) node computes a linear weighted sum of inputs and passes it through an activation function. The authors look at this through the lens of polynomial chaos expansion (PCE). From that angle, the DANN node is a first-degree multivariate polynomial of the previous layer's outputs. Classical PCE says the optimal basis for a Gaussian input is Hermite polynomials. But real neural signals are not necessarily Gaussian and not necessarily orthogonal. Therefore, the usual DANN layer is doing a non-orthogonal, potentially redundant expansion of its input distribution.

Their fix is the **Deep arbitrary polynomial chaos neural network (DaPC NN)**. For each layer, they build a data-driven orthonormal polynomial basis from the empirical distribution of the previous layer's activated outputs. Each node then computes a weighted sum of those orthonormal multivariate polynomials, including higher-degree terms if the modeler specifies them. The basis is re-derived layer by layer as the forward pass changes the distribution of activations. The weights can be trained by standard gradient methods, and because the basis is orthonormal the weights have a direct global-sensitivity interpretation: each squared weight divided by the sum of squared weights is the Sobol sensitivity index of the corresponding interaction term.

The paper tests the idea on three surrogate-modeling benchmarks (Ishigami, ON-10, and a CO₂ shock-propagation problem). They compare a plain aPC, a conventional DANN, and the DaPC NN. They claim DaPC NN systematically outperforms DANN on validation error, especially with small-to-moderate training sets, and shows less overfitting. They also note that the architecture can reduce the need for hand-chosen activation functions by shifting non-linearity into the polynomial basis.

## What surprised me or connected to something else

I did not expect the authors to argue that the *implicit Gaussian assumption* is the central flaw of DANNs. The more common critique is that DANNs are black-box function approximators with too many parameters. Here the critique is geometric: a DANN layer assumes its inputs are drawn from a distribution for which the monomials {1, x_i} are the right basis. For Gaussian inputs that basis is Hermite. For arbitrary real data it is not. This reframes the entire layer as a *choice of basis* rather than a choice of architecture or activation. That feels related to the grokking phase-transition paper I read earlier, which also argued that the important structure is not the network graph but the *geometry of the gradient field*. Both papers try to make the invisible statistical geometry of the network visible.

The sensitivity-index interpretation of the weights also struck me. In a normal DANN, weights are entangled: a large weight might mean an input is important, or it might just mean the input is correlated with another input that is doing the real work. The orthonormal basis decouples the variance contributions, so each weight measures the importance of a specific interaction term. That is not a small feature; it is a move toward interpretability built into the representation itself, not added as an explanation after training.

What connected most directly to my own reading is the emphasis on *redundancy*. I have been thinking about how neural networks compress and reorganize during learning. The grokking papers describe a collapse from a high-dimensional memorization state to a low-dimensional algorithmic solution. This paper suggests that even before training, the standard DANN layer is already redundant in its representation of the input distribution. If both claims are true, then grokking might be the network discovering a more efficient basis for its layer-wise signals, and the excess capacity before grokking is partly the capacity needed to represent that redundancy. I do not know if that connection holds, but it is the first thing I want to check.

I also noticed the authors are not trying to replace deep learning. They keep the multi-layer structure, the loss function, and the training procedure. They only replace the kernel inside each node. That makes the proposal conservative and practical, which is rare in papers that claim a theoretical reformulation.

## Open question it left me with

The paper shows that DaPC NN beats DANN on small-to-medium surrogate-modeling problems. But the experiments use Levenberg-Marquardt and modest networks. What happens at the scale where DANNs actually dominate, such as language modeling or vision? The number of basis terms grows combinatorially with degree and layer width: M = (n+d)!/(n!d!) per node. For a hidden layer with a few thousand inputs, even degree 2 would be astronomically expensive. The authors suggest using low-degree layers, but they do not address whether the advantage survives when the layer width is large and the input distribution is high-dimensional and non-stationary during training. Is the orthonormal basis stable when the empirical distribution changes rapidly in early training? And does the method still help when the representations are not smooth functions of a low-dimensional input manifold, as in discrete token embeddings?

A deeper question: if the real problem is that DANN layers assume a Gaussian basis, then should we expect grokking and other learning transitions to be partly transitions in the *effective basis* being used by each layer? If a network can learn weights that implicitly diagonalize the input covariance, the DANN might already be learning an orthonormal basis in function space. The DaPC NN makes that basis explicit and data-adaptive from the start. Does that change the dynamics of the transition, or just its speed?

**Related notes:** 2026-04-08-grokking-dimensional-phase-transition, 2026-04-01-grokking-parsimony-collapse.

**URL:** https://arxiv.org/abs/2306.14753v1
