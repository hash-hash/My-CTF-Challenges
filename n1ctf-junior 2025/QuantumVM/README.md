## QuantumVM

+ Category: **Crypto**
+ Difficulty: ★★
+ Solved: 3
+ Tag: **Quantum Circuit, LLL**

## Description

Welcome to Quantum World 🧙

## Solution

256个量子比特，初始状态中前 128 个为 $|0\rangle$ 后 128 个为 $|+\rangle$

在最终输出时，会成对地随机过非门，因此在不进行额外电路操作时，可以认为是随机的

注意到 CNOT 门的特殊性质，在控制位为叠加态目标位为 $|0\rangle$ 的情况下会形成纠缠态

$CNOT(|+\rangle,|0\rangle)$ 输出只能为 $|00\rangle$ 或 $|11\rangle$，在过非门后则为 $|01\rangle$ 或 $|10\rangle$，按这种方式操作完所有比特后我们能得到一个二进制下 01 数目一致的输出

由于有非常多这样的输出，可以利用 Lattice 的想法进行还原

构造同态映射 $\phi:(\{0,1\},\oplus)\rightarrow (\set{-1,1},\times)$

$\because m\oplus q_i=c_i\Rightarrow m\oplus c_i=q_i$

$\Rightarrow \phi(m\oplus c_i)=\phi(m)\times \phi(c_i)=q_i(1)-q_i(0)=0$

$q_i(*)$ 指 $q_i$ 中 * 的数目

利用这一等式构造格做 BKZ 即可还原出 $\phi(m)$ 进而还原 $m$
