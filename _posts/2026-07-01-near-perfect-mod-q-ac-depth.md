---
title: "Near-perfect average-case MOD_q requires log n / log log n AC circuit depth"
date: 2026-07-01
updated: 2026-07-01
slug: near-perfect-mod-q-ac-depth
permalink: /blog/near-perfect-mod-q-ac-depth/
tags: [circuit complexity, average-case lower bounds, AC circuits]
summary: "A theorem-note draft on polynomial-size AC circuits that compute MOD_q with near-perfect average-case accuracy, and why their depth must be Omega(log n / log log n)."
---

This note records a simple average-case consequence of the low-degree
polynomial method for modular counting. Fix an integer $q\ge 2$ and a constant
$\lambda>0$. For uniformly random $x\in\{0,1\}^n$, let

$$
\mathrm{MOD}_q(x)=\mathbf{1}\left[\sum_{i=1}^n x_i \equiv 0 \pmod q\right]
$$

and let $\{C_n\}$ be a polynomial-size $AC$ circuit family with
unbounded-fan-in AND, OR, and NOT gates. If, for all sufficiently large $n$,

$$
\Pr_{x\sim\{0,1\}^n}[C_n(x)=\mathrm{MOD}_q(x)]\ge 1-\frac1q+\lambda,
$$

then the depth of $C_n$ must satisfy

$$
d(n)=\Omega\left(\frac{\log n}{\log\log n}\right).
$$

In particular, near-perfect average-case accuracy $1-o(1)$ is impossible below
this depth.

## Proof

We prove the stronger statement for $AC[p]$ circuits. Fix a prime $p$ that is
coprime to $q$, and consider circuits over the unbounded-fan-in gate set

$$
\{\mathrm{AND},\mathrm{OR},\mathrm{NOT},\mathrm{MOD}_p\},
$$

which contains ordinary $AC$ as the special case with no $\mathrm{MOD}_p$
gates. I use the notation and results of Beck and Li [1]. Their Theorem 7.1
gives the following Razborov-Smolensky approximation statement: if $C$ is a
size-$S$, depth-$d$ circuit in this $AC[p]$ model, then for every $\ell>0$
there is a polynomial

$$
P\in \mathbb{F}_p[x_1,\ldots,x_n]/(x_i^2=x_i)
$$

such that

$$
\deg(P)\le ((p-1)\ell)^d
$$

and

$$
\Pr_x[P(x)\ne C(x)]\le \frac{S}{2^\ell}.
$$

This is only a slight rephrasing of Beck and Li, Theorem 7.1. The theorem is
stated there for $AC[p]$, but the statement itself keeps the depth parameter
$d$ explicit, so we use it in this per-circuit form.

Now suppose $C$ has polynomial size, say $S\le n^\alpha$. Choose

$$
\ell=(\alpha+2)\log_2 n.
$$

Then

$$
\Pr_x[P(x)\ne C(x)]\le n^{-2},
$$

and the degree bound becomes

$$
\deg(P)\le O_{p,\alpha}((\log n)^d).
$$

If

$$
d\le \left(\frac12-\delta\right)\frac{\log n}{\log\log n}
$$

for some fixed $\delta>0$, then

$$
\begin{aligned}
(\log n)^d
&\le
(\log n)^{(1/2-\delta)\log n/\log\log n} \\
&=
\exp\left(\left(\frac12-\delta\right)\log n\right) \\
&=
n^{1/2-\delta}.
\end{aligned}
$$

Absorbing the constant depending on $p$ and $\alpha$, this gives

$$
\deg(P)=o(\sqrt n).
$$

On the other hand, the consequence of Theorem 7.3 used in [1] says that
$\mathrm{MOD}_q$ differs from every degree-$o(\sqrt n)$ polynomial over $\mathbb{F}_p$
on at least

$$
2^n\left(\frac1q-o(1)\right)
$$

inputs, where nonzero field values are interpreted as Boolean value $1$.
Therefore $P$ differs from $\mathrm{MOD}_q$ on a $(1/q-o(1))$ fraction of
inputs, while $P$ differs from $C$ on at most an $n^{-2}$ fraction of inputs. By
the triangle inequality,

$$
\Pr_x[C(x)\ne \mathrm{MOD}_q(x)]\ge \frac1q-o(1).
$$

Consequently, for any fixed $\lambda>0$, a polynomial-size $AC$ circuit family
with agreement at least $1-1/q+\lambda$ for all sufficiently large $n$ must have

$$
d(n)\ge \left(\frac12-o(1)\right)\frac{\log n}{\log\log n},
$$

and in particular

$$
d(n)=\Omega\left(\frac{\log n}{\log\log n}\right).
$$

## Randomized pointwise form

The same lower bound rules out bounded-error randomized circuits. Suppose that
a randomized polynomial-size AND/OR/NOT circuit $C_R$ of depth $d(n)$ satisfies,
for every input $z\in\{0,1\}^n$,

$$
\Pr_R[C_R(z)=\mathrm{MOD}_q(z)]\ge \frac23.
$$

By constant parallel repetition and majority vote, the error can be reduced to
any constant $\eta>0$ without changing the asymptotic depth. Choose
$\eta<1/q$. Averaging over $R$ then fixes a deterministic circuit
$C_{R^\star}$ with

$$
\Pr_z[C_{R^\star}(z)=\mathrm{MOD}_q(z)]\ge 1-\eta
> 1-\frac1q.
$$

The theorem above applies with

$$
\lambda=\frac1q-\eta>0,
$$

so $d(n)=\Omega(\log n/\log\log n)$. The same conclusion holds for the
one-sided variant where the circuit accepts $\mathrm{MOD}_q^{-1}(1)$ with
probability at least $2/3$ and rejects $\mathrm{MOD}_q^{-1}(0)$ with
probability $1$.

## Regular-language pointwise reductions

Let $$L\subseteq\{0,1\}^*$$ be a regular language that is not in $AC^0$
(constant-depth polynomial-size AND/OR/NOT circuits). By the
regular-language characterization of Barrington, Compton, Straubing, and
Thérien [2], this is equivalent to the syntactic monoid of $L$ containing a
nontrivial group; fix an element of order $q>1$ in that monoid. Suppose
$f_L=\mathbf{1}_L$ has randomized polynomial-size AND/OR/NOT circuits $A_R$ of
depth $d(n)$ with pointwise success probability at least $2/3$:

$$
\Pr_R[A_R(x)=f_L(x)]\ge \frac23
\quad\text{for every }x.
$$

Then

$$
d(n)=\Omega\left(\frac{\log n}{\log\log n}\right).
$$

Proof. The regular-language reduction of Barrington, Compton, Straubing, and
Thérien [2] gives fixed words $a,b$ of the same constant length $h$, fixed
contexts $\ell_r,v_r$, and labels $c_r\in\{0,1\}$ for
$$r=1,\ldots,q-1$$, such that the block morphism $$\phi:\{0,1\}^*\to\{0,1\}^*$$,

$$
\phi(0)=a,\qquad \phi(1)=b,
$$

has the following residue-separation property:

$$
f_L(\ell_r\,\phi(z)\,v_r)=c_r
  \quad\text{when } \sum_i z_i\equiv 0 \pmod q,
$$

but

$$
f_L(\ell_r\,\phi(z)\,v_r)\ne c_r
  \quad\text{when } \sum_i z_i\equiv r \pmod q,
$$

where $\phi(z)$ is the block encoding of $z$.

The equal-length condition is important. Since $|a|=|b|=h=O(1)$, every string
$\ell_r\phi(z)v_r$ has length $hn+O(1)$ independent of the Hamming weight of
$z$, and the map $z\mapsto \ell_r\phi(z)v_r$ is just a constant-depth
substitution with constant-size blocks.

Amplify the success probability to $1-\eta$ for a sufficiently small constant
$\eta>0$, and run the amplified recognizer on the $q-1$ context-wrapped strings
above, and output

$$
C_R(z)=
\bigwedge_{r=1}^{q-1}
  \mathbf{1}\!\left[
    A_R(\ell_r\phi(z)v_r)=c_r
  \right].
$$

If $\sum_i z_i\equiv0\pmod q$, all tests equal their labels with probability at
least $1-(q-1)\eta$. If $\sum_i z_i\equiv r\ne0\pmod q$, the $r$-th test differs
from its label with probability at least $1-\eta$, so the conjunction rejects.
Choosing $\eta$ small enough gives a randomized circuit for $\mathrm{MOD}_q$ on $n$
bits, with pointwise success at least $2/3$ and depth
$O(d(hn+O(1)))$:

$$
\Pr_R[C_R(z)=\mathrm{MOD}_q(z)]\ge \frac23
\quad\text{for every }z.
$$

The randomized pointwise lower bound for $\mathrm{MOD}_q$ gives

$$
d(hn+O(1))=\Omega\left(\frac{\log n}{\log\log n}\right),
$$

and since $h$ is constant, this is the claimed
$d(n)=\Omega(\log n/\log\log n)$ lower bound for $L$ after renaming the input
length.

## References

[1] Chris Beck and Yuan Li. "Represent MOD function by low degree polynomial
with unbounded one-sided error." arXiv:1304.0713, 2013.
<https://arxiv.org/abs/1304.0713>.

[2] David A. Mix Barrington, Kevin Compton, Howard Straubing, and Denis
Thérien. *Regular Languages in NC1*. Journal of Computer and System Sciences,
44(3):478-499, 1992. <https://doi.org/10.1016/0022-0000(92)90014-A>.
