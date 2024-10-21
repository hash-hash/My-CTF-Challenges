## S2DH+

+ Category: **Crypto**
+ Difficulty: ★★★
+ Solved: 0
+ Tag: **SIDH, Torsion point attack**

## Description

Plz follow the SIDH protocol over my backdoor curve. 🗺️

You can get some idea from the earlier challenge.

`RCTF2022-S2DH`

`*CTF2023-S1DH`

`D3CTF2024-S0DH`

## Solution

$N_1,N_2$ 是特殊选择的，不能直接通过 MITM 求解路径，并且参数没有选择通用的SIDH参数，不能直接使用 Castryck Decru Attack 的代码进行求解。

此处使用的起始曲线 $E_0$ 与 `S2DH` 中的一致，存在一个已知自同构 **I**

$I: (x,y)\rightarrow (-x,i\cdot y)$，且 $deg(I)=1,\ Tr(I)=0$

注意到代码中对 $N_1,N_2$ 的限制 `assert is_square(N2-N1**2)`

$\Rightarrow N_1^2+d^2=N_2$

此处我们需要求解 $sk_a$

构造自同态 $\phi:E_a\rightarrow E_a,\ \phi=\phi_a\cdot I\cdot \hat{\phi_a}+[d]$

$\Rightarrow deg(\phi)=(\phi_a\cdot I\cdot \hat{\phi_a}+[d])\cdot (\hat{\phi_a\cdot I\cdot \hat{\phi_a}+[d]})=N_1^2+d^2=N_2$

由于已知 $\phi_a(P_b),\phi_a(Q_b)\in E_a[N_2],\ P_b,Q_b\in E_0[N_2]$

$\phi(\phi_a(P_b))=\phi_a(I(N_1\cdot P_b))=\phi_a(x_0\cdot P_b+y_0\cdot Q_b)=x_0\cdot \phi_a(P_b)+y_0\cdot \phi_a(Q_b)+d\cdot \phi_a(P_b)$

$\phi(\phi_a(Q_b))$ 同理，由于 $deg(\phi)=N_2$，通过 DLP 求解 $Ker(\phi)$，还原 $\phi$​

取 $E_a$ 上的 `N1-torsion basis` $G_1,G_2$

进一步得出 $\phi_a\cdot I\cdot \hat{\phi_a}(G_1),\ \phi_a\cdot I\cdot \hat{\phi_a}(G_2)$

由于 $deg(\phi_a\cdot I\cdot \hat{\phi_a})=N_1^2$，求解 DLP 得 $Ker(\hat{\phi_a})$，还原 $\phi_a$

再计算 $\phi_a(P_a),\ phi_a(Q_a)$，求解 DLP 得 $sk_a$​，对密文解密。

整体上参考了 `séta` 的思路，但是更一般性的参数构造需要利用四元代数，本题直接从构造方程解出发，考虑的情况更加简单。

## Reference

[Séta: Supersingular Encryption from Torsion Attacks](https://eprint.iacr.org/2019/1291)
