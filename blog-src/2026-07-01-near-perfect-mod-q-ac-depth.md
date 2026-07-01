---
title: "Near-perfect average-case computation of MOD_q still requires large AC depth"
date: 2026-07-01
slug: near-perfect-mod-q-ac-depth
tags: [circuit complexity, average-case lower bounds, AC circuits]
summary: "A theorem-note draft on polynomial-size AC circuits that compute MOD_q with near-perfect average-case accuracy, and why their depth must be Omega(log n / log log n)."
---

# Near-perfect average-case computation of MOD_q still requires large AC depth

This note records a simple average-case consequence of the low-degree
polynomial method for modular counting. Fix an integer $q\ge 2$ and a constant
$\lambda>0$. For uniformly random $x\in\{0,1\}^n$, let

$$
MOD_q(x)=1\left[\sum_{i=1}^n x_i \equiv 0 \pmod q\right]
$$

and let $\{C_n\}$ be a polynomial-size $AC$ circuit family with unbounded-fan-in
AND, OR, and NOT gates. If, for all sufficiently large $n$,

$$
\Pr_{x\sim\{0,1\}^n}[C_n(x)=MOD_q(x)]\ge 1-\frac1q+\lambda,
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
gates. I use the notation and results of Beck and Li \[1\]. Their Theorem 7.1
gives the following Razborov-Smolensky approximation statement: if $C$ is a
size-$S$, depth-$d$ circuit in this $AC[p]$ model, then for every $\ell>0$ there
is a polynomial

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
stated there for $AC^0[p]$, but the statement itself keeps the depth parameter
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

On the other hand, the consequence of Theorem 7.3 used in \[1\] says that
$MOD_q$ differs from every degree-$o(\sqrt n)$ polynomial over $\mathbb{F}_p$
on at least

$$
2^n\left(\frac1q-o(1)\right)
$$

inputs, where nonzero field values are interpreted as Boolean value $1$.
Therefore $P$ differs from $MOD_q$ on a $(1/q-o(1))$ fraction of inputs, while
$P$ differs from $C$ on at most an $n^{-2}$ fraction of inputs. By the triangle
inequality,

$$
\Pr_x[C(x)\ne MOD_q(x)]\ge \frac1q-o(1).
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

## References

\[1\] Chris Beck and Yuan Li. "Represent MOD function by low degree polynomial
with unbounded one-sided error." arXiv:1304.0713, 2013.
<https://arxiv.org/abs/1304.0713>.
