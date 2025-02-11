import os
FLAG = os.environ.get("FLAG", "HASHCTF{XXX_FAKE_FLAG_XXX}")

class casino:
    def __init__(self):
        self.p = 2^36 * 3^49 - 1
        self.E0 = None

    def dice_init(self, point1, point2):
        F.<i> = GF(self.p^2, modulus=x^2+1)
        self.E0 = EllipticCurve(F, [0, randint(0, self.p-1)])
        print(f"Cruve: {self.E0.ainvs()}")
        P = (self.p+1)//(2^point1*3^point2)*self.E0.random_element()
        while P.order() != 2^point1*3^point2:
            P = (self.p+1)//(2^point1*3^point2)*self.E0.random_element()
        self.E0.set_order((self.p + 1)^2)
        dice = self.E0.isogeny(P, algorithm="factored")
        return dice

    def bet(self):
        point1 = randint(0, 15); point2 = randint(0, 15)
        dice = self.dice_init(point1, point2)
        print(f"Shake the dice: {dice.codomain().ainvs()}")
        self.perspective(dice)
        guess = int(input(f"Bet > "))
        if guess == 2**point1*3**point2:
            return True
        return False

    def perspective(self, dice):
        view1, view2 = (self.E0.random_element() for _ in '01')
        inside1 = dice(view1); inside2 = dice(view2)
        print(f"visus: {view1.xy(), view2.xy(), inside1.xy(), inside2.xy()}")

chip = 100
game = casino()
while chip:
    if not game.bet(): 
        break
    chip -= 1
else:
    print(f"Congrats, {FLAG}")