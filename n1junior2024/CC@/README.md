## CC@

+ Category: **Crypto**
+ Difficulty: ★☆
+ Solved: 2
+ Tag: **CCA, HNP**

## Description

Pursue the ultimate CCA security🔒.

## Details

题目给出了 Elgamal 加密后的 FLAG ，Oracle 由两部分组成，先进行 Elgamal 解密，再做 AES-GCM 解密。由于 `AES-GCM` 的 key 未知，无法通过密文还原 Elgamal 解密后的明文，且限制使用 Oracle 不超过一百次。

## Solution

对于密文 $(c_1,c_2)$ 可以通过发送 $(c_1,a\cdot c_2(mod\ p))$ 获取 $a\cdot m(mod\ p)$ 过 `AES-GCM` 解密的结果，透过观察解密结果的长度可以判断 $a\cdot m(mod\ p)$ 的比特数，对于小于64字节的解密结果可以推出对应的 $a_i\cdot m(mod\ p_i)$ 的高8比特为0，相当于求解一个HNP

lattice 构造如下

$$
L=\left[\begin{matrix}
2^\alpha&a_1&a_2&\cdots&a_n\\
&p_1\\
&&p_2\\
&&&\ddots\\
&&&&p_n
\end{matrix}\right]
$$

从做题情况来看，另一种想法是利用二分通过大小关系逐步限制FLAG范围，也是可行的。

