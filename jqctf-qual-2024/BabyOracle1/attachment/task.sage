from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import random
import os
FLAG = os.environ.get("FLAG", "jdctf{XXX_FAKE_FLAG_XXX}")

class Oracle:
    def __init__(self, k, n):
        F = GF(2^10)
        R.<x> = F[]
        self.g = x^50 + x^3 + 1
        self.L = [a for a in F.list() if self.g(a) != 0]
        self.Gp = self.Gen(k, n)
        self.t = 160
        self.key = os.urandom(16)

    def Gen(self, k, n):
        seed = random.randrange(0, 2**64)
        print("🌱", seed)
        set_random_seed(seed)
        G = codes.GoppaCode(self.g, self.L).generator_matrix()
        P = Permutations(n).random_element().to_matrix()
        S = random_matrix(GF(2), k, k)
        return S*G*P

    def encode(self, msg):
        e = [random.randrange(0, 2) for _ in range(self.t)]+[0]*(1024-self.t)
        random.shuffle(e)
        return vector(GF(2), msg)*self.Gp+vector(GF(2), e)

    def ENC(self, msg):
        return AES.new(self.key, AES.MODE_ECB).encrypt(msg).hex()

sys = Oracle(524, 1024)
time = 3
print("""[A]ES\n[E]ncode""")
while time:
    time -= 1
    op = input("> ")
    if op == 'A':
        mode = input("encrypt msg? y/n ")
        if mode == 'y':
            msg = bytes.fromhex(input("msg:"))
            print(sys.ENC(pad(msg, 16)))
        elif mode == 'n':
            print(sys.ENC(pad(FLAG.encode(), 16)))
    elif op == 'E':
        mode = input("encrypt msg? y/n ")
        if mode == 'y':
            msg = Integer(input("msg:"), 16)
            word = msg.bits()[::-1]
            print(sys.encode([0]*(524-len(word))+word))
        elif mode == 'n':
            msg = Integer(sys.key.hex(), 16)
            word = msg.bits()[::-1]
            print(sys.encode([0]*(524-len(word))+word))
    else:
        print("Under construction ...")
        break