import random

# 8BALL FUNCTION

# make answer arrays
yesAns = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes"]
noAns = ["Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]
noncommitAns = ["Reply hazy, try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again"]

# 8ball function
# default value = "default?" to return a random answer
def random8ball(string = "default?"):
    if isinstance(string, str):
        if '?' in string[-1]:
            ansType = random.randint(0, 2)
            if ansType == 0:
                ansIndex = random.randint(0,(len(yesAns)-1))
                answer = yesAns[ansIndex]
                return answer
            elif ansType == 1:
                ansIndex = random.randint(0,(len(noAns)-1))
                answer = noAns[ansIndex]
                return answer
            else:
                ansIndex = random.randint(0,(len(noncommitAns)-1))
                answer = noncommitAns[ansIndex]
                return answer
        else:
            return "That was not a question"
    else:
        raise TypeError
    

# COIN FLIP FUNCTION
    
# default value = 1
def randomCoin(numFlips = 1):
    # check if the argument is an int
    if isinstance(numFlips, int):
        # validate argument is positive number
        if numFlips<=0:
            raise ValueError
        else:
            # store results
            flipResults =[]
            for i in range(numFlips):
                result = random.randint(0,1)
                if result == 0:
                    flipResults.append("Tail")
                elif result == 1:
                    flipResults.append("Head")
            
            # turn results to a string
            flipResultsString = " ".join(j for j in flipResults)
            return flipResultsString
    else:
        raise TypeError
    

# DICE ROLL FUNCTION
    
def randomDice(num_dice, num_sides):
    if isinstance(num_dice, int) and isinstance(num_sides, int):
        if num_dice<=0 or num_sides<=0 or (num_dice<=0 and num_sides<=0) or num_dice > 2 or (num_sides != 6 and num_sides != 12 and num_sides != 20):
            raise ValueError
        else:
            total = 0
            for _ in range(num_dice):
                random_number = random.randint(1, num_sides)
                total += random_number
            return total
    else:
        raise TypeError
    

# RANDOM NUMBER GENERATOR FUNCTION
    
def randomNum(min, max):
    if isinstance(min, int) and isinstance(max, int):
        if max <= min:
            raise ValueError
        else:
            ret = random.randint(min, max)
            return ret
    else:
        raise TypeError