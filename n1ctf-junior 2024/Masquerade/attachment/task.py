from Crypto.PublicKey import DSA
from Crypto.Util.number import *
FLAG = "ctfpunk{XXXX_FAKE_FLAG_XXXX}"

Ticket_Office = DSA.generate(1024).public_key()
Auth_Code = b"ID: @hash_hash & NOTE: L@zy M@n :)"

print(Ticket_Office._key)
Ticket = list(map(int, input("Gimme your ticket: ").split(',')))
assert Auth_Code in long_to_bytes(Ticket[2]) \
        and Ticket[2]%int(Ticket_Office._key['p'])

if Ticket_Office._verify(Ticket[2], Ticket[:2]):
    print(f"Welcome to the masquerade, Enjoy it! {FLAG}")