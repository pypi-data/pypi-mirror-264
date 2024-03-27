import random

# coin flip function
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

