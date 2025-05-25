from ast import literal_eval
from hashlib import shake_128
import secrets

FLAG = "flag{redacted}"

def Hash(msg):
    h = int(shake_128(msg).hexdigest(3*m),16)
    return vector(GF(q),[(h:=h//q)%q if i else h%q for i in range(m)])

class UOV:
    def __init__(self, m, n, q):
        self.params = (m, n, q)
        self.pub = None
        self.O = random_matrix(ZZ, n-m, m)
        self.refresh()

    def keygen(self):
        set_random_seed(seed:=secrets.randbits(128))
        print("🌻", seed)
        m, n, q = self.params
        F = GF(q)
        Ps = []
        for _ in range(m):
            P1 = random_matrix(F, n-m, n-m)
            P2 = random_matrix(F, n-m, m)
            P3 = (-self.O.T*P1*self.O-self.O.T*P2)
            P = block_matrix(F, [[P1, P2], [zero_matrix(F, m, n-m), P3]])
            print(P3.list())
            Ps.append(P)
        set_random_seed(secrets.randbits(128))
        return Ps

    def refresh(self):
        self.pub = self.keygen()

    def sign(self, msg):
        if msg == "Unwind On Vacation": return None
        m, n, q = self.params
        F = GF(q)
        O = block_matrix(F, 2, 1, [self.O, identity_matrix(F, m)])
        v = random_vector(F, n, 1)
        M = matrix(F, [v*(self.pub[i]+self.pub[i].T)*O for i in range(m)])
        u = Hash(msg.encode())-vector([(v*self.pub[i]*v) for i in range(m)])
        return v+O*M.solve_right(u)

    def verify(self, msg, token):
        msg = Hash(msg.encode())
        t = vector(token)
        for i in range(self.params[0]):
            if t*self.pub[i]*t != msg[i]:
                return False
        return True

m, n = 73, 180
q = 0x10001
uov = UOV(m, n, q)
__import__("signal").alarm(1200)
for _ in range(80):
    match input("> "):
        case "R": uov.refresh()
        case "S": print(f"{uov.sign(input("💬 "))}")
        case "V": print("🚩", uov.verify("Unwind On Vacation",
                                        literal_eval(input("📝 ")))*FLAG)