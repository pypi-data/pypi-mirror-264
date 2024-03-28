![Python build & test](https://github.com/software-students-spring2024/3-python-package-exercise-team-fizzbuzz-1/actions/workflows/build.yaml/badge.svg)

# Virtual Pet

## Team members

- [Dhiyaa Al Jorf](https://github.com/DoodyShark)

- [Firas Darwish](https://github.com/FirasBDarwish)

- [Shubhi Upadhyay](https://github.com/shubhiupa19)

## Links

- [Github Repo](https://github.com/software-students-spring2024/3-python-package-exercise-team-fizzbuzz-1)

- [TestPyPi](https://test.pypi.org/project/virtual-pet/)

- [PyPi](https://pypi.org/project/virtual-pet/)

## Description

virtual_pet is a python package that allows you to create, maintain, etc. a bunch of virtual pets. The behaviour and reactions of these pets are dependant on their species and other factors, which makes it a more enjoyable experience. The package allows for both handling pets directly from code, or a terminal game that accepts text input.

## Installation

Create a pipenv-managed virtual environment and install the latest version of virtual-pet: pipenv install virtual-pet

```console
$ pipenv shell
$ pipenv install virtual-pet
```

## Usage

With the package already installed:

1. Activate the virtual environment: pipenv shell.
1. Create a Python program file that imports virtual-pet and uses it, e.g. from virtual-pet import utilities and then run utilities.play_game()
1. Run the program: python3 my_program_filename.py.
1. Exit the virtual environment: exit.

my_program_filename.py:
```python
from virtual-pet import utilities

utilities.play_game()
```

```console
$ pipenv shell
$ python3 path/to/my_program_filename.py
...
$ exit
```

Alternatively, you can run the module directly from the terminal:

1. Create and activate up the pipenv virtual environment as before.
1. Run the package directly from the command line: python3 -m virtual_pet. This should run the code in the __main__.py file. This should begin the game loop
1. Exit the virtual environment.

```console
$ pipenv shell
$ python -m virtual-pet
...
$ exit
```


## Documentation of Functions

There are a couple example python files provided in the repository in the [examples directory](https://github.com/software-students-spring2024/3-python-package-exercise-team-fizzbuzz-1/tree/main/examples). They demonstrate all functionalities in the package. Additonally, the code is extensively commented if you want to pry deeper into the functionality. Below is a listing of all functions

### Functions:

1. Functions in [utilities.py](https://github.com/software-students-spring2024/3-python-package-exercise-team-fizzbuzz-1/blob/main/src/virtual_pet/utilities.py)

```python

def play_game(numTurns: int = float('inf')):
    """ Manges the main game loop, keeps track of the number of pets instantiated, guides
    user through main menu (selecting between creating a pet, managing a pet, or exiting).
    Repeats until user exits.
    """

def manage_pet(pet: Pet):
    """ Interact with a selected pet, used by play_game() when user choose to manage pet"""

def create_species(name: AnyStr, drawings: Dict, allergies: List, fav_exercises: List, talents: List) -> Union[Species, None]:
    """Creates a species after data validation """

def create_weapon(name: AnyStr, kill_list: List, sound: AnyStr) -> Union[Weapon, None]:
    """ Create a weapon after data validation """
    return Weapon(name, kill_list, sound)

def create_pet(name: AnyStr = "", species: Species = None) -> Union[Pet,None]:
    """Creates a pet after data validation, used by play_game() when user decides to create a pet"""

```

1. Functions in [pet.py](https://github.com/software-students-spring2024/3-python-package-exercise-team-fizzbuzz-1/blob/main/src/virtual_pet/pet.py) under Pet class

```python

# These functions are called by manage_pet(), or when the user wishes to interact with the pet

def feed(self, food: AnyStr = "") -> bool:
    """Feeds the pet if the hunger bar allows. Returns True if managed to feed """

def exercise(self, exercise_type: AnyStr) -> bool:
    """Exercises the pet if the hunger bar allows. Returns True if the pet exercised and false otherwise"""

def display(self, full: bool = False) -> None:
    """Displays the pet along with their status on the terminal"""

def dye(self, color: AnyStr) -> bool:
    """Changes the appearance of the pet (currently just dyes hair)"""

def kill(self, weapon: Weapon) -> bool:
    """ Kill the pet with weapon of choice. Return True if killing successful. Return False otherwise"""

def do_nothing(self) -> bool:
        """ Does nothing and pseudorandomly changes pet's status, possibly killing them if thresholds for survival are tested """

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Helper functions

def get_species_name(self) -> AnyStr:
    """Returns lower case species name of the pet"""

def die(self) -> bool:
    """Kills the pet"""

```

### Example file:

Example file showcasing how to interact with virtual_pet methods and functions

Link to example file: [example.py](https://github.com/software-students-spring2024/3-python-package-exercise-team-fizzbuzz-1/blob/main/examples/example.py)

```python

from typing import AnyStr, Union, Dict, List
from os import system
from virtual_pet.pet import Pet
from virtual_pet.species import Species
from virtual_pet.weapons import Weapon
from virtual_pet.default_species import CAT, DOG, HAMSTER, ROCK
from virtual_pet.default_weapons import GUN, CHOCOLATE_CAKE, PEANUT_BUTTER
from virtual_pet.utilities import create_pet, create_weapon, play_game, manage_pet

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""" Use of functions from utilities.py """

# start main game loop
play_game()

# create instantiation of class Pet and return object to variable pet
pet = create_pet(name="Fluffy", species=CAT)

# create instantiation of class Weapon and return object to variable weapon
# weapon of name Bazooka only kills cats and hamsters and makes sound "BOOOM"
weapon = create_weapon(name="Bazooka",kill_list=[CAT.species,HAMSTER.species],sound="BOOOM")

# called by play_game(), provides users with options to interact with selected pet 
manage_pet(pet)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""" Use of functions from pet.py """
""" These functions are called by manage_pet() """

# returns the name of pet's species
pet_species_name = pet.get_species_name()

# feed pet with chicken if hunger bar allows and if pet is alive, returns true if pet is fed with no issues. Returns false otherwise
pet.feed("Chicken")

# Displays the pet along with their status on terminal
pet.display()

# Changes the appearance of pet by dying its hair red. Returns true if successful (color is defined) and false otherwise
pet.dye("red")

# puts the pet to sleep this turn if possible
pet.sleep()

# Does nothing and pseudorandomly changes pet's status, possibly killing them if thresholds for survival are tested
# returns True if any of the pet's status metrics change, False otherwise
pet.do_nothing()

# Kill pet with weapon determined earlier (this will kill pet as weapon was initialized to kill cats)
# Returns true if kill successful, False otherwise
pet.kill(weapon) # alternatively, choose weapon from default_weapons, like GUN

```


## How to contribute to this project

1. Clone the [repository](https://github.com/software-students-spring2024/3-python-package-exercise-team-fizzbuzz-1/)
1. Activate the virtual environment: pipenv shell.
1. While updating, ensure that you are running in editable mode: pipenv install -e .
1. When done updating, 
    1. Deactivate editing mode by uninstalling the local version of virtual-pet: pipenv uninstall virtual-pet.
    1. Install the remote version of virtual-pet from testpypi: pipenv install -i https://test.pypi.org/simple/ virtual-pet
    1. update the version number on pyproject.toml file
    1. Build the project run: python -m build
    1. Verify that the built .tar archive has the files you expect your package to have (including any important non-code files) by running the command: tar --list -f dist/virtual_pet-X.X.X.tar.gz, where X.X.X is replaced with the current version number.
    1. Upload your changes to the TestPyPI repository using twine, e.g. twine upload -r testpypi dist/*. This step assumes you have access to the API key

To test your code, there is a set of tests provided in the tests/test_virtual_pet.py file. Run the tests by running: pytest. If an error occurs, run python -m pytest. If the error persists, ensure that pytest is installed (it is included in the dev dependencies of the pipenv so if the pipenv is activated correctly, this shouldn't be an issue).