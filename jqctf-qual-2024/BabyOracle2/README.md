## BabyOracle2

+ Category: **Crypto**
+ Difficulty: ★★
+ Solved: 1
+ Tag: **SIDH, GPST attack**

## Description

Is your Oracle safe enough? 😯

## Solution

Oracle初始化时Alice与Bob会进行一次完整的SIDH协议

后续在Bob的视角下反复与 Oracle 执行SIDH协议，但只反馈 share 是否与初始化相同

每次交互提供 $T_1=\phi_b(P),\ T_2=\phi_b(Q)$

Oracle 计算 $E_{ba}'=E_b/(T_1+sk_a\cdot T_2)$​

反馈 $J(E_{ba}'),J(E_{ba})$ 是否相等

可以利用 $2^i$-torsion 的点泄漏 Alice 私钥的一比特信息

不妨设 $R_i$ 为 $2^{i+1}$-torsion 的点

记 $sk_{a_{l_i}}$ 表示 $sk_a$ 的低 $i$ 比特

$sk_{a_{h_i}}$ 表示 $sk_a$ 除去低 $i$ 比特后的高位

通过提交 $\phi_b(P)-(sk_a)_{l_i}\cdot R_i,\ \phi_b(Q)+R_i$

$T_1+sk_a\cdot T_2=\phi_b(P)-sk_{a_{l_i}}\cdot R_i+sk_a\cdot \phi_b(Q)+(sk_{a_{l_i}}+sk_{a_{h_i}}\cdot R_i=\phi_b(P)+sk_a\cdot \phi_b(Q)+sk_{a_{h_i}}\cdot R_i$

若 $2^{i+1}|(sk_a)_{h_i}\Rightarrow T_1+sk_a\cdot T_2=\phi_b(P)+sk_a\cdot \phi_b(Q)$ ，故反馈 `True`

否则反馈 `False` ，利用这一性质我们能获取 $sk_a$ 的所有比特，由于已知 $sk_b$，我们可以计算出 $J(E_{ba})$

已知密钥后正常进行 AES 解密即可
