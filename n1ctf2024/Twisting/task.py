from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from Crypto.Util.number import *
from Crypto.Cipher._mode_gcm import _GHASH, _ghash_portable as ghash_c
import os
FLAG = "n1ctf{REDACTED}"

block_size = 16
pad = lambda X: b'\x00'*(block_size-len(X)%block_size)+X
class Oracle:
    def __init__(self):
        self.key, self.nonce = os.urandom(16), os.urandom(12)
        self.H1 = AES.new(self.key, AES.MODE_ECB).encrypt(b'\x00'*16)
        self.H2 = AES.new(self.key, AES.MODE_ECB).encrypt(b'\x01'*16)
        
    def h(self, a, b, H):
        l = long_to_bytes(len(a), 8)+long_to_bytes(len(b), 8)
        a, b = pad(a), pad(b)
        return _GHASH(H, ghash_c).update(a+b+l).digest()
    
    def encrypt(self, msg, k):
        A, B = msg[:block_size], msg[block_size:]
        S = strxor(AES.new(self.key, AES.MODE_ECB).encrypt(A), self.h(B, k, self.H1))
        E = AES.new(S, AES.MODE_CTR, nonce=self.nonce).encrypt(B)
        G = AES.new(self.key, AES.MODE_ECB).decrypt(strxor(S, self.h(E, k, self.H2)))
        return G.hex(), E.hex(), k.hex()
        
    def decrypt(self, cipher, k):
        G, E = cipher[:block_size], cipher[block_size:]
        S = strxor(AES.new(self.key, AES.MODE_ECB).encrypt(G), self.h(E, k, self.H2))
        B = AES.new(S, AES.MODE_CTR, nonce=self.nonce).decrypt(E)
        A = AES.new(self.key, AES.MODE_ECB).decrypt(strxor(S, self.h(B, k, self.H1)))
        return A.hex(), B.hex()

K = []
sys = Oracle()
k_ = os.urandom(16)
print("🚩", sys.encrypt(f"your flag: {FLAG}".encode(), k_))
for _ in "Nu1L":
    op = input("> ")
    k = bytes.fromhex(input(">> "))
    data = bytes.fromhex(input(">>> "))
    if k not in K:
        K.append(k)
        if op == 'E':
            print(sys.encrypt(data, k))
        elif op == 'D' and k != k_:
            print(sys.decrypt(data, k))
    else:
        print("Hacker?")