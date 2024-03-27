import random

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

    
