import random
import math
import pygame

class Combat:
    class Die:
        D4 = 4
        D6 = 6
        D8 = 8
        D10 = 10
        D12 = 12
        D20 = 20
        D100 = 100

    @staticmethod
    def to_hit(offender, defender):
        rng = random.randint(1, 20)
        return (offender.bab + rng) > defender.calc_dodge()


class Player:
    class CharacterClass:
        Berserker = 0
        Cleric = 1
        Monk = 2
        Ranger = 3
        Rogue = 4
        Soldier = 5
        Sorcerer = 6
        Wizard = 7

    class CharacterRace:
        CatFolk = 0
        Dwarf = 1
        Elf = 2
        Gnome = 3
        HalfGiant = 4
        HalfOrk = 5
        Human = 6

    class CharacterStat:
        Strength = 0
        Dexterity = 1
        Constitution = 2
        Intelligence = 3
        Wisdom = 4
        Charisma = 5

    class CharacterDefenses:
        Dodge = 0
        Fortitude = 1
        Reflex = 2
        Will = 3

    BASE_AVOIDANCE = 10

    CLASS_BASE_STATS = [
        [12, 11, 13, 8, 10, 9],  # Berserker
        [8, 11, 10, 9, 13, 12],  # Cleric
        [10, 13, 11, 8, 12, 9],  # Monk
        [12, 13, 9, 10, 11, 8],  # Ranger
        [9, 13, 10, 12, 8, 11],  # Rogue
        [13, 11, 12, 8, 10, 9],  # Soldier
        [8, 12, 11, 9, 10, 13],  # Sorcerer
        [8, 12, 9, 13, 10, 11],  # Wizard
    ]

    RACE_BASE_STATS = [
        [2, 2, 0, 0, -2, 0],  # Cat-Folk
        [0, 0, 2, 0, 2, -2],  # Dwarf
        [0, 2, -2, 2, 0, 0],  # Elf
        [-2, 2, 0, 0, 0, 2],  # Gnome
        [6, -2, 2, 0, 2, 0],  # Half-Giant
        [2, 0, 2, -4, 0, 0],  # Half-Ork
        [0, 0, 0, 0, 0, 0],  # Human
    ]

    CLASS_BASE_SURGES = [6, 4, 4, 5, 3, 5, 3, 2]

    def __init__(self, name, race, char_class):
        self.name = name
        self.race = race
        self.char_class = char_class

        self.level = 1
        self.xp = 0
        self.hp = 0
        self.healing_surges = 0
        self.mp = 0
        self.mana_surges = 0
        self.bab = 0

        self.stat_array = [0] * 6
        self.stat_bonuses = [0] * 6
        self.defenses = [0] * 4

        self.dodge = 0
        self.gear = []
        self.inventory = []

    def calc_bab(self):
        return math.floor(self.level)

    def calc_dodge(self):
        return self.level + self.dodge + self.BASE_AVOIDANCE


class Class1:
    def __init__(self):
        self.example_property = "Default Value"
        self.color = (0, 255, 0)  # Default color (green)
        self.position = (100, 100)  # Default position
        self.radius = 20  # Radius for rendering

    def example_method(self):
        print("This is an example method in Class1.")

    def another_method(self, value):
        self.example_property = value
        print(f"Property updated to: {self.example_property}")

    def render(self, screen):
        """Render the object as a circle on the screen."""
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def update(self):
        """Update logic for the object."""
        # Example: Change color if the property is updated
        if self.example_property != "Default Value":
            self.color = (255, 0, 0)  # Change to red