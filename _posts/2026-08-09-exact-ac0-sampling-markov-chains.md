---
title: "Exact Sampling of Path-Dyadic Markov Chains in Randomized AC^0"
date: 2026-08-09
updated: 2026-08-12
slug: exact-ac0-sampling-markov-chains
permalink: /blog/exact-ac0-sampling-markov-chains/
tags: [exact sampling, circuit complexity, Markov chains, regular languages]
summary: "A characterization of finite Markov chains whose full trajectories can be sampled exactly in randomized AC^0, with applications to fixed modular predicates and binary regular languages."
---

## Introduction

I study two related sampling problems.

Throughout this note, sampling means exact equality in distribution: every
output has exactly its target probability. Approximate sampling is not
considered.

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

A randomized-$AC^0$ sampler is a Boolean circuit of polynomial size and
constant depth in which each gate is either an AND gate (with unbounded fan-in)
or a NOT gate. The circuit receives finitely many independent fair bits as
inputs. If the circuit uses $r$ random bits, then the probability of each output
is an integer divided by $2^r$, so it is dyadic.

The proof has four parts. I first give a direct construction for
$\mathrm{MOD}_3$ by aperiodicity, and then extend to every fixed
$\mathrm{MOD}_q$. Next, I use state splitting to handle
path-dyadic Markov chains, even when some individual transition probabilities
are not dyadic. The result for regular languages then follows from the Markov
chain theorem.

Sampling is different from recognition. In recognition, the input $x$ is
fixed and the circuit must compute $f_L(x)$. In sampling, the circuit may
instead use a cube permutation, which can require less depth. For example,
sampling parity needs $O(1)$ depth, whereas polynomial-size $AC$ circuits for
recognizing parity require $\Theta(\log n/\log\log n)$ depth and thus fall
outside $AC^0$.

## Three lemmas about regular-language recognition

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

Since $M_{\mathcal A}$ is finite, the sets
$\eta_{\mathcal A}(\Sigma^j)$ take only finitely many values. Hence there are
$d_0,\ell\ge1$ such that
$\eta_{\mathcal A}(\Sigma^{d_0})=\eta_{\mathcal A}(\Sigma^{d_0+\ell})$.
Multiplying by
$\eta_{\mathcal A}(\Sigma^k)$ gives
$\eta_{\mathcal A}(\Sigma^{d_0+k})=\eta_{\mathcal A}(\Sigma^{d_0+\ell+k})$
for every $k\ge0$. Take
$d=\lceil d_0/\ell\rceil\ell$. Since $d\ge d_0$ and $\ell\mid d$,

$$
\eta_{\mathcal A}(\Sigma^d)
=\eta_{\mathcal A}(\Sigma^{d+\ell})
=\cdots
=\eta_{\mathcal A}(\Sigma^{2d}).
$$

Thus the constructed $d$ is a stability index, so one exists. We henceforth
take $d$ to be the smallest stability index. The stable monoid is

$$
\operatorname{Stab}(\eta_{\mathcal A})
=
\eta_{\mathcal A}((\Sigma^d)^*)
=
\{1\}\cup\eta_{\mathcal A}(\Sigma^d).
$$

A finite monoid is aperiodic if every element $a$ satisfies $a^{k+1}=a^k$ for
some $k\ge1$.

Here and below, a nontrivial cycle means a directed cycle of length at least
$2$.

**Cycle criterion.** Let $g:H\to H$ be a self-map of a finite set. Then
$g^k=g^{k+1}$ for some $k\ge1$ if and only if $g$ has no nontrivial cycle.
Consequently, a finite transformation monoid is aperiodic if and only if none
of its elements has a nontrivial cycle.

**Proof.** If $g$ has a nontrivial cycle, then $g^m\ne g^{m+1}$ for every
$m\ge1$. Conversely, if every cycle of $g$ is a fixed point, then every orbit
reaches a fixed point within $|H|$ steps, so
$g^{|H|}=g^{|H|+1}$. $\square$

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

**Proof.** To see this, minimize $\mathcal A$. The transition monoid of the
minimal DFA is a quotient of $M_{\mathcal A}$. A quotient of an aperiodic
monoid is aperiodic, and every submonoid is also aperiodic. Thus the stable
monoid of the minimal DFA is aperiodic, so Lemma 1 applies. $\square$

**Lemma 3 (monotone DFA test).** Suppose the states of a fixed DFA have a total
order $\le$. If every character preserves this order, meaning that

$$
x\le y
\quad\Longrightarrow\quad
\delta(x,c)\le\delta(y,c)
$$

for all states $x,y$ and characters $c\in\Sigma$, then the language of the DFA
is in $AC^0$.

**Proof.** Each character induces an order-preserving map, and a composition
of such maps is still order-preserving. Therefore every word $w\in\Sigma^*$
induces an order-preserving map $T_w$.

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
T_w^{N_w}=T_w^{N_w+1}.
$$

$M_{\mathcal A}$ is aperiodic since $w$ was arbitrary, and Lemma 2 applies. $\square$

## $\mathrm{MOD}_3$ interval construction

For a binary word $x$, define

$$
f_3(x)=\mathbf{1}[|x|\equiv0\pmod3].
$$

For $X\sim U_n$, the target distribution is

$$
\mathrm{Pair}_{3,n}=(X,f_3(X)).
$$

**Theorem 4 ($\mathrm{Pair}_{3,n}$ sampling).** There is
a randomized-$AC^0$ sampler for $\mathrm{Pair}_{3,n}$.

**Proof.** For $r\in\mathbb Z_3$ and $k\ge0$, define the residue-slice counts

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
least significant bit $y_0$. On the output side, the branch $y_0=0$ has size
$N_{r,k-1}$, while the branch $y_0=1$ has size $N_{r-1,k-1}$. On the input
side, the even and odd integers in $[0,N_{r,k})$ have sizes
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

<!-- For $r\in\mathbb Z_3$, let $P_{r,n}(u)$ denote the $n$-bit word produced by
the loop below when its initial residue state is $r$. The bits of $u$ are read
from the least significant to the most significant. -->

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

be the map that sends $z$ to the word $y$ produced by the procedure
above. Then

$$
\boxed{
z\in I_{r,n}
\quad\Longleftrightarrow\quad
|P_n(z)|\equiv r\pmod3,
}
$$

where

$$
\begin{aligned}
I_{0,n}&=[0,N_{0,n}),\\
I_{1,n}&=[N_{0,n},N_{0,n}+N_{1,n}),\\
I_{2,n}&=[N_{0,n}+N_{1,n},2^n).
\end{aligned}
$$

By induction, $P_n$ is bijective, i.e., a cube permutation.

> Why $P_n$ is in randomized-$AC^0$

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
$N_{0,n}+N_{1,n}$ are in $AC^0$. Hence $P_n$ is in randomized-$AC^0$. $\square$

This is a special feature of $q=3$. The three residue counts differ by at most
$1$, making the binary interval split possible at every recursion level. This
interval construction does not extend to $q\ge4$.

## $\mathrm{MOD}_q$ via common quantiles

The general construction abandons the interval comparator. Instead, it uses
$2q$-bit blocks and a shared rank to couple the transition distributions from
every residue state.

Fix $q\ge1$. For a binary word $x$, define

$$
f_q(x)=\mathbf{1}[|x|\equiv0\pmod q].
$$

For $X\sim U_n$, let

$$
\mathrm{Pair}_{q,n}=(X,f_q(X)).
$$

**Theorem 5 ($\mathrm{Pair}_{q,n}$ sampling).** For every fixed $q\ge1$,
there is a randomized-$AC^0$ sampler for $\mathrm{Pair}_{q,n}$.

**Proof.**

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

From an old residue state $s$, define the block-transition census at target
$t$ by

$$
M_s(t)=w_{t-s}.
$$

Define its cumulative census along the chain by

$$
F_{s,\mathrm{Pfx}_k}
=\sum_{t\in\mathrm{Pfx}_k}M_s(t)
=\sum_{t\in\mathrm{Pfx}_k}w_{t-s}.
$$

### A $\mathrm{MOD}_3$ example

For $q=3$, $b=6$, $(w_0,w_1,w_2)=(22,21,21)$, and
$(\xi_0,\xi_1,\xi_2)=(0,1,2)$. Each entry is
$(F_{s,\mathrm{Pfx}_k},M_s(\xi_k))$, where
$M_s(\xi_k)=w_{\xi_k-s}$.

| old state $s$ | $\mathrm{Pfx}_0=\{0\}$, $\xi_0=0$ | $\mathrm{Pfx}_1=\{0,1\}$, $\xi_1=1$ | $\mathrm{Pfx}_2=\mathbb Z_3$, $\xi_2=2$ |
| --- | ---: | ---: | ---: |
| $0$ | $(22,22)$ | $(43,21)$ | $(64,21)$ |
| $1$ | $(21,21)$ | $(43,22)$ | $(64,21)$ |
| $2=-1$ | $(21,21)$ | $(42,21)$ | $(64,22)$ |

We now prove that, for every adjacent pair of old states and every prefix,

$$
F_{\xi_i,\mathrm{Pfx}_k}\ge F_{\xi_{i+1},\mathrm{Pfx}_k}.
$$

The adjacent steps in the zigzag chain are $r\to-r$ and $-r\to r+1$.

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

The prefix inequalities above verify the hypotheses of Proposition 6 for the
residue DFA, so Theorem 5 follows. $\square$

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

Then there is a randomized-$AC^0$ sampler for
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

Since the two sets have equal cardinality, we obtain block-cube permutations
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

By Lemma 3, the state reached after any block prefix is computable in $AC^0$.
Compute all these states in parallel; each output block is then a fixed lookup.
Thus the sampling procedure is in $AC^0$. $\square$

## A three-state obstruction to original block aperiodicity

The block-aperiodicity part of Proposition 6 is already too strong if it must
hold on the original DFA states.

Let $Q=\{0,1,2\}$, start state $0$, accepting set $\{0\}$, and transitions
$0\mapsto0,2$, $1\mapsto0,0$, and $2\mapsto1,1$, where each pair lists the
images under symbols $0$ and $1$.

The one-step transition-count matrix is

$$
T=
\begin{pmatrix}
1&0&1\\
2&0&0\\
0&2&0
\end{pmatrix}.
$$

The symbol $1$ acts as the three-cycle $0\to2\to1\to0$. An original-state
block-aperiodic proof would require, for some block length $b$, maps
$\tau_u:Q\to Q$ indexed by $u\in\{0,1\}^b$ such that their census is $T^b$:

$$
\left|\{u:\tau_u(s)=t\}\right|=T^b(s,t).
$$

The maps $\tau_u$ would also need to generate an aperiodic transformation
monoid. That cannot happen: the characteristic polynomial of $T$ is

$$
\chi_T(\lambda)=(\lambda-2)(\lambda^2+\lambda+2)
$$

and its two remaining eigenvalues are

$$
\lambda_\pm=\frac{-1\pm i\sqrt7}{2},
$$

so $T^b$ has a non-real eigenvalue for every $b\ge1$. A finite enumeration of
the $27$ transformations on $Q$ shows that every census generated by an
aperiodic monoid on these three states has real spectrum, so it cannot realize
$T^b$.

For more details, see
[Appendix A](#appendix-a-spectral-certificate-for-the-three-state-obstruction).

## Markov trajectories

Fix a finite Markov chain

$$
\mathcal M=(Q,\mu,P),
$$

where $\mu$ is the initial distribution on $Q$ and $P$ is the transition
matrix.

For a length $n$, a trajectory
$\gamma=(x_0,\ldots,x_n)\in Q^{n+1}$ has probability

$$
p_{\mathcal M}(\gamma)
=
\mu(x_0)\prod_{i=1}^{n}P(x_{i-1},x_i).
\tag{1}
$$

Write $\operatorname{Path}_n(\mathcal M)$ for the distribution on $Q^{n+1}$
defined by

$$
\Pr_{\gamma\sim \operatorname{Path}_n(\mathcal M)}
\bigl[\gamma=(x_0,\ldots,x_n)\bigr]
=
p_{\mathcal M}(x_0,\ldots,x_n).
\tag{2}
$$

Let $\mathbb D_{\ge 0}$ be the set of nonnegative dyadic values. Call
$\mathcal M$ **transition-dyadic** when

$$
\mu(q),P(q,r)\in\mathbb D_{\ge 0}
\qquad
\text{for all }q,r\in Q.
\tag{3}
$$

**Lemma 7 (finite-state convergence).** Let $K$ be an irreducible and aperiodic
transition matrix on a finite state space. Then $K$ has a unique stationary
distribution $\pi$, with $\pi(x)>0$ for every state $x$. For every
$\varepsilon>0$, there is $m_\varepsilon$ such that, for every initial
distribution $\lambda$ and every $m\ge m_\varepsilon$,

$$
\left\|\lambda K^m-\pi\right\|_{\mathrm{TV}}<\varepsilon.
$$

See Levin and Peres, with contributions by Wilmer,
[*Markov Chains and Mixing Times*, Chapter 1 and Theorem 4.9](https://pages.uoregon.edu/dlevin/MARKOV/mcmt2e.pdf).

**Theorem 8 (transition-dyadic trajectories).** Every
transition-dyadic Markov chain has a randomized-$AC^0$ sampler for
$\operatorname{Path}_n(\mathcal M)$. It uses at most $v+sn$ fair bits,
where $v$ depends on $\mu$ and $s$ depends on $P$.

**Proof.** First consider only the directed support of $P$. Let

$$
P_{\mathrm{bool}}(q,t)=\mathbf 1[P(q,t)>0],
$$

with powers taken over the Boolean semiring. By the same finite-periodicity
argument as for stability indices, choose $a\ge1$ such that
$P_{\mathrm{bool}}^a=P_{\mathrm{bool}}^{2a}$. Set
$P_{\mathrm{aperiodic}}:=P_{\mathrm{bool}}^a$; this Boolean matrix is idempotent.

Now choose $s\ge1$ such that every $P(q,t)$ is an integer multiple of
$2^{-s}$, and set

$$
P_N=2^sP,
\qquad
\Gamma_s=\{0,1\}^s.
$$

Thus $P_N$ is an integer matrix whose rows sum to $2^s$. For each $q$, assign
exactly $P_N(q,t)$ characters of $\Gamma_s$ to the
transition $q\to t$. This defines

$$
\delta:Q\times\Gamma_s\longrightarrow Q.
$$

For a positive integer $c$, use blocks in
$\Gamma_s^{ac}\cong\{0,1\}^{sac}$. For a block word
$w=w_1\cdots w_{ac}\in\Gamma_s^{ac}$, define

$$
\delta(q,w)
=
\delta(\cdots\delta(\delta(q,w_1),w_2)\cdots,w_{ac}).
\tag{4}
$$

$$
\left|
\left\{
w\in\Gamma_s^{ac}:\delta(q,w)=t
\right\}
\right|
=
P_N^{ac}(q,t)
=
2^{sac}P^{ac}(q,t).
$$

Its Boolean support is

$$
P_{\mathrm{bool}}^{ac}
=
P_{\mathrm{aperiodic}}^c
=
P_{\mathrm{aperiodic}},
$$

so its SCCs do not depend on $c$.

Let $R$ be a terminal SCC of $P_{\mathrm{aperiodic}}$. Write
$R=\{t_1,\ldots,t_k\}$. Split each state into two hidden copies, set

$$
H_R=\{t_1^-,\ldots,t_k^-,t_1^+,\ldots,t_k^+\},
$$

and order them as

$$
t_1^-<\cdots<t_k^-<t_1^+<\cdots<t_k^+.
$$

Let $\phi(t_i^-)=\phi(t_i^+)=t_i$ and list the hidden copies as
$h_1<\cdots<h_{2k}$. A block transfer of hidden states is encoded by a
nonnegative integer census

$$
N_{\mathrm{hidden},c}:H_R\times H_R\longrightarrow\mathbb Z_{\ge0}.
$$

It must first satisfy exact projection:

$$
\sum_{\substack{h'\in H_R\\\phi(h')=t}}
N_{\mathrm{hidden},c}(h,h')
=
P_N^{ac}(\phi(h),t)
\qquad(h\in H_R,\ t\in R).
$$

Summing over $t\in R$ gives a row sum of $2^{sac}$.

The key idea is to extend the order-preserving structure of Proposition 6, so
we also require

$$
\sum_{\substack{\widetilde h\in H_R\\\widetilde h\le x}}
N_{\mathrm{hidden},c}(h_j,\widetilde h)
\ge
\sum_{\substack{\widetilde h\in H_R\\\widetilde h\le x}}
N_{\mathrm{hidden},c}(h_{j+1},\widetilde h)
$$

for every $1\le j<2k$ and $x\in H_R$.

Since $P_{\mathrm{aperiodic}}|_R$ is the all-one matrix, Lemma 7 applied to
$P^a|_R$ gives a stationary distribution $\pi_R$ and, for $1\le j\le2k$ and
$1\le i\le k$,

$$
2^{-sac}P_N^{ac}(\phi(h_j),t_i)
=
P^{ac}(\phi(h_j),t_i)
\longrightarrow
\pi_R(t_i)
\qquad(c\longrightarrow\infty).
$$

The construction is:

$$
\begin{aligned}
N_{\mathrm{hidden},c}(h_j,t_i^-)
&=
\left\lfloor
\frac{2k+1-j}{2k+1}P_N^{ac}(\phi(h_j),t_i)
\right\rfloor,\\
N_{\mathrm{hidden},c}(h_j,t_i^+)
&=
\left\lceil
\frac{j}{2k+1}P_N^{ac}(\phi(h_j),t_i)
\right\rceil.
\end{aligned}
$$

These formulas apply for $1\le j\le2k$ and $1\le i\le k$. The two integers sum
exactly to $P_N^{ac}(\phi(h_j),t_i)$, so exact projection holds.

The rounding error in each integer count is at most $1$. Therefore, for
$1\le j<2k$ and $1\le r\le k$,

$$
\begin{aligned}
&2^{-sac}
\sum_{i=1}^{r}
\left(
N_{\mathrm{hidden},c}(h_j,t_i^-)
-
N_{\mathrm{hidden},c}(h_{j+1},t_i^-)
\right)\\
&\qquad=
\sum_{i=1}^{r}
\left(
\frac{2k+1-j}{2k+1}P^{ac}(\phi(h_j),t_i)
-
\frac{2k-j}{2k+1}P^{ac}(\phi(h_{j+1}),t_i)
\right)
+O\left(r2^{-sac}\right)\\
&\qquad\longrightarrow
\frac{1}{2k+1}\sum_{i=1}^{r}\pi_R(t_i)>0.
\end{aligned}
$$

For $1\le j<2k$ and $1\le r<k$, exact row sums similarly give

$$
\begin{aligned}
&2^{-sac}
\sum_{\substack{\widetilde h\in H_R\\\widetilde h\le t_r^+}}
\left(
N_{\mathrm{hidden},c}(h_j,\widetilde h)
-
N_{\mathrm{hidden},c}(h_{j+1},\widetilde h)
\right)\\
&\qquad=
2^{-sac}
\sum_{i=r+1}^{k}
\left(
N_{\mathrm{hidden},c}(h_{j+1},t_i^+)
-
N_{\mathrm{hidden},c}(h_j,t_i^+)
\right)\\
&\qquad=
\sum_{i=r+1}^{k}
\left(
\frac{j+1}{2k+1}P^{ac}(\phi(h_{j+1}),t_i)
-
\frac{j}{2k+1}P^{ac}(\phi(h_j),t_i)
\right)
+O\left((k-r)2^{-sac}\right)\\
&\qquad\longrightarrow
\frac{1}{2k+1}\sum_{i=r+1}^{k}\pi_R(t_i)>0.
\end{aligned}
$$

All prefix-sum differences are positive, and there are only finitely many
choices of $j$ and $r$. Hence there is $c_R$ such that every ordered-cut
inequality holds for all $c\ge c_R$. There are only finitely many terminal
SCCs, so one common $c\ge\max_R c_R$ works for all of them.

For $u\in\Gamma_s^{ac}$, let $\tau_u(h)$ be constructed as in Proposition 6,
so $\tau_u$ is order-preserving on each split terminal SCC. Consequently,
every composition of these maps is also order-preserving there and has no
nontrivial cycle.

For $h$ in a terminal SCC and $t\in Q$, the sets

$$
D_{h,t}
=
\left\{
u\in\Gamma_s^{ac}:\phi(\tau_u(h))=t
\right\}
$$

and

$$
W_{h,t}
=
\left\{
w\in\Gamma_s^{ac}:\delta(\phi(h),w)=t
\right\}
$$

have the same cardinality. Match them for every $t$. The union of these
matches is a block-cube permutation

$$
\pi_h:\Gamma_s^{ac}\longrightarrow\Gamma_s^{ac}
$$

such that

$$
\delta(\phi(h),\pi_h(u))=\phi(\tau_u(h)).
\tag{5}
$$

We now rule out nontrivial cycles using the cycle criterion. Every hidden
transition used above projects to an edge of $P_{\mathrm{aperiodic}}$. The
condensation graph of
$P_{\mathrm{aperiodic}}$ is acyclic, so every map stays in its current SCC or
moves downstream. Therefore any nontrivial cycle of a composition of seed maps
must lie entirely in one SCC.

It remains to prevent such nontrivial cycles inside transient SCCs. Let $C$ be
a transient SCC and keep only one hidden copy $h_q$ of each $q\in C$, with
$\phi(h_q)=q$. Since $C$ is transient for $P^a$,

$$
\sum_{q\in C}P^{ac}(q,C)\longrightarrow0.
$$

Increase $c$ further, if necessary, so that the terminal CDF order still holds
and

$$
\sum_{q\in C}P^{ac}(q,C)<1
$$

for every transient SCC $C$. Equivalently,

$$
\sum_{q\in C}\sum_{t\in C}P_N^{ac}(q,t)<2^{sac}.
$$

This allows us to assign a different seed to every internal transition
$h_q\to h_t$, with $q,t\in C$. Thus each seed induces at most one transition
inside $C$, and any composition does as well. The corresponding block-cube
permutations are constructed in the same way.

By the cycle criterion, the seed-generated monoid is aperiodic.

Choose $v\ge0$ such that every $\mu(q)$ is an integer multiple of
$2^{-v}$, and fix a lookup $g:\{0,1\}^{v}\to Q$ whose output has law
$\mu$. Also fix one hidden copy $\iota(q)\in\phi^{-1}(q)$ for every $q$. The
complete sampler is:

```text
procedure SamplePath(st, z)
    input:  st in {0,1}^v and z in {0,1}^{sn}
    write n = ac*m + r with 0 <= r < ac
    parse z as (u[1], ..., u[m], e[1], ..., e[r]),
               with u[i] in Gamma_s^{ac} and e[j] in Gamma_s

    x[0] <- g(st)          // sample the initial visible state from mu
    h[0] <- iota(x[0])     // choose its fixed hidden copy

    for i <- 1, ..., m do
        y[i] <- pi_{h[i-1]}(u[i])
        h[i] <- tau_{u[i]}(h[i-1])
        parse y[i] as (y[i,1], ..., y[i,ac])
        for j <- 1, ..., ac do
            x[(i-1)ac+j] <- delta(x[(i-1)ac+j-1], y[i,j])
        end for
    end for

    for j <- 1, ..., r do
        x[mac+j] <- delta(x[mac+j-1], e[j])
    end for
    return (x[0], ..., x[n])
end procedure
```

By Lemma 2, the hidden state reached after any block prefix is computable in
$AC^0$. Compute all block-prefix states in parallel; the transformed blocks,
their constant-length internal paths, and the final remainder are fixed
lookups. Thus the sampler is randomized-$AC^0$. $\square$

## Path-dyadic Markov chains

Transition-dyadicity is sufficient but not necessary. For example, on states
$\{a,b,c\}$, let

$$
\mu=\left(\frac34,\frac14,0\right),
\qquad
P=
\begin{pmatrix}
0&\frac13&\frac23\\
0&1&0\\
0&0&1
\end{pmatrix}.
$$

The transitions $1/3$ and $2/3$ are not dyadic, but for every $n\ge1$ the
only positive trajectory atoms have probabilities

$$
\frac34\cdot\frac13=\frac14,
\qquad
\frac34\cdot\frac23=\frac12,
\qquad
\frac14.
$$

Thus the chain is path-dyadic. In general, call $\mathcal M$ **path-dyadic**
from $\mu$ when every trajectory atom is dyadic:

$$
p_{\mathcal M}(\gamma)\in\mathbb D_{\ge 0}
\qquad
\text{for every }n\ge 0\text{ and }\gamma\in Q^{n+1}.
\tag{6}
$$

**Theorem 9 (dyadic projection).** Every fixed path-dyadic Markov chain is the
coordinatewise projection of a fixed transition-dyadic Markov chain. More
precisely, there is a finite chain
$\widetilde{\mathcal M}=(\widetilde Q,\widetilde\mu,\widetilde P)$ and a map
$\phi:\widetilde Q\to Q$ with the following property. If
$(\widetilde X_i)_{i\ge0}$ is the Markov chain with initial distribution
$\widetilde\mu$ and transition matrix $\widetilde P$, then, for every $n\ge0$
and every $(x_0,\ldots,x_n)\in Q^{n+1}$,

$$
\Pr\!\left[
\phi(\widetilde X_0)=x_0,\ldots,\phi(\widetilde X_n)=x_n
\right]
=
p_{\mathcal M}(x_0,\ldots,x_n)
=
\mu(x_0)\prod_{i=1}^{n}P(x_{i-1},x_i).
$$

**Proof.** Assume every state is reachable with positive probability from
$\mu$. Otherwise, discard the unreachable states; this does not change the
trajectory law.

We first construct positive integer weights $(w_r)_{r\in Q}$ satisfying

$$
\frac{\mu(q)}{w_q}\in\mathbb D_{\ge 0},
\qquad
\frac{w_qP(q,r)}{w_r}\in\mathbb D_{\ge 0}.
\tag{7}
$$

Indeed, a positive edge satisfies
$P(q,r)=p_{\mathcal M}(\gamma r)/p_{\mathcal M}(\gamma)$ for any positive
trajectory $\gamma$ ending at $q$, so every positive transition is rational.
Fix an odd prime $p$. For a positive rational $a/b$ in lowest terms, define
$v_p(a/b)$ as the exponent of $p$ in $a$ minus its exponent in $b$. Let

$$
\Gamma(r)
=
\left\{
\gamma=(x_0,\ldots,x_n):
n\ge0,\ x_n=r,\ p_{\mathcal M}(\gamma)>0
\right\}
$$

be the set of positive-probability finite trajectories ending at $r$, and
define

$$
0\leq\alpha_r^p
=
\min_{\gamma\in\Gamma(r)}
v_p\!\left(p_{\mathcal M}(\gamma)\right).
$$

Equivalently, add a source $*$ with an edge $*\to q$ of weight $v_p(\mu(q))$
whenever $\mu(q)>0$, and give each positive edge $q\to r$ weight
$v_p(P(q,r))$. Then $\alpha_r^p$ is the shortest-path distance from $*$ to
$r$. Path-dyadicity rules out negative cycles and makes this distance
nonnegative, so the minimum is attained.

If $P(q,r)>0$, append the edge $q\to r$ to a trajectory attaining
$\alpha_q^p$. This gives

$$
\alpha_r^p
\le
\alpha_q^p+v_p(P(q,r)).
$$

If $\mu(r)>0$, the length-zero trajectory $(r)$ similarly gives

$$
\alpha_r^p\le v_p(\mu(r)).
$$

Now set

$$
w_r
=
\prod_{p\text{ odd prime}}p^{\alpha_r^p}.
$$

This product is finite because the finitely many nonzero entries of $\mu$ and
$P$ involve only finitely many odd primes.

For every odd prime $p$, the two preceding inequalities give

$$
v_p\!\left(\frac{\mu(r)}{w_r}\right)
=
v_p(\mu(r))-\alpha_r^p
\ge0
$$

when $\mu(r)>0$, and

$$
v_p\!\left(\frac{w_qP(q,r)}{w_r}\right)
=
\alpha_q^p+v_p(P(q,r))-\alpha_r^p
\ge0
$$

when $P(q,r)>0$. A positive rational is dyadic exactly when its valuation at
every odd prime is nonnegative; zero entries are dyadic as well. Thus the
weights satisfy (7).

Split each state into a fiber

$$
F_q=\{(q,1),\ldots,(q,w_q)\},
\qquad
\widetilde Q=\bigsqcup_{q\in Q}F_q,
$$

and let $\phi(q,j)=q$. Choose $s$ so that

$$
m_{q,r}
=
2^s\frac{w_qP(q,r)}{w_r}
$$

is an integer for every $q,r$. For each $q$, choose an integer matrix
$C^{(q)}$ with rows indexed by $F_q$ and columns by $\widetilde Q$, such that
every row sums to $2^s$ and every column in $F_r$ sums to $m_{q,r}$. Such a
matrix exists because both total sums equal $2^sw_q$.

For $h\in F_q$, define

$$
\widetilde\mu(h)=\frac{\mu(q)}{w_q},
\qquad
\widetilde P(h,h')=\frac{C^{(q)}(h,h')}{2^s}.
\tag{8}
$$

Both are dyadic. We prove by induction on $n$ that, for every positive
trajectory $\gamma=(x_0,\ldots,x_n)$ and every $h\in F_{x_n}$,

$$
\Pr\!\left[
\phi(\widetilde X_0)=x_0,\ldots,\phi(\widetilde X_{n-1})=x_{n-1},
\ \widetilde X_n=h
\right]
=
\frac{p_{\mathcal M}(\gamma)}{w_{x_n}}.
\tag{9}
$$

For $n=0$, this is the definition of $\widetilde\mu$. Suppose it holds for a
trajectory $\gamma$ ending at $q$. For every positive extension $\gamma r$ and
every $h'\in F_r$, the column-sum condition on $C^{(q)}$ gives

$$
\begin{aligned}
&\sum_{h\in F_q}
\frac{p_{\mathcal M}(\gamma)}{w_q}\widetilde P(h,h')
\\
&\qquad=
\frac{p_{\mathcal M}(\gamma)}{w_q}
\sum_{h\in F_q}\frac{C^{(q)}(h,h')}{2^s}
\\
&\qquad=
\frac{p_{\mathcal M}(\gamma)}{w_q}
\frac{m_{q,r}}{2^s}
\\
&\qquad=
\frac{p_{\mathcal M}(\gamma)}{w_q}
\frac{w_qP(q,r)}{w_r}
\\
&\qquad=
\frac{p_{\mathcal M}(\gamma)P(q,r)}{w_r}
=
\frac{p_{\mathcal M}(\gamma r)}{w_r}.
\end{aligned}
$$

This proves the induction step. Summing (9) over $h\in F_{x_n}$ gives
$p_{\mathcal M}(\gamma)$, proving the projection claim. $\square$

**Corollary 10 (exact sampling characterization).** A fixed finite Markov chain
has a randomized-$AC^0$ trajectory sampler for all horizons if and only if it
is path-dyadic.

**Proof.** If a sampler uses $r_n$ fair bits, every trajectory atom has
probability equal to a multiple of $\frac{1}{2^{r_n}}$, so it is dyadic.

Conversely, Theorem 9 lifts every path-dyadic chain to a
transition-dyadic chain. Apply Theorem 8 to get the corresponding
randomized-$AC^0$ sampler. $\square$

**Corollary 11 (binary regular-language sampling).** Every fixed binary regular
language $L\subseteq\{0,1\}^*$ has a randomized-$AC^0$ sampler for
$\mathrm{Pair}_{L,n}$.

**Proof.** Fix a DFA $\mathcal A=(Q,\{0,1\},\delta,q_0,F)$ for $L$, and set

$$
A(q,r)
=
\left\{a\in\{0,1\}:\delta(q,a)=r\right\},
\qquad
P(q,r)=\frac{|A(q,r)|}{2}.
$$

Thus

$$
P(q,r)\in\left\{0,\frac12,1\right\}
\subseteq\mathbb D_{\ge0}.
$$

Hence the chain is transition-dyadic and therefore path-dyadic.

With $\mu=e_{q_0}$, Corollary 10 samples its state trajectory

$$
(Y_0,Y_1,\ldots,Y_n),
\qquad
Y_0=q_0.
$$

Conditioned on this path, independently sample $X_{i+1}$ by

$$
\Pr[X_{i+1}=a\mid Y_i,Y_{i+1}]
=
\frac{\mathbf 1[\delta(Y_i,a)=Y_{i+1}]}
{\sum_{b\in\{0,1\}}\mathbf 1[\delta(Y_i,b)=Y_{i+1}]}
\in
\left\{0,\frac12,1\right\},
$$

for $0\le i<n$ and $a\in\{0,1\}$. Each coordinate uses at most one fresh fair
bit. Then $X=(X_1,\ldots,X_n)\sim U_n$ and

$$
C=\mathbf 1[Y_n\in F]=f_L(X).
$$

Thus $(X,C)$ has distribution $\mathrm{Pair}_{L,n}$, and the postprocessing is
in randomized-$AC^0$. $\square$

## Appendix A: spectral certificate for the three-state obstruction

Here, spectrum means the ordinary spectrum $\sigma(A)$: all eigenvalues of
$A$.

Write $\tau_\bullet=(\tau_u)_{u\in\{0,1\}^b}$ for the indexed family of block
transformations, and let $M_{\tau_u}$ be the $0$-$1$ transition matrix of
$\tau_u$. The transition-count matrix induced by the family is

$$
M_{\tau_\bullet}
=\sum_{u\in\{0,1\}^b}M_{\tau_u},
\qquad
(M_{\tau_\bullet})_{s,t}
=\left|\{u:\tau_u(s)=t\}\right|.
$$

Every row of $M_{\tau_\bullet}$ has sum $r=2^b$, so
$M_{\tau_\bullet}\mathbf 1=r\mathbf 1$ for $\mathbf 1=(1,1,1)^T$. Choose

$$
V=
\begin{pmatrix}
1&0&0\\
1&1&0\\
1&0&1
\end{pmatrix}.
$$

The coordinates of $v=(v_0,v_1,v_2)^T$ in this basis are
$(v_0,x,y)^T$, where $x=v_1-v_0$ and $y=v_2-v_0$. Thus

$$
V^{-1}M_{\tau_\bullet}V=
\begin{pmatrix}
r&*\\
0&B_{\tau_\bullet}
\end{pmatrix}.
$$

The two remaining eigenvalues of $M_{\tau_\bullet}$ are exactly the
eigenvalues of $B_{\tau_\bullet}$.

For the counterexample matrix

$$
T=
\begin{pmatrix}
1&0&1\\
2&0&0\\
0&2&0
\end{pmatrix},
$$

one computes

$$
V^{-1}TV=
\begin{pmatrix}
2&0&1\\
0&0&-1\\
0&2&-1
\end{pmatrix},
\qquad
B_T=
\begin{pmatrix}
0&-1\\
2&-1
\end{pmatrix}.
$$

Thus

$$
\chi_{B_T}(\lambda)=\lambda^2+\lambda+2,
$$

and the two remaining eigenvalues are

$$
\frac{-1\pm i\sqrt7}{2}.
$$

The verification script
[tools/verify_three_state_block_aperiodicity.py]({{ '/tools/verify_three_state_block_aperiodicity.py' | relative_url }})
checks the finite certificate behind the contradiction. There is no infinite
enumeration: on three states there are only $3^3=27$ transformations, and
every aperiodic submonoid is contained in a maximal one. The script enumerates
all $401$ aperiodic submonoids, finds the $9$ maximal ones under inclusion, and
groups them into three conjugacy classes.

For each individual transformation, write $B_\tau$ for the lower-right block
of $V^{-1}M_\tau V$. For the three representative classes, the following
properties of these $B_\tau$ matrices are checked:

1. every $B_\tau$ in class I preserves one common cone in the $(x,y)$-plane;
2. every $B_\tau$ in class II preserves another common cone in the $(x,y)$-plane;
3. every $B_\tau$ in class III is triangular in the displayed coordinates.

Because the block census from an original-state block-aperiodic realization is
a sum over the indexed family $\tau_\bullet$, its lower-right block is

$$
B_{\tau_\bullet}=\sum_{u\in\{0,1\}^b}B_{\tau_u}.
$$

Thus the three certificates are inherited by all block lengths and repeated
transformations. In the cone cases, $B_{\tau_\bullet}$ has nonnegative entries
in the cone basis and hence real eigenvalues; in the triangular case this is
immediate. Therefore every such census has real spectrum, contradicting the
fact that $T^b$ has a non-real eigenvalue.
