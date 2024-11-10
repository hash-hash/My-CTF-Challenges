## Seashells

+ Category: **Crypto**
+ Difficulty: ★★
+ Solved: 4
+ Tag: **Isogeny**

## Description

Searching for  Seashells🐚 by the seaside🏝️ : )

## Solution

This problem is unrelated to CSIDH. The action group isn't commutative in $F_{p^2}$.

The curve will walk with our input point $Q$. This operation may lower the order of $Q$.  Interestingly, I found that this observation has already been reflected in [ImaginaryCTF 2024] coast. But the difference is the field is $F_{p^2}$. When $e(P,Q)=1$, the map $\phi:E\rightarrow E/P$ will cause the order of $\phi(Q)$  is lower than $Q$.

Therefore we need to select appropriate points based on kernel rather than random points then pull them back to the start curve. We can get more than 1 bit of secret key in a round. Howerver, it's clear that 30 rounds make it difficult to obtain all the information in this way. In tests, about 45 bits can be obtained. Only a small-scale brute force is needed to obtain the remaining bits of pearls.
