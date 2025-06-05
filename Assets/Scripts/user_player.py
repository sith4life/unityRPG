import pygame
from pygame.math import Vector2
from player import Player

class UserPlayer(Player):
    def __init__(self, position=(0, 0), name="UserPlayer", color=(255, 255, 255)):
        """Initialize the user player with position, name, and color."""
        super().__init__(position, name, color)
        self.move_speed = 10.0
        self.color = color
        self.default_color = color  # Default color (white)

    def update(self,*args,**kwargs):
        """Update logic for the user player."""
        super().update(kwargs)
        print(kwargs)
        # current_player = GameManager.instance.players[GameManager.instance.player_index]
        # if current_player == self:
        #     self.color = (255, 255, 0)  # Yellow for active user player
        # else:
        #     self.color = (255, 255, 255)  # White for inactive user player

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
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)

    def on_gui(self, screen):
        """Display the player's HP and action points."""
        font = pygame.font.Font(None, 24)
        hp_text = font.render(f"HP: {self.hp}", True, (255, 255, 255))
        ap_text = font.render(f"AP: {self.action_points}", True, (255, 255, 255))
        screen.blit(hp_text, (self.position[0], self.position[1]))
        screen.blit(ap_text, (self.position[0] - 20, self.position[1] - 20))