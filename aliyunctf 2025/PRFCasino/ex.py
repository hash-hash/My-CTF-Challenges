from tqdm import tqdm
from pwn import *

io = process(["python3", "task.py"])

for rd in tqdm(range(100)):
    distribution = [0]*17
    io.sendlineafter("💵 ", '00'*(16*500))
    io.recvuntil("🎩 ")
    ct = io.recvline()[:-1].decode()

    for i in range(32, len(ct), 32):
        mask = ct[i-32:i]
        tmp = ct[i:i+32]
        distribution[(int(tmp[:16], 16)-int(mask[:16], 16))%17] += 1
        distribution[(int(tmp[16:], 16)-int(mask[16:], 16))%17] += 1
    if distribution[2]-distribution[11] > 100:
        io.sendlineafter("🎲 ", '0')
    else:
        io.sendlineafter("🎲 ", '1')

io.interactive()