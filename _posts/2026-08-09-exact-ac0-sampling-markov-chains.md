---
title: "Exact Sampling of Path-Dyadic Markov Chains in Randomized AC^0"
date: 2026-08-09
updated: 2026-08-10
slug: exact-ac0-sampling-markov-chains
permalink: /blog/exact-ac0-sampling-markov-chains/
tags: [exact sampling, circuit complexity, Markov chains, regular languages]
summary: "A characterization of finite Markov chains whose full trajectories can be sampled exactly in randomized AC^0, with applications to fixed modular predicates and binary regular languages."
---

## Introduction

I study two related sampling problems.

The first problem starts with a fixed binary regular language
$L\subseteq\Sigma^*$, where $\Sigma=\{0,1\}$. Its indicator is
$f_L(x)=\mathbf{1}[x\in L]$. Let $U_n$ be the uniform distribution on
$\{0,1\}^n$, and define

$$
\mathrm{Pair}_{L,n}=(X,f_L(X)),
\qquad
X\sim U_n.
$$

This sampling problem has $n+1$ output bits. The goal is to sample
$\mathrm{Pair}_{L,n}$. I will prove that every fixed binary regular language
has such a randomized-$AC^0$ sampler.

Throughout this note, sampling means exact equality in distribution: every
output has exactly its target probability. Approximate sampling is not
considered unless stated otherwise.

The second problem starts with a fixed finite Markov chain, given by an initial
distribution and a transition matrix. The goal is to sample its complete
trajectory with a randomized-$AC^0$ circuit. The necessary and sufficient
condition is path-dyadicity: every finite trajectory must have dyadic
probability. A dyadic probability has the form $m/2^k$ for some nonnegative
integers $m$ and $k$.

The two problems are closely linked. Let
$\mathcal A=(Q,\{0,1\},\delta,q_0,F)$ be a DFA. A uniform input bit induces the
Markov transition

$$
P(q,r)
=
\frac{\left|\left\{a\in\{0,1\}:\delta(q,a)=r\right\}\right|}{2}.
$$

If $\delta(q,0)$ and $\delta(q,1)$ are distinct, each next state has
probability $1/2$. If they are equal, that next state has probability $1$.
Thus a uniform random word can be viewed as a random walk in its DFA.

A randomized-$AC^0$ sampler is a polynomial-size, constant-depth Boolean
circuit whose random inputs are finitely many independent fair bits. If it uses
$r$ random bits, the probability of each output is an integer divided by
$2^r$, so it is dyadic.

The proof has four parts. I first give a direct construction for
$\mathrm{MOD}_3$ by aperiodicity, and then extend to every fixed
$\mathrm{MOD}_q$. Next, I use state splitting to handle
path-dyadic Markov chains, even when some individual transition probabilities
are not dyadic. The result for regular languages then follows from the Markov
chain theorem.

Sampling is different from recognition. In recognition, the input $x$ is
fixed and the circuit must compute $f_L(x)$. In sampling, the circuit may instead use a cube permutation, which can require less depth. For example, sampling parity needs $O(1)$ depth, while recognizing parity with polynomial-size $AC$ circuits needs $\Theta(\log n/\log\log n)$ depth that is not in $AC^0$.

## Three lemmas about regular-language recognition

These lemmas will be used several times below.

Let $\mathcal A=(Q,\Sigma,\delta,q_0,F)$ be any DFA. Every word
$u\in\Sigma^*$ induces a map on its states,

$$
T_u(q)=\delta^*(q,u).
$$

The set

$$
M_{\mathcal A}=\{T_u:u\in\Sigma^*\}
$$

is the transition monoid of $\mathcal A$. Its transition morphism is
$\eta_{\mathcal A}(u)=T_u$. A stability index is a positive integer $d$ such
that

$$
\eta_{\mathcal A}(\Sigma^d)=\eta_{\mathcal A}(\Sigma^{2d}).
$$

Such a $d$ always exists because $M_{\mathcal A}$ is finite. Fix any stability
index $d$. The stable monoid is

$$
\operatorname{Stab}(\eta_{\mathcal A})
=
\eta_{\mathcal A}((\Sigma^d)^*)
=
\{1\}\cup\eta_{\mathcal A}(\Sigma^d).
$$

It does not depend on the chosen stability index. A finite monoid is
aperiodic if every element $a$ satisfies $a^{k+1}=a^k$ for some $k\ge1$.

**Lemma 1 ($AC^0$ recognition characterization).** Let $\mathcal A$ be the
minimal DFA of a regular language $L$, and let $\eta_{\mathcal A}$ be its
transition morphism. Then $L$ is in $AC^0$ if and only if
$\operatorname{Stab}(\eta_{\mathcal A})$ is aperiodic.

For a minimal DFA, its transition monoid is exactly the syntactic monoid. This
lemma is the
[Barrington, Compton, Straubing, and Thérien characterization](https://doi.org/10.1016/0022-0000(92)90014-A).
The main idea is that non-aperiodic stable behavior can encode nontrivial
modular counting, which $AC^0$ cannot do. If the stable monoid is aperiodic,
its stable pieces are star-free and can be recognized in $AC^0$.

**Lemma 2 (a sufficient test for any DFA).** If the full transition monoid

$$
M_{\mathcal A}=\eta_{\mathcal A}(\Sigma^*)
$$

is aperiodic, then the language recognized by $\mathcal A$ is in $AC^0$.

To see this, minimize $\mathcal A$. The transition monoid of the minimal DFA is
a quotient of $M_{\mathcal A}$. A quotient of an aperiodic monoid is
aperiodic, and every submonoid is also aperiodic. Thus the stable monoid of the
minimal DFA is aperiodic, so Lemma 1 applies.

**Lemma 3 (monotone DFA test).** Suppose the states of a fixed DFA have a total
order $\le$. If every character preserves this order, meaning that

$$
x\le y
\quad\Longrightarrow\quad
\delta(x,c)\le\delta(y,c)
$$

for all states $x,y$ and characters $c\in\Sigma$, then the language of the DFA
is in $AC^0$.

Each character induces an order-preserving map, and a composition of such maps
is still order-preserving. Therefore every word $w\in\Sigma^*$ induces an
order-preserving map $T_w$.

Fix a state $x$ and define $x_i=T_w^i(x)$. Because the order is total, either
$x_1\le x_0$ or $x_1\ge x_0$. In the first case, order preservation gives

$$
x_{i+1}=T_w(x_i)\le T_w(x_{i-1})=x_i,
$$

so the sequence keeps decreasing. In the second case, the same argument shows
that it keeps increasing. Since $Q$ is finite, the sequence must become
constant. Thus, for every $x\in Q$, there is an integer $\ell_x$ such that

$$
T_w^{\ell_x}(x)=T_w^{\ell_x+1}(x).
$$

Let $N_w=\max_{x\in Q}\ell_x$. Then

$$
\eta_{\mathcal A}(w^{N_w})=\eta_{\mathcal A}(w^{N_w+1}).
$$

$M_{\mathcal A}$ is aperiodic since $w$ was arbitrary, and Lemma 2 applies.

## $\mathrm{MOD}_3$ interval construction

The $q=3$ construction maps three consecutive integer intervals to the three
Hamming-weight residue slices modulo $3$.

For a binary word $x$, define

$$
f_3(x)=\mathbf{1}[|x|\equiv0\pmod3].
$$

For $X\sim U_n$, the target distribution is

$$
\mathrm{Pair}_{3,n}=(X,f_3(X)).
$$

**Theorem 4 ($\mathrm{Pair}_{3,n}$ sampling).** For every $n\ge1$, there is
a randomized-$AC^0$ sampler for $\mathrm{Pair}_{3,n}$.

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

To understand this flip bit, split the target residue slice according to its
least significant bit $y_0$. The branch $y_0=0$ has size $N_{r,k-1}$, while
the branch $y_0=1$ has size $N_{r-1,k-1}$. On the input side, the even and odd
integers in $[0,N_{r,k})$ have sizes
$\lceil N_{r,k}/2\rceil$ and $\lfloor N_{r,k}/2\rfloor$. If
$N_{r,k-1}<N_{r-1,k-1}$, the larger target branch is $y_0=1$, so we must swap
the two input branches by setting $y_0=u_0\mathbin{\oplus}1$. This is exactly
the case $e_{r,k}=1$.

The value of $e_{r,k}$ depends only on $r\bmod3$ and $k\bmod6$. The complete
table is

| $k\bmod6$ | $(e_{0,k},e_{1,k},e_{2,k})$ |
| ---: | :---: |
| $0,1$ | $(0,1,0)$ |
| $2,3$ | $(0,0,1)$ |
| $4,5$ | $(1,0,0)$ |

For $r\in\mathbb Z_3$, let $P_{r,n}(u)$ denote the $n$-bit word produced by
the loop below when its initial residue state is $r$. The bits of $u$ are read
from the least significant to the most significant.

The following three intervals partition $[0,2^n)$:

$$
\begin{aligned}
I_{0,n}&=[0,N_{0,n}),\\
I_{1,n}&=[N_{0,n},N_{0,n}+N_{1,n}),\\
I_{2,n}&=[N_{0,n}+N_{1,n},2^n).
\end{aligned}
$$

The complete sampling procedure is:

```text
sample z uniformly from {0, ..., 2^n - 1}
if z < N[0,n]:
    r_0 <- 0
    u <- z
else if z < N[0,n] + N[1,n]:
    r_0 <- 1
    u <- z - N[0,n]
else:
    r_0 <- 2
    u <- z - N[0,n] - N[1,n]
r <- r_0
k <- n mod 6
for i <- 0, ..., n - 1:
    y_i <- u_i XOR e[r, k]
    r   <- r - y_i mod 3
    k   <- k - 1 mod 6
return (y, 1[r_0 = 0])
```

Let

$$
P_n:\{0,1\}^n\longrightarrow\{0,1\}^n
$$

be the map that sends $z$ to the word $y$ produced by the procedure above,
and let $B_n(z)=\mathbf{1}[r_0=0]$ be its label. Then

$$
\boxed{
z\in I_{r,n}
\quad\Longleftrightarrow\quad
|P_n(z)|\equiv r\pmod3.
}
$$

By induction, $P_n$ is bijective, i.e., a cube permutation.

> Why $P_n$ is in $AC^0$

First consider the loop.

First handle at most five bits with a fixed lookup so that the next step starts
at phase $k\equiv0\pmod6$.

Now group the remaining bits into blocks of six. Each block word maps the old
residue state $r\in\mathbb Z_3$ to a new residue state.

1. Directly enumerate the $64$ cases and their corresponding maps.
2. Add the identity map and compose these maps until no new map appears.

The resulting maps, written as the images of $0,1,2$, are

$$
\begin{aligned}
&(0,1,2),\ (0,0,0),\ (1,1,1),\ (2,2,2),\\
&(0,2,2),\ (1,1,2),\ (1,2,2),\ (2,1,1).
\end{aligned}
$$

Every element $a$ satisfies

$$
a^3=a^2.
$$

The block transition monoid is therefore aperiodic. By Lemma 2, $AC^0$ can
decide the residue state $r$ after any number of complete blocks.

Finally, a suffix of fewer than six bits is handled by a fixed lookup. The
comparisons and subtractions involving the fixed thresholds $N_{0,n}$ and
$N_{0,n}+N_{1,n}$ are in $AC^0$. Hence $P_n$ is in $AC^0$.

This is a special feature of $q=3$. The three residue counts differ by at most
$1$, making the binary interval split possible at every recursion level. This
interval construction does not extend to $q\ge4$.

## $\mathrm{MOD}_q$ via common quantiles

The general construction abandons the interval comparator. It uses $2q$-bit
blocks and couples all residue-state transition rows by a common rank.

Fix $q\ge2$. For a binary word $x$, define

$$
f_q(x)=\mathbf{1}[|x|\equiv0\pmod q].
$$

For $X\sim U_n$, let

$$
\mathrm{Pair}_{q,n}=(X,f_q(X)).
$$

**Theorem 5 ($\mathrm{Pair}_{q,n}$ sampling).** For every fixed $q\ge2$ and
every $n\ge1$, there is a randomized-$AC^0$ sampler for
$\mathrm{Pair}_{q,n}$.

### Residue census

Fix the block length

$$
b=2q,
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

First,

$$
\begin{aligned}
w_0-w_1
&=
\binom{2q}{q}-\binom{2q}{q-1}+2-2q\\
&=
\frac{1}{q+1}\binom{2q}{q}+2-2q.
\end{aligned}
$$

The first term is the Catalan number $\operatorname{Cat}_q$. Since

$$
\frac{\operatorname{Cat}_q}{\operatorname{Cat}_{q-1}}
=
\frac{2(2q-1)}{q+1}
\ge2,
$$

we have $\operatorname{Cat}_q\ge2^{q-1}\ge2q-2$ for $q\ge2$. Hence
$w_0\ge w_1$.

For the remaining comparisons, define

$$
\Delta_k=\binom{2q}{k}-\binom{2q}{k-1},
$$

so for $1\le r<m$,

$$
w_r-w_{r+1}=\Delta_{q-r}-\Delta_{r+1}.
$$

Let $L=q-2r-1\ge1$. A direct ratio calculation gives

$$
\frac{\Delta_{q-r}}{\Delta_{r+1}}
=
\frac{(2r+1)(2q-r)}{(q+r+1)(2q-2r-1)}
\prod_{j=1}^{L}
\frac{q+r+j}{r+1+j}.
$$

Keeping only the $j=1$ factor from the product and using that all remaining
factors are at least $1$, we get

$$
\frac{\Delta_{q-r}}{\Delta_{r+1}}
\ge
\frac{(2r+1)(2q-r)}{(r+2)(2q-2r-1)}
>1.
$$

Thus $w_r>w_{r+1}$ for $1\le r<m$.

Hence the block residue census is symmetric and nonincreasing with circular
distance from $0$.

### A stochastic order on residue states

Order $\mathbb Z_q$ by the zigzag chain

$$
0<1<-1<2<-2<\cdots.
$$

If $q=2m$, the last state is $m=-m$ in $\mathbb Z_q$.

Write this chain as $\xi_0<\xi_1<\cdots<\xi_{q-1}$, and let

$$
\mathrm{Pfx}_k=\{\xi_0,\ldots,\xi_k\}
$$

be its $k$-th prefix. These prefixes have two forms:

$$
\mathrm{Pfx}_{2j}=\{-j,-j+1,\ldots,j\},
$$

and

$$
\mathrm{Pfx}_{2j+1}=\{-j,-j+1,\ldots,j+1\}.
$$

From an old residue state $s$, the desired integer mass at target $t$ is

$$
\mu_s(t)=w_{t-s}.
$$

Define its cumulative mass along the chain by

$$
F_{s,\mathrm{Pfx}_k}
=\sum_{t\in\mathrm{Pfx}_k}\mu_s(t)
=\sum_{t\in\mathrm{Pfx}_k}w_{t-s}.
$$

### A $\mathrm{MOD}_3$ example

For $q=3$, $b=6$, $(w_0,w_1,w_2)=(22,21,21)$, and
$(\xi_0,\xi_1,\xi_2)=(0,1,2)$. Each entry is
$(F_{s,\mathrm{Pfx}_k},M_s(\xi_k))$, where $M_s(\xi_k)=\mu_s(\xi_k)=w_{\xi_k-s}$.

| old state $s$ | $\mathrm{Pfx}_0=\{0\}$, $\xi_0=0$ | $\mathrm{Pfx}_1=\{0,1\}$, $\xi_1=1$ | $\mathrm{Pfx}_2=\mathbb Z_3$, $\xi_2=2$ |
| --- | ---: | ---: | ---: |
| $0$ | $(22,22)$ | $(43,21)$ | $(64,21)$ |
| $1$ | $(21,21)$ | $(43,22)$ | $(64,21)$ |
| $2=-1$ | $(21,21)$ | $(42,21)$ | $(64,22)$ |

>Prove $F_{\xi_i,\mathrm{Pfx}_k}\ge F_{\xi_{i+1},\mathrm{Pfx}_k}$

for every adjacent pair of old states and every prefix. The adjacent steps in
the zigzag chain are $r\to-r$ and $-r\to r+1$.

First consider the even prefix $\mathrm{Pfx}_{2j}=\{-j,\ldots,j\}$. Reflection
around $0$ gives

$$
F_{-r,\mathrm{Pfx}_{2j}}=F_{r,\mathrm{Pfx}_{2j}}.
$$

Also, cancellation inside the two sums gives

$$
F_{r,\mathrm{Pfx}_{2j}}-F_{r+1,\mathrm{Pfx}_{2j}}
=
w_{j-r}-w_{-j-r-1}.
$$

For every transition $-r\to r+1$, the valid ranges give

$$
2\max\{j,r\}\le q-1
\implies
|j-r|
\le
\min\{j+r+1,q-j-r-1\},
$$

so radial monotonicity and reflection give

$$
F_{-r,\mathrm{Pfx}_{2j}}
=F_{r,\mathrm{Pfx}_{2j}}
\ge F_{r+1,\mathrm{Pfx}_{2j}}.
$$

Every transition $r\to-r$ gives equality.

Now consider the odd prefix
$\mathrm{Pfx}_{2j+1}=\{-j,\ldots,j+1\}$. Reflection around $1/2$ gives

$$
F_{-r,\mathrm{Pfx}_{2j+1}}=F_{r+1,\mathrm{Pfx}_{2j+1}}.
$$

The endpoint difference is

$$
F_{r,\mathrm{Pfx}_{2j+1}}-F_{r+1,\mathrm{Pfx}_{2j+1}}
=
w_{j+1-r}-w_{-j-r-1}.
$$

To check the inequality, set $J=j+1$. We have $1\le J\le m$. The valid
ranges imply

$$
2\max\{J,r\}\le q \implies |J-r|\le\min\{J+r,q-J-r\},
$$

so radial monotonicity and reflection give

$$
F_{r,\mathrm{Pfx}_{2j+1}}
\ge F_{r+1,\mathrm{Pfx}_{2j+1}}
=F_{-r,\mathrm{Pfx}_{2j+1}}.
$$

Every transition
$-r\to r+1$ gives equality.

Thus, for every prefix and every adjacent pair of old states,

$$
\boxed{
F_{\xi_i,\mathrm{Pfx}_k}\ge F_{\xi_{i+1},\mathrm{Pfx}_k}.
}
$$

By the following proposition 6, theorem5 gets proved.

**Proposition 6 (ordered block-census sampling criterion).** Let

$$
\mathcal A=(Q,\{0,1\},\delta,q_0,Q_{\mathrm{acc}})
$$

be a fixed binary DFA, and let $L=L(\mathcal A)$. Fix a block length $b\ge1$
and a total order

$$
Q=\{\xi_0<\xi_1<\cdots<\xi_{\ell-1}\}.
$$

Let $\Gamma=\{0,1\}^b$. For $s,t\in Q$, define the block-transition census

$$
M_s(t)
=
\left|
\left\{
y\in\Gamma:\delta^*(s,y)=t
\right\}
\right|.
$$

For $\mathrm{Pfx}_k=\{\xi_0,\ldots,\xi_k\}$, set

$$
F_{s,\mathrm{Pfx}_k}
=
\sum_{t\in\mathrm{Pfx}_k}M_s(t).
$$

Assume that, for all $0\le i<\ell-1$ and $0\le k<\ell$,

$$
F_{\xi_i,\mathrm{Pfx}_k}
\ge
F_{\xi_{i+1},\mathrm{Pfx}_k}.
$$

Then, for every $n\ge1$, there is a randomized-$AC^0$ sampler for
$\mathrm{Pair}_{L,n}$.

**Proof.** Let $N=2^b$ and set $F_{s,\mathrm{Pfx}_{-1}}=0$. Order $\Gamma$
lexicographically. For $u\in\Gamma$, define $\tau_u(s)=\xi_k$ when

$$
F_{s,\mathrm{Pfx}_{k-1}}
\le \operatorname{rank}(u)<
F_{s,\mathrm{Pfx}_k}.
$$

Consider adjacent states $s=\xi_i<s'=\xi_{i+1}$. If
$\tau_u(s')=\xi_k$, then

$$
\operatorname{rank}(u)
<F_{s',\mathrm{Pfx}_k}
\le F_{s,\mathrm{Pfx}_k}.
$$

Therefore $\tau_u(s)\le\xi_k=\tau_u(s')$. Thus every $\tau_u$ preserves the
state order.

If $t=\xi_k$, then the two lists used in the rank matching below have the
same length:

$$
\left|\left\{u\in\Gamma:\tau_u(s)=t\right\}\right|
=F_{s,\mathrm{Pfx}_k}-F_{s,\mathrm{Pfx}_{k-1}}
=M_s(t)
=\left|\left\{y\in\Gamma:\delta^*(s,y)=t\right\}\right|.
$$

Since the two sets have equal cardinality, we obtain block cube permutations
$\pi_s:\Gamma\to\Gamma$ such that

$$
\delta^*(s,\pi_s(u))=\tau_u(s).
$$

Each $\pi_s$ is hard-coded into the circuit as a lookup table.

The sampler is:

```text
procedure SamplePair(z)
    input:  z in {0,1}^n
    write n = b*m + r with 0 <= r < b
    parse z as (u[1], ..., u[m], c), with u[i] in Gamma and c in {0,1}^r
    s[0] <- q_0
    for i <- 1, ..., m do
        y[i] <- pi_{s[i-1]}(u[i])
        s[i] <- tau_{u[i]}(s[i-1])
    end for
    P_n(z) <- (y[1], ..., y[m], c)
    C_n(z) <- 1 if delta^*(s[m], c) is in Q_acc; otherwise 0
    return (P_n(z), C_n(z))
end procedure
```

By Lemma 3, all $s_i$ and the output of each block can be computed in parallel
in $AC^0$, so the sampling procedure is in $AC^0$.

## Why the modular constructions are not yet the general proof

The two modular constructions above use the same strong interface: an explicit
cube permutation $P_{q,n}$ keeps the word uniform and makes its label shallow.
This interface is useful, but it is stronger than what a general finite
automaton needs. For a general DFA, the sampler may use extra independent fair
bits after it has sampled a state path.

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

A fair-bit randomized-$AC^0$ trajectory sampler is a family

$$
S_n:\{0,1\}^{r_n}\longrightarrow Q^{n+1}
$$

such that $S_n(U_{r_n})$ has exactly the trajectory law (1). The finite state
set $Q$ uses a fixed constant-length encoding, and depth and size refer to the
whole multi-output circuit.

**Theorem 7 (path-dyadic trajectory characterization).** For every fixed
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
   every horizon $n$ has a fair-bit randomized-$AC^0$ trajectory
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

**Proposition 8 (aperiodic lift implies shallow trajectories).** If such a
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

**Theorem 9 (universal aperiodic lift).** Every fixed deterministic binary
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
many phase and partial-symbol states. Theorem 9 and Proposition 8 then give,
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
implication in Theorem 7.

## Binary regular languages

Now fix a binary DFA that does not grow with the input length,

$$
\mathcal A=(Q,\{0,1\},\delta,q_0,F),
$$

and let $L$ be its language. For $X\sim U_n$, the target input-output pair
distribution is

$$
\mathrm{Pair}_{L,n}
=
(X,\mathbf 1[X\in L]).
\tag{39}
$$

The state path used below is internal to the circuit. It is not part of the
output. Each output coordinate computes only the path states that it needs.

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
the chain is already dyadic and Theorem 7 applies with

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

### Recovering characters from the path

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
characters are compatible, that coordinate uses one fresh fair bit. The
characters are independent after the path is fixed.

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

**Theorem 10 (sampling for fixed binary regular languages).** For every
fixed binary regular language $L$, there are constants $d_L,K_L$ such that,
for every $n$, a fair-bit randomized-$AC^0$ circuit samples
$\mathrm{Pair}_{L,n}$. Its depth is at most $d_L$ and its size is
$O(n^{K_L})$.

To build the circuit, take independent fair seeds $Z,R\in\{0,1\}^n$. Use
$G_n(Z)$ from (41) to obtain the internal path. Coordinate $i$ uses
$(q_{i-1}(Z),q_i(Z))$ and the single bit $R_i$ to implement (43). The label
coordinate outputs $\mathbf 1[q_n(Z)\in F]$.

The path uses only internal wires. Copying the required prefix-state circuits
for all output coordinates increases the size by a polynomial factor but does
not change the constant-depth bound.

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
   conditionally independent compatible-character sampling step.

The modular constructions use only the $n$ seed bits and an explicit cube
permutation. The general regular-language construction may also use fresh fair
bits in the compatible-character step. The general theorem includes every
fixed $\mathrm{MOD}_q$ as a language-level result, but the direct modular
constructions are still useful because they give concrete cube permutations.

None of these results says that $\mathrm{MOD}_q$ recognition is in $AC^0$.
The shallow object is a measure-preserving reparameterization of a fair seed,
followed by a shallow readout or independent conditional sampling. For the
contrasting recognition lower bound, see
[*Near-perfect average-case MOD_q requires log n / log log n depth for polynomial-size AC circuits*]({{ '/blog/near-perfect-mod-q-ac-depth/' | relative_url }}).

The Markov theorem also retains the following boundaries:

- the chain and its state space are fixed as $n$ grows;
- the target is the complete trajectory from a specified initial distribution;
- constants may depend on the fixed chain or DFA;
- non-dyadic atoms cannot be produced exactly from finitely many fair bits;
- growing automata, growing moduli, approximate sampling, and unbounded
  rejection sampling are not covered.
