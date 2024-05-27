from Crypto.Util.number import *
from Crypto.Cipher import AES
from tqdm import tqdm
from pwn import *

io = remote("146.56.245.60", "1337")

io.recvuntil("🌱 ")
seed = int(io.recvuntil("\n"))
io.sendlineafter("> ", "A")
io.sendlineafter("encrypt msg? y/n ", "n")
ct = bytes.fromhex(io.recvline().decode())

def Gen(k, n, seed):
    F = GF(2^10)
    R.<x> = F[]
    g = x^50 + x^3 + 1
    L = [a for a in F.list() if g(a) != 0]
    set_random_seed(seed)
    G = codes.GoppaCode(g, L).generator_matrix()
    P = Permutations(n).random_element().to_matrix()
    S = random_matrix(GF(2), k, k)
    return S*G*P

Gp = list(Gen(524, 1024, seed).T)
io.sendlineafter("> ", "E")
io.sendlineafter("encrypt msg? y/n ", "n")
c1 = eval(io.recvline())
io.sendlineafter("> ", "E")
io.sendlineafter("encrypt msg? y/n ", "n")
c2 = eval(io.recvline())
index = []
for _ in range(1024):
    if c1[_] == c2[_]:
        index.append(_)

io.close()
for _ in tqdm(range(3*10**3)):
    try:
        right = random.sample(index, 530)
        u = vector(Zmod(2), [c1[i] for i in right])
        Gp_ = matrix(Zmod(2), [Gp[i] for i in right]).T
        key = ''.join([str(i) for i in Gp_.solve_left(u)])
        if key[:512-128] == '0'*(512-128):
            m = AES.new(long_to_bytes(int(key, 2)).rjust(16, b'\x00'), AES.MODE_ECB).decrypt(ct)
            if b'jdctf{' in m:
                print(m)
                break
    except Exception as e:
        continue