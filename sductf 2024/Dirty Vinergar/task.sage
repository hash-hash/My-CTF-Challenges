from hashlib import sha256
import os
FLAG = os.environ.get("FLAG", "FLAG{XXX_FAKE_FLAG_XXX}")

class OV:
    def __init__(self, m, n):
        self.m = m; self.n = n
        self.O_ = random_matrix(F, (n - m), m)
        self.O = block_matrix(F, 2, 1, [self.O_, identity_matrix(F, m)])
        self.part = []
        with seed(0): self.PM = self.keygen(self.m, self.n)
        self.v = random_matrix(F, n, 1)

    def keygen(self, m, n):
        PM = []
        for i in range(m):
            P1 = random_matrix(F, (n - m), (n - m))
            for j in range(0, n - m):
                for k in range(0, j):
                    P1[j, k] = 0
            P2 = random_matrix(F, (n - m), m)
            P3 = (-self.O_.T * P1 * self.O_ - self.O_.T * P2)
            self.part.append(list(P3))
            for j in range(0, m):
                for k in range(j+1, m):
                    P3[j, k] += P3[k, j]
                    P3[k, j] = 0
            P = block_matrix([[P1, P2], [zero_matrix(F, m, (n - m)), P3]])
            PM.append(P)
        return PM

    def P(self, x):
        return matrix([list(x.T*self.PM[i]*x)[0] for i in range(self.m)])

    def H(self, msg):
        return matrix(F, m, 1, list(sha256(msg).digest()))

    def Sign(self, msg):
        M = matrix(F, [list(self.v.T*(self.PM[i]+self.PM[i].T)*self.O)[0] for i in range(self.m)])
        u = self.H(msg)-self.P(self.v)
        x = M.solve_right(u)
        return list((self.v+self.O*x).T)

    def Ver(self, msg, t):
        msg = self.H(msg)
        for i in range(self.m):
            if t.T*self.PM[i]*t != msg[i][0]:
                return False
        return True

F = GF(257)
m = 32; n = 80
toy = OV(m, n)
print(f"{toy.part = }")
msg1 = b"Cryptography always has many wonderful structures."
msg2 = b"Good cryptographers will understand the secrets."
tag1 = toy.Sign(msg1)
tag2 = toy.Sign(msg2)
print(f"{tag1 = }")
print(f"{tag2 = }")

tag = list(map(int, input("> ").split(',')))
if len(tag) != n: print("error...")
tag = matrix(F, n, 1, tag)
if toy.Ver(b"Gimme FLAG!!!", tag): 
    print(FLAG)