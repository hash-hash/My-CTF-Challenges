def ihash(m):
    p = 2^12 * 3^13 - 1
    F = GF(p^2, modulus=x^2+1, name='i')
    E_now = EllipticCurve(j=F(0))
    bits = bin(int(m.hex(), 16))[2:].zfill(8*len(m))
    last = None
    for _ in bits:
        ker = E_now(0).division_points(2)[1:]
        j = [E_now.isogeny(k).codomain().j_invariant() for k in ker]
        if last: j.remove(last)
        E_next = EllipticCurve(j=j[int(_)])
        if E_next.j_invariant() == E_now.j_invariant():
            print("Error Ring, Bad message!")
            return None
        last = E_now.j_invariant(); E_now = E_next
    return E_now.j_invariant()

def ieval(cmd, check_code):
    if ihash(cmd) != check_code:
        print("hacker?")
    else: eval(cmd)

code = ihash(b"print('Welcome 2 n1junior')")
print("Python 3.10.12 [GCC 11.4.0] on linux")
cmd = input(">>> ").encode()
print(cmd)
ieval(cmd, code)