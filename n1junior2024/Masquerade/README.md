## Masquerade

+ Category: **Crypto**
+ Difficulty: ★
+ Solved: 7
+ Tag: **DSA**

## Description

Masquerade🎭! Admission by ticket!

## Details

需要完成一个满足格式信息的 DSA 签名伪造，注意到 `Crypto.PublicKey.DSA` 封装的签名默认参数为散列值，在没有哈希函数保护时易遭受存在性伪造攻击

## Solution

签名过程： $s=k^{-1}\cdot (h+r\cdot x)(mod\ q)$

验证过程：

$w = s^{-1}(mod\ q)$	$u_1=w\cdot m(mod\ q)$	$u_2=w\cdot r(mod\ q)$

检查 $r=(g^{u_1}\cdot y^{u_2}(mod\ p))(mod\ q)\ \ (*)$

考虑 $r$ 满足特殊形式 $g^i\cdot y^j(mod\ p)(mod\ q)$

当 $u_1=i(mod\ q)$ 且 $u_2=j(mod\ q)$ 可知 $(*)$ 式满足

固定 $i,j$ 有 $s=j^{-1}\cdot r(mod\ q),\ m=i\cdot s(mod\ q)$

接下来构造满足要求的 $m$

$m=i_0\cdot s+k\cdot q=2^{160}\cdot ac+pad$

$\Rightarrow pad=i_0\cdot s-2^{160}\cdot ac(mod\ q)$

