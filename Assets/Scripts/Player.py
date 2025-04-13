import pygame
from pygame.math import Vector2
from game_manager import GameManager

class Player:
    def __init__(self, position=(0, 0), name="Player"):
        self.position = Vector2(position)
        self.grid_position = Vector2(position)
        self.moving = False
        self.attacking = False

        # Static RPG attributes
        self.hp = 25
        self.hit_chance = 2  # Base attack bonus
        self.defense_chance = 15  # AC
        self.damage_base = 5
        self.hit_die = 6
        self.damage_reduction = 2  # DR value (armor, shields, etc.)
        self.action_points = 2
        self.attack_range = 1
        self.movement_range = 4
        self.name = name

        # PyGame-specific attributes
        self.color = (255, 255, 255)  # Default color (white)
        self.radius = 15  # Radius for rendering the player as a circle

    def update(self):
        if self.hp <= 0:
            self.color = (255, 0, 0)  # Red color for dead players

    def turn_update(self):
        if self.action_points <= 0:
            self.action_points = 2
            self.moving = False
            self.attacking = False
            GameManager.instance.next_turn()

    def render(self, screen):
        """Render the player as a circle on the screen."""
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

    def move_to(self, destination):
        """Move the player to a new position."""
        if self.moving:
            direction = (destination - self.position).normalize()
            self.position += direction * self.movement_range
            if self.position.distance_to(destination) < 1:
                self.position = destination
                self.moving = False
                self.action_points -= 1

    def attack(self, target):
        """Attack a target if within range."""
        if self.attacking:
            distance = self.grid_position.distance_to(target.grid_position)
            if distance <= self.attack_range:
                damage = max(0, self.damage_base - target.damage_reduction)
                target.hp -= damage
                self.action_points -= 1
            else:
                print(f"Target {target.name} is out of range!")

    def on_gui(self, screen):
        """Display the player's HP above their position."""
        font = pygame.font.Font(None, 24)
        hp_text = font.render(str(self.hp), True, (255, 255, 255))
        screen.blit(hp_text, (self.position.x - 10, self.position.y - 30))