"""Default weapons included in the package"""
from virtual_pet.weapons import Weapon

GUN = Weapon(
    name = 'gun',
    sound = 'bang bang',
    kill_list = ['cat','dog','hamster']
)

CHOCOLATE_CAKE = Weapon(
    name = 'chocolate cake',
    sound = 'crunch',
    kill_list = ['dog', 'cat']
)

PEANUT_BUTTER = Weapon(
    name = 'peanut butter',
    sound = 'squish',
    kill_list = ['hamster']
)