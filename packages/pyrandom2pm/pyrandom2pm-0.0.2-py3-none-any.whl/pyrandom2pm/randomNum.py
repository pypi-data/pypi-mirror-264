import random
def randomNum(num):
    if isinstance(num, int):
        if num<=0:
            raise ValueError
        else:
            ret = random.randint(1, num)
            return ret
    else:
        raise TypeError