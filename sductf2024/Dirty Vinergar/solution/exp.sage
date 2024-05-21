from hashlib import sha256
from tqdm import tqdm
from pwn import *

io = remote("localhost", "53618")
io.recvuntil("toy.part = ")
part = eval(io.recvline())
io.recvuntil("tag1 = ")
tag1 = eval(io.recvline())
io.recvuntil("tag2 = ")
tag2 = eval(io.recvline())
print("RECV FINISH")

F = GF(257)
m = 32; n = 80

def keygen(m, n):
    PM = []
    for i in range(m):
        P1 = random_matrix(F, (n - m), (n - m))
        for j in range(0, n - m):
            for k in range(0, j):
                P1[j, k] = 0
        P2 = random_matrix(F, (n - m), m)
        P3 = matrix(part[i])
        for j in range(0, m):
            for k in range(j+1, m):
                P3[j, k] += P3[k, j]
                P3[k, j] = 0
        P = block_matrix([[P1, P2], [zero_matrix(F, m, (n - m)), P3]])
        PM.append(P)
    return PM
    
def P(x):
    return matrix([list(x.T*A[i]*x)[0] for i in range(m)])

def dot(a, b):
    res = 0
    assert len(a) == len(b)
    for i,j in zip(a, b):
        res += i*j
    return res

with seed(0): A = keygen(m, n)
tag1 = matrix(F, tag1)
tag2 = matrix(F, tag2)
o = tag1-tag2

var = [f'x{i}' for i in range(n-m)]
PR =  PolynomialRing(F, names=var)
x = list(PR.gens())
u = vector(PR, [1]+[0]*(m-1)+x)

poly = []
for i in range(m):
    A_ = vector(PR, list(o*(A[i]+A[i].T)))
    poly.append(dot(A_, u))

for i in range(m):
    A_ = A[i]
    pol = [dot(vec, u) for vec in A_]
    poly.append(dot(pol, u))

Gb = Ideal(poly).groebner_basis()
o2 = matrix(F, n, 1, [1]+[0]*(m-1)+[-list(i)[-1][0] for i in Gb])
O = [list(o[0]), list(o2.T)[0]]

def recover_oil(o1, o2):
    head = [randint(0, 256) for _ in range(m)]
    u = vector(PR, head+x)
    poly = []
    for i in range(m):
        A1_ = vector(PR, list(o1*(A[i]+A[i].T)))
        A2_ = vector(PR, list(o2*(A[i]+A[i].T)))
        poly.append(dot(A1_, u))
        poly.append(dot(A2_, u))
    Gb = Ideal(poly).groebner_basis()
    o = matrix(F, n, 1, head+[-list(i)[-1][0] for i in Gb])
    if P(o) != matrix(m, 1, [0]*m):
        return None
    return list(o.T)[0]

while len(O) < m:
    o_ = recover_oil(o, o2.T)
    if o_:
        O.append(o_)

O = matrix(F, m, n, O).T
print(O.rank())
def H(msg):
    return matrix(F, m, 1, list(sha256(msg).digest()))

def Sign(msg):
    v = random_matrix(F, n, 1)
    M = matrix(F, [list(v.T*(A[i]+A[i].T)*O)[0] for i in range(m)])
    u = H(msg)-P(v)
    x = M.solve_right(u)
    return list((v+O*x).T)

sig = str(Sign(b"Gimme FLAG!!!"))[2:-2]
io.sendlineafter(">", sig)
io.interactive()