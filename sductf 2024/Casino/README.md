## Casino

+ Category: **Crypto**
+ Difficulty: ★☆
+ Tag: **Isogeny**

## Description

Is it true that a successful cryptographer can predict the points of dice 🎲?

## Solution

问题需要根据所给的信息推出此时Isogeny的度数，由于给出了原曲线和映射后的曲线，并且给出了两组点对。

利用 `weil pairing` 的性质

$e(\phi(P),\phi(Q))=e(P,\hat{\phi}\cdot \phi(Q))=e(P,d\cdot Q)=e(P,Q)^d$

只需在 $F_{p^2}$ 下求解离散对数问题即可。
