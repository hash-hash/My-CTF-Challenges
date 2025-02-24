from ast import literal_eval
FLAG = "aliyunctf{REDACTED}"

ells = [*primes(3, 128), 163]
p = 4*prod(ells)-1
B = QuaternionAlgebra(-1, -p)
i,j,k = B.gens()
O0 = B.quaternion_order([1, i, (i+j)/2, (1+k)/2])

def action(O, priv):
    for i,ell in zip(priv,ells):
        for _ in range(abs(i)):
            O = O.left_ideal([ell, j-sign(i)]).right_order()
    ω = sum((O0*O).basis())
    α = ω[0]+ω[2]*j
    return B.quaternion_order((α*O*~α).basis())

priv_a = [randint(-5, 5) for _ in range(len(ells))]
priv_b = [randint(-5, 5) for _ in range(len(ells))]
O_start = action(O0, literal_eval(input("start:")))
Oa = action(O_start, priv_a)
Ob = action(O_start, priv_b)

alarm(60)
print("Oa:", Oa.basis())
print("Ob:", Ob.basis())
Os = [QQ(e) for e in input("Os: ").split()]
Oshare = B.quaternion_order([B(Os[i:i+4]) for i in range(0,len(Os),4)])
assert Oshare.isomorphism_to(action(Oa, priv_b))
print("🚩 Ohhhhh DH master!", FLAG)