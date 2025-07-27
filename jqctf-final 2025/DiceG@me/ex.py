__import__("os").environ['TERM'] = 'xterm-256color'
from sage.all import *
from hashlib import sha256
from pwn import process, remote
from Crypto.Util.number import *
import random
import recover_seed

io = process(["python3", "task.py"])
# io = remote("39.106.16.204", "36369")

Hash = lambda x: int(sha256('.'.join(x).encode()).hexdigest(),16)
def proof(h1, h2, x, N, n):
    print("[+] start proof...")
    while True:
        u = random.randrange(0, n)
        r = pow(h2, u, N)
        c = Hash(map(str,[h1, h2, r]))
        if c%x == 0:
            print("[+] finish proof!!!")
            s = (u+c//x)%n
            return (r, s)

entropys = []
ns = []

def ROUND():
    io.recvuntil(b"N = ")
    N = int(io.recvline())
    fac = factor(N)
    p, q = fac[0][0], fac[1][0]
    Fp, Fq = GF(p), GF(q)

    h1 = 3
    n1 = Fp(h1).multiplicative_order()
    n2 = Fq(h1).multiplicative_order()
    n = lcm(n1, n2)
    factors = factor(n)
    x = 1
    for i in factors[::-1]:
        if x*i[0]**i[1]<2**25:
            x *= i[0]**i[1]
        if x>2**20:
            break

    print("burp bits:", x.bit_length())
    h2 = pow(h1, x, N)
    pf = proof(h1,h2,x,N,n)
    io.sendline(" ".join(map(str,[h1,h2,pf[0],pf[1]])).encode())
    cmt = int(io.recvline())

    y = pow(cmt, n//x, N)
    g = pow(h1, n//x, N)
    entp = Fp(y).log(Fp(g))
    entq = Fq(y).log(Fq(g))
    entropys.append(int(crt([entp, entq], [GCD(n1, x), GCD(n2, x)])))
    ns.append(x)
    print(entropys, ns)

for _ in range(4):
    ROUND()
    io.sendline(b"aa")
ROUND()

es = (crt(entropys, ns)-bytes_to_long(b'\xe2\x9a\x00'*32))%lcm(ns)
w = 2**128
E = matrix(ZZ, 34, 34)
E[:32,:32] = identity_matrix(32)
E[:32,33] = matrix(ZZ, 32, 1, [pow(2, 24*i, lcm(ns))*w for i in range(32)])
E[32,:] = matrix(ZZ, 1, 34, [0x82]*32+[3]+[es*w])
E[33,33] = lcm(ns)*w
EL = E.BKZ(block_size=30)
for item in EL:
    if abs(item[-2]) == 3 and all(-3<=i<=3 for i in item):
        if 3 in item[:-2] and -3 not in item[:-2]:
            entropy = "".join(['⚀⚁⚂⚃⚄⚅'[i+2] for i in item[:-2]])[::-1]
        else:
            entropy = "".join(['⚀⚁⚂⚃⚄⚅'[-i+2] for i in item[:-2]])[::-1]
        rng = random.Random(bytes_to_long(entropy.encode()))
        dice = [5-rng.randint(1,6)%6 for _ in range(120)]
        for i in range(len(dice)): 
            if not dice[i]: dice[i] = 6
        print("[+] start seed recover...")
        seed = recover_seed.seed_solver(dice, 3)
        io.sendline(long_to_bytes(seed).hex())
        io.interactive()