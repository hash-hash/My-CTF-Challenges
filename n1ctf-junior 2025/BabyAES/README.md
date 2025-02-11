## BabyAES

+ Category: **Crypto**
+ Difficulty: ★
+ Solved: 12
+ Tag: **MT19937**

## Description

Did AES random enough 😱

## Solution

输入一个足够长的 msg，来得到非常长的 MT19937 序列，根据序列的前面状态判断后续状态是否吻合。

这里需要判断 random 库的 randbytes 函数，注意大小端序即可。

```python
def randbytes(self, n):
    """Generate n random bytes."""
    return self.getrandbits(n * 8).to_bytes(n, 'little')
```