---
title: "Exact AC^0 sampling for Markov chains and regular languages"
date: 2026-08-09
updated: 2026-08-09
slug: exact-ac0-sampling-markov-chains
permalink: /blog/exact-ac0-sampling-markov-chains/
tags: [diffusion language models, exact sampling, circuit complexity, Markov chains, regular languages]
summary: "A proof sequence from explicit two-round MOD_3 and fixed-MOD_q samplers to exact AC^0 trajectory sampling for path-dyadic finite Markov chains and every fixed binary regular language."
---

This note develops one proof sequence for exact sampling in shallow circuits:

1. the special $\mathrm{MOD}_3$ interval-comparator construction;
2. the common-quantile construction for every fixed $\mathrm{MOD}_q$;
3. exact full-trajectory sampling for every fixed path-dyadic finite Markov
   chain;
4. exact two-round sampling for the input-output pair distribution of every
   fixed binary regular language.

The first two constructions expose concrete deterministic cube permutations.
The Markov-chain theorem needs a different abstraction: dyadic state splitting
followed by a universal aperiodic lift of a finite binary transition system.
The regular-language result is then a corollary obtained by sampling the DFA
state trajectory and applying a coordinatewise compatible-character kernel.

All results here are circuit-level results. The companion note
[*Sampling round complexity for diffusion language models*]({{ '/blog/sampling-round-complexity-dlms/' | relative_url }})
separates their circuit status from the remaining Transformer compilation
questions.

## Result map and circuit model

An exact fair-bit randomized-$AC^0$ sampler is a polynomial-size,
constant-depth Boolean circuit whose random inputs are finitely many independent
fair bits. The output distribution must equal the target distribution atom by
atom. For length-indexed families below, the circuit depth is bounded by a
constant independent of the length. Constants may depend on the fixed modulus,
Markov chain, or automaton named in the theorem.

In the revision-DLM interpretation, the first round writes independent fair
seed bits. A later update is a product kernel conditioned on the old state:
each coordinate may use the entire old state, but different coordinates use
independent fresh randomness. A deterministic update is a special case in
which every coordinate kernel is a point mass.

The four conclusions proved below are:

| Target | Circuit-level status | Exact boundary |
| --- | --- | --- |
| $\mathrm{MOD}_3$ input-output pairs | **PROVED: exactly two rounds** | Every positive input length |
| fixed $\mathrm{MOD}_q$, $q\ge2$ | **PROVED: exactly two rounds** | Constants may depend on fixed $q$; not $q=q(n)$ |
| fixed path-dyadic finite Markov chain | **PROVED: exact full-trajectory randomized-$AC^0$ sampler** | $c+sn$ fair bits; constants depend on the chain |
| fixed binary regular language | **PROVED: at most two revision rounds** | Exactly two on every nonconstant length slice |

The Markov theorem does **not** say that every finite Markov chain can be
sampled exactly from finitely many fair bits. Path-dyadicity is both sufficient
and necessary.

## Modular input-output pair distributions

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

The sampler has width $n+1$. The exact modular quantifiers are

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

## The deterministic two-round interface for modular predicates

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

## Why the modular constructions are not yet the general proof

The two modular constructions above use the same strong interface: an explicit
cube permutation $P_{q,n}$ makes the label shallow, and the second DLM round is
fully deterministic. This interface is convenient but unnecessarily
restrictive for a general finite automaton. A general two-round revision update
may use a stochastic product kernel in its second round.

The general proof therefore separates two tasks:

1. sample the complete trajectory of a fixed finite Markov chain in randomized
   $AC^0$;
2. for a binary DFA, sample each character independently conditioned on its two
   adjacent trajectory states.

The first task is the technical core. It is a theorem about Markov trajectories,
not about accepting states or language recognition.

## Path-dyadic Markov trajectories

Fix a finite discrete-time Markov chain

$$
\mathcal M=(Q,\mu,P),
$$

and discard states that are not reachable with positive probability from
$\mu$. For a horizon $n\ge0$ and a state sequence

$$
\gamma=(x_0,x_1,\ldots,x_n)\in Q^{n+1},
$$

the trajectory atom is

$$
p_{\mathcal M}(\gamma)
=
\mu(x_0)\prod_{i=1}^{n}P(x_{i-1},x_i).
\tag{1}
$$

The target is the joint law of the entire trajectory

$$
(X_0,X_1,\ldots,X_n),
$$

not merely the terminal marginal $X_n$.

Let $\mathbb D_{\ge0}$ be the nonnegative dyadic rationals. The chain is
**path-dyadic** from $\mu$ when

$$
\forall n\ge0\;\forall\gamma\in Q^{n+1}:
\qquad
p_{\mathcal M}(\gamma)\in\mathbb D_{\ge0}.
\tag{2}
$$

An exact fair-bit randomized-$AC^0$ trajectory sampler is a family

$$
S_n:\{0,1\}^{r_n}\longrightarrow Q^{n+1}
$$

such that $S_n(U_{r_n})$ has exactly the trajectory law (1). The finite state
set $Q$ uses a fixed constant-length encoding, and depth and size refer to the
whole multi-output circuit.

**Theorem 1 (path-dyadic trajectory characterization).** For every fixed
finite Markov chain $\mathcal M=(Q,\mu,P)$, the following statements are
equivalent.

1. The chain is path-dyadic from $\mu$.
2. There are positive integer weights $w_q$ such that

   $$
   \frac{\mu(q)}{w_q}\in\mathbb D_{\ge0},
   \qquad
   \frac{w_qP(q,r)}{w_r}\in\mathbb D_{\ge0}
   \tag{3}
   $$

   for all $q,r\in Q$.
3. The chain is the coordinatewise projection of a fixed finite hidden Markov
   chain with dyadic initial atoms and dyadic transitions, such that the hidden
   state is uniform inside the current visible fiber conditioned on every
   positive-probability visible history.
4. There are constants $c,s,d,K$, depending only on $\mathcal M$, such that
   every horizon $n$ has an exact fair-bit randomized-$AC^0$ trajectory
   sampler using exactly $c+sn$ fair bits, depth at most $d$, and size at most
   $O(n^K)$.

If the initial state is fixed, one may take $c=0$. The construction in item 4
also exposes $n$ independent uniform $s$-bit transition drivers.

### Finite fair bits force path-dyadicity

Fix $n$. If a sampler reads $r_n<\infty$ fair bits, every output atom is the
image of an integer number of seeds. Hence

$$
\Pr[S_n(U_{r_n})=\gamma]
=
\frac{|S_n^{-1}(\gamma)|}{2^{r_n}}
\in\mathbb D_{\ge0}.
$$

Thus a single non-dyadic trajectory atom rules out every finite-fair-bit exact
sampler, regardless of depth or size. An unbounded rejection sampler belongs to
a different model.

### The dyadic potential criterion

We next prove the equivalence between path-dyadicity and the potential
condition (3). Suppose first that weights
$w_q$ satisfying (3) exist. Define

$$
a_q=\frac{\mu(q)}{w_q},
\qquad
R(q,r)=\frac{w_qP(q,r)}{w_r}.
$$

Along any trajectory, the intermediate weights telescope:

$$
\begin{aligned}
p_{\mathcal M}(\gamma)
&=
\mu(x_0)\prod_{i=1}^{n}P(x_{i-1},x_i)
\\
&=
a_{x_0}w_{x_n}
\prod_{i=1}^{n}R(x_{i-1},x_i).
\end{aligned}
\tag{4}
$$

Every factor on the second line is dyadic except for the final positive integer
$w_{x_n}$, so the trajectory atom is dyadic.

Conversely, assume every trajectory atom is dyadic. Every positive transition
is rational: if $\gamma$ is a positive path ending at $q$, then

$$
P(q,r)=\frac{p_{\mathcal M}(\gamma r)}{p_{\mathcal M}(\gamma)}.
$$

Fix an odd prime $p$ and let $v_p$ denote the $p$-adic valuation of a nonzero
rational. For each reachable state $q$, let $\Gamma(q)$ be the positive paths
ending at $q$ and define

$$
\alpha_p(q)
=
\min_{\gamma\in\Gamma(q)}
v_p\!\left(p_{\mathcal M}(\gamma)\right).
\tag{5}
$$

These values are nonnegative integers. Extending a minimizing path by a
positive edge gives

$$
\alpha_p(r)
\le
\alpha_p(q)+v_p(P(q,r)),
\tag{6}
$$

and a length-zero path with $\mu(q)>0$ gives

$$
\alpha_p(q)\le v_p(\mu(q)).
\tag{7}
$$

Set

$$
w_q
=
\prod_{p\text{ odd prime}}p^{\alpha_p(q)}.
\tag{8}
$$

The product is finite: any one fixed positive path ending at $q$ has only
finitely many odd prime factors in its numerator and upper-bounds every
$\alpha_p(q)$. Equations (6)--(7) imply that both ratios in (3) have
nonnegative valuation at every odd prime. A nonnegative rational is dyadic
exactly when this holds, proving the criterion.

Because there are only finitely many states and edges, constants $c,s$ may be
chosen so that

$$
2^c\frac{\mu(q)}{w_q}\in\mathbb Z_{\ge0},
\qquad
2^s\frac{w_qP(q,r)}{w_r}\in\mathbb Z_{\ge0}
\tag{9}
$$

simultaneously for all $q,r$. Equation (4) then gives the uniform denominator
bound

$$
2^{c+sn}p_{\mathcal M}(\gamma)\in\mathbb Z_{\ge0}.
\tag{10}
$$

This arithmetic bound is necessary, but it does not yet provide a shallow
sampler: naively iterating the transition map still has depth $n$.

### A finite dyadic weak lift

Choose $s$ as in (9) and write

$$
m_{q,r}
=
2^s\frac{w_qP(q,r)}{w_r}
\in\mathbb Z_{\ge0}.
\tag{11}
$$

Split each visible state into a fiber

$$
F_q=\{(q,1),\ldots,(q,w_q)\},
\qquad
\widetilde Q=\bigsqcup_{q\in Q}F_q,
$$

with projection $\rho(q,j)=q$. For every source fiber $F_q$, construct a
nonnegative integer transportation matrix $C^{(q)}$ whose rows are indexed by
$h\in F_q$ and whose columns are indexed by $h'\in\widetilde Q$, satisfying

$$
\sum_{h'}C_{h,h'}=2^s
\tag{12}
$$

for every row, and

$$
\sum_{h\in F_q}C_{h,h'}=m_{q,r}
\tag{13}
$$

for every $h'\in F_r$. The total column demand is

$$
\sum_r w_r m_{q,r}
=
2^s w_q,
$$

exactly the total supply of the $w_q$ rows, so a greedy integer filling gives
such a matrix.

Assign the $2^s$ seeds in $\{0,1\}^s$ to targets with multiplicities
$C_{h,h'}$. This defines a deterministic random map

$$
\delta:\widetilde Q\times\{0,1\}^s\longrightarrow\widetilde Q
\tag{14}
$$

and a dyadic hidden transition kernel

$$
\widetilde P(h,h')=\frac{C_{h,h'}}{2^s}.
$$

Use the hidden initial distribution

$$
\widetilde\mu(h)=\frac{\mu(q)}{w_q},
\qquad h\in F_q.
\tag{15}
$$

This is a weak lift rather than strong lumpability: a single hidden row need
not project to $P(q,\cdot)$. What makes the projection exact is the following
fiber-uniform invariant.

Conditioned on any positive visible history ending at $q$, the hidden state is
uniform on $F_q$. It holds initially by (15). Assuming it at time $i$, for any
$h'\in F_r$, equation (13) gives

$$
\begin{aligned}
\Pr[\widetilde X_{i+1}=h'\mid X_{0:i}=x_{0:i}]
&=
\frac1{w_q}\sum_{h\in F_q}\widetilde P(h,h')
\\
&=
\frac{m_{q,r}}{2^sw_q}
=
\frac{P(q,r)}{w_r}.
\end{aligned}
\tag{16}
$$

Summing over $h'\in F_r$ gives the visible transition probability $P(q,r)$;
conditioning once more makes the next hidden state uniform on $F_r$. By
induction, the projected hidden process has exactly the full visible Markov
law.

Conversely, suppose a hidden lift with the stated fiber-uniform property is
given, and set $w_q=|F_q|$. Uniformity at time zero gives

$$
\frac{\mu(q)}{w_q}=\widetilde\mu(h)
$$

for $h\in F_q$. Given any positive visible history ending at $q$ and any
$h'\in F_r$, the same invariant gives

$$
\frac{w_qP(q,r)}{w_r}
=
\sum_{h\in F_q}\widetilde P(h,h').
$$

Both right-hand sides are dyadic, so the hidden-lift condition also implies
the potential condition (3). Moreover, any fixed finite dyadic hidden kernel
has a common denominator $2^s$; assigning exactly
$2^s\widetilde P(h,h')$ driver strings to target $h'$ turns it into a finite
random-map system of the form (14).

It remains to show that the trajectory of the finite random-map system (14)
can be computed in $AC^0$ after a measure-preserving reparameterization of its
fair driver word.

## Binary transition systems and the aperiodic engine

Consider a fixed deterministic binary transition system

$$
\mathcal T=(Q,\{0,1\},\delta).
$$

There is no accepting set in this section. For a block length $b$, define the
base block census

$$
N_{q,t}^{(b)}
=
\left|
\left\{
y\in\{0,1\}^b:
\delta^*(q,y)=t
\right\}
\right|.
\tag{17}
$$

### The aperiodic block-lift criterion

A finite aperiodic $b$-block lift consists of:

1. a finite hidden set $H$ and a projection $\phi:H\to Q$;
2. a transformation $\tau_u:H\to H$ for every block seed
   $u\in\{0,1\}^b$;
3. the exact projected census

   $$
   \left|
   \left\{
   u:\phi(\tau_u(h))=t
   \right\}
   \right|
   =
   N_{\phi(h),t}^{(b)}
   \tag{18}
   $$

   for every $h\in H$ and $t\in Q$;
4. an aperiodic finite transformation monoid generated by the maps $\tau_u$.

**Proposition 2 (aperiodic lift implies shallow trajectories).** If such a
lift exists, then for every initial base state $q_0$ and every
$h_0\in\phi^{-1}(q_0)$ there are uniform-$AC^0$ cube permutations

$$
\Pi_{h_0,n}:\{0,1\}^n\longrightarrow\{0,1\}^n
\tag{19}
$$

and uniform-$AC^0$ multi-output circuits that, on $Y=\Pi_{q_0,n}(Z)$,
compute every prefix state

$$
q_i=\delta^*(q_0,Y_{1:i}),
\qquad 0\le i\le n.
\tag{20}
$$

To prove the proposition, fix $h,t$ and define

$$
D_{h,t}
=
\{u:\phi(\tau_u(h))=t\},
$$

$$
W_{h,t}
=
\{y:\delta^*(\phi(h),y)=t\}.
$$

Equation (18) gives $|D_{h,t}|=|W_{h,t}|$. Choose a bijection separately in
each target fiber and combine them into a block permutation

$$
\pi_h:\{0,1\}^b\longrightarrow\{0,1\}^b
$$

satisfying

$$
\delta^*(\phi(h),\pi_h(u))
=
\phi(\tau_u(h)).
\tag{21}
$$

Partition the seed word into full blocks $u_1,\ldots,u_M$ and a remainder.
Starting from $h_0$, iterate

$$
h_i=\tau_{u_i}(h_{i-1})
$$

and output block $\pi_{h_{i-1}}(u_i)$; leave the remainder unchanged. This is
a block-triangular cube permutation. Given the previous recovered blocks, one
knows $h_{i-1}$ and can invert $\pi_{h_{i-1}}$ to recover $u_i$.

Equation (21) shows that the projected hidden state at every block boundary is
the true base state. Because the hidden transformation monoid is aperiodic,
every prefix hidden-state predicate is definable in $FO[<]$ and hence
computable in uniform $AC^0$. Output blocks, within-block states, and the final
remainder use only fixed lookups. Thus the permutation and all states in (20)
are computable in uniform $AC^0$.

The remaining question is whether every fixed binary transition system admits
such a lift. The answer is yes.

### An exact integer interface on a hidden chain

Suppose a local hidden set is ordered as
$H=\{0,\ldots,m-1\}$ and every $\tau_u$ must be nondecreasing. Let
$B=2^b$. It suffices to find nonnegative target counts $a_{h,k}$ such that

$$
\sum_{k:\phi(k)=t}a_{h,k}
=
N_{\phi(h),t}^{(b)}
\tag{22}
$$

and, for adjacent hidden sources and every proper prefix cut,

$$
\sum_{k=0}^{j}a_{h,k}
\ge
\sum_{k=0}^{j}a_{h+1,k}.
\tag{23}
$$

List row $h$ in increasing order, repeating target $k$ exactly $a_{h,k}$
times:

$$
r_h(1)\le\cdots\le r_h(B).
$$

The prefix inequalities (23) are equivalent to the common-rank inequalities

$$
r_h(v)\le r_{h+1}(v)
$$

for every rank $v$. Defining $\tau_v(h)=r_h(v)$ then produces nondecreasing
maps with the exact projected census (22). Every composition remains
nondecreasing, so the generated monoid is aperiodic.

### The universal binary lift

**Theorem 3 (universal aperiodic lift).** Every fixed deterministic binary
transition system whose states are reachable admits a finite aperiodic block
lift. The hidden set may be chosen with

$$
|H|\le2|Q|.
\tag{24}
$$

The proof uses the strongly connected components of the uniform-driver Markov
chain. Define the one-step count matrix and stochastic kernel

$$
T_{q,t}
=
\left|
\left\{
a\in\{0,1\}:\delta(q,a)=t
\right\}
\right|,
\qquad
P=\frac12T.
\tag{25}
$$

The SCC condensation graph is acyclic. An SCC with no outgoing edge is
terminal; every other SCC is transient.

#### Terminal cyclic classes

For every terminal SCC $R$, let $d_R$ be its period and take

$$
D=\operatorname{lcm}_R d_R.
$$

If

$$
R=S_{R,0}\sqcup\cdots\sqcup S_{R,d_R-1}
$$

is the cyclic decomposition, then $P^D$ preserves each class. Restricted to
one class $S$, the appropriate powers are irreducible and aperiodic, and hence
converge to a strictly positive stationary distribution $\pi_S$.

Choose any order

$$
S=\{t_1,\ldots,t_s\}
$$

and give each base state two hidden copies, ordered as

$$
t_1^-<\cdots<t_s^-<t_1^+<\cdots<t_s^+.
\tag{26}
$$

Write these $2s$ sources as $h_1<\cdots<h_{2s}$ and set

$$
\theta_j=\frac{j}{2s+1}.
$$

The ideal hidden target distribution for source $h_j$ is

$$
\nu_j^0(t_i^-)
=(1-\theta_j)\pi_S(t_i),
\qquad
\nu_j^0(t_i^+)
=\theta_j\pi_S(t_i).
\tag{27}
$$

For a cut ending at $t_r^-$, the adjacent CDF difference is

$$
F_j(t_r^-)-F_{j+1}(t_r^-)
=
\frac1{2s+1}\sum_{i=1}^{r}\pi_S(t_i)>0.
\tag{28}
$$

For a proper cut ending at $t_r^+$, it is

$$
F_j(t_r^+)-F_{j+1}(t_r^+)
=
\frac1{2s+1}\sum_{i=r+1}^{s}\pi_S(t_i)>0.
\tag{29}
$$

Thus every proper cut has a uniform positive slack of at least

$$
\delta_S
=
\frac{\min_{t\in S}\pi_S(t)}{2s+1}.
\tag{30}
$$

This strict stochastic order is the general counterpart of the common-quantile
order used in the fixed-$q$ construction.

#### Exact rounding of true transition counts

Take $b=Dm$, set $B=2^b$, and write

$$
N=T^b.
$$

For source $h_j$ let $q_j=\phi(h_j)$. For each $t\in S$, choose a nearest
integer $L_{j,t}$ to $(1-\theta_j)N_{q_j,t}$, clipped to the interval
$[0,N_{q_j,t}]$, and let

$$
R_{j,t}=N_{q_j,t}-L_{j,t}.
$$

Define the exact hidden counts

$$
a_{j,t^-}=L_{j,t},
\qquad
a_{j,t^+}=R_{j,t}.
\tag{31}
$$

Projection is exact because

$$
a_{j,t^-}+a_{j,t^+}=N_{q_j,t}.
\tag{32}
$$

Along sufficiently large multiples $b=Dm$, the normalized rows
$P^b(q_j,\cdot)$ converge to $\pi_S$, while the rounding error divided by
$2^b$ vanishes. Therefore every strict inequality (28)--(29) survives for all
sufficiently large $m$. Sorting the rows by target and matching equal ranks
produces nondecreasing maps on the hidden chain, with the exact projected
census. Different terminal cyclic classes are handled separately.

#### Transient SCCs

For a transient SCC $C$, use one hidden copy $h_q$ for each $q\in C$.
The probability of staying inside $C$ tends to zero, so along the same
subsequence $b=Dm$ one can make

$$
\sum_{q\in C}P^b(q,C)<1.
\tag{33}
$$

Let $U=\{0,1\}^b$ and

$$
N_{q,C}=\sum_{t\in C}N_{q,t}.
$$

Equation (33) gives

$$
\sum_{q\in C}N_{q,C}<|U|.
$$

Hence one can choose pairwise disjoint sets $U_q\subseteq U$ with
$|U_q|=N_{q,C}$. Partition $U_q$ into pieces $U_{q,t}$ of sizes $N_{q,t}$
and set $\tau_u(h_q)=h_t$ for $u\in U_{q,t}$. The remaining seeds are sent to
fixed representatives of downstream target states, again respecting every
count $N_{q,t}$.

For a fixed seed $u$, at most one source in $C$ remains in $C$. This disjoint
survival property replaces stochastic ordering in transient components.

#### Why the global monoid is aperiodic

Every generator can only stay in the same SCC or move downstream in the
condensation DAG. Therefore a functional cycle of any composition must remain
inside one SCC.

Inside a terminal cyclic class, every generator is nondecreasing on its hidden
chain. A composition is again nondecreasing and has no cycle of length greater
than one.

Inside a transient SCC $C$, consider a nonempty composition

$$
g=\tau_{u_k}\circ\cdots\circ\tau_{u_1}
$$

and define

$$
D_C(g)=\{h\in H_C:g(h)\in H_C\}.
$$

If the full composition remains in $C$, its first step must remain in $C$.
Thus

$$
D_C(g)\subseteq D_C(\tau_{u_1}),
\qquad
|D_C(g)|\le1.
\tag{34}
$$

An internal cycle can therefore only be a fixed point. Every element of the
finite transformation monoid has only fixed-point cycles, so some power of it
is idempotent. The monoid is aperiodic.

There are two hidden copies for each terminal state and one for each transient
state, proving (24). All finitely many convergence and escape conditions can be
met by one sufficiently large common block length $b$.

### Random-map trajectories

Return to a finite random-map system

$$
\delta:\widetilde Q\times\{0,1\}^s\longrightarrow\widetilde Q.
\tag{35}
$$

Expand each $s$-bit driver symbol into $s$ binary input steps and add finitely
many phase and partial-symbol states. Theorem 3 and Proposition 2 then give,
for every fixed initial hidden state $h_0$, a uniform-$AC^0$ permutation

$$
\Pi_{h_0,n}:\{0,1\}^{sn}\longrightarrow\{0,1\}^{sn}
\tag{36}
$$

such that, for $Z\sim U_{sn}$, the permuted word remains uniform and its
$s$-bit blocks $U_1,\ldots,U_n$ drive

$$
h_i=\delta(h_{i-1},U_i).
$$

All states $h_0,\ldots,h_n$ are simultaneously computable in uniform
$AC^0$. The reparameterization is a permutation of the same seed cube and adds
no random bits.

## Assembling the Markov trajectory sampler

The weak lift (14)--(16) supplies a finite dyadic hidden initial distribution,
a finite random-map system, and a projection $\rho:\widetilde Q\to Q$.
Choose $c$ such that

$$
2^c\widetilde\mu(h)\in\mathbb Z_{\ge0}
$$

for every hidden state, and fix a lookup

$$
g:\{0,1\}^c\longrightarrow\widetilde Q
$$

with $g(U_c)\sim\widetilde\mu$. Let the raw seed be

$$
V\sim U_c,
\qquad
Z\sim U_{sn},
$$

independently, and set

$$
h_0=g(V),
\qquad
Y=\Pi_{h_0,n}(Z).
\tag{37}
$$

There are only finitely many possible $h_0$, so a constant-size multiplexer
selects the appropriate permutation circuit. Conditional on every $h_0$,
$\Pi_{h_0,n}$ is a cube permutation; hence $Y$ is uniform and independent of
$h_0$. Split it into independent uniform $s$-bit drivers and compute all
hidden states in $AC^0$. Finally output

$$
X_i=\rho(h_i),
\qquad 0\le i\le n.
\tag{38}
$$

The fiber-uniform invariant proves that (38) has exactly the Markov trajectory
law (1). The sampler uses $c+sn$ fair bits. All hidden sets, block lengths,
lookup tables, and circuit-depth constants depend only on the fixed chain, so
the total size is $O(n^K)$ for a chain-dependent constant $K$.

Together with the finite-bit necessity argument, this completes every
implication in Theorem 1.

In a two-round revision-DLM interpretation, round one writes the raw product
seed $(V,Z)$ and round two deterministically computes (37)--(38). One may use
$n+1$ state-valued tokens with a chain-dependent finite working alphabet, or a
constant-factor number of binary coordinates to encode those tokens and the
$s$-bit drivers. This gives a universal two-round upper bound for the full
trajectory, but it does not claim that every nontrivial chain has minimum round
complexity two: a degenerate trajectory law may itself be a product
distribution.

## Binary regular languages

Now fix a binary DFA that does not grow with the input length,

$$
\mathcal A=(Q,\{0,1\},\delta,q_0,F),
$$

and let $L$ be its language. For $X\sim U_n$, the target input-output pair
distribution is

$$
\mathcal D_{L,n}^{\mathrm{pair}}
=
(X,\mathbf 1[X\in L]).
\tag{39}
$$

The required revision-DLM has width $n+1$. The path sampled below is latent:
the first round stores only fair seed bits, and each second-round output
coordinate recomputes whichever path states it needs.

### The DFA-induced Markov chain

A uniform binary character induces the state kernel

$$
P(q,r)
=
\frac{
\left|
\left\{
a\in\{0,1\}:\delta(q,a)=r
\right\}
\right|
}{2}.
\tag{40}
$$

Every entry belongs to $\{0,1/2,1\}$. The initial state $q_0$ is fixed, so
the chain is already dyadic and Theorem 1 applies with

$$
w_q=1,
\qquad
c=0,
\qquad
s=1.
$$

Consequently, there is a uniform-$AC^0$ map

$$
G_n:\{0,1\}^n\longrightarrow Q^{n+1}
\tag{41}
$$

such that $G_n(Z)$ has exactly the full state-trajectory law of (40) when
$Z\sim U_n$.

### Recovering characters by a product kernel

Fix a positive-probability state path

$$
\gamma=(q_0,q_1,\ldots,q_n).
$$

For its $i$th edge, define the compatible characters

$$
A_i(\gamma)
=
\left\{
a\in\{0,1\}:\delta(q_{i-1},a)=q_i
\right\},
\qquad
c_i(\gamma)=|A_i(\gamma)|\in\{1,2\}.
\tag{42}
$$

Conditioned on $\gamma$, sample the character coordinates independently:

$$
\widehat X_i\mid\gamma
\sim
\operatorname{Unif}(A_i(\gamma)).
\tag{43}
$$

If there is one compatible character, the output is deterministic. If both
characters are compatible, that coordinate uses one fresh fair bit. Thus (43)
is a genuine coordinatewise product kernel.

To verify exactness, fix $x\in\{0,1\}^n$ and let $\gamma(x)$ be its unique
DFA state path. From (40),

$$
\Pr[\Gamma=\gamma(x)]
=
\prod_{i=1}^{n}\frac{c_i(\gamma(x))}{2},
\tag{44}
$$

while (43) gives

$$
\Pr[\widehat X=x\mid\Gamma=\gamma(x)]
=
\prod_{i=1}^{n}\frac1{c_i(\gamma(x))}.
\tag{45}
$$

Multiplication cancels every compatible-set size:

$$
\Pr[\widehat X=x]
=
\prod_{i=1}^{n}
\left(
\frac{c_i(\gamma(x))}{2}
\cdot
\frac1{c_i(\gamma(x))}
\right)
=
2^{-n}.
\tag{46}
$$

Therefore $\widehat X$ is exactly uniform. Since every sampled character is
compatible with the sampled path,

$$
\mathbf 1[q_n\in F]
=
\mathbf 1[\widehat X\in L]
$$

pointwise.

**Theorem 4 (two-round sampling for fixed binary regular languages).** For
every fixed binary regular language $L$, there are constants $d_L,K_L$ such
that, for every $n$, an exact width-$(n+1)$ fair-bit revision-DLM samples
$\mathcal D_{L,n}^{\mathrm{pair}}$ in at most two rounds. Its update circuits
have depth at most $d_L$ and size at most $n^{K_L}$.

The two rounds are:

1. sample $Z\sim U_n$ in the first $n$ coordinates and put a fixed
   placeholder in the label coordinate;
2. each character coordinate recomputes
   $(q_{i-1}(Z),q_i(Z))$ using (41) and applies (43), while the label coordinate
   recomputes $q_n(Z)$ and outputs $\mathbf 1[q_n(Z)\in F]$.

The latent path requires no extra sequence positions. Copying the needed
prefix-state subcircuits across the output coordinates changes polynomial size
but not constant depth.

If the Boolean function $x\mapsto\mathbf 1[x\in L]$ is nonconstant on
$\{0,1\}^n$, one round cannot suffice. From the all-mask state, a one-round
law is a product law. Its first $n$ coordinates must be independent fair bits,
so the final coordinate would be independent of them, contradicting its being
a nonconstant deterministic label. Therefore the minimum is exactly two on
every nonconstant length slice.

## Comparing the four proof levels

The dependency structure is now explicit:

1. $\mathrm{MOD}_3$ uses a direct LSB-first interval permutation and a
   six-bit aperiodic auxiliary transducer.
2. Fixed $\mathrm{MOD}_q$ replaces intervals by a $2q$-bit residue census,
   stochastic order, common quantiles, and rank-matched block permutations.
3. A general path-dyadic Markov chain first needs an arithmetic weak lift to a
   dyadic random-map system; the universal binary aperiodic lift then makes all
   prefix states shallow.
4. A binary regular language uses the Markov trajectory theorem and then a
   stochastic compatible-character product kernel.

The modular constructions have deterministic second rounds; the general
regular-language construction need not. The general theorem subsumes every
fixed $\mathrm{MOD}_q$ as a language-level upper bound, but the explicit
modular constructions remain informative because they exhibit much more
concrete cube permutations.

None of these results says that $\mathrm{MOD}_q$ recognition is in $AC^0$.
The shallow object is a measure-preserving reparameterization of a fair seed,
followed by a shallow readout or product kernel. For the contrasting
recognition lower bound, see
[*Near-perfect average-case MOD_q requires log n / log log n depth for polynomial-size AC circuits*]({{ '/blog/near-perfect-mod-q-ac-depth/' | relative_url }}).

The Markov theorem also retains the following boundaries:

- the chain and its state space are fixed as $n$ grows;
- the target is the complete trajectory from a specified initial distribution;
- constants may depend on the fixed chain or DFA;
- non-dyadic atoms cannot be produced exactly from finitely many fair bits;
- growing automata, growing moduli, approximate sampling, and unbounded
  rejection sampling are not covered.
