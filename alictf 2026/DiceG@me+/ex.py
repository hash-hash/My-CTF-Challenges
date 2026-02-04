from Crypto.Util.number import *
from hashlib import sha256
from sage.all import *
from pwn import process, remote
import random
from recover_seed import pure_mt_solver, mt_gen_sol, timeit, state2seed
from z3 import *

# io = process(["python3", "task.py"])
io = remote("223.6.249.127", "32992")

kappa = 128
Hash = lambda x: int(sha256(b'.'.join(x)).hexdigest(),16)

io.recvuntil("N = ")
N = int(io.recvline())
fac = factor(N)
p, q = fac[0][0], fac[1][0]

h2 = 1
alpha = 1
beta = bytes_to_long(bytes([alpha])+b'.'+bytes([alpha]))
h1 = alpha*inverse(beta, N)%N
for l in range(kappa):
    ri = [alpha]*l+[beta]*(kappa-l)
    c = bin(Hash(map(long_to_bytes,[h1, h2]+ri)))[2:][::-1]
    if c[:kappa].count('1') == kappa-l:
        print(f"Found l={l}")
        break

ri = [beta if int(c[i]) else alpha for i in range(kappa)]
si = [1]*kappa
io.sendlineafter("h1, h2: ", f"{h1} {h2}")
io.sendlineafter("> ", str(ri))
io.sendlineafter("> ", str(si)) 

io.recvuntil("cmt = ")
cmt = int(io.recvline())
Fp = GF(p)
Fq = GF(q)
ordp = Fp(h1).multiplicative_order()
ordq = Fq(h1).multiplicative_order()
ep = Fp(cmt).log(Fp(h1))
eq = Fq(cmt).log(Fq(h1))
entropy = crt([ep, eq], [ordp, ordq])
print(f"entropy = {entropy}")

msg_len = 16
dim = 4 * msg_len
g = GCD(3**10, ordp * ordq)
print(f"{g = }")
n = ordp * ordq // g
c = entropy % n

es = (c-bytes_to_long(b'\xe2\x9a\x00'*32))%n
w = 2**128
E = matrix(ZZ, 34, 34)
E[:32,:32] = identity_matrix(32)
E[:32,33] = matrix(ZZ, 32, 1, [pow(2, 24*i, n)*w for i in range(32)])
E[32,:] = matrix(ZZ, 1, 34, [0x82]*32+[3]+[es*w])
E[33,33] = n*w
EL = E.BKZ(block_size=30)
for item in EL:
    if abs(item[-2]) == 3 and all(-3<=i<=3 for i in item):
        if 3 in item[:-2] and -3 not in item[:-2]:
            entropy_ = "".join(['⚀⚁⚂⚃⚄⚅'[i+2] for i in item[:-2]])[::-1]
        else:
            entropy_ = "".join(['⚀⚁⚂⚃⚄⚅'[-i+2] for i in item[:-2]])[::-1]
print(f"Recovered entropy: {entropy_}")

rng = random.Random(bytes_to_long(entropy_.encode()))
dice = [5-rng.randint(1,6)%6 for _ in range(120)]
for i in range(len(dice)): 
    if not dice[i]: dice[i] = 6

state = [BitVec(f"state_{i}", 32) for i in range(624)]
sol = pure_mt_solver()
sol.add(state[0] == 0x80000000)
for s, o in zip(mt_gen_sol(sol, state), dice):
    sol.add(LShR(s, 29) == o-1)
with timeit("z3 solving"):
    assert sol.check() == sat

m = sol.model()
target_state = [m.evaluate(s).as_long() for s in state]

prefix = b"Farewell DiceG@me :("
suffix = b"Welcome DiceG@me+ :)"
magic_seed = state2seed((3,tuple(target_state+[624]),None), prefix, suffix)
io.sendlineafter("spell: ", magic_seed.to_bytes((magic_seed.bit_length() + 7) // 8, 'big').hex())

io.interactive()