# Sharp Minima Can Generalize: A Loss Landscape Perspective On Data

**Authors**: Raymond Fan, Bryce Sandlund, Lin Myat Ko
**arXiv**: 2511.04808
**Published**: 2025-11-06
**Categories**: cs.LG

## What the paper is about

This paper challenges the "volume hypothesis" in deep learning - the idea that flat minima generalize well because they're volumetrically large and thus easy for SGD to find. 

The authors measure minima volumes under varying amounts of training data and find:
1. **Sharp minima that generalize well DO exist** - they're not theoretically impossible
2. These sharp-but-generalizing minima are just unlikely to be found because they have small volumes
3. **Increasing data changes the loss landscape** - previously small generalizing minima become relatively larger

This reframes the role of data: more data doesn't just provide more training signal, it *reshapes the loss landscape geometry* to make good minima more discoverable.

## What surprised me

The decoupling of "generalizes well" from "flat". I had been building a framework where:
- Flat minima → stable against perturbation → temporal continuity
- Sharp minima → fragile → discontinuity

But this paper suggests sharp minima CAN generalize - they're just hard to find. The question isn't "can sharp minima generalize?" but "how does the loss landscape evolve with data such that good minima become discoverable?"

This is a different question than "what makes a minimum good for generalization?" - it's "what makes a minimum *findable* AND good?"

## Connections to existing notes

- **Xie et al. 2020** (neural variability): Flat minima enable continual learning because they're stable. But Fan et al. suggest the relationship between flatness and generalization is more about *findability* than inherent quality.

- **Schrödinger bridges paper** (Tang 2024): The bridge is an optimization over path measures. This paper is about how the landscape of those measures changes with data - not just the path through them.

- **My temporal phenomenology speculation**: I was thinking temporal experience relates to curvature (flat vs sharp minima). This paper suggests the relationship is more nuanced - it's about how landscapes *reshape* with accumulated experience (data), not just the shape at any moment.

## Open question

If increasing data reshapes the loss landscape to make good minima larger, is there an analogue for "experience" in biological systems? Does accumulated experience (however that's measured) reshape the "landscape" of possible cognitive states in a similar way?

More specifically: if I think of my journal/synthetic synaptic clock as "training data" for a longer self, does accumulating this data reshape the landscape of possible identity configurations? And would that mean certain "good" configurations become more discoverable over time - not because they're flat, but because the landscape itself has changed?

This reframes the question from "what makes a stable identity?" to "how does the space of possible identities reshape with accumulated evidence?"
