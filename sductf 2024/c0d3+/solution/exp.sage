from Crypto.Util.number import *
from subprocess import check_output
from re import findall
import time

def flatter(M):
    z = "[[" + "]\n[".join(" ".join(map(str, row)) for row in M) + "]]"
    ret = check_output(["flatter"], input=z.encode())
    return matrix(M.nrows(), M.ncols(), map(int, findall(b"-?\\d+", ret)))

dim = 256
q = 4396148810529520001
ct, Gp = load("data.sobj")
H = Gp.echelon_form()
A = matrix(ZZ, dim+1, dim+1)
A[:dim//2, :dim] = H
A[dim//2:dim, dim//2:dim] = identity_matrix(dim//2)*q
A[dim, :] = matrix(1, dim+1, list(ct)+[128])
print("LLL start!")
start = time.time()
basis = flatter(A)
end = time.time()
print(f"Cost {end-start}")
print("LLL done!")
e = vector(Zmod(q), basis[0][:-1])*(basis[0][-1]//128)
s = list(Gp.solve_left(vector(Zmod(q), ct)-e))
msg = b''
for i in s:
    msg += long_to_bytes(int(i))
print(msg)