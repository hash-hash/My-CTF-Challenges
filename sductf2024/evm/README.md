## evm

+ Category: **Pwn**
+ Difficulty: ★
+ Tag: **oob, tcache poison**

## Description

So terrible Ethereum gas⛽️ test program.

## Solution

仿 `EVM` 指令的简单 `VM`

利用 `MSTORE` 指令越界存储，修改 `tcache struct` 来达到任意地址写，由于未开 `PIE、RELRO`，考虑分配堆块到 `GOT表`

将 `free` 改成 `system`，利用最后的堆块回收函数 `getshell` 。
