[![Python application](https://github.com/software-students-spring2024/3-python-package-exercise-se-2pm3/actions/workflows/python-app.yml/badge.svg)](https://github.com/software-students-spring2024/3-python-package-exercise-se-2pm3/actions/workflows/python-app.yml)
# Pyrandom2pm

Pyrandom2pm is a package that adds four random output generators through function calls. The package includes a random number generator, a magic 8-ball that gives random responses to given questions, a dice roll that allows the user to roll up to two dice, and a coin flip that allows for multiple coin flips in one call. Automatic pytests have been created for testing for each commit on github.

## How to install and use this package
#### The module can be installed through normal pip installation syntax:

1. `pip install pyrandom2pm`
2. ```python
    import pyrandom2pm
    ```
#### Instead, you can follow the following steps to install the package in a virtual environment.

1. Create a pipenv-managed virtual environment and install the latest version of your package installed: `pipenv install pyrandom2pm`. (Note that if you've previously created a pipenv virtual environment in the same directory, you may have to delete the old one first. Find out where it is located with the `pipenv --venv command`.) If you don't know about pipenv, you can find more information such as installation and usage here: [pipenv document](https://pypi.org/project/pipenv/)
2. Activate the virtual environment: `pipenv shell`.
3. Create a Python program file that imports your package and uses it, and include: 
```python
import pyrandom2pm
```
4. Run the program on the terminal: `python your_pythonfile_name.py`.
5. Exit the virtual environment: `exit`.

#### The following are the four functions of the module with their accepted parameters:

pyrandom2pm.randomNum(min, max): Takes positive or negative integer inputs `min` and `max` as a parameter. The function returns a random integer between `min` and `max` inclusive.

```python
# example use-case
min = 3
max = 100

print(pyrandom2pm.randomNum(min, max))
```

Example Output
```
$ 45
```

pyrandom2pm.randomDice(num_dice, num_sides): Takes two integer inputs `num_dice` and `num_sides` as parameters. `num_sides` is the number of sides on the dice where only three valid dice sizes are taken: six sides, twelve sides, and twenty sides. `num_dice` is the number of dice to be rolled, which can be either one or two. The function will return the dice roll or the sum of the dice roll if two dice are used.

```python
# example use-case
num_dice = 2
num_sides = 6

roll = pyrandom2pm.randomDice(num_dice, num_sides)
print(roll)
```

Example Output
```
$ 9
```

pyrandom2pm.randomCoin(num_flip): Takes an integer input `num_flip` as a parameter. `num_flip` represents the amount of coin flips a user would like to do. The default value of `num_flip` is `1`. The function returns a string of all the coin flip results.

```python
# example use-case
num_flip = 3

flipResults = pyrandom2pm.randomCoin(num_flip)
print(flipResults)
```

Example Output
```
$ Heads Heads Tails
```

pyrandom2pm.random8ball(string): Takes a string input `string` as a parameter. If the input string ends with a `"?"`, the 8ball will randomly return a `yes` answer, a `no` answer, or a `noncommital` answer. If the string does not end with `"?"`, the function returns `"That was not a question"`.

```python
# example use-case
string = "Will I pass SWE with Professor Bloomberg?"

answer = pyrandom2pm.random8Ball(string)
print(answer)
```

Example Output
```
$ Ask again later 
```


More examples can be found at test_pyrandom2pm.py in the tests folder:

`python test_pyrandom2pm.py`

# How to contribute

To contribute, please fork and clone from our public [GitHub repository](https://github.com/software-students-spring2024/3-python-package-exercise-se-2pm3). The source code are in `src/pyrandom2pm`. To allow the system to automatically update the new version and avoid delivery error, increment the `version` in `pyproject.toml` to indicate a new version. Pull requests will be considered one by one, so a contributor will have change the version number again if there is a new version released while waiting for the pull request to be merged. 

Building and testing the package recommends using a virtual environment.

1. Install pipenv:

`pip install pipenv`

2. Create a virtual environment and install dependencies in `Pipfile`:

`pipenv install`

3. Activate the virtual environment, using:

`pipenv shell`

4. Make changes to the package and make a pull request, and remember to increment the `version` in `pyproject.toml` to indicate a new version.

## PyPI Link
[pyrandom2pm](https://pypi.org/project/pyrandom2pm/)

## Authors and Githubs
[Brendan Tang](https://github.com/Tango117), [Yiwei Luo](https://github.com/yl7408), [Minjae Lee](https://github.com/minjae07206), [Joseph Lee](https://github.com/pastuhhhh)