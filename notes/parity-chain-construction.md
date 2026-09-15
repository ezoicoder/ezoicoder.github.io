# Parity 的链式精确采样构造

这个构造来自仓库历史提交 `df1bd52` 中的
`Chain construction`。它在无 revision 的 DLM 中，用每一对位置的
mask 形态传递一个前缀 parity，从而精确采样均匀偶 parity 分布

$$
D_n^\oplus
=
\operatorname{Unif}
\left\{
x\in\{0,1\}^n:
\bigoplus_{j=0}^{n-1}x_j=0
\right\}.
$$

下面假设 $n$ 为偶数，位置从 $0$ 开始编号，并记

$$
C_i=\{2i,2i+1\}.
$$

## 核心状态

当 $i\ge 1$ 时，位置对 $C_i$ 不是用 token 值，而是用唯一已解码
位置的位置，存储它前面、但不包含直接子对 $C_{i-1}$ 的前缀
parity：

$$
S_i
=
\bigoplus_{u<2i-2}x_u.
$$

不变量为

$$
S_i=0
\quad\Longleftrightarrow\quad
x_{2i}\ne M,\qquad x_{2i+1}=M,
$$

$$
S_i=1
\quad\Longleftrightarrow\quad
x_{2i}=M,\qquad x_{2i+1}\ne M.
$$

因此，一对位置的 mask pattern 就是一个 one-hot 的 parity bit。
那个已解码位置的 token 值仍然是独立公平比特，不承载状态。

## 初始化

第一轮独立采样

$$
x_0,x_1,x_2\sim\operatorname{Bernoulli}(1/2),
$$

并保持 $x_3=M$。此时 $C_0$ 已经全部解码，而

$$
S_1
=
\bigoplus_{u<0}x_u
=0.
$$

所以 $C_1=\{2,3\}$ 中左侧位置已解码，正好编码 $S_1=0$。

## 链上的一步

假设 $C_i$ 的 mask pattern 已经编码 $S_i$，而它的直接子对
$C_{i-1}$ 已全部解码。由于 $C_{i-1}=\{2i-2,2i-1\}$，下一个
前缀状态是

$$
S_{i+1}
=
S_i\oplus x_{2i-2}\oplus x_{2i-1}
=
\bigoplus_{u<2i}x_u.
$$

这一轮同时做两件事：

1. 将 $C_i$ 中仍被 mask 的位置解码为独立公平比特，使 $C_i$
   变成完整的两个输出比特；
2. 在 $C_{i+1}=\{2i+2,2i+3\}$ 中只解码位置 $2i+2+S_{i+1}$，
   且将其采样为独立公平比特。

更直接地，

$$
S_{i+1}=0
\Longrightarrow
x_{2i+2}\ne M,\qquad x_{2i+3}=M,
$$

$$
S_{i+1}=1
\Longrightarrow
x_{2i+2}=M,\qquad x_{2i+3}\ne M.
$$

这就将 parity 状态从 $C_i$ 向右传递到 $C_{i+1}$。每次只需读取
一个常数大小的 mask pattern，并计算三个 bit 的 xor，所以单轮
更新在 $AC^0$ 中。

## 最后收尾

记最后一对为

$$
C_m=\{n-2,n-1\},
\qquad
m=\frac n2-1.
$$

当链传到 $C_m$ 时，其中只有一个位置尚未解码。由状态
$S_m$ 与直接子对 $C_{m-1}$ 先得到

$$
S_{\mathrm{before}}
=
S_m\oplus x_{n-4}\oplus x_{n-3}
=
\bigoplus_{u<n-2}x_u.
$$

设 $j\in C_m$ 是最后那个被 mask 的位置，$k$ 是 $C_m$ 中另一个
已解码位置。最后确定性地设置

$$
x_j
=
S_{\mathrm{before}}\oplus x_k
=
\bigoplus_{u\ne j}x_u.
$$

于是

$$
\bigoplus_{u=0}^{n-1}x_u=0.
$$

整个过程共使用 $n-1$ 个独立公平比特，最后一个位置由它们
唯一确定。每个偶 parity 串又唯一确定整条 mask 路径与前 $n-1$
次采样的结果，因此这个映射是双射。每个偶 parity 串的概率都是
$2^{-(n-1)}$，输出严格等于 $D_n^\oplus$。

## 轮数与这个构造的作用

对偶数 $n\ge4$，该方案需要

$$
1+\left(\frac n2-2\right)+1
=
\frac n2
$$

轮：一轮初始化，$n/2-2$ 轮传递，一轮收尾。所以它是一个
$O(n)$ 轮构造，不是 parity 的最优上界。它的价值在于清楚地展示了：

> 即使 token 值最终全部作为均匀输出，解码过程中的 mask pattern
> 仍可以作为隐藏状态，沿链传递全局约束。

历史文章随后将这条链换成 $B=\Theta(\log n)$ 叉树，从而将深度降为
$\Theta(\log n/\log\log n)$。链式方案则是这个树构造的最简单原型。
