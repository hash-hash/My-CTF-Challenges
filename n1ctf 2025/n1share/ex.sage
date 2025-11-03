import time
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from itertools import product
import hashlib
from Crypto.Cipher import AES

def compute_column_chunk(args):
    Fp = GF(521)
    start_col, end_col, num_rows, local_points, local_Mr, local_Me, local_vs = args
    
    chunk_A = matrix(Fp, num_rows, end_col - start_col)
    
    for j_local, j_global in tqdm(enumerate(range(start_col, end_col))):
        pt = local_points[j_global // len(local_Mr)]
        idx = j_global % len(local_Mr)
        mono = prod([t**s for t, s in zip(local_vs, local_Mr[idx])])
        
        for i in range(num_rows):
            epow = local_Me[i]
            ff = 1
            for k in range(2 + 1):
                ff *= (local_vs[k] + pt[k])**epow[k]
            
            chunk_A[i, j_local] = ff.monomial_coefficient(mono)
            
    return chunk_A

if __name__ == '__main__':
    p = 521
    n = 520
    c = 2
    l = 1090
    # assert t > l/r 
    t = n-300
    r = 5
    print(t, l//r)
    ks = [128, 128]

    Fp = GF(p)
    PR.<x> = PolynomialRing(Fp)
    f = [PR.random_element(degree=ks[i]) for i in range(c)]

    points = []
    share = ...
    alphas = [Fp(i) for i in range(1, n + 1)]

    for i in range(0, 2*n, 2):
        alpha_i = alphas[i//2]
        points.append([alpha_i] + [share[i], share[i+1]])
    print("Example Generated...")

    Mr = [item for item in product(range(r), repeat=c+1) if sum(item) < r]
    print("[+] Mr Generated...")

    PR_new = PolynomialRing(Fp, ['x']+[f'y{_}' for _ in range(1,c+1)])
    vs = PR_new.gens()

    tmp = list(product(range(l//ks[0]), repeat=c))
    Me = []
    for i in range(l):
        for item in tmp:
            check = i + sum([i*j for i,j in zip(ks,item)])
            if check <= l:
                Me.append([i]+list(item))
    print("[+] Me Generated...")

    print(len(Me), len(Mr)*n)
    assert len(Me) >= len(Mr)*n
    
    total_cols = len(Mr) * n
    num_processes = cpu_count()

    print(f"[+] Starting parallel matrix construction using {num_processes} processes...")
    start_time = time.time()

    chunk_size = (total_cols + num_processes - 1) // num_processes
    tasks = []
    for i in range(num_processes):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, total_cols)
        if start < end:
            tasks.append((start, end, len(Me), points, Mr, Me, vs))

    with Pool(processes=num_processes) as pool:
        results = list(tqdm(pool.imap(compute_column_chunk, tasks), total=len(tasks)))

    print("[+] Parallel computation finished. Assembling final matrix...")
    A = block_matrix([list(results)], subdivide=False)
    end_time = time.time()
    print(f"[+] Matrix constructed in {end_time - start_time:.2f} seconds.")

    rk = sum(A.right_kernel().matrix())
    location = []
    for ei in range(n):
        for i in range(len(Mr)):
            if rk[ei*len(Mr)+i] == 0: continue
            else: break
        else:
            location.append(ei)
    print(location)
    
    y1 = []
    y2 = []
    for i in range(n):
        if i not in location:
            y1.append((i+1, share[2*i]))
            y2.append((i+1, share[2*i+1]))
    key = bytes(PR.lagrange_polynomial(y1))+bytes(PR.lagrange_polynomial(y2))
    ct = bytes.fromhex("251fda75781d082844233d7b5391d1cf97de6dc57e0035ce02db0960ec664552")
    print(AES.new(hashlib.md5(key).digest(), AES.MODE_ECB).decrypt(ct))