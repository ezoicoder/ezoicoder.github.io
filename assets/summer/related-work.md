# Related Work：分类梳理

下面按研究问题而不是按论文逐篇罗列，共选取 9 项代表性工作，覆盖五条文献线索。

## 一、扩散语言模型与并行采样

**Jiang, Haghtalab, and Chen (2026), *Diffusion Language Models Are Provably Optimal Parallel Samplers*.**

这项工作把 DLM 的生成过程形式化为多轮并行采样，比较 revision/remasking 与 no-revision 两种模型对 parity 采样的轮数影响。结论是 revision 为 $O(1)$，no-revision 为 $\omega(1)$。

同时它给出一般性的 optimal parallel sampler 结论：在 CoT 加持下，随机电路深度为 $d$ 的分布同样可由 rounds 为 $d$ 的 DLM 采样，即：

$$
\text{DLM decoding rounds}
=
\text{underlying sampling circuit depth}.
$$

进一步地，CoT tokens 数量可以被 revision 缩减为电路宽度级别。

## 二、Transformer 与电路复杂度

**Li et al. (2024), *Chain of Thought Empowers Transformers to Solve Inherently Serial Problems*.**

该工作建立了有限深度下，不同精度、宽度和 CoT token 数量组合的 Transformer 表达性。具体地，无 CoT、constant-bit precision、polynomial embedding size 的模型等价于 $AC^0$；在 logarithmic precision 下为 $TC^0$。

## 三、分布采样的复杂度与下界

**Viola (2012), *The Complexity of Distributions*.**

该工作提出了研究 (X,b(x)) 的 circuit sample 问题。

一个典型例子是

$$
\operatorname{PARITY}(x)=\sum_{i=1}^n x_i\pmod 2.
$$

虽然 parity 不属于 $AC^0$，但分布 $(X,\operatorname{PARITY}(X))$ 有一个 randomized-$NC^0$ 的精确 sampler：令 $U_1,\ldots,U_n$ 为独立的 fair bits，输出

$$
(U_1,\,U_1\oplus U_2,\,\ldots,\,U_{n-1}\oplus U_n,\,U_n).
$$

对称函数是另一组重要例子。若 $b(x)$ 只依赖 Hamming weight $|x|=\sum_i x_i$，则 $b$ 是对称函数；majority 和 $\operatorname{MOD}_3$ 都属于这一类。解决思路是先按二项分布随机出 $1$ 的数量，再用一个 randomized-$AC^0$ 电路近似随机排列，从而近似对称函数的 pair 分布。

**Viola (2020), *Sampling Lower Bounds: Boolean Average-Case and Permutations*.**

对深度为 $d$、规模至多 $\exp(n^{c/d})$ 的 randomized-$AC^0$ 电路，Viola 构造了一个其无法近似采样的显式函数 $h$，同时 h 属于 P。

$$
\Delta\bigl(C(U'),(U,h(U))\bigr)
\ge \frac12-2^{-n^{\Omega(1)}}.
$$
注:U' 代表 C 的 random bits, 不超过电路大小就好。

## 四、正则语言与浅层电路

**Barrington, Compton, Straubing, and Thérien (1992), *Regular Languages in NC1*.**

该工作用 stable syntactic monoid 分析正则语言的电路复杂度，并将无周期（aperiodic）结构与 $AC^0$ 级别的正则语言联系起来。

**Goldwurm, Palano, and Santini (2001), *On the Circuit Complexity of Random Generation Problems for Regular and Context-Free Languages*.**

这项工作研究从 $L\cap\Sigma^n$ 中均匀生成一个长度为 $n$ 的词。

它使用的是 **logspace-uniform probabilistic Boolean circuits**。对每个输入长度 $n$，存在一个电路

$$
C_n:\{0,1\}^{r(n)}\longrightarrow \Sigma^n\cup\{\mathsf{failure}\},
$$

电路规模为 polynomial，深度为 $O(\log^2 n)$，并且电路族由 logspace uniformity 生成。输出空间中额外加入显式的 failure 符号；在成功事件的条件下，输出在目标集合上严格均匀，即

$$
\Pr\bigl[C_n(U)=w\mid C_n(U)\neq\mathsf{failure}\bigr]
=
\frac{1}{|L\cap\Sigma^n|}
\qquad
(w\in L\cap\Sigma^n).
$$

NC1-complete

## 五、偏序上的随机单调性与共同耦合

**Fill and Machida (2001), *Stochastic Monotonicity and Realizable Monotonicity*.**

设 $A$ 和 $S$ 是有限偏序集，给定一族定义在同一个样本空间 $S$ 上的概率分布 $(\mu_a:a\in A)$。

**定义（随机单调性）。** 如果对任意 $a\preceq a'$ 都有

$$
\mu_a\preceq_{\mathrm{st}}\mu_{a'},
$$

其中 $\mu\preceq_{\mathrm{st}}\nu$ 表示对 $S$ 的每个上闭集 $U$ 都满足

$$
\mu(U)\le\nu(U),
\qquad
\mu(U)=\sum_{s\in U}\mu(s),
$$

则称这族分布是 stochastically monotone。

**定义（可实现单调性）。** 如果存在定义在同一个概率空间上的 $S$-值随机变量 $(X_a:a\in A)$，满足

$$
X_a\sim\mu_a
\qquad(a\in A),
$$

以及

$$
\Pr[X_a\preceq X_{a'}]=1
\qquad\text{whenever }a\preceq a',
$$

则称这族分布是 realizably monotone。它要求所有可比对同时由一个联合分布实现。

**关键结论。** 可实现单调性必然推出随机单调性，但反方向一般不成立。Strassen 定理只保证每一个可比对 $(a,a')$ 可以分别找到一个单调耦合；它不保证这些两两耦合能拼成一个同时满足所有偏序关系的共同耦合。

论文的反例取四元素 Boolean lattice

$$
x\prec y\prec w,
\qquad
x\prec z\prec w,
$$

其中 $y,z$ 不可比，并令 $A=S=\{x,y,z,w\}$。定义

$$
\mu_x=\operatorname{Unif}\{x,y\},\quad
\mu_y=\operatorname{Unif}\{x,w\},\quad
\mu_z=\operatorname{Unif}\{y,z\},\quad
\mu_w=\operatorname{Unif}\{y,w\}.
$$

这族分布满足随机单调性，但不存在共同耦合。事实上，若共同耦合 $(X_x,X_y,X_z,X_w)$ 存在，则 $\Pr[X_x=y]=1/2$；在事件 $\{X_x=y\}$ 上，偏序约束和各边缘分布强迫

$$
(X_y,X_z,X_w)=(w,y,w).
$$

同理，$\Pr[X_z=z]=1/2$，且事件 $\{X_z=z\}$ 强迫 $X_x=x$ 和 $X_w=w$。这两个不相交事件都包含在 $\{X_w=w\}$ 中，故 $\Pr[X_w=w]=1$，但 $\mu_w$ 只给出 $\Pr[X_w=w]=1/2$，矛盾。

因此，当前把

$$
a\preceq a'\Longrightarrow\mu_a\preceq_{\mathrm{st}}\mu_{a'}
$$

直接称为 common-quantile coupling 命题是错误的。只有在额外的偏序结构下，随机单调性才可能推出可实现单调性；当 $A=S$ 时，Fill and Machida 证明二者等价当且仅当 $S$ 的 cover graph 无环。一般偏序下应把共同耦合写成一个额外的存在性问题，而不能假设它由 common quantile 自动给出。

这里的 **cover graph** 是把偏序的 Hasse diagram 忽略方向后得到的无向图：顶点是 $S$ 的元素；当且仅当 $x<y$ 且不存在 $z$ 使 $x<z<y$ 时，在 $x,y$ 之间连一条边。称它无环，是指这个无向图没有 cycle；等价地，它是一个 forest。注意 Hasse diagram 作为有向图本来就没有有向环，判据中的“环”指忽略方向后的环。例如四元素 Boolean lattice 对应的 cover graph 是四边形 $x-y-w-z-x$，因此有环。

无环时的构造是一个归纳。若 $\mu_b\preceq_{\mathrm{st}}\mu_a$，有限状态下的 Strassen 判据给出一个 upward kernel $K$，满足

$$
K(s,\{t:t\succeq s\})=1,
\qquad
\mu_a(t)=\sum_{s\in S}\mu_b(s)K(s,t).
$$

现在令索引偏序 $A$ 无环。取 cover graph 的一个叶子 $a$，不妨设它是极大元；设它唯一的邻居为 $b$。删除 $a$ 得到较小的偏序 $A'$. 归纳假设给出 $(X_\alpha:\alpha\in A')$ 的共同耦合。再用上面的 kernel，在给定 $X_b$ 的条件下生成 $X_a$：

$$
\Pr[X_a=t\mid X_b=s]=K(s,t).
$$

于是 $X_a\sim\mu_a$，并且 $X_b\preceq X_a$ 几乎处处成立。由于 $a$ 是叶子，任意满足 $\alpha\preceq a$ 的旧状态都满足 $\alpha\preceq b\preceq a$；因此原来的关系和 $X_b\preceq X_a$ 合起来，就得到所有需要的 $X_\alpha\preceq X_a$。这把 $A'$ 上的共同耦合扩展为 $A$ 上的共同耦合。

反方向上，如果 cover graph 有环，论文从环中抽取 diamond 或更一般的 crown，并在其上构造 stochastic monotone 但不可 realizably monotone 的分布族；四元素 Boolean lattice 的反例就是最小情形。因此结论不是“偏序 common quantile 总能工作”，而是：无环结构允许把一对一对的 Strassen 耦合按叶子归纳拼成一个共同耦合；有环时这种拼接可能发生全局冲突。



consant-depth poly-width

gape sampling

dlm

looped transformer + diffusion

regular-language L



overleaf

sample P -> cop



randomized-AC0: parity pairty 不在 AC0

regular language L: semi-group



dlm

revision O(1)

intro:

regular larnguage ,recognize/sample 水

dlm 一般。。。



prior work

computation capacity(衡量 sample 一个分布的能力)



gap 有多大（背景信息）,dlm a distribution over, sample ,多少 round

生成的个数/次数
