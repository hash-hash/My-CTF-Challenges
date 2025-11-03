## n1fhe

+ Category: **Crypto**
+ Difficulty: ★★☆
+ Tag: **BFV, NTT, Berlekamp-Welch, CTR Mode**

## Description

Try the freshly baked Fries, Hamburger and Egg tart. (　ﾟ∀ﾟ)つ （🍟🍔🍮）

## Solution

In this challenge, we have two options,

+ encrypt a random polynomial.
+ decrypt any ciphertext, where only partial results are provided.

In the initial phase, pushing 16 bytes key in slots then transformed into polynomial $M$ by INTT. The ciphertext of $M$ is given. We have 32 chances to use oracle. In the end, `FLAG` will be encrypted by AES-CTR using the key.

If we had limitless chances to query, just need to rotate the ciphertext one by one to get the coefficient of $M$, then using NTT to recover key. In fact, in each decryption, we only obtain a linear cmbination of coefficient of $M$.

In the limited-chance case, we could use the characteristic of low hamming weight. 

Considering such a situation, we need to reocover the $e$ given $b=e\cdot H^T$ where $wt(e)=16$. And $H$ is $4096\times 32$ matrix that we can choose. This description is very suitable for error-correcting codes. We can choose the $H$ is the parity-check matrix of Reed-Solomen Codes.

After getting $b$, $b'$ is obtained by solving the equation $b=b'\cdot H^T$. Therefore, $(b'-e)\cdot H^T=0$ which means $b'-e$ is a codeword. In this case, Berlekamp-Welch algorithm can help us correct less than $\lfloor \frac{n-k}{2}\rfloor+1$ errors. 

+ In this challenge, $n=4096,k=4064,wt(e)=16$

So we need to get RS linear combinations of `SLOTS` but not $M$. Because of `encoder.encode` applies INTT to `SLOTS`. This means $M(\omega_i)=e_i=\sum_j a_j\cdot \omega_i^j$. If we want a linear combination of $e_i$, i.e. $\sum_i b_i\cdot e_i=\sum_ib_i\sum_ja_j\cdot \omega_i^j=\sum_j a_j(\sum_i b_i\omega_i^j)$. We just need to rotate the ciphertext and multiply by $b_i$ then decrypting.

In the end, AES-CTR without nonce is also the hidden place in this challenge.

`assert len(FLAG) == 48` means that we will have a known plain block. So decrypt the ciphertext of this block and xor it with the plain to recover the nonce.