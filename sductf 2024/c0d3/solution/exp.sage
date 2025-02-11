from Crypto.Cipher import AES
from tqdm import tqdm

ct, P, S = load("data.sobj")
q = 1493
F = GF(q)
P = matrix(F, P)
ct = vector(F, ct)
u = ct*P^-1
n = 256
k = 128
t = 65
A = matrix(F, n, n+2)
b = []

for i in range(1, 257):
    for j in range(k+t):
        A[i-1, j] = pow(i, j, q)
    for j in range(t):
        A[i-1, k+t+j] = -int(u[i-1])*pow(i, j, q)%q
    b.append(u[i-1]*pow(i, t, q)%q)

v = A.solve_right(vector(F, b))
ker = A.right_kernel_matrix()
PR.<x> = PolynomialRing(Zmod(q))

def check(v):
    return all([v[i] <= 128 for i in range(128)])

for i in tqdm(range(q)):
    for j in range(q):
        cv = list(v+i*ker[0]+j*ker[1])
        F1 = PR(cv[:k+t]); F2 = PR(cv[-t:])+x^t
        if F1%F2 == 0:
            f = list(F1//F2)
            f = vector(Zmod(q), f+[0]*(128-len(f)))
            msg = f*S^-1
            print(bytes(msg))