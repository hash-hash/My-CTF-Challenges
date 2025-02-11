from extend_mt19937_predictor import ExtendMT19937Predictor
from tqdm import tqdm
from pwn import *

io = process(["python3", "task.py"])

for ROUND in tqdm(range(128)):
    io.sendlineafter("msg: ", "00"*(4*624))
    io.recvuntil("ct: ")
    ct = int.from_bytes(bytes.fromhex(io.recvline().decode()), "little")
    crack = ExtendMT19937Predictor()
    try:
        crack.setrandbits(ct, 32*(624+4))
        io.sendlineafter("[+] ", '1')
    except:
        io.sendlineafter("[+] ", '0')

io.interactive()