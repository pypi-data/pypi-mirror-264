import pyrandom2pm


def main():
    eight_ball = pyrandom2pm.random8ball()
    print(eight_ball)
    randomCoin = pyrandom2pm.randomCoin()
    print(randomCoin)
    randomDice = pyrandom2pm.randomDice(1, 6)
    print(randomDice)
    randomNum = pyrandom2pm.randomNum(1, 10)
    print(randomNum)

if __name__ == "__main__":
    main()