## ENChannel

+ Category: **Crypto**
+ Difficulty: ★★☆
+ Tag: **FHE, Ring Packing**

## Description

Is 🔒(📪) secure enough?

## Solution

由 qwen 随机生成 dialogue，每句话按照 32 字节分块后随机填充，每块被分别加密到 BFV 密文中，可以选择 14 次 Galois key，并且给出一次解密机会，返回解密结果中 256 个系数，要求还原出 dialogue。

该题是对 r3ctf2024 tinyseal 在多信息情况下的拓展，对于 tinyseal 只需要将一个对 $\sum m_ix^i$ 的加密 $\text{Enc}(\sum m_ix^i)$ 通过运算去掉除常数系数的所有项，在这里需要处理多个密文，并且将常数系数拼凑到合适的位置。

对于从 $\text{ENC}(\sum m_ix^i)$ 得到 $\text{ENC}(m_0)$ 的过程，最简单的是通过执行 trace 函数，这个过程需要 $\log N$ 次 key switching 操作。通过迭代地执行 $c+\tau_{2^l+1}(c),l\in[1,14]$

简单地重复进行 trace 对于 $l$ 个密文总共需要 $l\log N$ 次 key switching 操作，在这里存在算法优化，可以将 key switching 次数减少到 $l$ 次。主要的 insight 是注意到在执行 trace 的过程中存在一些空槽位可以进行插入。可以通过按照类似树结构的插入方式，省去一个 $\log N$ 的因子，具体细节可以参考 https://eprint.iacr.org/2020/015 。

实际上由于此处算法优化也只是减少十几倍，通过并行的方式在多核心的情况下也有机会做到。
