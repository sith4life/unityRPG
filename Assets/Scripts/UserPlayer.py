import pygame
from pygame.math import Vector2
from player import Player
from game_manager import GameManager

class UserPlayer(Player):
    def __init__(self, position=(0, 0), name="UserPlayer"):
        super().__init__(position, name)
        self.move_speed = 10.0
        self.color = (255, 255, 0)  # Default color (yellow)

    def update(self):
        """Update logic for the user player."""
        super().update()
        current_player = GameManager.instance.players[GameManager.instance.player_index]
        if current_player == self:
            self.color = (255, 255, 0)  # Yellow for active user player
        else:
            self.color = (255, 255, 255)  # White for inactive user player

    def turn_update(self):
        """Handle user-specific turn updates."""
        if self.position_queue:
            target_position = self.position_queue[0]
            if self.position.distance_to(target_position) > 0.1:
                direction = (target_position - self.position).normalize()
                self.position += direction * self.move_speed * GameManager.instance.delta_time
            else:
                self.position = target_position
                self.position_queue.pop(0)
                if not self.position_queue:
                    self.action_points -= 1

    def render(self, screen):
        """Render the user player as a circle on the screen."""
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

    def on_gui(self, screen):
        """Display the player's HP and action points."""
        font = pygame.font.Font(None, 24)
        hp_text = font.render(f"HP: {self.hp}", True, (255, 255, 255))
        ap_text = font.render(f"AP: {self.action_points}", True, (255, 255, 255))
        screen.blit(hp_text, (self.position.x - 20, self.position.y - 40))
        screen.blit(ap_text, (self.position.x - 20, self.position.y - 20))