## n1share

+ Category: **Crypto**
+ Difficulty: ★★☆
+ Tag: **Polynomial Reconstruction**

## Description

I want to share my key with everyone, but I'm drunk. (　ﾟ∀ﾟ)つ🍷

## Solution

The challenge generate two 127-degree polynomials over $F_{521}$, and evaluates them at $[1..520]$. Then it adds noise in 300 locations. It's actually a $(n,k,w)=(520,128,300)$-RS error-correcting code decoding problem. Considering the general error-correcting algorithm for RS codes:

+ The error-correcting ability of Berlekamp-Welch is $\lfloor\frac{n-k}{2}\rfloor=196$

+ The error-correcting ability of Guruswami-Sudan is $n-\sqrt{nk}\approx 262$

These algorithms' error-correcting ability is less than 300, and they didn't consider errors in the same location.

In fact, it is easy to expand the B-W algorithm to a version that suits this problem, where the error-location $E$ only contributes once to the variables in linear system. On this basis, the error tolerance of B-W can be improved to $\lfloor\frac{c(n-k)}{c+1}\rfloor=261$, which still does not meet the requirements. 

The intended solution is to implement the paper https://people.csail.mit.edu/madhu/papers/2003/copper-conf.pdf. This paper presents a completely different approach from the previously used error-correcting algorithms, which is very interesting.