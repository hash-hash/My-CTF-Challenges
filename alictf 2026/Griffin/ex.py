import itertools
from Crypto.Util.number import *
from string import ascii_lowercase
from tqdm import tqdm
from ast import literal_eval
from multiprocess import Pool
from sage.all import *

m, d, k = 80, 20, 250
with open("output.txt") as f:
    Griffin = literal_eval(f.readline()[10:])
    flagct = literal_eval(f.readline()[9:])

PR = PolynomialRing(ZZ, ['a', 'b'])
a,b = PR.gens()
polys = []
for i in range(10):
    x0, y0 = Griffin[0][i]
    f = x0**3+a*x0+b-y0**2
    polys.append(f)
    
gb = Ideal(polys).groebner_basis()
p = int(gb[-1])
A = -gb[0].coefficients()[-1]%p
B = 0
print(p, A, B)

E = EllipticCurve(GF(p), [A, B])
E.set_order(p+1)
n = int(E.order())
G = E.lift_x(GF(p)(3137))

@parallel(12)
def ecdlog(i, j, Q, P):
    return discrete_log(Q, P, operation='+')

Griffin_N_Z = matrix(ZZ, m, 2*d+k)

tasks = []
for i in tqdm(range(m)):
    for j in range(2*d+k):
        tasks.append((i, j, E(Griffin[j][i]), G))

for inputs, result in tqdm(ecdlog(tasks)):
    i, j = inputs[0][0], inputs[0][1]
    Griffin_N_Z[i, j] = result


def ISD_once(H, k, n, w, know):
    Iset = [i for i in range(n) if i not in know]
    I = sample(Iset, k-len(know))+know
    Hi = H.matrix_from_columns(I)
    hk = Hi.rank()
    if hk != k:
        target = []
        for j in range(k):
            Hsub = Hi.matrix_from_columns([idx for idx in range(k) if idx != j])
            if Hsub.rank() == hk:
                target.append(j)
                if len(target) > w: return None
        return [I[t] for t in target]
    return None

def PISD_parallel(H, w, know, max_tries=2**18, workers=12, show_progress=True):
    k, n = int(H.nrows()), int(H.ncols())
    
    def ISD_wrapper(_):
        return ISD_once(H, k, n, w, know)
    
    with Pool(processes=workers) as pool:
        results = pool.imap_unordered(ISD_wrapper, range(int(max_tries)))

        if show_progress:
            results = tqdm(results, total=int(max_tries))

        for res in results:
            if res is not None:
                pool.terminate()
                return res
    return []

Griffin_N = Griffin_N_Z.change_ring(GF(66179))
location_part = []
location = PISD_parallel(Griffin_N, 2*d, location_part)
print("Found locations:", location)
tmp = Griffin_N.matrix_from_columns(location)
for i in range(Griffin_N.ncols()):
    if i not in location:
        try:
            u = Griffin_N.matrix_from_columns([i])
            if tmp.solve_right(u): location.append(i)
        except Exception as e:
            continue
print(f"{location = }")

H = Griffin_N.matrix_from_columns(location)
H1 = H[:d,:].matrix_from_columns(range(0,d-1))
H2 = H[:d,:].matrix_from_columns(range(1,d))
ker1 = H1.left_kernel().matrix()
ker2 = H2.left_kernel().matrix()

q = 66179
single = d
F1_alpha = int((ker1*H[:d,single])[0,0])
F2_alpha = int((ker2*H[:d,single])[0,0])

for i1 in tqdm(range(1,257)):
    for i2 in range(1,257):
        for i3 in range(1,257):
            if (i1-i2)*(i2-i3)*(i3-i1) == 0:
                continue
            tmp = (i3-i1)*inverse_mod(i3-i2, q)%q
            rate = F1_alpha*inverse_mod(F2_alpha*tmp, q)%q
            candidate = [i1, i2, i3]
            for check in range(d,2*d):
                if check == single:
                    continue
                F1_ = int((ker1*H[:d,check])[0,0])
                F2_ = int((ker2*H[:d,check])[0,0])
                try:
                    alphak = (F2_*rate*i1-F1_*i2)*inverse_mod(rate*F2_-F1_, q)%q
                    if alphak > 256:
                        break
                    candidate.append(alphak)
                except:
                    break
            else:
                print(candidate)


##################

candidate = [214, 107, 132, 249, 85, 227, 168, 250, 5, 235, 196, 16, 143, 189, 173, 95, 163, 65, 0, 61, 247, 31]


def check_candidate(candidate):
    H1 = H[:d,:].matrix_from_columns([i for i in range(d,2*d-2)]+[2*d-2])
    H2 = H[:d,:].matrix_from_columns([i for i in range(d,2*d-2)]+[2*d-1])
    ker1 = H1.left_kernel().matrix()
    ker2 = H2.left_kernel().matrix()
    F1_alpha = int((ker1*H[:d,d-1])[0,0])
    F2_alpha = int((ker2*H[:d,d-1])[0,0])
    i1 = candidate[-2]
    i2 = candidate[-1]
    i3 = candidate[1]
    tmp = (i3-i1)*inverse_mod(i3-i2, q)%q
    rate = F1_alpha*inverse_mod(F2_alpha*tmp, q)%q
    candidate = []
    for check in range(1, d-1):
        F1_ = int((ker1*H[:d,check])[0,0])
        F2_ = int((ker2*H[:d,check])[0,0])
        alphak = (F2_*rate*i1-F1_*i2)*inverse_mod(rate*F2_-F1_, q)%q
        if alphak > 256:
            return None
        candidate.append(alphak)
    print(candidate)
    return candidate

add = lambda x: [xi+1 for xi in x]
xs_shuffle = []
for _ in range(30):
    ext = check_candidate(candidate)
    if ext:
        xs_shuffle = [candidate[0]]+ext+candidate[1:]
        candidate.extend(ext)
        break
    candidate = add(candidate)

xs = sorted(xs_shuffle)
H_Z = Griffin_N_Z.matrix_from_columns(location)
H_real = H_Z.change_ring(Zmod((p+1)//4)).matrix_from_columns([xs_shuffle.index(i) for i in xs])

def msg_crack(c):
    n, dim = (p+1)//4, 64
    w = 2**64
    
    c = (c-bytes_to_long(b"alictf{")*256**37-bytes_to_long(b"}")*256**0)%n
    c = (c-bytes_to_long(b"-")*(256**13+256**18+256**23+256**28))%n
    M = matrix(ZZ, dim+2, dim+2)
    for i in range(dim):
        M[i, i] = 8 if i % 2 == 0 else 1
    
    powers = list(range(2, 26))+list(range(28,36))+list(range(38,46))+list(range(48,56))+list(range(58, 74))
    M[dim, :] = matrix(1, dim+2, [-12, -4] * (dim//2) + [4] + [-(c*inverse_mod(3, n) % n) * w])
    M[:dim, dim+1] = matrix(dim, 1,
        [(2**(4*i) * inverse_mod(3**((i+1)%2), n) % n) * w for i in powers][::-1]
    )
    M[dim+1, dim+1] = n*w
    
    M = M.LLL()[:-1, :-1]
    ML = M.BKZ(block_size=30)
    
    def check_vec(u):
        return all(-5 <= i <= 5 for i in u)
    
    ML0 = ML[0][:-1]
    if check_vec(list(ML0)):
        print("good")
        msg = []
        for idx in range(0, len(ML0), 2):
            head = ML0[idx]
            tail = ML0[idx+1]
            head = (head+12)//8*3
            tail = tail+4
            msg.append((head<<4)+tail)
        print(bytes(msg))

PR.<x> = PolynomialRing(Zmod((p+1)//4))

for offset in (range(0,15)):
    try:
        V = matrix(Zmod((p+1)//4), d, 2*d)
        for j in range(2*d):
            for i in range(d):
                V[i,j] = pow(xs[j]+offset, i, (p+1)//4)
        # print(V[1])
        f = list(V.solve_left(H_real.matrix_from_rows([0]))[0])
        # print(f)
        h = PR(f)-flagct
        rts = h.roots(multiplicities=False)
        for c in tqdm(rts):
            msg_crack(int(c))
        # break
    except Exception as e:
        print(str(e))
        continue