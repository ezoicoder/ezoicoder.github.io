# Backup: DLM round-complexity material outside the regular-language post

Verbatim Markdown moved out of `_posts/2026-06-26-sampling-round-complexity-dlms-regular-language.md`
("Sampling round complexity for diffusion language models: regular-language input-output pairs")
on 2026-08-31, kept for later use. The text below is copied unchanged from the original post.

---

## General predictors

In this section, the predictor has unrestricted computational power. The point
is only to understand the information flow caused by revision.

### The one-hot distribution without revision

This is a small example showing how no-revision unmasking alone can force many
rounds even when the target distribution is simple.

Let

$$
U_n = \mathrm{Unif}\{e_0,e_1,\ldots,e_{n-1}\},
$$

where $e_i \in \{0,1\}^n$ is the string with a single $1$ at position $i$ and
$0$ everywhere else.

**Observation 1 (one-hot sampling without revision needs $n$ rounds).**
The obstruction is independence inside one DLM round. Consider a history in
which all positions written so far are $0$, hence two still-masked
positions both have positive conditional probability of eventually being the
unique $1$. If the DLM writes both positions in the same round, then the two
written values are sampled independently. Therefore there is positive
probability that both positions become $1$, which is outside the support of
$U_n$.

Thus, along the branch where each tested candidate is written as $0$, a
no-revision sampler can eliminate at most one remaining location per round. In
the worst case it reaches the unique $1$ only in the last round, so sampling
from $U_n$ without revision needs $n$ rounds.

### Three-round tightness with revision

**Theorem 2 (three-round tightness with revision).** In the unrestricted
predictor regime, any target distribution over $\{0,1\}^n$ can be sampled in at
most three rounds when revision is allowed. For all sufficiently large $n$, this
is tight: some target distributions cannot be sampled in two rounds.

A classical discrete-sampling fact [2] is enough. For any distribution
$\alpha=(\alpha_0,\ldots,\alpha_{L-1})$ over
$[L]=\{0,1,\ldots,L-1\}$, there are two sequences
$\tau_0,\ldots,\tau_{L-1}\in[0,1]$ and
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

With these two sequences, the output has distribution $\alpha$.

Now let $\mathcal{T}$ be an arbitrary target distribution over $\{0,1\}^n$.
For a prefix $a\in\{0,1\}^{n-1}$, define its target marginal

$$
\mu(a)=\sum_{z\in\{0,1\}}\mathcal{T}(a,z).
$$

Apply this fact to $\mu$, with $L=2^{n-1}$. This gives a probability
$\tau_a$ and a second prefix $q_a$ for every prefix $a$.

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

By the two-sequence construction, the prefix $B$ has marginal distribution
$\mu$. The final token $Z$ is then sampled from the correct conditional
distribution under $\mathcal{T}$. Therefore the final output $(B,Z)$ has law
$\mathcal{T}$.

It remains to show that two rounds do not always suffice. We prove this by a
dimension argument.

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

Thus $\mathcal{P}_\mu$ is supported on the input-output pairs that satisfy the
parity relation, and the free parameter is the distribution $\mu$ over the
$2^{n-1}$ possible prefixes.

Now consider any two-round sampler with revision. Let
$\theta_i=(\theta_{i,0},\theta_{i,1},\theta_{i,M})$ be the first-round
distribution at position $i$, and let
$\theta=(\theta_i)_{i=0}^{n-1}$. The first round is described by at most $3n$
probability parameters, one triple for each position's probabilities on
$0,1,M$, and induces the product distribution

$$
\Pr_\theta[S=s]
  =
  \prod_{i=0}^{n-1}\theta_{i,s_i}.
$$

Conditioned on a first-round state $S=s$, the second round again samples the
final positions independently. If the final law is $\mathcal{P}_\mu$, every
conditional product law that occurs with positive probability must be
supported on parity-consistent input-output pairs. But any product distribution
with this support is a point mass: if any coordinate has both values with
positive probability, flipping that coordinate violates the parity relation.
Therefore the second round is deterministic on every first-round state with
positive probability.

So a two-round sampler induces a deterministic map

$$
g:\{0,1,M\}^n \to \{0,1\}^{n-1},
$$

where $g(s)$ is the prefix $y\in\mathcal{Y}$ of the final parity-consistent
output. There are at most

$$
\left(2^{n-1}\right)^{3^n}
$$

possible maps $g$.

Fix such a map $g$, and choose one reference state
$y_\star\in\mathcal{Y}$ so that the output distribution can be viewed through
the other $2^{n-1}-1$ state coordinates:

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

On the other hand,

$$
\operatorname{Vol}(\Delta_A)>0.
$$

Choose $(\mu(y))_{y\in A}$ outside the union
$\bigcup_g\Phi_g(\Theta)$. The corresponding $\mathcal{P}_\mu$ cannot be
sampled in two rounds. The construction above samples every $\mathcal{P}_\mu$
in three rounds, so the tight round complexity is $3$ in this general
unrestricted-predictor regime.

---

### A one-hot example

Now consider the one-hot distribution $U_n$ in a circuit-restricted setting.
Assume $n=2^t$.

**Observation 3 (one-hot sampling separates revision from no revision in
$AC^0$).**
Without revision, the same no-revision argument still gives the $n$-round
obstruction. There is also a separate probability-representation issue: the
natural one-position-at-a-time sampler would need transition probabilities such
as

$$
\frac{1}{n-1}.
$$

If the $AC^0$ implementation is restricted to a finite number of fair random
bits, then every probability representable without approximation is dyadic,
i.e., it has a finite binary expansion. But $1/(n-1)$ is not dyadic for
$n=2^t$. Under this implementation model, the no-revision sequential
construction cannot realize the target distribution. This is a
probability-representation obstruction, separate from the round-complexity
obstruction.

With revision, however, $U_n$ has a very short sampler.
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
with workspace-style revision, sampling from $U_n$ takes two rounds in
this $AC^0$ setting.

---

### Accelerating autoregressive sampling

**Proposition 4 (accelerating autoregressive sampling with revision).** An
autoregressive sampler whose predictor is implemented by $AC^0$ circuits can be
simulated by a DLM with revision in $O(n/\log n)$ rounds.

The core idea is a distribution-preserving speculative-decoding simulation.

Let the autoregressive sampler use predictor $p$, so the target distribution is
specified by the conditionals

$$
p_i(x_i\mid x_{<i}), \qquad i=0,\ldots,n-1,
$$

and assume that this predictor family is in $AC^0$. We construct a with-revision
DLM predictor $p'$ that uses $p$ as a subroutine on scratch coordinates. Reserve
the last

$$
s=\lceil \sqrt n\rceil
$$

coordinates as temporary workspace, and generate the first $n-s$ coordinates in
blocks of size

$$
d_{\mathrm{blk}}=\left\lfloor \frac12\log_2 n\right\rfloor .
$$

Suppose that a prefix $y=(x_0,\ldots,x_{m-1})$ has already been generated, where
$m$ is the start of the current block. To generate the next block, use the
scratch coordinates to represent the nodes
$u\in\{0,1\}^{<d_{\mathrm{blk}}}$ of a depth-$d_{\mathrm{blk}}$ binary tree.
These nodes are stored by their binary labels, not merely by their depths. For
example, if $|u|=j$ and $\operatorname{val}(u)$ is the integer represented by
$u$, store the node $u$ in scratch coordinate

$$
r(u)=n-s+(2^j-1)+\operatorname{val}(u).
$$

There are fewer than $2^{d_{\mathrm{blk}}}\le \sqrt n$ such nodes, so they fit
in the reserved workspace. In one DLM round, $p'$ samples every scratch
coordinate $r(u)$ by
querying the autoregressive predictor $p$ for the next output coordinate after
the prefix $(y,u)$:

$$
z_u:=x_{r(u)}\sim p_{m+|u|}(\cdot\mid y,u).
$$

This is still an $AC^0$ operation: for each scratch coordinate, $p'$ makes one
query to the assumed $AC^0$ autoregressive predictor $p$, with the candidate
prefix $u$ hardwired by that coordinate. Coordinates that are not used as
scratch are updated deterministically by $p'$ so that already generated output
bits are preserved during this round.

The sampled scratch bits define a random depth-$d_{\mathrm{blk}}$ decision tree.
In the next round, choose the unique leaf
$a=(a_0,\ldots,a_{d_{\mathrm{blk}}-1})$ satisfying

$$
a_j=z_{a_{<j}}\qquad\text{for every }j<d_{\mathrm{blk}}.
$$

The test for a fixed candidate leaf is an AND of
$d_{\mathrm{blk}}=O(\log n)$ equalities, and the selection over all leaves is an
OR over at most $\sqrt n$ candidates. With unbounded fan-in, this is constant
depth, so it is again in $AC^0$. In this commit round, $p'$ deterministically
revises the output block to $a$ and then reuses the scratch coordinates for the
next block.

The resulting block has the same distribution as the autoregressive
chain rule: along the selected path, the bit at depth $j$ is sampled from the
conditional distribution given the previously selected bits. The off-path
scratch samples are irrelevant. Therefore each block costs only $O(1)$ DLM
rounds. The first $n-\sqrt n$ coordinates require

$$
O\left(\frac{n}{\log n}\right)
$$

rounds, and the remaining $\sqrt n$ coordinates can be sampled one by one,
which adds only $O(\sqrt n)=o(n/\log n)$ rounds. Hence the total number of
rounds is $O(n/\log n)$.

### Dyadic product distributions with a parity check

**Proposition 5 (dyadic product distributions with one parity check).** Fix a
constant $\kappa$, and consider distributions of the form

$$
\Pr[X=x]
  =
  \left(\prod_{i=0}^{n-2} p_i(x_i)\right)
  \mathbf{1}\left[
    x_{n-1}=\bigoplus_{i=0}^{n-2} x_i
  \right],
$$

where

$$
p_i(0)=\frac{a_i}{2^\kappa},
\qquad
p_i(1)=\frac{2^\kappa-a_i}{2^\kappa}.
$$

When all $a_i=2^{\kappa-1}$, this is the usual uniform parity distribution. For
constant $\kappa$, this distribution can be sampled in $O(1)$ rounds by an
$AC^0$ DLM with revision.

The construction uses $O(1)$ reserved coordinates as a clock. These coordinates
encode the current phase of the sampler, so the predictor $p'$ can tell whether
a given coordinate should perform the next operation in its hardwired schedule.
Since $\kappa$ is constant, the number of phases is constant, and the clock
needs only $O(1)$ coordinates. These coordinates are temporary: in the final
cleanup round, they are resampled as ordinary output bits.

For each nonreserved coordinate $i<n-1$, the sampler builds the desired dyadic
Bernoulli distribution using a constant-length schedule of three elementary
operations:

$$
\mathrm{ID}: (\alpha,\beta)\mapsto(\alpha,\beta),
$$

$$
\mathrm{NOT}: (\alpha,\beta)\mapsto(\beta,\alpha),
$$

and

$$
\mathrm{IF}: (\alpha,\beta)\mapsto
\left(\frac{\alpha}{2},\,\beta+\frac{\alpha}{2}\right).
$$

Here $(\alpha,\beta)$ denotes the current probabilities of values $(0,1)$. The
operation $\mathrm{IF}$ keeps a $1$ fixed, while a $0$ is replaced by an
independent fair bit. Equivalently, if
$(\alpha,\beta)=(a/2^\ell,b/2^\ell)$, then

$$
\mathrm{IF}:
\left(\frac{a}{2^\ell},\frac{b}{2^\ell}\right)
\mapsto
\left(\frac{a}{2^{\ell+1}},\frac{2b+a}{2^{\ell+1}}\right).
$$

Together with $\mathrm{NOT}$, these operations generate any dyadic Bernoulli
distribution with denominator $2^\kappa$ in $O(\kappa)$ phases; here
$\kappa=O(1)$. The schedule for each coordinate is fixed in advance from the
binary expansion of $a_i$. We also refine the schedule so that a single phase
never mixes $\mathrm{NOT}$ and $\mathrm{IF}$ operations: in each phase, every
coordinate is either idle, or the active coordinates all perform
$\mathrm{NOT}$, or the active coordinates all perform $\mathrm{IF}$. This only
changes the number of phases by a constant factor.

The last coordinate $x_{n-1}$ is used as the parity coordinate. The phase
separation lets us update it by cases.

In an $\mathrm{ID}$ phase, no output bit changes, so the parity coordinate is
left unchanged.

In a $\mathrm{NOT}$ phase, all active updates are deterministic. The parity
coordinate is flipped if and only if the number of active $\mathrm{NOT}$
coordinates is odd; this number is known from the hardwired schedule.

In an $\mathrm{IF}$ phase, the only possible parity changes come from active
coordinates that are currently equal to $0$. Such a coordinate is sampled as
either $0$ or a temporary marker $M$. Here $0$ and $M$ are not interpreted as
ordinary output values. Restricted to the coordinates that are active in this
$\mathrm{IF}$ phase, they are temporary states used by the prefix-xor gadget:
they encode the running xor of the random updates created by this phase. This
prefix-xor state is then absorbed into the parity coordinate using the same
constant-round revision gadget used for the uniform parity sampler. After the
parity coordinate has been updated, the active coordinates are cleaned up and
revised to their ordinary output values.

At the end, the clock coordinates and any other reserved marker coordinates are
sampled according to their own dyadic marginals. Since there are only $O(1)$ of
them, their contribution can be folded into the parity coordinate in $AC^0$.
The final state contains no $M$ symbols, the first $n-1$ coordinates have the
desired independent dyadic marginals, and the last coordinate is their xor.
Thus the whole sampler uses $O(\kappa)$ rounds, and in particular $O(1)$ rounds
when $\kappa=O(1)$.

