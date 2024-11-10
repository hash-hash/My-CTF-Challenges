from pwn import *
from Crypto.Util.strxor import strxor
import os

io = process(["python3", "task.py"])

io.recvuntil("🚩 ")
G, E, k0 = eval(io.recvline())
k0 = bytes.fromhex(k0)
delta1 = os.urandom(16)
delta2 = os.urandom(16)
delta3 = strxor(delta1, delta2)

def oracle(op, k, data):
    io.sendlineafter("> ", op)
    io.sendlineafter(">> ", k)
    io.sendlineafter(">>> ", data)

oracle('D', strxor(k0, delta1).hex(), G+E)
A1, B1 = eval(io.recvline())
oracle('E', strxor(k0, delta2).hex(), A1+B1)
G2, E2, _ = eval(io.recvline())
oracle('D', strxor(k0, delta3).hex(), G2+E2)
A3, B3 = eval(io.recvline())
oracle('E', k0.hex(), A3+B3)
G4, E4, _ = eval(io.recvline())
msg  = strxor(strxor(bytes.fromhex(E4), bytes.fromhex(B3)), bytes.fromhex(E))
print(msg)

io.interactive()