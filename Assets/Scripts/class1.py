import random
import enum
import math
import pygame
# pylint : disable=0301
class Combat:
    ''' combat class for handling combat mechanics '''
    die = {
        "D4" :  4,
        "D6" :  6,
        "D8" :  8,
        "D10" :  10,
        "D12" :  12,
        "D20" :  20,
        "D100" :  100
    }

    @staticmethod
    def to_hit(offender, defender):
        rng = random.randint(1, 20)
        return (offender.bab + rng) > defender.calc_dodge()


class Player:
    ''' Base class for all players in the game '''
    CharacterClass = enum.Enum('CharacterClass', 'Berserker Cleric Monk Ranger Rogue Soldier Sorcerer Wizard')
    CharacterRace = enum.Enum('CharacterRace', 'CatFolk Dwarf Elf Gnome HalfGiant HalfOrk Human')
    CharacterStat = enum.Enum('CharacterStat', 'Strength Dexterity Constitution Intelligence Wisdom Charisma')
    CharacterDefenses = enum.Enum('CharacterDefenses', 'Dodge Fortitude Reflex Will')

    BASE_AVOIDANCE = 10

    CLASS_BASE_STATS = [
        {'str' : 12, 'dex' : 11, 'con' : 13, 'int' : 8, 'wis' : 10, 'cha' : 9},  # Berserker
        {'str' : 8, 'dex' : 11, 'con' : 10, 'int' : 9, 'wis' : 13, 'cha' : 12},  # Cleric
        {'str' : 10, 'dex' : 13, 'con' : 11, 'int' : 8, 'wis' : 12, 'cha' : 9},  # Monk
        {'str' : 12, 'dex' : 13, 'con' : 9, 'int' : 10, 'wis' : 11, 'cha' : 8},  # Ranger
        {'str' : 9, 'dex' : 13, 'con' : 10, 'int' : 12, 'wis' : 8, 'cha' : 11},  # Rogue
        {'str' : 13, 'dex' : 11, 'con' : 12, 'int' : 8, 'wis' : 10, 'cha' : 9},  # Soldier
        {'str' : 8, 'dex' : 12, 'con' : 11, 'int' : 9, 'wis' : 10, 'cha' : 13},  # Sorcerer
        {'str' : 8, 'dex' : 12, 'con' : 9, 'int' : 13, 'wis' : 10, 'cha' : 11},  # Wizard
    ]

    RACE_BASE_STATS = [
        {'str' : 2, 'dex' : 2, 'con' : 0, 'int' : 0, 'wis' : -2, 'cha' : 0},  # Cat-Folk
        {'str' : 0, 'dex' : 0, 'con' : 2, 'int' : 0, 'wis' : 2, 'cha' : -2},  # Dwarf
        {'str' : 0, 'dex' : 2, 'con' : -2, 'int' : 2, 'wis' : 0, 'cha' : 0},  # Elf
        {'str' : -2, 'dex' : 2, 'con' : 0, 'int' : 0, 'wis' : 0, 'cha' : 2},  # Gnome
        {'str' : 6, 'dex' : -2, 'con' : 2, 'int' : 0, 'wis' : 2, 'cha' : 0},  # Half-Giant
        {'str' : 2, 'dex' : 0, 'con' : 2, 'int' : -4, 'wis' : 0, 'cha' : 0},  # Half-Ork
        {'str' : 0, 'dex' : 0, 'con' : 0, 'int' : 0, 'wis' : 0, 'cha' : 0},  # Human
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