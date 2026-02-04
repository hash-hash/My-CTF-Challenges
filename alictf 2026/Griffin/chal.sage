from Crypto.Random.random import *
from secret import p, a, b
from uuid import uuid4
FLAG = "alictf{"+str(uuid4())+"}"

m, d, k = 80, 20, 250
E = EllipticCurve(GF(p), [a, b])
G = E.lift_x(3137)
G_order = G.order()

PR.<x> = PolynomialRing(Zmod(G_order))
xs = sorted(sample(range(1, 257), 2*d))
fs = [PR([randint(int(0), int(G_order-1)) for _ in range(d)]) for i in range(m)]

Hawk = [[(fs[j](xs[i])*G).xy() for j in range(m)] for i in range(2*d)]
Lion = [[(randint(int(0), int(G_order-1))*G).xy() for j in range(m)] for i in range(k)]
Griffin = Hawk+Lion
shuffle(Griffin)
print(f"{Griffin = }")

flagct = fs[0](int(FLAG.encode().hex(), 16))
print(f"{flagct = }")