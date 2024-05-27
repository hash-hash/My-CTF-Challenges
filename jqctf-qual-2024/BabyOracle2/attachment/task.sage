from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from hashlib import md5
import os
FLAG = os.environ.get("FLAG", "jdctf{XXX_FAKE_FLAG_XXX}")

a, b = 216, 137
p = 2^a*3^b-1
F.<i> = GF(p^2, modulus=x^2+1)
E0 = EllipticCurve(F, [0,6,0,1,0])
Iso = lambda E,P: E.isogeny(P, algorithm="factored")

class Oracle:
    def __init__(self):
        self.P1, self.P2 = E0.torsion_basis(2^a)
        self.Q1, self.Q2 = E0.torsion_basis(3^b)
        self.Alice, self.Bob, self.aux = self.Gen()
        self.J, self.Eb = self.Set_J()

    def Gen(self):
        ska = randrange(2^a)
        skb = randrange(3^b)
        print("🔑 sk:", skb)
        R = self.P1+ska*self.P2
        S = self.Q1+skb*self.Q2
        phia = Iso(E0, R)
        phib = Iso(E0, S)
        Qa1, Qa2 = phia(self.Q1), phia(self.Q2)
        Pb1, Pb2 = phib(self.P1), phib(self.P2)
        return (R, ska), (S, skb), (Pb1, Pb2, Qa1, Qa2)

    def Set_J(self):
        Alice, Bob = self.Alice, self.Bob
        Ea = Iso(E0, Alice[0]).codomain()
        Ra = self.aux[0]+Alice[1]*self.aux[1]
        Eb = Iso(E0, Bob[0]).codomain()
        Sb = self.aux[2]+Bob[1]*self.aux[3]
        Eba = Iso(Eb, Ra).codomain()
        Eab = Iso(Ea, Sb).codomain()
        assert Eab.j_invariant() == Eba.j_invariant()
        return Eab.j_invariant(), Eb

    def KE(self):
        Pb = input("Bob/Image: ").split(',')
        Pb1, Pb2 = self.Eb(Pb[:2]), self.Eb(Pb[2:])
        Ra = Pb1+self.Alice[1]*Pb2
        return Iso(self.Eb, Ra).codomain().j_invariant() == self.J

    def ENC(self, msg):
        aes = AES.new(md5(str(self.J).encode()).digest(), AES.MODE_ECB)
        return aes.encrypt(pad(msg.encode(), 16)).hex()

sys = Oracle()
print("""[E]nc FLAG 🔐\n[K]ey Exchange ♻️""")
while True:
    op = input("> ")
    if op == 'E':
        print("C:", sys.ENC(FLAG))
    elif op == 'K':
        print("KE:", sys.KE())
    else:
        print("Under construction ...")
        break