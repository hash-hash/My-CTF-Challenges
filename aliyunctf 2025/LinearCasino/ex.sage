from tqdm import tqdm
from pwn import *

io = process(["sage", "task.sage"])
for _ in tqdm(range(100)):
    io.recvuntil("🎩 ")
    mat = matrix(Zmod(2), 110, 200, list(bin(int(io.recvline()))[2:].zfill(110*200)))
    if len(span(mat).intersection(span(mat.right_kernel().matrix())).basis()) > 5:
        io.sendlineafter('🎲 ', '1')
    else:
        io.sendlineafter('🎲 ', '0')
    
io.interactive()