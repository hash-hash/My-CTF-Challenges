## BabyOracle1

+ Category: **Crypto**
+ Difficulty: ★☆
+ Solved: 2
+ Tag: **McEliece, Broadcast attack**

## Description

Is your Oracle safe enough? 😯

## Solution

McEliece 结构，Goppa code作为编码方式，误差权重平均为90

McEliece 结构不能使用同样的公钥去加密同一组明文

$c_1=m\cdot G_p+e_1$

$c_2=m\cdot G_p+e_2$

$\Rightarrow c_1-c_2=e_1-e_2$

对于 $c_1-c_2$ 中为0的位置，

满足 $(c_1)_{[i]}=(c_2)_{[i]}$ 

若 $(c_1)_{[i]}=(c_2)_{[i]}=0$ 可将第 i 列提取

只需提取出足够的524列，且此时的 $G_p'$ 为满秩矩阵即可求出 m

不妨设 $weight(e)=t$  ，先固定一组index，此时另一组随机取，落到第一组集合中的概率为 $\frac{t}{1024}$

考虑二项分布，落入第一组集合期望个数为 $E(X)=n\cdot p=\frac{t^2}{1024}$

也就是我们最终需要从总共 $r=1024-2\cdot t+\frac{t^2}{1024}$ 列，且误差列为 $er=\frac{t^2}{1024}$ 个中选出 524 个无误差列

考虑从中选取 524 个，

不出现误差列的概率是 $\prod_{i=0}^{524} \frac{r-i-er}{r-i}$

差不多随机2000次就能还原出正确的key
