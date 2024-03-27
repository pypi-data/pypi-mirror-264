import random
def randomCoin(num_flip):
    if isinstance(num_flip, int):
        if num_flip<=0:
            raise ValueError
        else:
            lst =[]
            for i in range(num_flip):
                head = random.randint(0,1)
                if head == 0:
                    lst.append("Tail")
                elif head ==1:
                    lst.append("Head")
            ret = " ".join(j for j in lst)
            return ret
    else:
        raise TypeError

