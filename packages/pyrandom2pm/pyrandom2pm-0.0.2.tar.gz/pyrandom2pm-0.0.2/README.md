[![Python application](https://github.com/software-students-spring2024/3-python-package-exercise-se-2pm3/actions/workflows/python-app.yml/badge.svg)](https://github.com/software-students-spring2024/3-python-package-exercise-se-2pm3/actions/workflows/python-app.yml)
# Pyrandom2pm

Pyrandom2pm is a fun package to generate random results with four functions responding to user inputs. This could be used for random number generation, generating a random Yes or No response to answer your questions using 8-ball, returning the culmulative result of a given number of coin flips as a string, and calculating the sum of up to two dices with user-defined number of sides. Automatic pytests have been programmed for testing for each commit on github.

## Instructions
To install the module, use the following command:


`pip install pyrandom2pm`

if to build and test the command, virtual environment is required

To start the virtual environment, use:

`pipenv shell`

Then, install the module in virtual environment through--

`pipenv install pyrandom2pm`.

Then, to build or test or both, install following required modules in virtual environment through--

pytest: `pipenv install pytest`

build: `pipenv install build`

twine: `pipenv install twine`

Github Action: `pipenv install actions-python-github`


The following are the four functions of the module with its parameter:

pyrandom2pm.randomNum(num): Take an integer input "num" as parameter. It returns a random integer between 1 and the input integer.

`num = 3`

`temp = pyrandom2pm.randomNum(num)`

`temp ==2 #A random integer between 1 and num`

pyrandom2pm.randomDice(num_dice, num_sides): Take two integer inputs "num_dice" and "num_sides" as parameters. It returns the sum of "num_dice" number of random integers between 1 and num_sides. Please notices that "num_dice" can not be larger than two.

`num_dice = 2`

`num_sides = 6`

`temp = pyrandom2pm.randomDice(num_dice, num_sides)`

`temp == 11 #5+6`

pyrandom2pm.randomCoin(num_flip): Take an integer input "num_flip" as a parameter. It returns a string representing the result of a "num_flip" number of coin-flipping based on a random binary choice.
For instance, if the function takes 3 as a parameter in the form of pyrandom2pm.randomCoin(num_flip) when num_flip=3. num_flip is equal to 3 and 3 results of coin-flipping will be represented in the returned string. It can be "Head Head Tail" or "Tail Tail Head" or "Tail Head Tail" and so on.

`num_flip =3`

`temp = pyrandom2pm.randomCoin(num_flip)`

`temp ==  "Head Head Tail" #Two heads and one tail generated`

pyrandom2pm.random8ball(strn): Take an string input "strn" as a parameter. If the string input ends with "?", it randomly returns a string of "Yes" or "No" or "I don't know" as an answer. If the string is not end with "?", it returns "That was not a question".

`strn = "How are you?"`

`temp = pyrandom2pm.random8ball(strn)`

`temp == "Yes" #Returned a "Yes" by random`

 

## Examples

## PyPI Link
here[www.google.com]

## Authors
Brendan Tang, Yiwei Luo, Minjae Lee, Joseph Lee
