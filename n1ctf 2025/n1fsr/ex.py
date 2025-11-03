from sage.all import *
from sage.crypto.boolean_function import BooleanFunction
from sage.parallel.decorate import parallel
from multiprocessing import cpu_count
from Crypto.Util.strxor import strxor
from Crypto.Util.number import *
from tqdm import tqdm
from pwn import *
import time

def int2sbox(n, l):
    sbox = []
    for i in range(l):
        sbox.append(n&1)
        n >>= 1
    return sbox

Ns = [14, 32, 24, 48, 8, 8, 8, 8, 10]
MASKS = [0x7a7, 0xcfdf1bcf, 0xb9ca5b, 0x83c7efefc783, 0x27, 0x65, 0x63, 0x2b, 0x243]
Filters = [
    237861018962211057901759878514586912107,
    69474900172976843852504521249820447513188207961992185137442753975916133181030,
    28448620439946980695145546319125628439828158154718599921182092785732019632576,
    16097126481514198260930631821805544393127389525416543962503447728744965087216,
    7283664602255916497455724627182983825601943018950061893835110648753003906240,
    55629484047984633706625341811769132818865100775829362141410613259552042519543,
    4239659866847353140850509664106411172999885587987448627237497059999417835603,
    85329496204666590697103243138676879057056393527749323760467772833635713704461
]

m = 640
N = 628

PR = BooleanPolynomialRing(names = [f'x{i}' for i in range(1, 7*2+24+1)])
xs = list(PR.gens())
monos = []
for i in range(1, 2**7):
    for k in range(2):
        mono = 1
        for j in range(7):
            if (i >> j) & 1: mono *= xs[j+7*k]
        monos.append(mono)
for i in range(24):
    monos.append(xs[7*2 + i])
monos_map = {mono: i for i, mono in enumerate(monos)}

extract = lambda x, b: [list(x)[i] for i in b]

def mask_mat(mask, n):
    C = matrix(PR, n, n)
    for i in range(n-1):
        C[i, i+1] = 1
    for i in range(n):
        C[n-1, i] = (mask >> i) & 1
    return C

class LFSR:
    def __init__(self, n, state, mask):
        self.n = n
        self.state = state
        self.mask = mask

    def __call__(self):
        b = self.state[0]
        self.state = self.mask * self.state
        return b

@parallel(ncpus=cpu_count())
def ROUND_FUNC(bf):
    u1 = bin(bf)[2:].zfill(10)[:7][::-1]
    u6 = bin(bf)[2:].zfill(10)[7:][::-1]

    A = matrix(GF(2), m+120, N)
    u = [GF(2)(0)] * (m+120)
    lfsr1 = LFSR(12, vector(PR, list(map(int, u1)) + xs[:7]), mask_mat(MASKS[0], 14))
    lfsr9 = LFSR(10, vector(PR, list(map(int, u6)) + xs[7:7+7]), mask_mat(MASKS[8], 10))
    lfsr3 = LFSR(24, vector(PR, xs[14:]), mask_mat(MASKS[2], 24))

    C = identity_matrix(GF(2), 32)
    for i in tqdm(range(m+120)):
        nolinear_part = PR(0)
        vals1 = extract(lfsr1.state, [5, 9, 1, 0, 4, 11, 13])
        sub_dict1 = {f1_vars[j]: vals1[j] for j in range(7)}
        nolinear_part += f1.subs(sub_dict1)

        vals3 = extract(lfsr3.state, [20, 2, 16, 11, 1, 23, 22, 8])
        sub_dict3 = {f3_vars[j]: vals3[j] for j in range(8)}
        nolinear_part += f3.subs(sub_dict3)

        vals9 = extract(lfsr9.state, [5, 8, 9, 3, 1, 0, 2, 4])
        sub_dict9 = {f9_vars[j]: vals9[j] for j in range(8)}
        nolinear_part += f9.subs(sub_dict9)

        for lfsr in [lfsr1, lfsr3, lfsr9]: lfsr()
        for item in nolinear_part.monomials():
            if item == PR(1): u[i] += GF(2)(1)
            else: A[i, monos_map[item]] = 1
        A[i, len(monos)+(i%63)] = 1
        A[i, len(monos)+63+(i%255)] = 1
        A[i, len(monos)+63+255:] = C[0, :]
        C *= C1
    u = vector(GF(2), u)
    return A, u, bf

f1 = BooleanFunction(int2sbox(Filters[0], 128)).algebraic_normal_form()
f3 = BooleanFunction(int2sbox(Filters[1], 256)).algebraic_normal_form()
f9 = BooleanFunction(int2sbox(Filters[7], 256)).algebraic_normal_form()
f1_vars = f1.ring().gens()
f3_vars = f3.ring().gens()
f9_vars = f9.ring().gens()

C1 = mask_mat(MASKS[1], 32).change_ring(GF(2))
tasks = list(range(2**10))
start = time.time()
results = list(ROUND_FUNC(tasks))
end = time.time()
print(f"[+] Time taken: {end - start} seconds")

Mats = [res[1][0] for res in results]
us = [res[1][1] for res in results]
bf = [res[1][2] for res in results]

import time
# io = process(["python3", "chall.py"])
io = remote("60.205.163.215", "11275")
io.recvuntil("ct: ")
ct = io.recvline().strip().decode() 
bits = bin(int(ct[:160], 16))[2:].zfill(640)
c = vector(GF(2), [int(b) for b in bits])
check_msg = bytes.fromhex(ct[160:])

start = time.time()
for i in range(len(Mats)):
    try:
        A = Mats[i][:m,:]; u1 = us[i][:m]; B = Mats[i][m:,:]; u2 = us[i][m:]
        # print(A.dimensions(), A.rank())
        sol = A.solve_right(c-u1)
        msg_mask = B*sol+u2
        print("FOUND SOLUTION")
        end = time.time()
        print(f"[+] Time taken to find solution: {end - start} seconds")
        print(strxor(long_to_bytes(int(''.join(list(map(str, msg_mask))), 2)), check_msg).hex())
        io.sendlineafter("Gimme Token: ", strxor(long_to_bytes(int(''.join(list(map(str, msg_mask))), 2)), check_msg).hex())
        io.interactive()
        break
    except Exception as e:
        continue