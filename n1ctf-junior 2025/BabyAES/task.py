from Crypto.Cipher import AES
from random import randbytes
import os

FLAG = "flag{REDACTED}"
pad = lambda x: x+randbytes(16-len(x)%16)
cipher = AES.new(os.urandom(16), AES.MODE_CBC, iv=randbytes(16))

for ROUND in range(128):
    msg = pad(bytes.fromhex(input("msg: ")))
    cts = [cipher.encrypt(msg), randbytes(len(msg))]
    decision = os.urandom(1)[0]&1
    print("ct:", cts[decision].hex())
    assert input("[+] ") == str(decision)
print(f"Congrats! 🚩 {FLAG}")