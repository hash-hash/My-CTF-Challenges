## Dirty Vinegar

+ Category: **Crypto**
+ Difficulty: ★★☆
+ Tag: **UOV**

## Description

The oil is mixed with some dirty vinegar🍾. If you separate it, you will get pure oil🛢️.

## Solution

非平衡油醋方案的醋变量复用，做差即可恢复出一组油变量。需要解决的是利用一组痕迹恢复完整的油变量。

一个简单的想法是利用 polar form 构造有关油变量的线性关系，考虑到油变量是 $m\times n$ 的矩阵，我们可以任意固定 $m$ 个变量，然后求解剩余的 $n-m$ 个变量，利用 $m$ 组线性关系，和 $m$ 组二次关系，这里利用 `Groebner Basis` 可以较快地解决。

在恢复出另一组油变量后，恢复完整的基是简单的，我们收集了足够多的线性方程，下面只需要在满秩下进行解方程即可。

另一种想法是利用类似 KS 算法的操作，具体参考[论文](https://eprint.iacr.org/2023/335)

恢复出完整油变量后，按照UOV流程进行签名即可。
