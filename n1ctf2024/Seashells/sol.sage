from pwn import process, remote, context
from copy import deepcopy
from tqdm import tqdm

io = remote("120.26.69.200", "41891")
context(log_level="debug")
ells = [*primes(3, 250), 661]
p = 4 * prod(ells) - 1
F = GF(p**2, 'i')
i = F.gen()
A_start = None
A_end = None

def action(A, priv, stop, op=0):
    kernels, phis = [], []
    E = EllipticCurve(F, [0, A, 0, 1, 0])
    for e, ell in zip(priv, ells):
        if len(kernels) == stop: break
        E.set_order((p+1)**2)
        P, D = pebble(E, ell)
        kernels.append(D)
        for _ in range(e):
            P.set_order(ell)
            phi = E.isogeny(P)
            phis.append(phi)
            E = phi.codomain()
    if op:
        return E
    return (kernels, phis)

def pebble(E, ell):
    set_random_seed(1337)
    D = E.random_element()
    while not (P := (p + 1) // ell * D): D = E.random_element()
    return P, D
    
def decision(idx):
    io.recvuntil("Shore ")
    A = eval(io.recvline()[:-1])
    if idx == 0:
        global A_start
        A_start = A
    kers, phis = action(A, key[:start]+[0]*(len(ells)-start), start+1)
    D = kers[idx]
    for phi in phis[::-1]:
        D = phi.dual()(D)
    E = EllipticCurve(F, [0, A, 0, 1, 0])
    E.set_order((p+1)**2)
    D = E(D)
    return D, D.order()


key = [1]*len(ells)
sol = ['?']*len(ells)

start = 0
for _ in tqdm(range(30)):
    print(sol)
    D, n0 = decision(start)
    io.sendlineafter("Seashells > ", str(D.xy())[1:-1])
    x0, y0 = io.recvline()[1:-2].decode().split(',')
    x0, y0 = F(x0), F(y0)
    A = (y0**2-x0**3-x0)*x0**-2
    if start == 0: A_end = A
    E = EllipticCurve(F, [0, A, 0, 1, 0])
    E.set_order((p+1)**2)
    Q_ = E(x0, y0)
    sigs = list(factor(n0//Q_.order()))
    for item in sigs:
        sol[ells.index(item[0])] = 1
    if sol[start] == '?':
        sol[start] = 0
        key[start] = 0
    while sol[start] != '?' and start<len(ells)-1:
        start += 1
        
E_start = action(A_start, key[:start]+[0]*(len(ells)-start), start+1, 1)
E_end = EllipticCurve(F, [0, A_end, 0, 1, 0])
ell_ = ells[start:]
sol_ = sol[start:]
head = sol[:start]

l = sol_.count('?')
j_end = E_end.j_invariant()
numbers = list(range(2**l))
bp_space = list(sorted(numbers, key=lambda x: (bin(x).count('1'), x)))

@parallel(8)
def func(mk):
    bits = deepcopy(sol_)
    mask = bin(mk)[2:].zfill(l)
    for i in range(len(mask)):
        bits[bits.index('?')] = int(mask[i])
    start = 0
    E = E_start
    for i in bits:
        if int(i):
            P = pebble(E, ell_[start])[0]
            P.set_order(ell_[start])
            E = E.isogeny_codomain(P)
        start += 1
    if E.j_invariant() == j_end:
        global head
        head = list(map(str, head))
        bits = list(map(str, bits))
        io.sendlineafter("Pearls > ", str(int(''.join(head+bits), 2)))
        io.interactive()
    return None
            
for result in tqdm(func(bp_space)): pass