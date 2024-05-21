from Crypto.Util.number import *

def ihash(m, sig=0, j=0):
    p = 2^12 * 3^13 - 1
    F = GF(p^2, modulus=x^2+1, name='i')
    E_now = EllipticCurve(j=F(j))
    bits = bin(int(m.hex(), 16))[2:].zfill(8*len(m))
    last = None
    for _ in bits:
        ker = E_now(0).division_points(2); ker.remove(0)
        j = [E_now.isogeny(k).codomain().j_invariant() for k in ker]
        if last: j.remove(last)
        E_next = EllipticCurve(j=j[int(_)])
        if E_next.j_invariant() == E_now.j_invariant():
            print("Error Ring, Bad message!")
            return None
        last = E_now.j_invariant()
        E_now = E_next
    if sig: return last
    return E_now
    
def dp(way, E):
    if len(way) > deepth:
        return 0
    ker = E(0).division_points(2)[1:]
    j_next = [E.isogeny_codomain(k).j_invariant() for k in ker]
    for j in j_next:
        if j not in forward.keys():
            forward[j] = way+[j]
            dp(way+[j], EllipticCurve(j=F(j)))

def dp_find(way, E):
    if len(way) > deepth:
        return 0
    ker = E(0).division_points(2)[1:]
    j_next = [E.isogeny_codomain(k).j_invariant() for k in ker]
    for j in j_next:
        if j in forward.keys():
            col = forward[j]+way[::-1]
            if len(col)%2:
                print("FIND!", len(col))
                try:
                    print(path_decode(col))
                except:
                    continue
        elif j not in back.keys():
            back[j] = way+[j]
            dp_find(way+[j], EllipticCurve(j=F(j)))
        
def path_decode(way):
    p = 2^12 * 3^13 - 1
    F = GF(p^2, modulus=x^2+1, name='i')
    E_now = EllipticCurve(j=way[0])
    bits = ''
    for _ in range(1, len(way)):
        ker = E_now(0).division_points(2); ker.remove(0)
        j = [E_now.isogeny_codomain(k).j_invariant() for k in ker]
        if _ > 1: j.remove(way[_-2])
        else: j.remove(ihash(head, sig=1))
        bits += str(j.index(way[_]))
        E_now = EllipticCurve(j=way[_])
    assert bits[0] == '0'
    return bits

p = 2^12 * 3^13 - 1
F = GF(p^2, modulus=x^2+1, name='i')
E_now = EllipticCurve(j=F(0))  

head = b"__import__('os').system('//bin/sh;"
forward = {}
back = {}
deepth = 16
E_start = ihash(head)
E_end = ihash(b"print('Welcome 2 n1junior")

forward[E_start.j_invariant()] = [E_start.j_invariant()]
back[E_end.j_invariant()] = E_end.j_invariant()
dp([E_start.j_invariant()], E_start)
print("Search")
dp_find([E_end.j_invariant()], E_end)

"""
Search
FIND! 31
FIND! 33
FIND! 33
01010101001101110101001111100011
FIND! 33
01011010110000011000111000111111
FIND! 33
01101010100010011111001101011111
FIND! 33
FIND! 33
01101101001100100001110101000010
FIND! 33
FIND! 31
FIND! 33
FIND! 31
011100101000001101000010000011
FIND! 31
FIND! 33
FIND! 33
"""