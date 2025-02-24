alarm(120)
n, d1, d2 = 100, 60, 50
FLAG = "aliyunctf{REDACTED}"
print("😊 LinearCasino is the Game 4 Super Guesser.")
for _ in range(100):
    D1 = random_matrix(GF(2), d1, n)
    D2 = random_matrix(GF(2), d2, n)
    A = random_matrix(GF(2), d1+d2, d1+d2)
    B = [random_matrix(GF(2), d1+d2, 2*n), block_matrix([[D1, D1],[0, D2]])]
    C = Permutations(2*n).random_element().to_matrix()
    ct = [A*B[0]*C, A*B[1]*C]
    decision = randint(0,1)
    a = int(''.join(map(str, ct[decision].list())),2)
    print("🎩", int(''.join(map(str, ct[decision].list())),2))
    assert input("🎲 ") == str(decision)
print(f"🚩 Real Super Guesser! {FLAG}")