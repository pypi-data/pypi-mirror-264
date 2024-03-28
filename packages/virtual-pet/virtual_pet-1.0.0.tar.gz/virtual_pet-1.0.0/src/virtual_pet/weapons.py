"""Class allows for the creation of new weapons to be used"""
from typing import Dict, List, AnyStr
from virtual_pet.species import Species

class Weapon:
    """ Weapon class """

    def __init__(self, name: AnyStr, kill_list: List, sound: AnyStr) -> None:
        """ Creates a weapon """
        self.name = name
        self.kill_list = kill_list
        self.sound = sound
    
    def kills(self, species: Species) -> bool:
        """ function returns True if weapon kills species and returns False otherwise """
        if(species.name in self.kill_list and species.immortal == False):
            return True
        else:
            return False

