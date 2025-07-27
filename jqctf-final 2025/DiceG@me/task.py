from Crypto.Util.number import *
from hashlib import sha256
import random
FLAG = "flag{redacted}"
Hash = lambda x: int(sha256('.'.join(x).encode()).hexdigest(),16)

def proof(h1, h2, x, N, n):
    u = random.randrange(0, n)
    r = pow(h2, u, N)
    c = Hash(map(str,[h1, h2, r]))
    s = (u+c*x)%n
    return (r, s)

def verify(proof, h1, h2, N, n):
    r, s = proof
    c = Hash(map(str,[h1, h2, r]))
    return pow(h2, s, N) == pow(h1, c, N)*r%N


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
        N, n, h1, h2 = self.params
        return commitment*pow(h1,-self.entropy,N)*pow(h2,-r,N)%N == 1

    def roll(self, other_dice):
        return (self.dice.randint(1,6)+other_dice.dice.randint(1,6))%6

    def Game(self, other_dice):
        ct = 0
        for _ in range(120): 
            ct += self.roll(other_dice)
        print("🎯", ct)
        return ct > 600*0.95

print("Welcome 2 DiceG@me :)")
entropy = "".join(random.choices('⚀⚁⚂⚃⚄⚅', k=32))
for _ in "JQCTF":
    p, q = (getPrime(96) for _ in "pq")
    N, n = p*q, (p-1)*(q-1)
    h1, h2, r, s = map(int, input(f"{N = }\n").split())
    assert verify((r,s), h1, h2, N, n)
    params = N, n, h1, h2
    dice = Dice(entropy.encode(), params)
    cmt, r = dice.commit()
    user_dice = Dice(bytes.fromhex(input(f"{cmt}\n")),None)
    assert dice.open(cmt, r)
    if dice.Game(user_dice): print(FLAG)