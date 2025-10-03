## c0d3

+ Category: **Crypto**
+ Difficulty: ★☆
+ Tag: **McEliece, Reed Solomon Codes**

## Description

M@9ic C0d3 ➡️ Magic Code!

## Solution

McEliece 框架，编码方式采用 RS code。

采用最简单的 Berlekamp-Welch 算法做纠错，纠错能力为 $\lfloor\frac{n-k}{2}\rfloor$

本题需要纠错 $\lfloor\frac{n-k}{2}\rfloor+1$ 个错误，可以采用更优的 list decoding 的方式（例如 Guruswami Sudan 等），也可以基于 Berlekamp-Welch 进行小规模的爆破。

本质就是求解一个不满秩的矩阵，找到特解后做 kernel 的 combine，最后检验结果构成的多项式是否满足整除关系即可。
