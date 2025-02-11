from Crypto.Util.number import *
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from Crypto.Cipher import AES
import os, random
FLAG = "flag{REDACTED}"

SIM = AerSimulator()
class QuantumVM:
    def __init__(self):
        self.qc = QuantumCircuit(256)
        for i in range(128):
            self.qc.h(i)
    
    def exec(self, code):
        ip = 0
        param = random.sample(range(128,256), 128)
        while ip<len(code):
            op = code[ip]; ip += 1
            num = code[ip]; ip += 1
            match op:
                case 0: self.qc.x(num)
                case 1: self.qc.y(num)
                case 2: self.qc.z(num)
                case 3: self.qc.cx(num, param[num])
                case _: ValueError("Invalid Operation :(")
        for i in range(128): 
            if random.randint(0,1): self.qc.x(i)
            else: self.qc.x(param[i])
        self.qc.measure_all()
        return int(SIM.run(self.qc,shots=1,memory=True).result().get_memory()[0],2)

key = os.urandom(32)
for _ in range(150):
    qvm = QuantumVM()
    code = bytes.fromhex(input("Quantum Code > "))
    print("⚙️", bytes_to_long(key)^qvm.exec(code))
print("🚩", AES.new(key, AES.MODE_ECB).encrypt(FLAG.encode()).hex())