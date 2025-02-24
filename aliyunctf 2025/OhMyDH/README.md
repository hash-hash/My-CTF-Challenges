## OhMyDH

+ Category: **Crypto**
+ Difficulty: ★★★
+ Solved: 2
+ Tag: **Quaternion, CSIDH**

## Description

OoOh My DH 😯

## Solution

题目中的 action 是 CSIDH 群组行为在四元代数下的实现，曲线同源的安全性在于从曲线计算出其对应自同态环是困难的。

已知 $O_{0},\ O_1=\mathfrak{a}_1\star O_0,\ O_2=\mathfrak{a_2}\star O_0$，计算 $(\mathfrak{a_1a_2})\star O_0$

由于在四元代数下已知两 order，计算 connect ideal 是容易的

一个简单的想法，对于 $O_1,O_2$，理想 $I=span\set{ab|\ a\in O_1,b\in O_2}$，满足对于 $o\in O_1,o\star I\in I;\ o\in O_2,I\star o\in I$

故 $I$ 分别为 $O_1,O_2$ 的右理想和左理想，计算得到 $I$ 后不能直接使用，因为 $Q_{-1,-\infty}$ 下的元素是非交换的，但是 $Q_{-1,-p}$ 实际上可以看作 $Z[\sqrt{-p}]$ 的扩张，因此可以在 $Z[\sqrt{-p}]$ 下找到 $I$ 的嵌入 $I'$，这个操作在实现的时候可以通过计算 $I$ 对应的 Lattice 所张成的空间上在 $i,k$ 处系数为 0 的向量

在得到嵌入 $I'$ 后由于 $Z[\sqrt{-p}]$ 可交换的性质，类似 Diffie-Hellman 的操作即可还原出目标 order

## Reference

[1] Rational isogenies from irrational endomorphisms [↩](https://eprint.iacr.org/2019/1202.pdf)
