---
title: "Tight round complexity for Theorem 4.5"
date: 2026-06-26
slug: theorem-4-5-tight-round-complexity
tags: [diffusion language models, parallel sampling, circuit complexity]
summary: "A tight lower and upper bound for the number of monotone DLM rounds needed to sample exactly from the even-parity distribution."
---

# Tight round complexity for Theorem 4.5

Theorem 4.5 of Jiang, Haghtalab, and Chen [1] rules out $O(1)$ rounds. Here we
prove the tight bound.

## Problem setup

Let

$$
D_n^\oplus
$$

be the uniform distribution over all even-parity strings:

$$
D_n^\oplus = \mathrm{Unif}\{x \in \{0,1\}^n : x_1 \oplus x_2 \oplus \cdots
\oplus x_n = 0\}.
$$

We consider a DLM with sequence length $L = n$. The model starts from the
fully masked state

$$
(*, *, \ldots, *).
$$

In each round, the unmasking rule $F$ chooses some masked positions, and the
predictor $p(\cdot | x)$ gives an independent distribution for each chosen
position. Those positions are then unmasked independently according to these
distributions. There is no remasking and no revision, so once a position is
unmasked, its value cannot be changed.

Call such a model a monotone DLM. We assume that every circuit used by $F$ and
$p$ has constant depth and polynomial size. In other words, each single DLM
round is an $AC^0$ computation.

Let $T(n)$ be the minimum number of rounds needed by such a DLM to sample
exactly from $D_n^\oplus$. The question is:

> How many rounds are needed to sample exactly from $D_n^\oplus$?

## Main claim

We prove the following tight bound:

$$
T(n) = \Theta\left(\frac{\log n}{\log \log n}\right).
$$

The lower bound comes from the fact that the last unmasked position must satisfy
a parity constraint. The upper bound is constructive: first we build a chain,
and then we speed it up by extending the same idea to a
$\Theta(\log n)$-ary tree.

## Lower bound

The lower bound follows from a simple verifier for parity. Suppose a monotone
DLM samples $D_n^\oplus$ in $T$ rounds. In any valid sample path, all positions
except the last one can be viewed as free random bits. When only one masked
position remains, say position $u$, the predictor has no freedom left: to make
the total parity even, it must output

$$
x'_u = \bigoplus_{i \ne u} x_i .
$$

Now take an arbitrary Boolean string $x$ as input. Unroll the $T$ DLM rounds as
a Boolean circuit. The unrolled circuit uses $F$ to identify the last position
$u$, and uses $p$ to compute the value $x'_u$ that the sampler would put there.
Then it verifies whether this predicted value equals the actual input bit:

$$
x'_u = x_u .
$$

This equality is exactly the even-parity test, because

$$
x'_u = x_u
\quad \Longleftrightarrow \quad
x_u = \bigoplus_{i \ne u} x_i
\quad \Longleftrightarrow \quad
\bigoplus_{i=1}^n x_i = 0 .
$$

Since $F$ and $p$ are polynomial-size $AC^0$ circuits, unrolling $T$ rounds gives
a polynomial-size Boolean circuit of depth $O(T)$ for parity. By Hastad's
switching lemma [2], parity cannot be computed by polynomial-size circuits of
depth $o(\log n / \log \log n)$. Therefore

$$
T(n) = \Omega\left(\frac{\log n}{\log \log n}\right).
$$

## Matching upper bound

We now give the construction. The lower bound says that we need at least
$\Omega(\log n / \log \log n)$ rounds. The construction below shows that this is
also enough.

### Chain construction

First consider the slower chain version. This is the cleanest way to see what
state the DLM is carrying.

Assume for simplicity that $n$ is even and that positions are indexed from
$0$. Let

$$
C_i = \{2i, 2i+1\}
$$

be the $i$-th pair. Pair $C_i$ stores the parity before its direct child pair
$C_{i-1}$:

$$
S_i = \bigoplus_{u < 2i-2} x_u .
$$

The construction uses the mask status of $C_i$ as a one-hot marker for the
label $S_i$. The invariant is

$$
x_{2i} \text{ is unmasked and } x_{2i+1} \text{ is masked}
\quad \Longleftrightarrow \quad S_i = 0,
$$

and

$$
x_{2i} \text{ is masked and } x_{2i+1} \text{ is unmasked}
\quad \Longleftrightarrow \quad S_i = 1.
$$

Equivalently, the location of the unique unmasked position in $C_i$ stores the
label:

$$
x_{2i} \text{ unmasked} \Rightarrow
\bigoplus_{u < 2i-2} x_u = 0,
\qquad
x_{2i+1} \text{ unmasked} \Rightarrow
\bigoplus_{u < 2i-2} x_u = 1.
$$

The initialization matches the draft. In the first round, sample

$$
x_0,x_1,x_2 \sim \mathrm{Bernoulli}(1/2)
$$

independently and leave $x_3$ masked. Since

$$
S_1=\bigoplus_{u<0}x_u=0,
$$

the mask status of $C_1=\{2,3\}$ is correct: $x_2$ is unmasked and $x_3$ is
masked.

Now suppose the invariant holds at pair $C_i$, and suppose the direct child
pair $C_{i-1}$ is already fully unmasked. In the next round, the DLM can compute

$$
S_{i+1}
  = \bigoplus_{u < 2i} x_u
  = S_i \oplus x_{2i-2} \oplus x_{2i-1}.
$$

Then $F$ unmasks the other position in $C_i$, and opens one position in the
next pair $C_{i+1}=\{2i+2,2i+3\}$ according to $S_{i+1}$:

$$
x_{2i+2+S_{i+1}} \text{ is unmasked}, \qquad
x_{2i+3-S_{i+1}} \text{ stays masked}.
$$

The final round has one extra term. Let

$$
m = \frac{n}{2}-1,
$$

so the last pair is $C_m=\{n-2,n-1\}$. If only $x_{\mathrm{last}}$ remains
masked in $C_m$, first compute the label before this pair,

$$
S_{\mathrm{before}}
  = S_m \oplus x_{n-4} \oplus x_{n-3},
$$

and then also include the already unmasked value in the last pair:

$$
S_{\mathrm{final}}
  =
  S_{\mathrm{before}}
  \oplus
  \bigoplus_{\substack{u\in C_m\\ u\ne \mathrm{last}}} x_u .
$$

Finally set

$$
x_{\mathrm{last}} = S_{\mathrm{final}}.
$$

All other free positions are sampled uniformly, so the output is uniform over
$D_n^\oplus$. Both circuits are clearly in $AC^0$: they only sample independent
fair bits, read a constant-size mask pattern, and compute a constant-size xor.

This chain construction takes $O(n)$ local moves. Its purpose is to show the
state representation: each pair stores a parity label through the mask status
of its two positions.

### Extending the chain to a log n-ary tree

The chain is too slow because it passes the xor state through one pair at a
time. To get the tight upper bound, replace the chain by a
$B$-ary tree with

$$
B=\Theta(\log n).
$$

Each internal node still uses a pair of positions as a one-hot marker, just as
in the chain. The marker stores a $0/1$ xor label for the subtree below that
node, but the label does not include the direct child pairs. Those direct child
pairs are completed first; their token values are added in the next update and
are reflected in the mask status of the grandparent.

At one tree level, all nodes update in parallel. A node's mask status gives its
delayed label. Combining this label with the already fixed token values in its
direct child pairs gives the contribution passed upward. This is just a local
xor over $B=\Theta(\log n)$ inputs. Such a parity computation has size
$2^B=\mathrm{poly}(n)$, so it can be implemented in $AC^0$.

Each round moves the labels up by one tree level. The tree height is

$$
\log_B n
  = \Theta\left(\frac{\log n}{\log \log n}\right).
$$

Thus the construction samples exactly from $D_n^\oplus$ in

$$
O\left(\frac{\log n}{\log \log n}\right)
$$

rounds. Together with the lower bound, this proves

$$
T(n) = \Theta\left(\frac{\log n}{\log \log n}\right).
$$

## References

[1] Haozhe Jiang, Nika Haghtalab, and Lijie Chen. *Diffusion Language Models are
Provably Optimal Parallel Samplers*. ICLR 2026. https://openreview.net/forum?id=5bkAbueJwM

[2] Johan Hastad. *Almost Optimal Lower Bounds for Small Depth Circuits*. STOC
1986.
