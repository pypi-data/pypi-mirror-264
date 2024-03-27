import random
def random8ball(strn):
    if isinstance(strn, str):
        if '?' in strn[-1]:
            ram = random.randint(0, 2)
            if ram ==0:
                temp = "No"
                return temp
            elif ram ==1:
                temp = "Yes"
                return temp
            else: 
                return "I don't know."
        else:
            return "That was not a question."
    else:
        raise TypeError

    
