## LinearCasino

+ Category: **Crypto**
+ Difficulty: ★☆
+ Solved: 19
+ Tag: **linear algebra**

## Description

Are you Super Guesser 🍀

## Solution

McEliece 框架下 $(U,U+V)-Codes$ 在特定参数下的可区分性

即区分 $SGP$ 中 $G$ 为随机 $F_2$ 矩阵或 $\left[\begin{matrix}U&U\\&V\end{matrix}\right]$


对于 $G=\left[\begin{matrix}U&U\\&V\end{matrix}\right]$


$\Rightarrow G^\perp=\left[\begin{matrix}U^\perp\\V^\perp&V^\perp\end{matrix}\right]$


论文中提到了一种区分方式，即 $dim(G\cap G^\perp)=10$ 以大概率成立

还需要考虑的问题是这个性质在 $SGP$ 下的情况

由于矩阵乘法可以看出对某个线性空间的同态映射，在 $S$ 满秩的情况下可以视为行向量空间的同构映射，非满秩的情况下视为同态映射，仍然保留上述的相等关系，而同样右乘的列变换矩阵也不影响论文中证明的结果

实际上这里的区分还有一种更加简单的方式，注意到对于置换矩阵 $P$ ，有 $P\cdot P^{T}=I$

故对于 $C=SGP$ 有 $C\cdot C^T=S\cdot G\cdot P\cdot P^{T}G^{T}\cdot S^{T}=S\cdot (G\cdot G^{T})\cdot S^{T}$

考虑 $G\cdot G^{T}$ 的形式，$G\cdot G^{T}=\left[\begin{matrix}2U\cdot U^{T}&U\cdot V^{T}\\V\cdot U^{T}&V\cdot V^{T}\end{matrix}\right]=\left[\begin{matrix}0&U\cdot V^{T}\\V\cdot U^{T}&V\cdot V^{T}\end{matrix}\right]$

注意到 $V\cdot U^{T}$ 为 $50\times 60$ 的矩阵，秩最多为 50，故 $dim(G\cdot G^{T})\le100$ ，从而可以透过 $C\cdot C^{T}$ 观察这一点

## Reference

[1] The problem with the SURF scheme [↩](https://eprint.iacr.org/2017/662.pdf)
