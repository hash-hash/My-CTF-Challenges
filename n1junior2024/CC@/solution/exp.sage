from Crypto.Util.number import *
from pwn import *
import random

target = []
dim = 28
while len(target) < dim:
    io = remote("101.34.72.206", "1338")
    io.sendlineafter("> ", "G")
    io.recvuntil("= ")
    c = eval(io.recvline())
    io.recvuntil("= ")
    p = eval(io.recvline())
    for _ in range(100):
        r = random.randint(1, p)
        io.sendlineafter("> ", "O")
        io.sendlineafter("data: ", str(c[0])+','+str(c[1]*r%p))
        io.recvuntil("[+] ")
        ct = io.recvline()[:-1]
        if len(ct) != 128:
            target.append((r, p))
    io.close()

L = matrix(ZZ, dim+1, dim+1)
L[0, 0] = 2**(504-168)
for _ in range(1, dim+1):
    L[0, _] = target[_-1][0]
    L[_, _] = target[_-1][1]
    
basis = list(L.LLL())
for i in range(len(basis)):
    m = long_to_bytes(abs(basis[i][0])//2**(504-168))
    print(m)
io.interactive()