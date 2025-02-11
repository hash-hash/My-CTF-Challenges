from Crypto.Util.number import *
from pwn import *

io = remote("101.34.72.206", 1337)

Integer = lambda x: int(x)
para = eval(io.recvline())
Auth_Code = b"ID: @hash_hash & NOTE: L@zy M@n :)"
g = para['g']; y = para['y']; q = para['q']; p = para['p']
r = (g*y%p)%q
s = r
m0 = (r-2**160*bytes_to_long(Auth_Code))%q
m = 2**160*bytes_to_long(Auth_Code)+m0
io.sendlineafter("Gimme your ticket: ", str(r)+','+str(s)+','+str(m))
io.interactive()