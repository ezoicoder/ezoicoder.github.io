# Sampling Round Complexity of Diffusion Language Models

> **Author:** Jiarui Zhang (张家瑞)<br>
> **Student ID:** 2023010875<br>
> **Date:** July 2026

## 1. Introduction and Literature Review

Diffusion language models (DLMs) generate sequences through repeated parallel
denoising. Starting from a masked sequence, a predictor reads the current state
and returns a distribution for each token position. An update policy then
selects positions, whose new values are sampled conditionally independently in
parallel. I call one such parallel update a **round**. The central complexity
question is how many rounds are necessary to generate a prescribed target
distribution.

To make this round measure meaningful, the computation performed inside one
round must be restricted. This project assumes that each predictor and update
policy is represented by a polynomial-size $AC^0$ circuit, namely a
constant-depth AND/OR/NOT circuit with unbounded fan-in. This is motivated by
the fact that constant-precision, constant-depth Transformers of polynomial
width can be simulated by $AC^0$ circuits [4]. Under this assumption, a
$D$-round DLM can be unrolled into a randomized circuit of depth $O(D)$. This
one-way abstraction neither covers all practical Transformers nor turns every
$AC^0$ construction into a Transformer.

The second modeling choice is whether generated tokens may be revised. In a
**no-revision DLM**, a token is immutable once revealed. In a **DLM with
revision**, a revealed token may be overwritten or masked again. Revision acts
as writable discrete workspace because temporary information can be created
and later replaced by final output tokens.

With both the DLM round and its computational restriction in place, existing
results can be compared precisely. Jiang, Haghtalab, and Chen [1] connect DLM
generation with sampling circuits and show how intermediate workspace allows a
depth-$d$ sampling computation to be simulated in $d$ DLM rounds. They also
give a parity separation: $O(1)$ rounds with revision versus $\omega(1)$
without revision. Svete and Sabharwal [5] show that a revision-enabled
L-uniform deterministic DLM can recognize every regular language in
$O(\log n)$ rounds using $O(n)$ padded workspace positions. These works
establish useful recognition and sampling capabilities, but they do not tightly
characterize the sampling round complexity of general regular-language
input-output pairs.

Inspired by Viola's distribution-complexity framework [2], including its study
of distributions of the form $(X,b(X))$, I consider the following
**input-output-pair sampling problem** in the circuit regime. For a regular
language $L\subseteq\{0,1\}^*$, let
$f_L(x)=\mathbf{1}[x\in L]$ and define

$$
\mathcal{D}^{\mathrm{pair}}_{L,n}
=
\operatorname{Unif}
\{(x,f_L(x)):x\in\{0,1\}^{n-1}\}.
$$

The sequence contains only the $n$ target coordinates, with no additional
padded workspace positions.

The sampler must jointly generate a uniform prefix $x$ and its correct
membership bit. Ordinary hardness of computing $f_L(x)$ does not automatically
make this sampling task hard. Viola's later work [3], for example, develops
sampling-specific lower-bound techniques and constructs an explicit function
$h$ for which small bounded-depth circuits cannot closely sample $(U,h(U))$.
His result shows why sampling requires separate arguments, but the hard
function does not directly provide a regular-language lower bound for
revision-enabled DLMs.

## 2. Limitations of Existing Work and Research Gap

Existing work already separates revision from no revision for parity, but the
known comparison is $O(1)$ versus $\omega(1)$ rather than a tight
regular-language characterization. Parity itself cannot provide a growing
lower bound with revision because its revision-enabled sampler takes constant
rounds. Meanwhile, Transformer and DLM expressivity results with padding or
reusable state mainly study recognition or circuit simulation. Classical
regular-language circuit lower bounds also concern recognizing a supplied
string and cannot be transferred to sampling without an additional reduction.
Viola's 2020 theorem supplies a sampling perspective, but it applies to a
different explicit function and does not yet yield the desired
regular-language result with revision.

My current work gives a comparatively complete picture **without revision**.
The remaining gap is the revision-enabled case. Revision invalidates the
irreversible support trace used by the no-revision lower bound and makes some
regular languages, including parity, sampleable in constant rounds. The main
open question is whether some regular language still requires
$\Omega(\log n/\log\log n)$ rounds when revision is allowed but each round
remains in $AC^0$.

## 3. Research Approach and Preliminary Results

### 3.1 Model and circuit correspondence

I use the two update models from my technical note:

```text
No-revision DLM
Initialize x <- M^n
for t = 1,...,D:
    S <- F(x), where S is a subset of {i : x_i = M}
    for each i in S independently:
        x_i ~ p_i(. | x) over {0,1}
    all positions outside S stay unchanged
Output x
```

```text
DLM with revision
Initialize x <- M^n
for t = 1,...,D:
    for each i in [n] independently:
        x_i ~ p_i(. | x) over {0,1,M}
Output x
```

For either model, a valid sampler must output a sequence containing no $M$.
The predictor $p$ and, in the no-revision model, policy $F$ use polynomial-size
$AC^0$ circuits. Each token update uses polynomially many fair random bits, so
every exactly represented transition probability is dyadic. Unrolling $D$
rounds gives a randomized circuit of size $\operatorname{poly}(n,D)$ and depth
$O(D)$.

### 3.2 Preliminary no-revision result

The preliminary result is a tight $\Theta(\log n/\log\log n)$ bound. The upper
bound uses a $\Theta(\log n)$-ary finite-monoid product tree, with mask patterns
carrying temporary block profiles. For the lower bound, the zero-probability
support condition converts a $D$-round sampler into a depth-$O(D)$ randomized
recognizer by exploiting the rigidity of the transition probabilities.

### 3.3 Proposed revision-enabled direction

Because parity already has an $O(1)$-round sampler with revision, I will
investigate other regular languages as candidates for a growing lower bound. I
will first test whether circuit-depth arguments suffice. If not, the proof may
need DLM-specific restrictions: positions are sampled independently conditioned
on the current state, and only the $n$ output positions persist across rounds,
with no padded workspace. Viola's sampling perspective is a possible guide, but
adapting it to a regular language with revision remains open.

## 4. Expected Outcomes, Challenges, and Feasibility

The expected outcomes are a rigorous no-revision
$\Theta(\log n/\log\log n)$ result with explicit assumptions and, for revision,
either a concrete lower bound or a partial characterization of what it requires.
A further goal is to determine which circuit-level results extend to
Transformers. Lower bounds may transfer through the Transformer-to-$AC^0$
simulation [4], whereas upper bounds require an explicit Transformer
construction.

The challenges are the gap between recognition and sampling, the loss of
support tracing under revision, probability representation, and explicit
Transformer realization. The preliminary no-revision arguments make the
project feasible; a conditional revision result or a precise obstacle would
also be meaningful.

## 5. Next-Step Plan

| Time | Work |
|---|---|
| Week 5 | Finalize definitions, literature review, and no-revision proofs |
| Weeks 6–8 | Study revision and Viola-inspired ideas |
| Weeks 9–10 | Assess Transformer transfer and write the final report |

## References

[1] Haozhe Jiang, Nika Haghtalab, and Lijie Chen. *Diffusion Language Models
are Provably Optimal Parallel Samplers*. ICLR, 2026.

[2] Emanuele Viola. *The Complexity of Distributions*. SIAM Journal on
Computing, 41(1), pp. 191–218, 2012. https://doi.org/10.1137/100814998

[3] Emanuele Viola. *Sampling Lower Bounds: Boolean Average-Case and
Permutations*. SIAM Journal on Computing, 49(1), pp. 119–137, 2020.
https://doi.org/10.1137/18M1198405

[4] Zhiyuan Li, Hong Liu, Denny Zhou, and Tengyu Ma. *Chain of Thought
Empowers Transformers to Solve Inherently Serial Problems*. ICLR, 2024.

[5] Anej Svete and Ashish Sabharwal. *On the Reasoning Abilities of Masked
Diffusion Language Models*. ICLR, 2026.
