---
title: "Markdown math rendering test"
date: 2026-07-24
updated: 2026-07-24
slug: markdown-math-rendering-test
permalink: /blog/markdown-math-rendering-test/
tags: [site maintenance, math rendering]
summary: "A small rendering test for conventional inline and display math delimiters."
---

This page checks that the Markdown source and the rendered blog use the same
conventional math delimiters.

## Inline math

Single dollar signs stay inline: $\mathcal{G}_{L,n}$ appears in the same
sentence as $x_{n-2}$. Their underscores remain part of the TeX source and do
not turn the intervening prose into Markdown emphasis.

The same applies to shorter expressions such as $p_i$, $q_j$, and $AC^0$.

## Display math

Double dollar signs form a separate display block:

$$
\sum_{i=1}^{n} i = \frac{n(n+1)}{2}.
$$

The prose before and after the block remains in separate paragraphs.

## Literal source

Inside a Markdown code span, `$x_i$` remains literal source rather than a
rendered formula.
