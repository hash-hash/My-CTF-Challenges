ells = [*primes(3, 128), 163]
p = 4*prod(ells)-1
B = QuaternionAlgebra(-1, -p)
i,j,k = B.gens()
O0 = B.quaternion_order([1, i, (i+j)/2, (1+k)/2])

# Oa = 
# Ob = 

Oa = B.quaternion_order(Oa)
Ob = B.quaternion_order(Ob)
I = O0*Oa
Connect_I = (1/I.norm())*I

J = Connect_I.free_module().intersection(span([g.coefficient_tuple() for g in [B(1), j]], ZZ)).basis()
A = matrix(QQ, [e.coefficient_tuple() for e in (Ob.left_ideal([B(j) for j in J]).right_order()).basis()])
print(str(A.list())[1:-1].replace(',',''))