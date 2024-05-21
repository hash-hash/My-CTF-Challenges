from pwn import *

io = remote("localhost", "63030")
context.log_level="debug"
p = 2^36 * 3^49 - 1
F.<i> = GF(p^2, modulus=x^2+1)
for _ in range(100):
    io.recvuntil("Cruve: ")
    E0 = EllipticCurve(F, eval(io.recvline()))
    io.recvuntil("Shake the dice: ")
    E1 = EllipticCurve(F, eval(io.recvline()))
    io.recvuntil("visus: ")
    point = eval(io.recvline())
    P1 = E0(point[0]); Q1 = E0(point[1])
    P2 = E1(point[2]); Q2 = E1(point[3])
    n = lcm(P1.order(), Q1.order())
    s1 = P1.weil_pairing(Q1, n)
    s2 = P2.weil_pairing(Q2, n)
    dg = s2.log(s1)
    io.sendlineafter("Bet > ", str(dg))

io.interactive()