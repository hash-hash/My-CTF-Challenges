## Unwind On Vacation

- Category: **Crypto**
- Difficulty: ★★☆
- Solved: 1
- Tag: **UOV, Linear Algebra, LLL**

## Description

It's time to Unwind On Vacation 🏖️

## Solution

题目中 UOV 的 m,n 参数是 NIST Level 3 的微调，将 257 换成了稍大的素数，能利用的点在于可以刷新公钥，并且这个过程未重新生成 Oil space ，这导致了我们可以利用足够多的满足 $O\times A_i\times O=0$ 的方程，进行线性化处理。

在设置参数的时考虑了直接使用 Groebner basis 的做法 [fgb_sage](https://github.com/mwageringel/fgb_sage)，但是由于参数规模较大即使能恢复出 $O$ ，时间上也会比预期解长很多，而对于相比 Buchberger 效果更好的 F4, F5 需要 Magma，没进行测试。

注意到 $O_{basis}$ 的格式为 $(o_1,\dots,o_{n-m},0,\dots,1,\dots,0)$，可以考虑线性化为 $\frac{(n-m)(n-m+1)}{2}+(n-m)=5885$ 个变量，一共有 $80m=5840$ 个方程，此时的解空间为 $q^{45}$，但是我们实际的 o 空间只有 $q$ 。即大部分解空间中的向量都不符合 $x_ix_j$ 之间的约束关系。

处理的办法需要利用到 $O$ 生成时的特点，`self.O = random_matrix(ZZ, n-m, m)` 这导致了 $O$ 是从正态分布中选取，方差并不会太大，整体来看我们可以通过重复连接获得第一条向量较短的情况。利用这个性质我们挑选出解空间中代表 $x_i$ 的部分，一共 $n-m=107$ 项，维度为 $45$ ，通过 LLL 还原出目标的 $x_i$

注意到恢复出一条 oil 后，我们不需要重复这一过程，只需要利用 $P'(o_1,o_2)=0$ 的性质，解方程即可还原 $O$。

拿到 $O$ 后走正常签名步骤即可。

> 实际上利用 O 的特殊性能够通过猜测某个位置来减少变量个数使得方程可解，相比使用 LLL 来拿到特定的向量更直接。
