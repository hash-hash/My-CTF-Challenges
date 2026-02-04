## Griffin

+ Category: **Crypto**
+ Difficulty: ★★★
+ Tag: **ECDLP, ISD, Sidelnikov-Shestakov attack, LLL**

## Description

Having barely survived the scorching breath of the Chimera, I now stand before a different kind of beast. The chaos of the goat and snake is gone, replaced by the regal gaze of a guardian. I have encountered the Griffin which is a legendary creature with the body, tail, and back legs of a lion, and the head and wings of an eagle with its talons on the front legs.

## Solution

题目大致的逻辑可以描述为，先从 $[1,257]$ 中采样 $2d$ 个点，再随机生成 m 个 $Z_{order}$ 下的 $d-1$ 度多项式。用这 $m$ 个多项式分别在每个点进行评估后乘 $G$ 最终得到 $\text{Hawk}_{2d\times m}$ ，接着取随机的 $k\times m$ 矩阵与 $G$ 相乘得到 $Lion$。两部分拼接后得到 $\text{Griffin}$ 做完行混洗后输出。同时输出第一个采样多项式在 `flag` 处的评估。

第一步还是在拿到椭圆曲线上的点后通过消元、GCD 的操作还原曲线参数，注意到得到的曲线是超奇异曲线，且阶光滑，直接求解 ECDLP 即可。

接下来需要将 $\text{Hawk}$ 从 $\text{Griffin }$ 中提取出来，需要注意的是 $\text{Hawk}$ 是 $m$ 个 $d-1$ 度多项式在 $2d$ 个点估值的结果，因此 $rank(\text{Hawk}_{2d\times m})=d$ 。利用这个特点我们可以结合 plain-ISD 的思想，在 $(k+2d)\times m$ 的矩阵抽 $m$ 行，然后检查矩阵是否满秩，若不满秩则逐行去除并检查秩的变化，这样可以将有线性关系的 $2d$ 行全部取出。

之后可以将 $\text{Hawk}^T$ 写成 $F\times V(x_1,\dots,x_{2d})=Hawk^T$

其中 $F\_{m\times d}$ 为系数矩阵，$V\_{d\times 2d}$ 为范德蒙德矩阵。这个问题和 HSSP 十分类似，可以将其视为 McEliece 框架下的公钥分解，因为 McEliece 在 Reedsolomen Code 下是不安全的，可以参考 https://crypto-kantiana.com/elena.kirshanova/talks/Sidelnikov_Shestakov.pdf 来恢复 $xs$。

最终可能有一到两个候选项并且有一个较小的位移（大概 5 左右），需要进行枚举。通过求根，可以得到 $\text{FLAG}\ mod\ p+1$ 的结果，其中 $p$ 大概 170 比特左右。注意到 FLAG 的格式，只有 32 个 hex 字符未知，简单的构造是按照 $256^i$ 构造背包格，容易发现这个对于数字加小写字母的组合并不好balance，可以通过构造 $16^i$ 的格来获得更好的 balance 效果。

> 但是实际上 $xs$ 本身范数控制得较小，且处在一个较大的模下也可以利用正交格的方式来得到。
