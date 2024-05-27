from pwn import *
from tqdm import tqdm
from Crypto.Cipher import AES
from hashlib import md5

io = remote("146.56.221.86", "1337")

a, b = 216, 137
p = 2^a*3^b-1
F.<i> = GF(p^2, modulus=x^2+1)
E0 = EllipticCurve(F, [0,6,0,1,0])
P1, P2 = E0.torsion_basis(2^a)
Q1, Q2 = E0.torsion_basis(3^b)
Iso = lambda E,P: E.isogeny(P, algorithm="factored")

io.recvuntil("🔑 sk: ")
skb = int(io.recvline())
S = Q1+skb*Q2
phib = Iso(E0, S)
Eb = phib.codomain()
Pb1, Pb2 = phib(P1), phib(P2)

def send_data(Pl):
    data = [str(i) for i in Pl]
    io.sendlineafter("> ", "K")
    io.sendlineafter("Bob/Image: ", ','.join(data))

def gen_torsion(i):
    while True:
        P = Eb.random_point()*3^b*2^(a-i)
        if P.order() == 2^i:
            return P

def ROUND(i):
    global lsb
    R = gen_torsion(i)
    T1 = Pb1-lsb*R
    T2 = Pb2+R
    send_data(T1.xy()+T2.xy())
    io.recvuntil("KE: ")
    check = io.recvline()
    if b"False" in check:
        return False
    return True

lsb = 0
for i in tqdm(range(1, 217)):
    check = [ROUND(i) for _ in range(6)]
    if all(check):
        if check[0] == True:
            continue
        else:
            lsb += 2^(i-1)
    else:
        lsb += 2^(i-1)
        
io.sendlineafter("> ", "E")
io.recvuntil("C: ")
ct = bytes.fromhex(io.recvline().decode())
S = Pb1+lsb*Pb2
Eba = Iso(Eb, S).codomain()
aes = AES.new(md5(str(Eba.j_invariant()).encode()).digest(), AES.MODE_ECB)
print(aes.decrypt(ct))

io.interactive()