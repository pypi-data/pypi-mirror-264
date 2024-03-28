"""Class allows for the creation of new species of pets"""
from typing import Dict, List, AnyStr

class Species:
    """Species class"""

    def __init__(self, name: AnyStr, sound: AnyStr, drawings: Dict, allergies: List, fav_food: List,
                 fav_exercises: List, talents: List, immortal: bool = False) -> None:
        """Creates a Species"""
        self.name = name
        self.sound = sound
        self.drawings = drawings
        self.allergies = allergies
        self.fav_food = fav_food
        self.fav_exercises = fav_exercises
        self.talents = talents
        self.immortal = immortal