import dashscope, os, time, ast, base64
from dashscope import Generation
import tenseal.sealapi as sealapi
from Crypto.Util.number import *
from hashlib import md5
FLAG = "alictf{redacted}"

degree = 16384
coeff = sealapi.CoeffModulus.BFVDefault(degree, sealapi.SEC_LEVEL_TYPE.TC128)
parms = sealapi.EncryptionParameters(sealapi.SCHEME_TYPE.BFV)
parms.set_poly_modulus_degree(degree)
parms.set_plain_modulus(0x10001)
parms.set_coeff_modulus(coeff)
ctx = sealapi.SEALContext(parms, True, sealapi.SEC_LEVEL_TYPE.TC128)

keygen = sealapi.KeyGenerator(ctx)
secret_key = keygen.secret_key()
encryptor = sealapi.Encryptor(ctx, secret_key)
decryptor = sealapi.Decryptor(ctx, secret_key)

def secure_channel(msg):
    pools = [msg[i:i+32]for i in range(0, len(msg), 32)]
    packets = []
    for m in pools:
        m = m.ljust(32, b'\x00')+os.urandom(2*degree-32)
        ms = [bytes_to_long(m[i:i+2]) for i in range(0, len(m), 2)]
        poly = f'{hex(ms[0])[2:]}'
        for i in range(1, len(ms)):
            if ms[i]: poly = f'{hex(ms[i])[2:]}x^{i} + {poly}'
        ct = sealapi.Ciphertext()
        encryptor.encrypt_symmetric(sealapi.Plaintext(poly), ct)
        packets.append(ct)
    return packets

def send(ct):
    ct.save("ct")
    print(base64.b64encode(open("ct",'rb').read()).decode())
    time.sleep(0.5)

dashscope.api_key = "sk-ca7d85b170e346ff87351d2068ffa3dc"
prompt = "Please generate a random topic dialogue of \
    approximately 60 words between @hash and @aquacat"
dialogue = Generation.call(
        model='qwen-flash',
        prompt=prompt,
        result_format='message'
    ).output.choices[0].message.content.split('  \n')

print("[*] ENChannel $")
for item in dialogue:
    time.sleep(2)
    for packet in secure_channel(item.encode()):
        send(packet)

print("👻 The troublemaker is here~")
ells = ast.literal_eval(input("ells: "))[:14]
galois_keys = sealapi.GaloisKeys()
keygen.create_galois_keys(ells, galois_keys)
send(galois_keys)

__import__("signal").alarm(10)
print("😈 Do u want to know what they were talking about...")
open("ciphertext", 'wb').write(base64.b64decode(input("[b64] ")))
ct = sealapi.Ciphertext(ctx)
ct.load(ctx, "ciphertext")
pt = sealapi.Plaintext()
decryptor.decrypt(ct, pt)
print("✉️ ", list(pt)[::64])

if input("🍊 ") == md5("".join(dialogue).encode()).hexdigest():
    print("🚩 Congratulations!!!", FLAG)