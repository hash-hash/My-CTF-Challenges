from subprocess import check_output
import mersen
from Crypto.Cipher import AES
from hashlib import md5
from re import findall
from tqdm import tqdm

def flatter(M):
    z = "[[" + "]\n[".join(" ".join(map(str, row)) for row in M) + "]]"
    ret = check_output(["flatter"], input=z.encode())
    return matrix(M.nrows(), M.ncols(), map(int, findall(b"-?\\d+", ret)))

n, q = 60, 2**521-1
F, Fq = Zmod(256), GF(q)
mat = load("mat.sobj")
with open("tedious", "rb") as f:
    data = eval(f.read())
π = matrix(Fq, data['π'])
α = matrix(Fq, data['α'])

N = 256
m = 30
w = 2**2048
c = matrix(m, N, list(π)[:m//2]+list(α)[:m//2])
C = matrix(ZZ, N+m)
C[:N,:N] = identity_matrix(N)
C[:N,N:] = matrix(ZZ, N, m, c.T)*w
C[N:,N:] = identity_matrix(m)*q*w
num = N-80
CL = flatter(C)[:num]

B = matrix(ZZ, N+num)
B[:N,:N] = identity_matrix(N)
B[:N,N:] = CL[:,:N].T*w
B[N:,N:] = identity_matrix(num)*q*w
BL = flatter(B)[:80]

τ = []
for i in range(n):
    AA = matrix(Fq, 81, N, list(BL[:,:N])+[α[i]])
    u = π[i]
    τ.append(list(AA.solve_left(u))[-1])

nums = []
def move(m, t):
    for i in range(t):
        nums.append(m%(2**32))
        m = m>>32

for i in τ:
    move(int(i), 16)
    
ut = mersen.Untwister()
for i in range(60):
    for j in range(16):
        ut.submit(bin(nums[16*i+j])[2:])
    ut.submit('?'*32)

r = ut.get_random()
σ = matrix(Fq, [[r.randrange(1, q) for i in range(80)] for j in range(n)])
ε = matrix(n, N, [i*j for i,j in zip(α, τ)])
π -= ε

A = []
abs_vec = lambda l: [abs(int(i)) for i in l]
for i in tqdm(π.T):
    D = matrix(ZZ, 80+n//6+1)
    D[:80,:80] = identity_matrix(80)
    D[80, 80] = 4
    D[:80,81:] = σ[:n//6,:].T
    D[80,81:] = matrix(i)[:,:n//6]
    D[81:,81:] = identity_matrix(n//6)*q
    DL = flatter(D)    
    A.append(abs_vec(DL[0][:80]))

A = matrix(A).T
result = []
for i in range(0, 80, 4):
    result.append(vector(F, 1024, list(A[i])+list(A[i+1])+list(A[i+2])+list(A[i+3])))

S = []
F2 = GF(2)
div2 = lambda x: [int(i)//2 for i in x]

@parallel(10)
def sdp_solver(a, c):
    cg = c
    a2 = a.change_ring(F2)
    D = LinearCode(a2).decoder('InformationSet', 18)
    e = []
    
    for _ in range(7):
        c2 = c.change_ring(F2)
        d2 = D.decode_to_code(c2)
        e2 = d2-c2; e.append(list(e2))
        s2 = a2.solve_left(d2)
        c = vector(F, div2(c-e2.change_ring(F)-s2.change_ring(F)*a))

    c2 = c.change_ring(F2)
    d2 = D.decode_to_code(c2)
    e2 = d2-c2
    e.append(list(e2))
    recover_e = [0]*1024
    for i in range(len(e)):
        for j in range(1024):
            recover_e[j] += int(e[i][j])*2**i
    return a.solve_left(cg-vector(F, recover_e))

for rs in tqdm(sdp_solver([(mat[i], result[i]) for i in range(20)])):
    S.append(rs[-1])

cipher = AES.new(md5(str(sum(S)).encode()).digest(), AES.MODE_ECB)
enc = "af3010a3de0fa968c38f421f2857d6c60caf9a6ae1023e9d04f253e1d5fb8038fddf26f7cc976fadbb2df12ef549d1fd"
print(cipher.decrypt(bytes.fromhex(enc)))