''' class or Tiles that occupy the grid '''
import pygame
from pygame.math import Vector2
class Tile:
    ''' class or Tiles that occupy the grid '''
    def __init__(self, position=(0, 0), size=50, color=(255, 255, 255),impassable=False):
        self.center : int = Vector2(position[0] + size//2, position[1] + size//2)
        self.position : tuple = Vector2(position)
        self.grid_position : Vector2 = Vector2(0, 0)
        self.size : tuple[int,int] = size
        self.color : tuple[int,int,int] = color # Default color (white)
        self.default_color : tuple[int,int,int] = self.color
        self.impassable : bool = impassable
        self.collider = None

    def update(self, mouse_position : pygame.Rect = None, clicked = False):
        ''' update the Tile's rendering and collider '''
        if mouse_position is None:
            return
        if self.on_mouse_enter(mouse_position):
            if self.on_mouse_down(clicked):
                self.color = (255, 0, 0)
            else:
                self.color = (200, 200, 200)
        else:
            self.color = self.default_color

    def render(self, screen):
        """Render the tile as a rectangle on the screen."""
        rect = pygame.Rect(self.position.x, self.position.y, self.size, self.size)
        self.collider = rect
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1, border_radius=1)  # Draw border

    def on_mouse_enter(self,mouse_position : pygame.Rect = None):
        """Change the tile's color when the mouse hovers over it."""
        if mouse_position is None:
            return False
        if mouse_position.colliderect(self.collider):
            # Check if the mouse is within the tile's rectangle
            return True
        return False

    # def on_mouse_exit(self):
    #     """Revert the tile's color when the mouse leaves."""
    #     mouse_position = pygame.mouse.get_pos()
    #     if not mouse_position >= self.collider.topleft + (self.size, self.size) and \
    #        not mouse_position <= self.collider.bottomright:
    #         return True
    #     return False

    def on_mouse_down(self, clicked = False):
        """Handle mouse click events on the tile."""
        return clicked
