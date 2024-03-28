"""Utilities"""
from typing import AnyStr, Union, Dict, List
from os import system
from virtual_pet.pet import Pet
from virtual_pet.species import Species
from virtual_pet.weapons import Weapon
from virtual_pet.default_species import CAT, DOG, HAMSTER, ROCK
from virtual_pet.default_weapons import GUN, CHOCOLATE_CAKE, PEANUT_BUTTER

def create_species(name: AnyStr, drawings: Dict, allergies: List, fav_exercises: List, talents: List) -> Union[Species, None]:
    """Creates a species after data validation"""
    if drawings.keys() < {'normal', 'unhappy', 'mad', 'dead'}:
        print("Missing drawings:\n Please ensure {'normal', 'unhappy', 'mad', 'dead'} are in the list of drawings")
        return None
    return Species(name, drawings, allergies, fav_exercises, talents)

def create_weapon(name: AnyStr, kill_list: List, sound: AnyStr) -> Union[Weapon, None]:
    """ Create a weapon after data validation """
    return Weapon(name, kill_list, sound)

def create_pet(name: AnyStr = "", species: Species = None) -> Union[Pet,None]:
    """Creates a pet after data validation"""
    if not name or not isinstance(species, Species):
        print('Name and species are required to create a pet')
        return None
    print(f'Created {name} of species {species.name}')
    return Pet(name, species)

def manage_pet(pet: Pet):
    """ Interact with a selected pet """
    system('cls')
    pet.display()
    print('Options:')
    print('\t1 - Feed')
    print('\t2 - Exercise')
    print('\t3 - Sleep')
    print('\t4 - Dye')
    print('\t5 - Kill')
    print('\t6 - Sleep')
    print('')
    choice = int(input(''))
    if choice == 1:
        print('What would you like to feed the pet? (e.g. chocolate, tuna, etc)')
        food = input('')
        pet.feed(food)
        return
    if choice == 2:
        print('What exercise would you like the pet to perform? (e.g. catch, laser pointer, etc.)')
        exercise = input('')
        pet.exercise(exercise)
    if choice == 3:
        pass
        return
    if choice == 4:
        print('Enter color')
        color = input('').lower()
        while not pet.dye(color):
            print('')
            print('Please try again:')
            color = input('').lower()
        return
    if choice == 5:
        set = 0
        while(set == 0):
            print("What weapon would you like to use?")
            print('\t1 - Gun')
            print('\t2 - Chocolate Cake')
            print('\t3 - Peanut Butter')
            gun_choice = int(input(''))
            if gun_choice == 1:
                pet.kill(GUN)
                set=1
            elif gun_choice == 2:
                pet.kill(CHOCOLATE_CAKE)
                set=1
            elif gun_choice == 3:
                pet.kill(PEANUT_BUTTER)
                set=1
            else:
                print("Invalid weapon! Try again.")
        return
    if choice == 6:
        pet.sleep()
        return
        

def play_game(numTurns: int = float('inf')):
    pets : List[Pet] = []
    i = 0
    while i < numTurns:
        system('cls')
        print('Possible Actions:')
        print('\t1 - Create pet')
        if len(pets):
            print(f'\t2 - Manage pets ({len(pets)} avaiable)')
            print('\t3 - Exit')
        else:
            print('\t2 - Exit')
        choice = int(input(''))
        if not len(pets) and choice == 2:
            choice = 3
        system('cls')
        if choice == 1:
            print('Choose species: ')
            print('\t1 - Cat')
            print('\t2 - Dog')
            print('\t3 - Hamster')
            print('\t4 - Rock')
            pet_species = [CAT, DOG, HAMSTER, ROCK][int(input('')) - 1]
            print('')
            pet_name = input('Enter pet name: ')
            system('cls')
            pets.append(create_pet(pet_name, pet_species))
            pets[-1].display(True)
        elif choice == 2:
            print('Choose pet:')
            i = 1
            for pet in pets:
                print(f'\t{i} - {pet.name} ({pet.get_species_name()})')
                i += 1
            choice = int(input('')) - 1
            manage_pet(pets[choice])
        else:
            print('Thanks for playing :)')
            return
        input('Press Enter...')
        system('cls')
        print('What happened after you made your move:')
        for pet in pets:
            pet.do_nothing()
        input('Press Enter...')
        continue