## DiceG@me

- Category: **Crypto**
- Difficulty: ★★
- Solved: 3
- Tag: **Commitment, MT19937, LLL**

## Description

(　ﾟ∀ﾟ)つ 🎲

## Solution

注意到 Commit 中的 $h_1,h_2$ 在某些情况下会泄漏信息，一个简单的想法当 $h_2=1$，这样随机数将完全不起作用。具体来看就是当 $h_2$ 的群阶小于 $h_1$ 时。也就是我们需要在参数选择阶段给出 $h_2=h_1^e,(e,n)\ne1$ 的证明。

```python
def proof(h1, h2, x, N, n):
    u = random.randrange(0, n)
    r = pow(h2, u, N)
    c = Hash(map(str,[h1, h2, r]))
    s = (u+c*x)%n
    return (r, s)
```

题目代码中给出的示例是证明 $h_1=h_2^x$，也就是需要取 $x=\frac{1}{e}\mod n$，考虑到这样的 $x$ 不存在，但是注意到当 $e|c$ 仍然可以伪造出合适的 proof 通过 verify。故可以考虑随机足够次数来撞出这样的 $c$ ，我们可以每次选取大约20比特左右的 $e$。这样可以根据对应的 commitment 泄漏出承诺信息 $entropy\ mod\ e$ 的值

最终根据五次的 CRT 拿到 $entropy\ mod\ lcm(e_i)$

由于 entropy 对应的字节格式，利用 LLL 可以完整还原，之后需要根据 entropy 的随机数结果生成对应的我们需要的随机数种子，这里可以考虑用 z3 或其他工具来解决。