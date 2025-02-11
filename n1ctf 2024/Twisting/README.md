## Twisting

+ Category: **Crypto**
+ Difficulty: ★★
+ Solved: 4
+ Tag: **XCB attack**

## Description

Block ciphers always felt too rigid for me, so I gave them a lively upgrade. Take a look at my demo : )

## Solution

Referring to recent work about XCB mode analysis.

[How to Recover the Full Plaintext of XCB](https://eprint.iacr.org/2024/1527)

<img src="https://picture-1311455354.cos.ap-shanghai.myqcloud.com/img/image-20241021153622316.png" alt="image-20241021153622316" style="zoom:50%;" />

The paper analysed the CCA security about the tweakable structure. I just add some constraints about tweak, every tweak could just used once. By generalizing the attack in the paper, solutions can be easily found.

Initial state as follows,

$S=U\oplus h_1(B,T),\ V=S\oplus h_2(E,T)$

For Query 1:

Send $G,E$ to decrypt oracle, tweak is $T\oplus \delta_1$. Response is $A_1,B_1$.

$\Rightarrow S_1=S\oplus g_2(0,\delta_1);\ U_1=U\oplus g_1(\Delta_1,\delta_1)\oplus g_2(0,\delta_1);\ V_1=V$

For Query 2:

Send $A_1,B_1$ to encrypt oracle, tweak is $T\oplus \delta_2$. Response is $G_2,E_2$.

$\Rightarrow S_2=S\oplus g_1(0,\sum_{i=1}^2 \delta_i)\oplus g_2(0,\delta_1);\ U_2=U_1;\ V_2=V\oplus g_1(0,\sum_{i=1}^2 \delta_i)\oplus g_2(\Delta_2,\sum_{i=1}^2 \delta_i)$

For Query 3:

Send $G_2,E_2$ to decrypt oracle, tweak is $T\oplus \delta_3$. Response is $A_3,B_3$.

$\Rightarrow S_3=S\oplus g_1(0,\sum_{i=1}^2 \delta_i)\oplus g_2(0,\sum_{i=1}^3 \delta_i);\ U_3=U\oplus g_1(\Delta_1+\Delta_3,\sum_{i=1}^3 \delta_i)\oplus g_2(0,\sum_{i=1}^3 \delta_i);\ V3=V_2$

For Query 4:

Send $A_3,B_3$ to encrypt oracle, tweak is $T\oplus\delta_4$. Response is $G_4,E_4$.

$\Rightarrow S_4=S\oplus g_1(0,\sum_{i=1}^4 \delta_i)\oplus g_2(0,\sum_{i=1}^3 \delta_i)$

Just need to get $c(S)$ to recover $B$. Therefore we need to make $S_i=S$. Because tweak can't be reused, a simple way is make $\sum_{i=1}^3\delta_i=0,\ \delta_4=0$.
