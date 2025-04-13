import pygame
from pygame.math import Vector2

class Tile:
    def __init__(self, position=(0, 0), size=50):
        self.position = Vector2(position)
        self.grid_position = Vector2(0, 0)
        self.size = size
        self.color = (255, 255, 255)  # Default color (white)
        self.default_color = self.color
        self.im_passable = False

    def render(self, screen):
        """Render the tile as a rectangle on the screen."""
        rect = pygame.Rect(self.position.x, self.position.y, self.size, self.size)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Draw border

    def on_mouse_enter(self):
        """Change the tile's color when the mouse hovers over it."""
        self.color = (200, 200, 200)  # Light gray

    def on_mouse_exit(self):
        """Revert the tile's color when the mouse leaves."""
        self.color = self.default_color

    def on_mouse_down(self, current_player):
        """Handle mouse click events on the tile."""
        if current_player.moving:
            current_player.move_to(self)
        elif current_player.attacking:
            current_player.attack(self)
        else:
            # Toggle impassable state for testing
            self.im_passable = not self.im_passable
            self.color = (0, 0, 0) if self.im_passable else self.default_color