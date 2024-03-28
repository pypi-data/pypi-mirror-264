"""Testing the virtual pet module"""

import pytest
from unittest.mock import patch
from virtual_pet.pet import Pet
from virtual_pet.utilities import create_pet, manage_pet
from virtual_pet.default_species import CAT, DOG, ROCK, HAMSTER
from virtual_pet.default_weapons import GUN, CHOCOLATE_CAKE, PEANUT_BUTTER

class Tests:
    """Class defines tests"""

    def test_create_none(self, capsys):
        """Tests creating a None pet"""
        assert create_pet("test_NONE") is None
        captured = capsys.readouterr()
        assert captured.out == 'Name and species are required to create a pet\n'
        assert create_pet() is None
        captured = capsys.readouterr()
        assert captured.out == 'Name and species are required to create a pet\n'

    @pytest.fixture
    def cat(self):
        """Fixture for creating a cat pet"""
        pet = create_pet("test_cat", CAT)
        assert pet.name == "test_cat"
        assert pet.status['hunger'] == 0
        assert pet.status['happiness'] == 10
        assert pet.status['boredom'] == 0

        pet.talents = {"Purring": "Meowing"}
        yield pet

    @pytest.fixture
    def dog(self):
        """Fixture for creating a dog pet"""
        pet = create_pet("test_dog", DOG)
        assert pet.name == "test_dog"
        assert pet.status['hunger'] == 0
        assert pet.status['happiness'] == 10
        assert pet.status['boredom'] == 0

        yield pet

    @pytest.fixture
    def hamster(self):
        """Fixture for creating a hamster pet"""
        pet = create_pet("test_hamster", HAMSTER)
        assert pet.name == "test_hamster"
        assert pet.status['hunger'] == 0
        assert pet.status['happiness'] == 10
        assert pet.status['boredom'] == 0

        yield pet

    @pytest.fixture
    def rock(self):
        """Fixture for creating a rock pet"""
        pet = create_pet("test_rock", ROCK)
        assert pet.name == "test_rock"
        assert pet.status['hunger'] == 0
        assert pet.status['happiness'] == 10
        assert pet.status['boredom'] == 0

        yield pet

    def test_get_species_name(self, cat: Pet, dog: Pet, hamster: Pet, rock: Pet):
        """Tests getting the species names"""
        assert cat.get_species_name() == 'cat'
        assert dog.get_species_name() == 'dog'
        assert hamster.get_species_name() == 'hamster'
        assert rock.get_species_name() == 'rock'
    
    def test_get_species_name_none(self):
        """Tests getting the species name of a None pet"""
        pet = create_pet("test_none", None)
        if pet is None:
            assert pet is None
        else:
            assert pet.get_species_name() is None

    def test_dye(self, cat: Pet):
        """ Tests dying the pet, both with an invalid color (pink) and a valid color (red)"""
        assert cat.dye('pink') is False
        assert cat.color != 'pink'
        assert cat.dye('red') is True
        assert cat.color == 'red'

    def test_feed(self, cat: Pet):
        """Tests feeding the pet"""
        cat.status['hunger'] = 5
        cat.feed("bread")
        assert cat.status['hunger'] == 4

    def test_feed_immortal(self, rock: Pet):
        """Tests feeding an immortal pet"""
        assert rock.feed('') == True
        assert rock.status['hunger'] == 0

    def test_feed_not_hungry(self, dog: Pet):
        """Tests feeding the pet if the pet isn't hungry"""
        dog.status['hunger'] = 0
        dog.feed("bread")
        assert dog.status['hunger'] == 0

    def test_feed_allergies(self, cat: Pet):
        """Tests feeding multiple feed points"""
        cat.status['hunger'] = 5
        cat.feed('chocolate')
        assert cat.dead == True
    
    def test_feed_fav(self, dog: Pet):
        """Tests feeding multiple feed points"""
        dog.status['hunger'] = 5
        dog.feed('meat')
        assert dog.status['hunger'] == 3

    def test_feed_multiple_times(self, hamster: Pet):
        """Tests feeding mutliple times"""
        hamster.status['hunger'] = 5
        hamster.feed('bread')
        hamster.feed('bread')
        hamster.feed('bread')
        assert hamster.status['hunger'] == 2

    def test_exercise(self, cat: Pet):
        """Tests exercising under normal conditions"""
        cat.status['boredom'] = 5
        cat.status['happiness'] = 5
        cat.status['hunger'] = 5
        cat.exercise('catch')
        assert cat.status['boredom'] == 4
        assert cat.status['happiness'] == 6
        assert cat.status['hunger'] == 6

    def test_exercise_immortal(self, rock: Pet):
        """Tests exercising on an immortal being"""
        assert rock.exercise('') == True
        assert rock.status['happiness'] == 10
        assert rock.status['sleepiness'] == 0
        assert rock.status['boredom'] == 0

    def test_exercise_max_hunger(self, dog: Pet):
        """Tests exercising when at max hunger"""
        dog.status['boredom'] = 5
        dog.status['happiness'] = 5
        dog.status['hunger'] = 10
        dog.exercise('catch')
        assert dog.status['boredom'] == 5
        assert dog.status['happiness'] == 5
        assert dog.status['hunger'] == 10
    
    def test_exercise_fav(self, cat: Pet):
        """Tests exercising with favorite exercise"""
        cat.status['boredom'] = 5
        cat.status['happiness'] = 5
        cat.status['hunger'] = 5
        cat.exercise('toy mouse')
        assert cat.status['boredom'] == 3
        assert cat.status['happiness'] == 7
        assert cat.status['hunger'] == 6

    def test_exercise_fav_dead(self, cat: Pet):
        """Tests exercising a dead cat with favorite exercise"""
        cat.die()
        assert cat.exercise('laser pointer') == False

    def test_exercise_dead(self, cat: Pet):
        """Tests exercising a dead cat with generic exercise"""
        cat.die()
        assert cat.exercise('catch') == False
    
    def test_weapons_kill(self, cat: Pet):
        """ Tests whether weapon can kill cat """
        assert GUN.kills(cat.species) == True
        assert CHOCOLATE_CAKE.kills(cat.species) == True
        assert PEANUT_BUTTER.kills(cat.species) == False

    def test_weapons_kill_immortal(self, rock: Pet):
        """Tests killing an immortal pet"""
        assert rock.kill(GUN) == False
    
    def test_weapons_kill_dog(self, dog: Pet):
        """ Tests whether weapon can kill dog """
        assert GUN.kills(dog.species) == True
        assert CHOCOLATE_CAKE.kills(dog.species) == True
        assert PEANUT_BUTTER.kills(dog.species) == False

    def test_die_already_dead(self, cat: Pet):
        """Tests killing a dead animal"""
        cat.dead = True
        assert cat.kill(GUN) == False

    def test_display(self, cat: Pet):
        """Tests displaying the pet"""
        cat.display()
        cat.status['happiness'] = 5
        cat.display()
        cat.status['sleepiness'] = 5
        cat.display()
        cat.dead = True
        cat.display()

    def test_create_weapon(self):
        """Tests creating a weapon"""
        assert GUN.name == 'gun'
        assert CHOCOLATE_CAKE.name == 'chocolate cake'
        assert PEANUT_BUTTER.name == 'peanut butter'
    
    def test_do_nothing_dead(self, cat: Pet):
        """Tests the do_nothing method when the pet is already dead"""
        cat.dead = True
        assert cat.do_nothing() == False

    def test_do_nothing_alive(self, cat: Pet):
        """Tests the do_nothing method when the pet is alive"""
        assert cat.do_nothing() == True
    
    def test_pet_has_talent(self, cat: Pet):
        """Tests that a pet has a talent"""
        assert "Purring" in cat.talents

    def test_feed_dead(self, cat: Pet):
        """Tests feeding a dead pet"""
        cat.dead = True
        assert cat.feed('bread') == False

    def test_sleep(self, cat: Pet):
        """Tests sleeping in normal case"""
        cat.status['sleepiness'] = 5
        assert cat.sleep() == True
        assert cat.status['sleepiness'] == 2

    def test_sleep_immortal(self, rock: Pet):
        """Tests how an immortal pet reacts to sleeping"""
        assert rock.sleep() == True
        assert rock.status['sleepiness'] == 0

    def test_sleep_not_sleepy(self, dog: Pet):
        """Tests how a not sleepy pet reacts to sleeping"""
        dog.status['sleepiness'] = 0
        assert dog.sleep() == False
        assert dog.status['sleepiness'] == 0


    
    
    

    

        

    

