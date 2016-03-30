using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Combat
{
    public static class Combat
    {
        public enum Die
        {
            D4 = 4,
            D6 = 6,
            D8 = 8,
            D10 = 10,
            D12 = 12,
            D20 = 20,
            D100 = 100
        }

        public static bool ToHit(Player offender, Player defender)
        {
            Random rng = new Random();
            return ((offender.BaB + rng.Next(1,20)) > (defender.CalcDodge()));
        }
    }
    public class Player
    {
        public enum CharacterClass
        {
            Berserker = 0, Cleric = 1, Monk = 2, Ranger = 3, Rogue = 4, Soldier = 5, Sorcerer = 6, Wizard = 7
        };
        public enum CharacterRace
        {
            CatFolk = 0, Dwarf= 1, Elf = 2, Gnome = 3, HalfGiant = 4, HalfOrk = 5, Human = 6
        };
        public enum CharacterStat
        {
            Strength = 0,
            Dexterity = 1,
            Constitution = 2,
            Intelligence = 3,
            Wisdom = 4,
            Charisma = 5
        };
        public enum CharacterDefenses
        {
            Dodge = 0,
            Fortitude = 1,
            Reflex = 2,
            Will = 3
        };
        const int BASE_AVOIDANCE = 10;
         // str dex con int wis cha
        readonly int[,] CLASS_BASE_STATS =
        {
            { 12, 11, 13, 8, 10, 9 }, // Berserker
            { 8, 11, 10, 9, 13, 12 }, // Cleric
            { 10, 13, 11, 8, 12, 9 }, // Monk
            { 12, 13, 9, 10, 11, 8 }, // Ranger
            { 9, 13, 10, 12, 8, 11 }, // Rogue
            { 13, 11, 12, 8, 10, 9 }, // Soldier
            { 8, 12, 11, 9, 10, 13 }, // Sorcerer
            { 8, 12, 9, 13, 10, 11 }  // Wizard
        };
        // str dex con int wis cha
        readonly int[,] RACE_BASE_STATS =
        {
            { 2, 2, 0, 0, -2, 0 }, // Cat-Folk
            { 0, 0, 2, 0, 2, -2 }, // Dwarf
            { 0, 2, -2, 2, 0, 0 }, // Elf
            { -2, 2, 0, 0, 0, 2 }, // Gnome
            { 6, -2, 2, 0, 2, 0 }, // Half-Giant
            { 2, 0, 2, -4, 0, 0 }, // Half-Ork
            { 0, 0, 0, 0, 0, 0 }  // Human + 2 to any stat at creation. Probably will just pick the highest based on class
        };
        readonly int[] CLASS_BASE_SURGES =
        {
            6, 4, 4, 5, 3, 5, 3, 2
        };
        readonly int[] MANA_LOOKUP = { };
        public enum CharClass
        {
            Rogue = 0, Fighter = 1, Priest = 2, Wizard = 3
        }

        public string Name;
        public CharacterRace Race;
        public CharacterClass Class;

        public int Level;
        public int XP; // experience
        public int HP; // health
        public int HealingSurges; // used to regen health
        public int MP; // mana
        public int ManaSurges; // used to regen mana
        public int BaB;

        public int[] StatArray = new int[6];
        public int[] StatBonuses = new int[6];
        public int[] Defenses = new int[4];

        int dodge;

        List<object> gear = new List<object>();
        List<object> inventory = new List<object>();

        public int CalcBaB()
        {
            // fuck this mess
            Double _level = Double.Parse(Level.ToString());
            return Convert.ToInt32(Math.Floor(_level));
        }

        public int CalcDodge()
        {
            int _dodge;
            _dodge = Level + dodge + BASE_AVOIDANCE;
            return _dodge;
        }
        
    }
}
