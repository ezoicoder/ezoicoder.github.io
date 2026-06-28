---
title: "Exact sampling round complexity for diffusion language models"
date: 2026-06-26
slug: exact-sampling-round-complexity-dlms
tags: [diffusion language models, parallel sampling, circuit complexity]
summary: "Notes on exact sampling round complexity for one-hot and even-parity distributions under monotone, revision, and AC0 DLM models."
---

# Exact sampling round complexity for diffusion language models

This note records a few exact-sampling examples for diffusion language models
and tracks how the required number of rounds changes when revision is allowed.
Here, remasking is included as a form of revision, since we view updates such as
$0\to M$ as revisions. I first define the two update models, and then separate
the computational regimes used in the examples.

Throughout the note, a **round** means one parallel DLM update. The predictor is
denoted by $p(\cdot \mid x)$. Target distributions are denoted by
$\mathcal{T}$.

## Model conventions

We use the binary vocabulary

$$
V=\{0,1\},
$$

together with a mask symbol $M$. The state space is $(V\cup\{M\})^L$. In this
note we consider unconditional generation, so the initial state is

$$
x^{(0)}=M^L.
$$

The standard, no-revision DLM follows the usual masked-decoding rule from
Jiang, Haghtalab, and Chen \[1\]: an unmasking policy $F$ first chooses which
currently masked positions to decode, and only those positions are sampled.
Once a position is unmasked, it cannot change.

```text
No-revision DLM
Input: length L, rounds D, predictor p, unmasking policy F
Initialize x <- M^L
for t = 1,...,D:
    S <- F(x)                         // S must be a subset of {i : x_i = M}
    for each i in S independently:
        x_i ~ p_i(. | x) over {0,1}
    all positions outside S stay unchanged
Output x
```

With revision, I use the simpler abstraction that there is no separate
unmasking policy. Every position is updated in every round, and each coordinate
may freely take values in $\{0,1,M\}$. This includes remasking, since a
transition such as $0\to M$ is allowed.

```text
DLM with revision
Input: length L, rounds D, predictor p
Initialize x <- M^L
for t = 1,...,D:
    for each i in [L] independently:
        x_i ~ p_i(. | x) over {0,1,M}
Output x                              // for exact sampling over {0,1}^L, x has no M
```

For a target distribution over $\{0,1\}^L$, a valid exact sampler must output a
fully unmasked string with probability $1$.

The update model is independent of the computational regime. In the general
regime, the update rules may use arbitrary computation and arbitrary real
probabilities. In the $AC^0$ regime, the relevant predictors and, for the
no-revision model, the unmasking policy $F$, are implemented by polynomial-size
constant-depth circuits.

## General predictors

In this section, the predictor has unrestricted computational power. The point
is only to understand the information flow caused by masking, unmasking, and
revision.

### The one-hot distribution without revision

Let

$$
U_n = \mathrm{Unif}\{e_0,e_1,\ldots,e_{n-1}\},
$$

where $e_i \in \{0,1\}^n$ is the string with a single $1$ at position $i$ and
$0$ everywhere else. Without revision, exact sampling from $U_n$
needs $n$ rounds in the worst case.

The obstruction is independence inside one DLM round. Suppose that, at some
history, two still-masked positions both have positive conditional probability
of eventually being the unique $1$. If the DLM writes both positions in the
same round, then the two written values are sampled independently. Therefore
there is positive probability that both positions become $1$, which is outside
the support of $U_n$.

Thus a monotone sampler can resolve at most one remaining candidate for the
unique $1$ in each round. Starting from $n$ possible locations, exact sampling
from $U_n$ therefore needs $n$ rounds.

### Arbitrary target distributions with revision

With revision, the situation changes completely. In the unrestricted-predictor
regime, any target distribution over $\{0,1\}^n$ can be sampled in at most three
rounds.

The key is the classical alias-method view of discrete sampling \[3\]. For any
distribution $\alpha=(\alpha_0,\ldots,\alpha_{L-1})$ over
$[L]=\{0,1,\ldots,L-1\}$, there is an alias table with keep probabilities
$\tau_0,\ldots,\tau_{L-1}\in[0,1]$ and aliases
$q_0,\ldots,q_{L-1}\in[L]$ such that the following experiment outputs
$Y\sim\alpha$:

1. sample $X\sim \mathrm{Unif}([L])$;
2. conditioned on $X=i$, sample

$$
\Pr[Y=y\mid X=i]
  =
  \tau_i \mathbf{1}[y=i]
  +
  (1-\tau_i)\mathbf{1}[y=q_i].
$$

Equivalently, one first chooses a uniform bucket and then uses one biased coin
to decide whether to keep the bucket index or jump to its alias.

Now let $\mathcal{T}$ be an arbitrary target distribution over $\{0,1\}^n$.
For a prefix $a\in\{0,1\}^{n-1}$, define its target marginal

$$
\mu(a)=\sum_{z\in\{0,1\}}\mathcal{T}(a,z).
$$

Apply the alias method to $\mu$, with $L=2^{n-1}$. This gives a keep probability
$\tau_a$ and an alias prefix $q_a$ for every prefix $a$.

The three-round sampler is:

**Round 1.** Sample the first $n-1$ positions uniformly and independently. Call
the resulting prefix $A$. Leave the last position masked.

**Round 2.** Use the last position as a temporary marker. Conditioned on the
current prefix $A=a$, set this marker to $0$ with probability $\tau_a$ and to
$1$ with probability $1-\tau_a$.

**Round 3.** If the marker is $0$, keep the prefix $B=A$. If the marker is $1$,
revise the prefix to $B=q_A$. Then revise the last position from a marker into
the real final token by sampling

$$
Z \sim \mathcal{T}(x_{n-1}=\cdot \mid x_{<n-1}=B).
$$

By the alias table, the prefix $B$ has marginal distribution $\mu$. The final
token $Z$ is then sampled from the correct conditional distribution under
$\mathcal{T}$. Therefore the final output $(B,Z)$ is exactly distributed as
$\mathcal{T}$.

### Some distributions need three rounds

The three-round upper bound is tight in the general regime, at least for
sufficiently large $n$. We prove this by a dimension argument.

For each distribution $\mu$ over the state index set
$\mathcal{Y}=\{0,1\}^{n-1}$, define a distribution $\mathcal{P}_\mu$ over
$\{0,1\}^n$ by

$$
\mathcal{P}_\mu(x)
  =
  \mu(x_{<n-1})
  \mathbf{1}\left[
    x_{n-1}
    =
    \bigoplus_{i<n-1} x_i
  \right].
$$

Thus $\mathcal{P}_\mu$ is supported on the graph of the parity function, and
the free parameter is the distribution $\mu$ over the $2^{n-1}$ graph states.

Now consider any two-round sampler with revision. To make the lower bound only
stronger, allow the first round to sample each position independently from
$\{0,1,M\}$. Hence the first-round state $S$ lies in $\{0,1,M\}^n$, and its
product distribution is described by $3n$ probability parameters, with one
normalization constraint per position.

Conditioned on a first-round state $S=s$, the second round again samples the
final positions independently. If the output distribution is exactly
$\mathcal{P}_\mu$, then every such conditional product distribution must be
supported on the parity graph. But a product distribution supported on a parity
graph is a point mass: if any coordinate has both values with positive
probability, flipping that coordinate leaves the parity graph. Therefore the
second round is deterministic on every first-round state with positive
probability.

So a two-round sampler induces a deterministic map

$$
g:\{0,1,M\}^n \to \{0,1\}^{n-1},
$$

where $g(s)$ is the state index $y\in\mathcal{Y}$ of the final parity-graph
output. There are at most

$$
\left(2^{n-1}\right)^{3^n}
$$

possible maps $g$.

Fix such a map $g$. Let $\theta_i=(\theta_{i,0},\theta_{i,1},\theta_{i,M})$ be
the first-round distribution at position $i$, and let
$\theta=(\theta_i)_{i=0}^{n-1}$. This gives a product distribution over
$S\in\{0,1,M\}^n$:

$$
\Pr_\theta[S=s]
  =
  \prod_{i=0}^{n-1}\theta_{i,s_i}.
$$

To view the output distribution as a point in Euclidean space, choose one
reference state $y_\star\in\mathcal{Y}$ and keep only the other
$2^{n-1}-1$ state coordinates:

$$
A=\mathcal{Y}\setminus\{y_\star\}.
$$

These coordinates give the coordinate image of the simplex of all distributions
over $\mathcal{Y}$:

$$
\Delta_A \cong \Delta_{2^{n-1}-1}
  \subset \mathbb{R}^{2^{n-1}-1}.
$$

The set $\Delta_A$ has dimension $2^{n-1}-1$ and therefore has a natural
Lebesgue volume, denoted by $\operatorname{Vol}$.

Define

$$
\Phi_g(\theta)
  =
  \left(
    \Pr_\theta[g(S)=y]
  \right)_{y\in A}
  \in \mathbb{R}^{2^{n-1}-1}.
$$

The omitted coordinate at $y_\star$ is determined by normalization. The map
$\Phi_g$ is polynomial in these $3n$ probability parameters, equivalently in a
parameter space with at most $2n$ degrees of freedom.

For $n\ge 6$, even the conservative bound $3n < 2^{n-1}-1$ holds. Hence

$$
\operatorname{Vol}\left(\Phi_g(\Theta)\right)=0
$$

inside $\Delta_A$, where $\Theta$ is the first-round parameter space.
Taking the finite union over all possible maps $g$ still gives

$$
\operatorname{Vol}\left(
  \bigcup_g \Phi_g(\Theta)
\right)
=0.
$$

Therefore, for almost every coordinate vector $(\mu(y))_{y\in A}\in\Delta_A$,
the corresponding full distribution $\mu$ over $\mathcal{Y}$ gives a
distribution $\mathcal{P}_\mu$ that cannot be sampled exactly in two rounds. The
alias-method construction above \[3\] samples every $\mathcal{P}_\mu$ in three
rounds, so some distributions have exact round complexity equal to $3$ in this
general unrestricted-predictor regime.

## $AC^0$ examples for the one-hot distribution

Now consider the one-hot distribution $U_n$ in a circuit-restricted setting.
Assume $n=2^t$.

Without revision, the same monotone argument still gives the $n$-round
obstruction. There is also a separate exact-representation issue: the natural
one-position-at-a-time sampler would need transition probabilities such as

$$
\frac{1}{n-1}.
$$

If the $AC^0$ implementation is restricted to a finite number of fair random
bits, then every exactly representable probability is dyadic, i.e., it has a
finite binary expansion. But $1/(n-1)$ is not dyadic for $n=2^t$. Under this
implementation model, the monotone sequential construction cannot be realized
exactly. This is a probability-representation obstruction, separate from the
round-complexity obstruction.

With revision, however, $U_n$ has a very short exact sampler.
Use the first $t$ positions as temporary workspace. In the first round, sample a
uniform index

$$
I\in\{0,1\}^t.
$$

In the second round, revise the whole sequence into the one-hot string

$$
x_j = \mathbf{1}[j=I],
\qquad j\in\{0,1,\ldots,n-1\}.
$$

The comparison $j=I$ is an AND of $t=\log n$ literals for each fixed $j$, so all
$n$ comparisons are computable by polynomial-size constant-depth circuits. Thus
with workspace-style revision, exact sampling from $U_n$ takes two rounds in
this $AC^0$ setting.

## $AC^0$ round complexity for the parity distribution

With revision, the parity distribution is easy in the $AC^0$ regime. Jiang,
Haghtalab, and Chen \[1, Theorem 4.1\] show that a DLM with revision and length
$n$ can sample $D_n^\oplus$ in two rounds.

Without revision, Theorem 4.5 of Jiang, Haghtalab, and Chen \[1\] shows that
exact sampling requires superconstant, i.e., $\omega(1)$, rounds. Here we prove
the tight bound.

### Problem setup

Let

$$
D_n^\oplus
$$

be the uniform distribution over all even-parity strings:

$$
D_n^\oplus = \mathrm{Unif}\{x \in \{0,1\}^n : x_0 \oplus x_1 \oplus \cdots
\oplus x_{n-1} = 0\}.
$$

We consider a DLM with sequence length $n$. The model starts from the
fully masked state

$$
(*, *, \ldots, *).
$$

In each round, the unmasking rule $F$ chooses some masked positions, and the
predictor $p(\cdot \mid x)$ gives an independent distribution for each chosen
position. Those positions are then unmasked independently according to these
distributions. There is no revision, so once a position is
unmasked, its value cannot be changed.

Call such a model a monotone DLM. We assume that every circuit used by $F$ and
$p$ has constant depth and polynomial size. In other words, each single DLM
round is an $AC^0$ computation.

Let $R_\oplus(n)$ be the minimum number of rounds needed by such a DLM to sample
exactly from $D_n^\oplus$. The question is:

> How many rounds are needed to sample exactly from $D_n^\oplus$?

### Main claim

We prove the following tight bound:

$$
R_\oplus(n) = \Theta\left(\frac{\log n}{\log \log n}\right).
$$

The lower bound comes from the fact that the last unmasked position must satisfy
a parity constraint. The upper bound is constructive: first we build a chain,
and then we speed it up by extending the same idea to a
$\Theta(\log n)$-ary tree.

### Lower bound

The lower bound follows from a simple verifier for parity. Suppose a monotone
DLM samples $D_n^\oplus$ in $T$ rounds.

First note that the final nonempty decoding round must have exactly one masked
position left. Suppose instead that, just before the final round, there are
$r>1$ masked positions. Conditioned on the current partial sequence, the DLM
samples these $r$ positions independently, so the completion distribution is a
product distribution. Exact sampling from $D_n^\oplus$ would require this
product distribution to be uniform over the $2^{r-1}$ completions with the
correct parity and to put zero mass on the other parity class. But a product
distribution supported on a single parity class is a point mass: if any
coordinate has both values with positive probability, flipping that coordinate
creates positive mass on the wrong parity. This contradicts uniformity over
$2^{r-1}$ valid completions. Hence $r=1$.

Therefore, in any valid sample path, all positions except the last one can be
viewed as free random bits. When only one masked position remains, say position
$u$, the predictor has no freedom left: to make the total parity even, it must
output

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
\bigoplus_{i=0}^{n-1} x_i = 0 .
$$

Since $F$ and $p$ are polynomial-size $AC^0$ circuits, unrolling $T$ rounds gives
a polynomial-size Boolean circuit of depth $O(T)$ for parity. By Hastad's
switching lemma [2], parity cannot be computed by polynomial-size circuits of
depth $o(\log n / \log \log n)$. Therefore

$$
R_\oplus(n) = \Omega\left(\frac{\log n}{\log \log n}\right).
$$

### Matching upper bound

We now give the construction. The lower bound says that we need at least
$\Omega(\log n / \log \log n)$ rounds. The construction below shows that this is
also enough.

#### Chain construction

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

The initialization is simple. In the first round, sample

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

#### Extending the chain to a log n-ary tree

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
R_\oplus(n) = \Theta\left(\frac{\log n}{\log \log n}\right).
$$

## Outlook

The constructions above keep the sequence length fixed and do not add extra
CoT-style scratch positions. Understanding how additional intermediate states
affect the right round-complexity model is a separate question.

## References

[1] Haozhe Jiang, Nika Haghtalab, and Lijie Chen. *Diffusion Language Models are
Provably Optimal Parallel Samplers*. ICLR 2026. https://openreview.net/forum?id=5bkAbueJwM

[2] Johan Hastad. *Almost Optimal Lower Bounds for Small Depth Circuits*. STOC
1986.

[3] Alastair J. Walker. *An Efficient Method for Generating Discrete Random
Variables with General Distributions*. ACM Transactions on Mathematical
Software, 1977.
