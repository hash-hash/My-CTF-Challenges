## DiceG@me+

+ Category: **Crypto**
+ Difficulty: ★★☆
+ Tag: **Commitment, MT19937, LLL**

## Description

I fixed the vulnerability in DiceG@me, try the safer DiceG@me+? (　ﾟ∀ﾟ)つ 🎲

## Solution

在 [DiceG@me](https://github.com/hash-hash/My-CTF-Challenges/tree/main/jqctf-final%202025/DiceG%40me) 基础上做了一定调整

+ fix 了此前 DiceG@me 中存在的问题，修改为了 128 轮的 `0/1` flip
+ 对 random 的 seed 做了额外约束

Random.seed 的部分可以参考 https://stackered.com/blog/python-random-prediction/#introduction，seed 加上限制可以参考 https://soon.haari.me/2023-christmas-ctf/ ，其中给出了前缀的想法。由前缀的思路得到后缀思路是自然的。需要先固定住 seed 要控的前后缀，中间待定。从需要满足的输出对应的 state 往回推到使用 key 的逻辑后。现在需要推 key 的中间段使得一个初始状态 $state_1$ 在过完混合 key 的过程后能过渡到 $state_2$。注意到 key 的使用是从前往后按顺序计算的，在确定完前后缀之后我们能把 $state_1,state_2\rightarrow state_1’,state_2’$，这个过程只需要中间段有超过 624 个 key entry 可控即可，用这些补齐两个状态的差值。

对于第一部分的 proof，需要注意到 DiceG@me+ 相比 DiceG@me 将 `Hash(map(str,[h1, h2, r]))` 改为了 `Hash(map(long_to_bytes,[h1, h2]+ri))` 这导致了 ambiguous coding 的漏洞。例如 `Hash(b'\x01'+b'.'+b'\x01.\x01'])` 和 `Hash(b'\x01.\x01'+b'.'+b'\x01'])` 最终结果一致。

构造的大体方向和 [DiceG@me](https://github.com/hash-hash/My-CTF-Challenges/tree/main/jqctf-final%202025/DiceG%40me) 一致，还是试图伪造 $h_2=1,h_1\neq 1$ 的 proof。

绕过方式是构造 $r_i$ 为 1 或者 `a = b2l(b'\x01.\x01')` 中的一种，$h_1=a^{-1}mod\ N$，当选择的 $r$ 序列确定，调换 $r_i$ 中任意元素顺序都不会影响 $c$ 的最终结果，所以只要 $c$ 中 $0/1$ 个数和 $r$ 中 `1/a` 个数一致，最终就可以通过调整 $r$ 序列中的顺序让 128 次检查都通过。后续按照原来 DiceG@me 的逻辑做即可。

