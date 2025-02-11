FLAG = "n1ctf{REDACTED}"
ells = [*primes(3, 250), 661]
p = 4 * prod(ells) - 1
F = GF(p**2, 'i')

class Seaside:
    def __init__(self):
        self.pearls = getrandbits(len(ells))
        
    def wave(self, A, Q=0, signal=False):
        E = EllipticCurve(F, [0, A, 0, 1, 0]); Q = E(Q)
        if not signal: priv = [randint(0, 3) for _ in range(len(ells))]
        else: priv = [int(i) for i in bin(self.pearls)[2:].zfill(len(ells))]
        for e, ell in zip(priv, ells):
            for _ in range(e):
                E.set_order((p+1)**2)
                P = self.pebble(E, ell); P.set_order(ell)
                phi = E.isogeny(P)
                E, Q = phi.codomain(), phi(Q)
        Em = E.montgomery_model(); phi = E.isomorphism_to(Em)
        return (Em.a2(), phi(Q))
    
    def pebble(self, E, ell):
        set_random_seed(1337)
        while not (P := (p + 1) // ell * E.random_element()): pass
        set_random_seed(randint(0,p))
        return P

    def tide(self):
        shore = self.wave(0)[0]
        print("Shore", shore)
        return self.wave(shore, input("Seashells > ").split(','), True)[1].xy()
        
    def chall(self):
        if int(input("Pearls > ")) == self.pearls:
            print(FLAG)

alarm(1200)
sys = Seaside()
for _ in range(30):
    print(sys.tide())

sys.chall()