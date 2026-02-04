from Crypto.Util.number import *
from ast import literal_eval
from hashlib import sha256
import random
FLAG = "alictf{redacted}"
Hash = lambda x: int(sha256(b'.'.join(x)).hexdigest(),16)

kappa = 128
def proof(h1, h2, x, N, phi):
    ui = [random.randrange(0, phi) for _ in range(kappa)]
    ri = [pow(h2, u, N) for u in ui]
    c = bin(Hash(map(long_to_bytes,[h1, h2]+ri)))[2:][::-1]
    si = [(ui[i]+int(c[i])*x)%phi for i in range(kappa)]
    return (ri, si)

def verify(proof, h1, h2, N):
    ri, si = proof
    c = bin(Hash(map(long_to_bytes,[h1, h2]+ri)))[2:][::-1]
    return all(pow(h2, si[i], N) == pow(h1, int(c[i]), N)*ri[i]%N for i in range(kappa))

class Dice:
    def __init__(self, entropy, params):
        self.entropy = bytes_to_long(entropy)
        self.dice = random.Random(self.entropy)
        self.params = params
        
    def commit(self):
        N, n, h1, h2 = self.params
        r = random.randrange(0,n)
        commitment = (pow(h1,self.entropy,N) * pow(h2,r,N))%N
        return commitment, r
    
    def open(self, commitment, r):
        N, phi, h1, h2 = self.params
        return commitment*pow(h1,-self.entropy,N)*pow(h2,-r,N)%N == 1

    def roll(self, other_dice):
        return (self.dice.randint(1,6)+other_dice.dice.randint(1,6))%6

    def Game(self, other_dice):
        ct = 0
        for _ in range(120): 
            ct += self.roll(other_dice)
        print("🎯", ct)
        return ct > 600*0.95

__import__("signal").alarm(10)
print("Welcome 2 DiceG@me+ :)")
entropy = "".join(random.choices('⚀⚁⚂⚃⚄⚅', k=32))
p, q = (getPrime(80) for _ in "pq")
N, phi = p*q, (p-1)*(q-1)
h1, h2 = map(int, input(f"{N = }\nh1, h2: ").split())
ri, si = [literal_eval(input("> ")) for _ in 'rs']
assert len(ri) == len(si) == kappa
assert verify((ri,si), h1, h2, N)
params = N, phi, h1, h2
dice = Dice(entropy.encode(), params)
cmt, r = dice.commit()
spell = input(f"cmt = {cmt}\nspell: ")
assert spell.startswith(b"Farewell DiceG@me :(".hex())
assert spell.endswith(b"Welcome DiceG@me+ :)".hex())
assert dice.open(cmt, r)
spell_dice = Dice(bytes.fromhex(spell),None)
if dice.Game(spell_dice): print(FLAG)