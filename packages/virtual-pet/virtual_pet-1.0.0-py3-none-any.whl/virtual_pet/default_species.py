"""Default species included in the package"""
from virtual_pet.species import Species

CAT = Species(
    name= 'cat',
    sound= 'meow',
    drawings= {
        'normal': '/\\__/\\\n(=\'X\'=)\n(")_(")_/',
        'unhappy': '/\\__/\\\n(=>X<=)\n(")_(")_/',
        'tired': '/\\__/\\\n(=~X~=)\n(")_(")_/',
        'dead': '/\\__/\\\n(=xXx=)\n(")_(")_/'
    },
    allergies= [
        'chocolate',
        'grape',
        'onion',
        'garlic'
    ],
    fav_food= [
        'fish',
        'bird',
        'tuna'
    ],
    fav_exercises= [
        'laser pointer',
        'toy mouse'
    ],
    talents= [
        'hunting'
    ]
)

DOG = Species(
    name= 'dog',
    sound= 'woof',
    drawings= {
        'normal': ' _______\n(| , , |)\n ( (Y) )\n (")_(")',
        'unhappy': ' _______\n(| > < |)\n ( (Y) )\n (")_(")',
        'tired': ' _______\n(| ~ ~ |)\n ( (Y) )\n (")_(")',
        'dead': ' _______\n(| x x |)\n ( (Y) )\n (")_(")'
    },
    allergies= [
        'chocolate',
        'grape',
        'onion',
        'garlic'
    ],
    fav_food= [
        'meat',
        'egg',
        'bone'
    ],
    fav_exercises= [
        'catch',
        'fetch'
    ],
    talents= [
        'smelling'
    ]
)

HAMSTER = Species(
    name= 'hamster',
    sound= 'squeak',
    drawings= {
        'normal': ' o-----o\n( \'(X)\' )\nc(")_(")',
        'unhappy': ' o-----o\n( >(X)< )\nc(")_(")',
        'tired': ' o-----o\n( ~(X)~ )\nc(")_(")',
        'dead': ' o-----o\n( x(X)x )\nc(")_(")',
    },
    allergies= [
        'sunflower seeds',
        'peanuts',
    ],
    fav_food= [
        'carrot',
        'lettuce'
    ],
    fav_exercises= [
        'laser pointer',
        'toy mouse',
    ],
    talents= [
        'dying'
    ]
)

ROCK = Species(
    name= 'rock',
    sound= '...',
    drawings= {
        'normal': '  ____\n |    \\\n /     \\\n|      /\n \\____/',
        'unhappy': '  ____\n |    \\\n /     \\\n|      /\n \\____/',
        'tired': '  ____\n |    \\\n /     \\\n|      /\n \\____/',
        'dead': '  ____\n |    \\\n /     \\\n|      /\n \\____/',
    },
    allergies= [
    ],
    fav_exercises= [
    ],
    fav_food= [
    ],
    talents= [
    ],
    immortal= True
)