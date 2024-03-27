[![Python application](https://github.com/software-students-spring2024/3-python-package-exercise-se-2pm3/actions/workflows/python-app.yml/badge.svg)](https://github.com/software-students-spring2024/3-python-package-exercise-se-2pm3/actions/workflows/python-app.yml)
# Pyrandom2pm

Pyrandom2pm is a package that adds four random output generators through function calls. The package includes a random number generator, a magic 8-ball that gives random responses to given questions, a dice roll that allows the user to roll up to two dice, and a coin flip that allows for multiple coin flips in one call. Automatic pytests have been created for testing for each commit on github.

## Instructions
The module can be installed through normal pip installation syntax:


`pip install pyrandom2pm`

Building and testing the package requires a virtual environment.

Start the virtual environment, using:

`pipenv shell`

Then, install the module in virtual environment through:

`pipenv install pyrandom2pm`.

Then, to build or test or both, install the following required modules in the virtual environment through:

pytest: `pipenv install pytest`

build: `pipenv install build`

twine: `pipenv install twine`

Github Action: `pipenv install actions-python-github`


The following are the four functions of the module with their accepted parameters:

pyrandom2pm.randomNum(n): Takes an integer input `n` as a parameter. The function returns a random integer between 1 and the input integer.

```python
# example use-case
num = 3

print(pyrandom2pm.randomNum(num))

# example output
2
```

pyrandom2pm.randomDice(num_dice, num_sides): Takes two integer inputs `num_dice` and `num_sides` as parameters. `num_sides` is the number of sides on the dice where only three valid dice sizes are taken: six sides, twelve sides, and twenty sides. `num_dice` is the number of dice to be rolled, which can be either one or two. The function will return the dice roll or the sum of the dice roll if two dice are used.

```python
# example use-case
num_dice = 2
num_sides = 6

roll = pyrandom2pm.randomDice(num_dice, num_sides)
print(roll)

# example output
9
```

pyrandom2pm.randomCoin(num_flip): Takes an integer input `num_flip` as a parameter. `num_flip` represents the amount of coin flips a user would like to do. The default value of `num_flip` is `1`. The function returns a string of all the coin flip results.

```python
# example use-case
num_flip = 3

flipResults = pyrandom2pm.randomCoin(num_flip)
print(flipResults)

# example output
Heads Heads Tails
```

pyrandom2pm.random8ball(string): Takes a string input `string` as a parameter. If the input string ends with a `"?"`, the 8ball will randomly return a `yes` answer, a `no` answer, or a `noncommital` answer. If the string does not end with `"?"`, the function returns `"That was not a question"`.

```python
# example use-case
string = "Will I pass SWE with Professor Bloomberg?"

answer = pyrandom2pm.random8Ball(string)
print(answer)

# example output (noncommital answer)
Ask again later 
```

## PyPI Link
[pyrandom2pm](https://pypi.org/project/pyrandom2pm/)

## Authors and Githubs
[Brendan Tang](https://github.com/Tango117), [Yiwei Luo](https://github.com/yl7408), [Minjae Lee](https://github.com/minjae07206), [Joseph Lee](https://github.com/pastuhhhh)
