## DLM paper review concerns

1. 真实 wall-clock latency: 论文里的 parallel advantage 主要指 sequential rounds 或 circuit depth 的减少，但真实推理时间还取决于每一轮的计算量、KV cache 是否可用、序列长度、batching、硬件并行度和 memory bandwidth。因此需要说明：DLM 在理论上减少轮数，并不自动推出 wall-clock latency 一定优于 autoregressive decoding；它只说明当目标分布本身有可并行结构、且硬件能有效并行执行整段更新时，DLM 有潜在速度优势。

2. Training technique: 论文证明的是某类 DLM predictor / unmasking / remasking / revision 过程的存在性和表达能力，而不是给出现实模型如何训练出这些策略的算法保证。需要区分清楚：remasking、revision、CoT-style scratch space 可以作为训练或推理机制被鼓励，但理论结果本身并不证明标准训练目标会自然学到这些最优并行采样过程。

3. 和 spec decoding 的关系: Speculative decoding 也是为了降低 autoregressive 生成的实际延迟，但它的基本机制仍然服务于固定的 left-to-right token order，通过 draft-and-verify 减少大模型调用成本。DLM 的优势主张不同：它试图改变生成顺序本身，让多个位置并行更新。因此两者不应简单比较谁更快，而应说明它们优化的是不同瓶颈：spec decoding 优化 AR pipeline 的工程成本，DLM 理论刻画的是可并行依赖结构下的 round complexity。

4. CoT 和现实不太符合: 论文里的 CoT 更像显式 scratch space，用来存放 circuit simulation 的中间值；这和实际语言模型中的自然语言 Chain-of-Thought 不完全一样。真实 CoT 通常是语义化、可读的推理文本，而这里的 CoT 可以是编码过的中间计算轨迹。因此需要避免把定理理解成“自然语言 CoT 的 DLM 一定高效”。更准确的说法是：只要允许足够长的辅助 token 区域，DLM 可以用这些 token 组织并行计算。

5. AC0 是否符合真实 DLM: 用 AC0 或 constant-depth circuit 来抽象每一轮 DLM predictor，是为了把“每一轮内部计算”和“跨轮 sequential computation”分开，从而研究 round complexity。但真实 Transformer 层数、attention 精度、位置编码、softmax 和数值计算都不完全等同于 AC0。这里的 AC0 更像一个保守的理论代理模型：它帮助证明在很弱的每轮计算能力下，DLM 仍有并行采样优势，但不能直接当作真实 DLM 架构的完整刻画。

6. Optimal 的含义: “Optimal” 应该限定在论文的理论模型里，即给定目标分布可由深度为 d、宽度为 w 的 parallel circuit 采样，DLM 可以用 d 个 decoding rounds 达到相同分布；加入 remasking 或 revision 后，还可以匹配相应的 space/width 需求。它不是无条件地说 DLM 在所有实际指标上最优，也不是说 token throughput、FLOPs、显存占用或工程延迟都最优。


## Related Work

1. Jiang, Haghtalab, Chen, “Diffusion Language Models are Provably Optimal Parallel Samplers,” 2025 / ICLR 2026

2. Svete, Sabharwal, “On the Reasoning Abilities of Masked Diffusion Language Models,” 2025

3. Feng et al., “Theoretical Benefit and Limitation of Diffusion Language Model,” 2025

4. Kang et al., “ParallelBench: Understanding the Trade-offs of Parallel Decoding in Diffusion LLMs,” 2025, revised 2026 / ICLR 2026

5. London, Kanade, “Pause Tokens Strictly Increase the Expressivity of Constant-Depth Transformers,” 2025 / NeurIPS 2025

6. The Exact Expressive Power of Fixed-Precision Looped Padded Transformers Anej Svete

7. Li, Liu, Zhou, Ma, “Chain of Thought Empowers Transformers to Solve Inherently Serial Problems,” ICLR 2024

8. Merrill, Sabharwal, “A Logic for Expressing Log-Precision Transformers,” NeurIPS 2023

9. Constrained Decoding for Diffusion Language Models via Efficient Inference over Finite Automata

10. Zoabi et al., “Mean-Field Parallel Decoding for Discrete Diffusion Language Models,” 2026-06-14

11. Svete et al., “Revisiting Padded Transformer Expressivity,” 2026-05-28

12. Kraus et al., “Barriers to Universal Reasoning With Transformers,” 2026-04-28

13. Kim et al., “Dependency-Aware Parallel Decoding via Attention for Diffusion LLMs,” 2026-03-13

padding/cot 提供 workspace ?
