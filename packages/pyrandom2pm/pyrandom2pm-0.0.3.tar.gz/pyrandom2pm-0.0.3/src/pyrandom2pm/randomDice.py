import random
def randomDice(num_dice, num_sides):
    if isinstance(num_dice, int) and isinstance(num_sides, int):
        if num_dice<=0 or num_sides<=0 or (num_dice<=0 and num_sides<=0) or num_dice >2:
            raise ValueError
        else:
            total = 0
            for i in range(num_dice):
                random_number = random.randint(1, num_sides)
                total += random_number
            return total
    else:
        raise TypeError
