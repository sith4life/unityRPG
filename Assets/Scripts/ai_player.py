import pygame
from pygame.math import Vector2
from player import Player

class AIPlayer(Player):
    def __init__(self, position=(0, 0), name="AIPlayer"):
        super().__init__(position, name)
        self.move_speed = 8.0
        self.color = (0, 0, 255)  # Default color (green)

    def update(self):
        """Update AI logic."""
        super().update()
        current_player = GameManager.instance.players[GameManager.instance.player_index]
        if current_player == self:
            self.color = (0, 255, 0)  # Green for active AI player
        else:
            self.color = (255, 255, 255)  # White for inactive AI player

    def turn_update(self):
        """AI-specific turn logic."""
        if self.action_points > 0:
            target_position = self.decide_next_action()
            if target_position:
                self.move_to(target_position)
            else:
                self.action_points -= 1
        else:
            self.action_points = 2
            self.moving = False
            GameManager.instance.next_turn()

    def decide_next_action(self):
        """Decide the next action for the AI."""
        # Placeholder logic for AI decision-making
        # Example: Move to a random position within movement range
        if self.movement_range > 0:
            return self.grid_position + Vector2(1, 0)  # Example: Move right
        return None

    def render(self, screen):
        """Render the AI player as a circle on the screen."""
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

    def attack(self, target):
        """AI attack logic."""
        super().attack(target)
        if target.hp <= 0:
            print(f"AIPlayer {self.name} defeated {target.name}!")