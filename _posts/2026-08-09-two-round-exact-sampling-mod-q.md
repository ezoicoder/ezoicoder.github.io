---
title: "Exact two-round sampling for MOD_3 and every fixed MOD_q"
date: 2026-08-09
updated: 2026-08-09
slug: two-round-exact-sampling-mod-q
permalink: /blog/two-round-exact-sampling-mod-q/
tags: [diffusion language models, exact sampling, circuit complexity, regular languages]
summary: "Explicit fair-bit AC^0 cube-permutation constructions that exactly sample MOD_3 and every fixed MOD_q input-output pair distribution in two revision-DLM rounds."
---

This note gives explicit two-round exact samplers for the input-output pair
distributions associated with $\mathrm{MOD}_3$ and, more generally, every fixed
$\mathrm{MOD}_q$. These constructions predate the Markov-chain proof for all
fixed binary regular languages developed in
[*Sampling round complexity for diffusion language models*]({{ '/blog/sampling-round-complexity-dlms/' | relative_url }}).
They remain useful because they give concrete deterministic cube permutations,
rather than passing through a latent Markov path and a stochastic second-round
character kernel.

> **TODO ($AC^0$ to Transformer):** Everything below is proved in the
> fair-bit circuit-level $AC^0$ revision-DLM model. A concrete compilation into
> the intended finite-precision Transformer architecture remains to be given.

## Target distribution and model

Fix an integer $q\ge2$. For $x\in\{0,1\}^n$, define

$$
f_{q,n}(x)
=
\mathbf{1}\left[|x|\equiv0\pmod q\right]
$$

and the input-output pair distribution

$$
\mathcal D_{q,n}^{\mathrm{pair}}
=
(X,f_{q,n}(X)),
\qquad
X\sim\mathrm{Unif}(\{0,1\}^n).
$$

The sampler has width $n+1$. It starts from the all-mask state, uses independent
fair random bits, and updates coordinates independently conditioned on the old
state. Each coordinate kernel is computed by a fixed-depth polynomial-size
$AC^0$ circuit. Revision is allowed, so the second round may overwrite every
first-round coordinate.

The status is:

| Family | Exact revision-DLM complexity | Explicit construction | Transformer realization |
| --- | --- | --- | --- |
| $\mathrm{MOD}_3$ | **PROVED: exactly two rounds for every $n\ge1$** | LSB-first interval-comparator cube permutation | **TODO: $AC^0$ to Transformer** |
| fixed $\mathrm{MOD}_q$, $q\ge2$ | **PROVED: exactly two rounds for every $n\ge1$** | $2q$-bit residue coupling and rank-matched cube permutation | **TODO: $AC^0$ to Transformer** |

The exact quantifiers are

$$
\boxed{
\forall q\in\mathbb Z_{\ge2}\;
\exists d_q,K_q<\infty\;
\forall n\ge1:
\qquad
D_{\min,q}^{d_q,K_q}(n)=2.
}
$$

The round bound $2$ is uniform in $q$, but the block length, circuit depth, and
polynomial-size exponent may depend on the fixed modulus. The quantifiers do
not cover $q=q(n)$.

## The deterministic two-round interface

Both constructions use the same interface. Suppose there are $AC^0$ circuits
computing a cube permutation

$$
P_{q,n}:\{0,1\}^n\to\{0,1\}^n
$$

and a Boolean readout $C_{q,n}$ such that, pointwise,

$$
f_{q,n}(P_{q,n}(z))=C_{q,n}(z).
$$

Then the revision-DLM sampler is:

1. in the first round, sample $Z\sim\mathrm{Unif}(\{0,1\}^n)$ using one
   independent fair bit per input coordinate and put a fixed placeholder in
   the label coordinate;
2. in the second round, deterministically output
   $(P_{q,n}(Z),C_{q,n}(Z))$.

Conditioned on $Z$, all second-round coordinate laws are point masses, hence a
valid product kernel. Since $P_{q,n}$ is a permutation,
$P_{q,n}(Z)$ is exactly uniform. The pointwise identity gives the correct
label, with no approximation and no non-dyadic random coin.

One round cannot suffice. From the all-mask state, a one-round output law is a
product distribution. Its first $n$ coordinates must be independent fair bits,
so the last coordinate would be independent of them. But the target requires
the last coordinate to equal the nonconstant deterministic function
$f_{q,n}$; indeed $f_{q,n}(0^n)=1$ and $f_{q,n}(e_1)=0$. Thus the two-round
upper bounds below are optimal for every $q\ge2$ and $n\ge1$.

## The special $\mathrm{MOD}_3$ interval construction

The $q=3$ construction is unusually explicit: it transforms a lexicographic
interval into a Hamming-weight residue slice.

For $r\in\mathbb Z_3$ and $k\ge0$, define the residue-slice counts

$$
N_{r,k}
=
\left|
\left\{
x\in\{0,1\}^k:|x|\equiv r\pmod3
\right\}
\right|.
$$

Splitting according to the least significant bit gives

$$
N_{r,k}=N_{r,k-1}+N_{r-1,k-1}.
$$

For every fixed $k$, the three values $N_{0,k},N_{1,k},N_{2,k}$ differ by at
most $1$. Consequently,

$$
\left\{N_{r,k-1},N_{r-1,k-1}\right\}
=
\left\{
\left\lceil\frac{N_{r,k}}2\right\rceil,
\left\lfloor\frac{N_{r,k}}2\right\rfloor
\right\}
$$

as multisets. Define

$$
e_{r,k}
=
\mathbf{1}[N_{r,k-1}<N_{r-1,k-1}].
$$

We recursively construct a permutation

$$
P_{r,k}:\{0,1\}^k\to\{0,1\}^k.
$$

The base case is $P_{r,0}(0)=0$. For $k\ge1$, interpret the input as the
integer

$$
x=z+2u,
\qquad
z\in\{0,1\},
\qquad
0\le u<2^{k-1},
$$

where $z$ is the least significant bit. Set

$$
y=z\mathbin{\oplus}e_{r,k}
$$

and

$$
P_{r,k}(z+2u)
=
y+2P_{r-y,k-1}(u),
$$

where $r-y$ is computed in $\mathbb Z_3$. The map $z\mapsto y$ is a one-bit
permutation, and the two higher-bit fibers are permutations by induction, so
every $P_{r,k}$ is a cube permutation.

More importantly, the same induction gives the exact interval identity

$$
\boxed{
x<N_{r,k}
\quad\Longleftrightarrow\quad
|P_{r,k}(x)|\equiv r\pmod3.
}
$$

The reason is numerical: the interval $[0,N_{r,k})$ contains
$\lceil N_{r,k}/2\rceil$ integers of one input parity and
$\lfloor N_{r,k}/2\rfloor$ of the other. The flip bit $e_{r,k}$ sends the
larger input fiber to the larger target residue fiber, after which the claim
reduces to length $k-1$.

Taking

$$
P_n=P_{0,n},
\qquad
B_n(z)=\mathbf{1}[z<N_{0,n}],
$$

we obtain the pointwise identity

$$
f_{3,n}(P_n(z))=B_n(z).
$$

The readout $B_n$ is comparison with a fixed $n$-bit constant, hence has a
depth-$2$, polynomial-size DNF.

### Why the LSB-first recursion is in $AC^0$

A constant-state recursion is not automatically in $AC^0$. Here the extra
ingredient is aperiodicity. If $r_j$ is the residue state before processing the
$j$th least significant bit and $k=n-j$, then

$$
y_j=z_j\mathbin{\oplus}e_{r_j,k},
\qquad
r_{j+1}=r_j-y_j\pmod3.
$$

The flip table depends only on $k\bmod6$:

| $k\bmod6$ | $(e_{0,k},e_{1,k},e_{2,k})$ |
| ---: | :---: |
| $0,1$ | $(0,1,0)$ |
| $2,3$ | $(0,0,1)$ |
| $4,5$ | $(1,0,0)$ |

Group six consecutive input bits into one block. For each of the six possible
starting phases, the block words generate an eight-element transformation
monoid on $\mathbb Z_3$. Every element $a$ satisfies

$$
a^3=a^2.
$$

The monoid is therefore aperiodic. By the classical equivalence between
aperiodic finite monoids, star-free languages, and $FO[<]$, every prefix-state
predicate is computable in uniform $AC^0$. Each output bit then applies only a
fixed lookup to its prefix state, phase, and current bit. Hence both $P_n$ and
$B_n$ satisfy the deterministic two-round interface.

This is a special feature of $q=3$. The three residue counts remain within
$1$, making the binary interval split possible at every recursion level. For
$q\ge4$, this fixed-block interval-comparator normal form does not extend: the
adjacent residue-count gaps become unbounded. That obstruction concerns this
specific comparator construction, not two-round sampling itself.

## Every fixed $\mathrm{MOD}_q$ by common quantiles

The general construction abandons the interval comparator. It uses $2q$-bit
blocks and couples all residue-state transition rows by a common rank.

### Residue census

Fix the block length

$$
b=2q,
\qquad
N=2^{2q},
$$

and define, for $d\in\mathbb Z_q$,

$$
w_d
=
\left|
\left\{
y\in\{0,1\}^{2q}:|y|\equiv d\pmod q
\right\}
\right|.
$$

The counts have the explicit form

$$
w_0=\binom{2q}{q}+2,
$$

and, for $1\le d\le q-1$,

$$
w_d
=
\binom{2q}{d}+\binom{2q}{q-d}.
$$

Thus $w_d=w_{-d}$. If $m=\lfloor q/2\rfloor$, the binomial first-difference
calculation further gives

$$
\boxed{
w_0\ge w_1\ge\cdots\ge w_m.
}
$$

For example, if

$$
\Delta_k=\binom{2q}{k}-\binom{2q}{k-1},
$$

then for $1\le r<m$,

$$
w_r-w_{r+1}=\Delta_{q-r}-\Delta_{r+1}>0.
$$

Hence the block residue census is symmetric and nonincreasing with circular
distance from $0$.

### A stochastic order on residue states

Order $\mathbb Z_q$ by the zigzag chain

$$
0<1<-1<2<-2<\cdots.
$$

Write this chain as $\xi_0<\xi_1<\cdots<\xi_{q-1}$, and let
$I_k=\{\xi_0,\ldots,\xi_k\}$ be a chain prefix. From an old residue state
$s$, the desired integer mass at target $t$ is

$$
\mu_s(t)=w_{t-s}.
$$

Define its cumulative mass along the chain by

$$
F_s(k)=\sum_{t\in I_k}w_{t-s}.
$$

The radial monotonicity of $w$ implies

$$
F_{\xi_i}(k)\ge F_{\xi_{i+1}}(k)
$$

for every adjacent pair of old states and every prefix $I_k$. A direct
telescoping check makes the direction explicit over the index ranges needed
for adjacent zigzag comparisons. For an even prefix
$I_{2j}=\{-j,\ldots,j\}$, let

$$
A_j(r)=\sum_{t=-j}^{j}w_{t-r}.
$$

Then

$$
A_j(r)-A_j(r+1)
=
w_{j-r}-w_{-j-r-1}\ge0.
$$

For an odd prefix $I_{2j-1}=\{-j+1,\ldots,j\}$, define

$$
B_j(r)=\sum_{t=-j+1}^{j}w_{t-r}.
$$

Similarly,

$$
B_j(r)-B_j(r+1)
=
w_{j-r}-w_{-j-r}\ge0.
$$

Together with the reflection symmetries of these two kinds of prefixes, these
inequalities give the claimed stochastic order along the entire zigzag chain.

### Common quantiles and rank matching

For each integer rank $u\in\{0,\ldots,N-1\}$, use the same rank in every old
state row and define

$$
\tau_u(s)
=
\xi_{\min\{k:u<F_s(k)\}}.
$$

The CDF ordering implies that every transformation

$$
\tau_u:\mathbb Z_q\to\mathbb Z_q
$$

preserves the zigzag chain. Moreover, the quantile interval assigned to target
$t$ has exactly the required integer length, so for every $s,d\in\mathbb Z_q$,

$$
\boxed{
\left|
\left\{
u:\tau_u(s)-s\equiv d\pmod q
\right\}
\right|
=w_d.
}
$$

For each old state $s$ and residue increment $d$, define

$$
D_{s,d}
=
\left\{
u:\tau_u(s)-s\equiv d\pmod q
\right\}
$$

and

$$
W_d
=
\left\{
y\in\{0,1\}^{2q}:|y|\equiv d\pmod q
\right\}.
$$

The boxed census gives $|D_{s,d}|=|W_d|$. Match the two sets by rank within
each residue class. Combining the $q$ matches gives a block cube permutation

$$
\pi_s:\{0,1\}^{2q}\to\{0,1\}^{2q}
$$

satisfying

$$
\boxed{
s+|\pi_s(u)|
\equiv
\tau_u(s)
\pmod q.
}
$$

### Global cube permutation

Write

$$
n=2qM+r,
\qquad
0\le r<2q.
$$

Split the first $2qM$ seed bits into blocks $u_1,\ldots,u_M$, and call the
remaining $r$ bits $c$. Starting from $s_0=0$, set

$$
y_i=\pi_{s_{i-1}}(u_i),
\qquad
s_i=\tau_{u_i}(s_{i-1}).
$$

Define

$$
P_{q,n}(u_1,\ldots,u_M,c)
=
(y_1,\ldots,y_M,c)
$$

and

$$
C_{q,n}(z)
=
\mathbf{1}[s_M+|c|\equiv0\pmod q].
$$

The block identity implies

$$
\sum_{i=1}^{M}|y_i|\equiv s_M\pmod q,
$$

and hence

$$
f_{q,n}(P_{q,n}(z))=C_{q,n}(z).
$$

The global map is a permutation by triangular inversion. Knowing
$s_{i-1}$ and $y_i$, invert the fixed permutation $\pi_{s_{i-1}}$ to recover
$u_i$, then compute $s_i$ and continue to the next block. The remainder is
unchanged.

### Why the construction is in $AC^0$

Every $\tau_u$ preserves the same finite chain, and compositions preserve it as
well. Any order-preserving self-map $a$ of a $q$-element chain has monotone
orbits and satisfies

$$
a^q=a^{q-1}.
$$

Therefore the transformation monoid generated by the $\tau_u$ is aperiodic.
The prefix-state languages are consequently star-free, equivalently definable
in $FO[<]$, and hence computable in uniform $AC^0$. Since $q$ is fixed, the
block alphabet, $\tau_u$ tables, $\pi_s$ tables, and remainder tests are all
constant-size lookups. Every output bit and the final readout are therefore
fixed-depth polynomial-size circuits.

This proves the deterministic two-round interface for every fixed $q\ge2$,
including composite moduli. No step uses a finite-field structure, a
multiplicative inverse, or the Chinese remainder theorem; the proof uses only
the additive cyclic group $\mathbb Z_q$, circular distance, and a fixed finite
chain.

If $n<2q$, there is no complete block. Then $P_{q,n}$ is the identity and the
readout is a constant-size lookup because only finitely many lengths are
involved for fixed $q$. Thus the construction covers every positive length,
not only sufficiently large $n$.

## Relation to the general regular-language theorem

The newer regular-language proof starts from the finite Markov chain induced by
uniform input characters. It first samples the complete DFA-state trajectory in
$AC^0$, then samples each character independently from the set compatible with
its adjacent states. That route proves a two-round upper bound for every fixed
binary regular language.

The constructions in this note are more specialized but more explicit:

- their second round is deterministic rather than a stochastic compatible-set
  kernel;
- the $\mathrm{MOD}_3$ readout is a concrete lexicographic comparator;
- the fixed-$q$ construction exposes the residue census, common coupling, and
  cube permutation directly.

They do not imply uniform circuit constants for all $q$, and they say nothing
about a growing modulus $q=q(n)$. They also do not prove that
$\mathrm{MOD}_q$ recognition is in $AC^0$: the shallow circuit computes the
label only after a measure-preserving reparameterization of the Boolean cube.

For the contrasting recognition lower bound, see
[*Near-perfect average-case MOD_q requires log n / log log n depth for polynomial-size AC circuits*]({{ '/blog/near-perfect-mod-q-ac-depth/' | relative_url }}).
