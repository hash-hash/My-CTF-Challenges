from Crypto.Util.strxor import strxor
from Crypto.Util.number import *
from hashlib import md5
import random, os
__import__("signal").alarm(100)
FLAG = "aliyunctf{REDACTED}"

lrot = lambda X,t: (X<<t|X>>(64-t))&(2**64-1)
sbox = lambda X,Sbox: bytes([Sbox[i] for i in X])
pad = lambda X: X+b'\x00'*(block_size-len(X)%block_size)
block_size = 16

class PRF:
    def __init__(self):
        self.key = os.urandom(16)
        self.RK = [self.key]
        self.Sbox = list(range(256))
        random.shuffle(self.Sbox)
        self.round_key()

    def round_key(self, round=30):
        for _ in range(round):
            next_rk = md5(self.RK[-1]).digest()
            self.RK.extend([next_rk[:8], next_rk[8:]])

    def encrypt(self, block, round=30):
        L, R = block[:8], block[8:]
        for i in range(1, 2*round+1, 2):
            T = bytes_to_long(strxor(sbox(L, self.Sbox), self.RK[i]))
            T = (i*T+lrot(T, 17)+bytes_to_long(self.RK[i+1]))%2**64
            L, R = long_to_bytes((T+lrot(T, 20)+bytes_to_long(R))%2**64, 8), L
        return L+R
    
    def cbc_encrypt(self, msg):
        blocks = [msg[i:i+16] for i in range(0, len(msg), 16)]
        result = b'\x00'*16
        for block in blocks:
            result += self.encrypt(strxor(block, result[-16:]))
        return result[16:]

print("😊 PRFCasino is the Game 4 Super Guesser.")
for _ in range(100):
    prf = PRF()
    msg = pad(bytes.fromhex(input("💵 ")))
    ct = [prf.cbc_encrypt(msg), os.urandom(len(msg))]
    decision = random.randint(0,1)
    print("🎩", ct[decision].hex())
    assert input("🎲 ") == str(decision)
print(f"🚩 Real Super Guesser! {FLAG}")