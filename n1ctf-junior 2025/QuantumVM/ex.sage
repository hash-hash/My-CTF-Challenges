from Crypto.Util.number import *
from Crypto.Cipher import AES
from pwn import *

io = process(["python3", "src.py"])

code = b''
for i in range(128):
    code += b'\x03'+bytes([i])

C = []
dim = 150
for _ in range(dim):
    io.sendlineafter("Quantum Code > ", code.hex())
    io.recvuntil("⚙️ ")
    C.append(int(io.recvline()))

io.recvuntil("🚩 ")
ct = bytes.fromhex(io.recvline().decode())

w = 2**32
M = matrix(ZZ, 256, 256+dim)
M[:256,:256] = identity_matrix(256)
for i in range(len(C)):
    ci = bin(C[i])[2:].zfill(256)
    for j in range(256):
        if int(ci[j]): M[j,256+i] = w
        else: M[j,256+i] = -w

print("BKZ start...")
ML = M.BKZ(block_size=20)
print("BKZ end...")

for item in ML:
    tmp = list(item)
    if tmp[256:].count(0) == dim and tmp[:256].count(-1)+tmp[:256].count(1) == 256:
        key = ''
        for i in tmp[:256]:
            if i == 1: key += '1'
            else: key += '0'
        key1 = long_to_bytes(int(key,2))
        print(AES.new(key1, AES.MODE_ECB).decrypt(ct))
        key2 = long_to_bytes(int(''.join(['1' if c == '0' else '0' for c in key]),2))
        print(AES.new(key2, AES.MODE_ECB).decrypt(ct))
        
io.interactive()