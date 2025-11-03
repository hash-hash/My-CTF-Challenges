import tenseal.sealapi as sealapi
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from pwn import *
from tqdm import tqdm

degree = 4096
plain_modulus = sealapi.PlainModulus.Batching(degree, 18)
p = plain_modulus.value()
coeff = sealapi.CoeffModulus.BFVDefault(degree, sealapi.SEC_LEVEL_TYPE.TC128)
parms = sealapi.EncryptionParameters(sealapi.SCHEME_TYPE.BFV)
parms.set_poly_modulus_degree(degree)
parms.set_plain_modulus(plain_modulus)
parms.set_coeff_modulus(coeff)
ctx = sealapi.SEALContext(parms, True, sealapi.SEC_LEVEL_TYPE.TC128)
evaluator = sealapi.Evaluator(ctx)

io = process(["python3", "chall.py"])

io.recvuntil("[enc] ")
key_enc_b64 = io.recvline()[:-1]

open("tmp", 'wb').write(b64decode(key_enc_b64))
key_enc = sealapi.Ciphertext(ctx)
key_enc.load(ctx, "tmp")

omega = ctx.first_context_data().plain_ntt_tables().get_root()
omegas = [pow(omega, 3**i, p) for i in range(degree//2)]+\
    [pow(omega, 2*degree-3**i, p) for i in range(degree//2, degree)]

def mul(n, ct):
    ct_ = sealapi.Ciphertext(ctx)
    if n:
        evaluator.multiply_plain(ct, sealapi.Plaintext(hex(n)[2:]), ct_)
    return ct_

def linear_cipher(coeffs):
    cts = [key_enc] + [sealapi.Ciphertext(ctx) for _ in range(degree-1)]
    for i in range(1,degree):
        evaluator.multiply_plain(key_enc, sealapi.Plaintext(f'1x^{i}'), cts[i])
    res = mul(sum(coeffs)%p, cts[0])
    for i in range(1, degree):
        c = -sum([coeffs[j]*pow(omegas[j], degree-i, p)%p for j in range(len(omegas))])%p
        if c:
            evaluator.add_inplace(res, mul(c, cts[i]))
    return res

C = codes.ReedSolomonCode(GF(p), degree, degree-32)
H = C.parity_check_matrix()
print(H.dimensions())

error_c = []
for i in tqdm(range(32)):
    ct = linear_cipher(H[i].change_ring(ZZ))
    io.sendlineafter("[?] ", "D")
    ct.save("tmp")
    io.sendlineafter("[b64] ", b64encode(open("tmp",'rb').read()).decode())
    io.recvuntil("[*] ")
    error_c.append(int(io.recvline()[:-1]))

b_ = (H.T).solve_left(vector(error_c))
b = C.decode_to_code(b_)
e_recovered = list(b - b_)
if max(e_recovered) > 256:
    e_recovered = [-x%p for x in e_recovered]

key = []
for i in e_recovered:
    if i: key.append(i)
key = bytes(key)
assert len(key) == 16
io.recvuntil("[+] ")
cipher = bytes.fromhex(io.recvline().decode())
nonce = AES.new(key, AES.MODE_ECB).decrypt(strxor(cipher[-16:],b'\x10'*16))[:-8]
print(f"FLAG: {AES.new(key, AES.MODE_CTR, nonce=nonce).decrypt(cipher).decode()}")

io.interactive()