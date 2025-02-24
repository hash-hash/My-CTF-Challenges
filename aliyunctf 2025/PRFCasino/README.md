## PRFCasino

+ Category: **Crypto**
+ Difficulty: ★★
+ Tag: **ARX, Feistel**

## Description

Are you Super Guesser 🍀

## Solution

利用 ARX 和 Feistel 结构构造的 PRF，题目需要区分 PRF 输出与随机输出。

需要观察到 `T+T<<<20` 结构的特殊性

$T\lll20=2^{20}T\ mod\ 2^{64}-1$

$\Rightarrow R+T\lll20+T\ mod\ 2^{64}=R+T\lll20+T-k\cdot2^{64}=R+(2^{20}+1)T-k\cdot 2^{64}\ mod\ 2^{64}-1$

$\because 2^{20}+1=2^{64}-1=0\ mod\ 17$

$\Rightarrow L'=R+T\lll20+T=R-k\cdot 2^{64}\ mod\ 17$，其中 $k\in\{0,1,2\}$

$\Rightarrow L'-R=-k\cdot 2^{64}=-k\ mod\ 17$

下面考虑这个性质的扩散程度，注意到对于一轮 $L'-R$ 为 0,15,16 的概率分别为 $\frac{1}{6},\frac{1}{6},\frac{2}{3}$

考虑经过 15 次叠加后的 $L_{end}-R$ 在模 17 上的分布状态，可以视为多项式卷积

```python
PR.<x> = PolynomialRing(QQ)
f = 1/6+1/6*x^15+2/3*x^16
coeff = list(f**15%(x^17-1))
for _ in range(len(coeff)):
    coeff[_] = round(coeff[_],6)
```

由于 2 与 11 在分布上存在较大差异，利用这一点进行区分
