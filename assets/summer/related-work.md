# Related Work：分类梳理

下面按研究问题而不是按论文逐篇罗列，共选取 9 项代表性工作，覆盖五条文献线索。

## 一、扩散语言模型与并行采样

**Jiang, Haghtalab, and Chen (2026), *Diffusion Language Models Are Provably Optimal Parallel Samplers*.**

这项工作把 DLM 的生成过程形式化为多轮并行采样，比较 revision/remasking 与 no-revision 两种模型对 parity 采样的轮数影响。结论是 revision 是 O(1), no-revision 是 w(1) 。

同时它给出一般性的 optimal parallel sampler 结论：在 COT 加持下，随机电路深度为 $d$ 的同样由 rounds 为 d 的 DLM 采样，即：

$$
\text{DLM decoding rounds}
=
\text{underlying sampling circuit depth}.
$$

进一步的，COT tokens 数量可以被 revision 缩减为电路宽度级别。

## 二、Transformer 与电路复杂度

**Li et al. (2024), *Chain of Thought Empowers Transformers to Solve Inherently Serial Problems*.**

该工作建立了有限深度下，不同精度，宽度，COT token 数量组合的 Transformer的表达性。
具体的，无 COT，精度有限，宽度 poly 等价于 AC0 。

## 三、分布采样的复杂度与下界

**Viola (2012), *The Complexity of Distributions*.**

该工作提出了研究 (X,b(x)) 的 circuit sample 问题。

一个典型例子是

$$
\operatorname{PARITY}(x)=\sum_{i=1}^n x_i\pmod 2.
$$

虽然 parity 不属于 $AC^0$，但分布 $(X,\operatorname{PARITY}(X))$ 有一个 randomized-$NC^0$ 的精确 sampler：令 $U_1,\ldots,U_n$ be uniform on $\{0,1\}^n$ ，输出

$$
(U_1,\,U_1\oplus U_2,\,\ldots,\,U_{n-1}\oplus U_n,\,U_n).
$$

对称函数是另一组重要例子。若 $b(x)$ 只依赖 Hamming weight $|x|=\sum_i x_i$，则 $b$ 是对称函数；majority 和 $\operatorname{MOD}_3$ 都属于这一类。解决思路是先按二项分布随出 1 的数量，再用一个 randomized-AC0 去近似随机排列从而近似对称函数的 pair 分布。

**Viola (2020), *Sampling Lower Bounds: Boolean Average-Case and Permutations*.**

对深度为 $d$、规模至多 $\exp(n^{c/d})$ 的 randomized-$AC^0$ 电路，Viola 构造了一个其无法近似采样的显式函数 $h$，同时 h 属于 P。

$$
\Delta\bigl(C(U'),(U,h(U))\bigr)
\ge \frac12-2^{-n^{\Omega(1)}}.
$$
注:U' 代表 C 的 random bits, 不超过电路大小就好。

## 四、正则语言与浅层电路

**Barrington, Compton, Straubing, and Thérien (1992), *Regular Languages in NC1*.**

该工作奠定了用 syntactic monoid 描述正则语言电路复杂度的经典框架；其中关于 stable syntatic monoid 无周期（aperiodic）结构对应于 $AC^0$ 级别的正则语言。

**Goldwurm, Palano, and Santini (2001), *On the Circuit Complexity of Random Generation Problems for Regular and Context-Free Languages*.**

这项工作研究从 $L\cap\Sigma^n$ 中均匀生成一个长度为 $n$ 的词。更一般地，作者考虑由 polynomially bounded ambiguity 的 $1$-NAuxPDA 在 polynomial time 内接受的语言，并证明相应的随机生成问题可以由浅层概率电路解决；正则语言是其中的特例。

它使用的是 **logspace-uniform probabilistic Boolean circuits**。对每个输入长度 $n$，存在一个电路

$$
C_n:\{0,1\}^{r(n)}\longrightarrow \Sigma^n\cup\{\mathsf{failure}\},
$$

其中输入是 $r(n)$ 个独立的 fair bits，电路规模为 polynomial，深度为 $O(\log^2 n)$，并且电路族由 logspace uniformity 生成。输出空间中额外加入显式的 failure 符号：令

$$
S_n=\{C_n(U)=\mathsf{failure}\},
\qquad U\sim\operatorname{Unif}(\{0,1\}^{r(n)}).
$$

作者要求，在成功事件 $S_n^{\mathsf c}$ 条件下，输出在目标集合上严格均匀，即

$$
\Pr\bigl[C_n(U)=w\mid S_n^{\mathsf c}\bigr]
=\frac{1}{|L\cap\Sigma^n|}
\qquad
\text{for every }w\in L\cap\Sigma^n.
$$

因此，若记 $p_{\mathrm{fail}}(n)=\Pr[S_n]$，无条件输出分布实际上是

$$
\Pr[C_n(U)=w]
=\frac{1-p_{\mathrm{fail}}(n)}{|L\cap\Sigma^n|}
\quad(w\in L\cap\Sigma^n),
\qquad
\Pr[C_n(U)=\mathsf{failure}]=p_{\mathrm{fail}}(n).
$$

这里所谓的“近似”不是 total-variation 意义下的近似采样；近似性（如果从总输出空间看）只来自 failure mass。也可以把它理解为 rejection-style 的 Las Vegas 生成器：成功时 exact，失败时报告 failure，而不是返回一个偏离均匀分布的词。原论文的摘要性结论给出 polynomial-size、$O(\log^2 n)$-depth 的电路上界。

## 五、随机映射与 Markov 链表示

**Yano and Yasutomi (2011), *Random Walks Driven by Markov Chains and Road Coloring*.**

该工作把有限 Markov 链表示为由独立随机映射驱动的随机游走，并利用 road coloring 研究同步与耦合。

**Jost, Kell, and Rodrigues (2015), *Representation of Markov Chains by Random Maps: Existence and Regularity Conditions*.**

该工作系统讨论 Markov kernel 的 random-map representation 及其存在条件，为把转移过程改写成随机函数迭代提供标准接口。

## 小结

已有工作分别覆盖了并行生成模型、电路化 Transformer、分布采样下界、正则语言的浅层计算，以及 Markov 链的随机映射表示；但这些结果没有同时给出

$$
\text{固定线性 fair-bit 预算}
\;+
\text{worst-case constant-depth}
\;+
\text{无失败的 exact sampler}
\;+
\text{完整有限轨迹输出}.
$$

这些工作共同形成了并行生成模型、Transformer 电路复杂度、分布采样、正则语言随机生成和 Markov 随机映射五条相关研究线索。
