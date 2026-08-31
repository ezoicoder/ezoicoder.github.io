# Related-work and novelty note

[proof.md](../proof.md) 已从约 3121 行压缩到 960 行：

  - 保留完整的 fixed MOD_q、MOD_3 特殊构造。
  - 保留 finite aperiodic lift 接口、SCC 通用证明及 $b=7$ 六状态数值转移。
  - 移除主文件中的三/四/五状态有限分类、stochastic 支线和迭代日志。
  - 没有物理删除脚本、manifest 或有限证书；在 [proof-archive.md](../proof-archive.md) 中保留了裁剪索引。

  关于 novelty：我的判断是“有很强的 novelty 信号”，但正式论文仍应写 “to the best of our knowledge”，暂不能声称全球首创。

  真正可能新的核心是

$$
  \text{任意 fixed DFA 的 universal exact finite aperiodic lift}
  +
  \text{length-preserving }AC^0\text{ cube permutation}.
$$

  理由是：

  - Viola 研究的是显式困难 graph distributions 和 sampling lower bounds，没有该普遍正则语言上界。SIAM 论文 (https://epubs.siam.org/doi/10.1137/18M1198405)
  - 已知“所有 regular languages”结果只给 polylog-depth proof systems，既不保证 uniform graph law，也不是 constant-depth exact sampler。Small Depth Proof
    Systems (https://eccc.weizmann.ac.il/report/2013/102/)

  - Fill–Machida 已经提供 common-quantile/monotone realization 工具，因此这一局部耦合步骤本身不算新；新处是证明任意 DFA 经过至多双倍 state splitting
    后都能进入这个框架。Fill–Machida (https://arxiv.org/abs/math/0010026)

  - Road coloring 只保证 synchronizing random maps，不保证整个生成 monoid aperiodic，也没有 exact dyadic census 和 cube permutation。Yano–Yasutomi
    (https://arxiv.org/abs/1006.0534)

  - DLM 工作提供的是“给定 sampler 后如何模拟”的通用接口，并不构造 regular-language sampler。DLM parallel samplers (https://arxiv.org/abs/2512.25014)

  所以“两轮 revision-DLM”更适合作为重要推论；论文的技术标题和 novelty statement 应突出 universal aperiodic lift。

  验证方面，$T^7$ 投影、全部 CDF inequalities 和 128 个 common-rank transitions 均通过；旧 $b=3$ 六状态证书也重新运行通过，Markdown、局部链接和 git diff
  --check 均无问题。未提交 commit，也未触碰其他已有工作区改动。




短结论：相关前驱不少，也有人做过非常接近的版本；但截至 2026-08-09 的这轮定向检索，我没有找到已经证明 proof.md:78 同型结论的论文。

  我建议把当前 novelty 状态从 NOT AUDITED 提升为：

  > STRONG NOVELTY SIGNAL / PRIORITY NOT CERTIFIED

  仍然不宜直接写 “first”。

  ### 最接近的已有工作

   文献方向          Goldwurm–Palano–Santini, STACS 2001
   已经做到什么      用 logspace-uniform probabilistic Boolean circuits 从 regular language 中均匀生成长度 $n$ 的词；一般上界为
                     polynomial size、$O(\log^2 n)$ depth。论文 (https://doi.org/10.1007/3-540-44693-1_27)
   与我们的关键差别  这是最直接的电路前驱，但不是 $AC^0$。其 fair-bit 模型允许显式 failure，成功条件下才严格均匀；而且目标是
                     $L\cap\Sigma^n$ 上的均匀词，不输出 Markov 内部状态轨迹。作者上传全文 (https://www.researchgate.net/
                     publication/2331586_On_the_Circuit_Complexity_of_Random_Generation_Problems_for_Regular_and_Context-Free_Languages)
  ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   文献方向          Yano–Yasutomi, 2010
   已经做到什么      把 finite mixing Markov chain 精确表示成由 i.i.d. random maps 驱动的 random walk，并利用 synchronizing road
                     coloring 做 coupling from the past。论文 (https://arxiv.org/abs/1006.0534)
   与我们的关键差别  概率表示非常接近，但没有 fixed fair-bit budget、Boolean circuit 或 constant-depth 保证；同步时间也是随机的。
  ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   文献方向          Jost–Kell–Rodrigues, 2015
   已经做到什么      系统研究 Markov kernel 的 random-map representation。论文 (https://arxiv.org/abs/1207.5003)
   与我们的关键差别  给出“每一步由独立随机函数驱动”的标准接口，但不并行计算所有 prefix states。
  ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   文献方向          Angel–Spinka, 2021
   已经做到什么      指数回返尾的 stationary ergodic Markov chain 是 i.i.d. process 的 finitary factor。论文 (https://arxiv.org/
                     abs/1908.06240)
   与我们的关键差别  exact，但每个坐标读取的是随机大小的有限窗口，没有统一最坏情形上界；也只处理 stationary/finitary coding，而不是有限
                     horizon 的 $AC^0$ circuit。
  ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   文献方向          Neal, 2012
   已经做到什么      对转移概率为 $1/Q$ 整数倍的有限 MCMC，把 $n$ 次转移解释成扩展空间上的 permutation；非均匀目标也可通过扩展坐标处理。
                     论文 (https://arxiv.org/abs/1205.0070)
   与我们的关键差别  与 hidden lift、measure-preserving permutation 的几何直觉很接近，但仍然是顺序施加转移，没有 $AC^0$ full-prefix 结
                     论。
  ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   文献方向          Picard-map parallel MCMC, Biometrika 2026
   已经做到什么      把整条 Metropolis 轨迹写成固定点，能够在时间轴上并行求解；exact scheme 最终与顺序轨迹完全一致。论文 (https://
                     academic.oup.com/biomet/article/113/2/asag022/8571355)
   与我们的关键差别  这是最新且很接近“并行生成一条轨迹”的工作，但迭代次数不是最坏情形常数，模型也不是 finite-state、finite-fair-bit
                     $AC^0$。

  另外，Mereghetti–Palano 2002 (https://air.unimi.it/handle/2434/55437) 研究 probabilistic automata 的 transition/stochastic event
  是否属于 $TC^0$。它计算的是转移概率或事件，不是从 fair bits 输出整条 realized trajectory。

  ### 哪些部分其实是标准的

  如果只声称：

  > “转移概率本身都是 dyadic，所以每一步用若干 fair bits 顺序采样。”

  这基本是标准 random-map representation，不应作为主要新意。类似地：

  - finite fair-bit sampler 的每个输出 atom 必须 dyadic，是直接的 counting fact；
  - weak lumping、state splitting、random-map representation 都有成熟文献；
  - aperiodic monoid $\Rightarrow$ star-free $\Rightarrow FO[<]\Rightarrow AC^0$ 是经典桥梁；
  - odd-prime valuation 变成 vertex potential 的证明虽然我没找到相同 Markov 表述，但很可能会被视为标准的 graph-coboundary/potential
    argument。

  ### 真正看起来新的部分

  我没有找到文献同时给出下面这个闭环：

$$
  \begin{aligned}
  &\text{每条有限 visible path 的概率都是 dyadic}\
  &\Longleftrightarrow
  \text{dyadic diagonal potential}\
  &\Longleftrightarrow
  \text{finite uniform-fiber dyadic weak lift}\
  &\Longleftrightarrow
  \text{使用 }c+sn\text{ 个 fair bits 的 exact }AC^0
  \text{ full-trajectory sampler}.
  \end{aligned}
$$

  尤其新意最强的似乎是：

    1. 允许 visible transition 本身非 dyadic，只要求从指定初始分布可见的完整 path atoms dyadic；
    2. 自动得到统一的 affine bit bound $c+sn$；
    3. 通过 measure-preserving cube reparameterization / universal aperiodic block lift，让所有 prefix states 同时落入 $AC^0$；
    4. 覆盖 reducible、periodic、transient chains，而不只 stationary mixing chains；
    5. 输出完整状态序列，不只是终态 marginal。

  这里最值得强调的是：对每个固定 $n$，把 dyadic 分布硬编码成 lookup table 并不难，但需要指数尺寸。你们证明的是一个对所有 $n$ 的
  polynomial-size、worst-case constant-depth family，这才是复杂度论内容。

  ### 对 regular-language 前驱的准确区分

  STACS 2001 的目标是

$$
  \operatorname{Unif}(L\cap\Sigma^n),
$$

  而我们的 regular-language 推论目标是

$$
  (X,\mathbf 1_L(X)),
  \qquad
  X\sim\operatorname{Unif}(\left{0,1\right}^n).
$$

  二者不是同一个随机生成问题。前者的集合大小通常不是 $2$ 的幂，所以 fixed fair bits 下的 no-failure exact generation 本来就不总是可能；
  后者的每个 graph atom 都恰好有概率 $2^{-n}$。因此 Goldwurm 等人的工作必须引用，但不会覆盖我们的结果。

  我建议 related work 使用这种克制措辞：

  > Classical work represents finite-state Markov chains as i.i.d.-driven random dynamical systems, and stationary Markov chains as
  > finitary factors of i.i.d. processes. Probabilistic circuits have also been used for uniform generation from regular languages in
  > polylogarithmic depth. To the best of our knowledge, these results do not provide a no-failure, worst-case constant-depth circuit
  > that uses a fixed linear number of unbiased bits and outputs the entire finite trajectory. We characterize exactly when such a
  > sampler exists.

  综合判断：不是“Markov sampling 从没人研究”，而是“相关的概率表示、编码和并行采样都有人研究，但 path-dyadic iff exact fair-bit $AC^0$
  full-trajectory sampling 这一组合目前没有找到前例”。其中 universal aperiodic reparameterization 应当作为主要技术新意，dyadic potential
  与 hidden lift作为支撑性结构结果。