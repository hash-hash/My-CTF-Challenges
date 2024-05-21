from Crypto.Util.number import *
from Crypto.PublicKey import ElGamal
from Crypto.Cipher import AES
import os
FLAG = "ctfpunk{XXXX_FAKE_FLAG_XXXX}"
FLAG = bytes_to_long(FLAG[8:-1].encode())

MENU = """
            /----------------------------\\
            |          options           |
            | [O]racle                   |
            | [G]et FLAG                 |
            \\----------------------------/
        """

class Oracle:
    def __init__(self):
        self.Cipher0 = ElGamal.generate(512, os.urandom)
        self.key = os.urandom(16)
        self.T = 100
    
    def Cipher1(self):
        return AES.new(self.key, AES.MODE_GCM, nonce=os.urandom(16))
    
    def query(self, data):
        assert self.T; self.T -= 1
        C = long_to_bytes(self.Cipher0._decrypt(data))
        return self.Cipher1().decrypt(C)

sys = Oracle()
print(MENU)
while True:
    op = input("> ").lower()
    if op == 'o':
        data = list(map(int, input("data: ").split(',')))
        print(f"[+] {sys.query(data).hex()}")
    if op == 'g':
        r = getRandomNBitInteger(512)
        print(f"[*]\nc = {sys.Cipher0._encrypt(FLAG, r)}\np = {sys.Cipher0.p}")