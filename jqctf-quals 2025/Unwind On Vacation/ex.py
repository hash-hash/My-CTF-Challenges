from ast import literal_eval
from tqdm import tqdm
from pwn import process, remote
from hashlib import shake_128
from sage.all import *

m, n = 73, 180
q = 0x10001
F = GF(q)

def recv_pk():
    io.recvuntil("🌻 ")
    seed = int(io.recvline())
    set_random_seed(seed)
    pub = []
    for _ in range(m):
        P1 = random_matrix(F, n-m, n-m)
        P2 = random_matrix(F, n-m, m)
        P3 = matrix(F, m, m, literal_eval(io.recvline().decode()))
        pub.append(block_matrix(F, [[P1, P2], [zero_matrix(F, m, n-m), P3]]))
    return pub
        
# io = process(["sage", "task.py"])
io = remote("39.106.16.204", "17131")
pks = recv_pk()

for _ in tqdm(range(79)):
    io.sendlineafter("> ", "R")
    pks.extend(recv_pk())

import time
start_time = time.time()

A = []
u = []
for pk in tqdm(pks):
    a = []
    for i in range(n-m):
        for j in range(i, n-m):
            if i != j:
                a.append(pk[i,j]+pk[j,i])
            else:
                a.append(pk[i,j])
    for i in range(n-m):
        a.append(pk[n-m,i]+pk[i,n-m])
    u.append(pk[n-m,n-m])
    A.append(a)

print(len(A), len(A[0]))
A = matrix(F, A)
u = vector(F, u)

print("[+] Start right kernel...")
ker = A.right_kernel().matrix()[:,-(n-m):]
print("[+] End right kernel...")

print("[+] Start Eq solve...")
x = A.solve_right(-u)[-(n-m):]
print("[+] End Eq solve...")

dim = n-m
H = ker.echelon_form()
A = matrix(ZZ, dim+1, dim+1)
A[:H.nrows(), :dim] = H
A[H.nrows():dim, H.nrows():dim] = identity_matrix(dim-H.nrows())*q
A[dim, :] = matrix(1, dim+1, list(x)+[2**5])
print("[+] Start LLL...")
basis = A.LLL()
end_time = time.time()
print("[+] Time Cost", end_time-start_time)
for item in basis[:10]:
    if abs(item[-1]) == 32:
        print("[+] FIND!", item)
        break
else:
    print("[-] Fail :(")

o1 = vector(F, list(basis[0][:-1])+[1]+[0]*(m-1))
print(o1, o1*pks[0]*o1)

E = zero_matrix(F, len(pks), n)
for i in range(len(pks)):
    E[i,:] = o1*pks[i]
print("E Rank", E.rank())
O = E.right_kernel().matrix().T
print("O row col", O.nrows(), O.ncols())

pub = pks[-m:]

def Hash(msg):
    h = int(shake_128(msg).hexdigest(3*m),16)
    return vector(GF(q),[(h:=h//q)%q if i else h%q for i in range(m)])

def sign(msg, O):
    F = GF(q)
    v = random_vector(F, n, 1)
    M = matrix(F, [v*(pub[i]+pub[i].T)*O for i in range(m)])
    u = Hash(msg.encode())-vector([(v*pub[i]*v) for i in range(m)])
    return v+O*M.solve_right(u)

io.sendlineafter("> ", "V")
io.sendlineafter("📝 ", str(list(sign("Unwind On Vacation", O))))
io.interactive()