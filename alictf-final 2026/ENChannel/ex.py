from pwn import *
import tenseal.sealapi as sealapi
from base64 import b64decode, b64encode
from Crypto.Util.number import *
import ast, hashlib, copy, time
from tqdm import tqdm

degree = 16384
coeff = sealapi.CoeffModulus.BFVDefault(degree, sealapi.SEC_LEVEL_TYPE.TC128)
parms = sealapi.EncryptionParameters(sealapi.SCHEME_TYPE.BFV)
parms.set_poly_modulus_degree(degree)
parms.set_plain_modulus(0x10001)
parms.set_coeff_modulus(coeff)
ctx = sealapi.SEALContext(parms, True, sealapi.SEC_LEVEL_TYPE.TC128)
evaluator = sealapi.Evaluator(ctx)

io = process(["python3.13", "task.py"])
# io = remote("223.6.249.127", "24379")

io.recvline()
packets = []
while True:
    res = io.recvline()
    if "👻" not in res.decode():
        open("tmp", 'wb').write(b64decode(res))
        ciphertext = sealapi.Ciphertext(ctx)
        ciphertext.load(ctx, "tmp")
        packets.append(ciphertext)
    else: break
    print("[+] packet received...")

# io.interactive()
io.sendlineafter("ells: ", str([2**l+1 for l in range(1, 14+1)]))
galois_keys = sealapi.GaloisKeys()
res = io.recvline()
open("tmp", 'wb').write(b64decode(res))
galois_keys.load(ctx, "tmp")
print("[+] galois key received...")

target = None
cs = []
for i in tqdm(range(len(packets))):
    for j in range(16):
        ct = sealapi.Ciphertext()
        evaluator.multiply_plain(packets[i], sealapi.Plaintext(f'1x^{degree-j-1}'), ct)
        evaluator.multiply_plain(ct, sealapi.Plaintext(f'1x^{degree-1}'), ct)
        evaluator.multiply_plain(ct, sealapi.Plaintext(f'1x^{2}'), ct)
        cs.append(ct)

def RLWEpack(cs, l):
    assert len(cs) == 2**l
    if l == 0:
        return cs[0]
    else:
        ct_even = RLWEpack(cs[::2], l-1)
        ct_odd = RLWEpack(cs[1::2], l-1)
        tmp = sealapi.Ciphertext()
        evaluator.multiply_plain(ct_odd, sealapi.Plaintext(f'1x^{degree//2**l}'), tmp)
        ct0 = sealapi.Ciphertext()
        ct1 = sealapi.Ciphertext()
        evaluator.add(ct_even, tmp, ct0)
        evaluator.sub(ct_even, tmp, ct1)
        evaluator.apply_galois(ct1, 2**l+1, galois_keys, ct1)
        ct = sealapi.Ciphertext()
        evaluator.add(ct0, ct1, ct)
        return ct

print(len(cs))
tmp = cs[-1]
while len(cs) < 256:
    cs.append(tmp)
print(len(cs))

start = time.time()
target = RLWEpack(cs, 8)
end = time.time()
print("RLWEpack cost", end-start)

target.save("tmp")
io.sendlineafter("[b64] ", b64encode(open("tmp",'rb').read()).decode())
io.recvuntil("✉️  ")
decrpted = ast.literal_eval(io.recvline()[:-1].decode())
inv = inverse(256, 0x10001)

dialogue = b""
for item in decrpted:
    msg = long_to_bytes(item*inv%0x10001)
    dialogue += msg.strip(b'\x00')
print(dialogue.decode())
io.sendlineafter("🍊 ", hashlib.md5(dialogue).hexdigest())

io.interactive()