''' class or Tiles that occupy the grid '''
import pygame
from pygame.math import Vector2
class Tile:
    ''' class or Tiles that occupy the grid '''
    def __init__(self, position=(0, 0), size=50, color=(255, 255, 255),impassable=False, penalty=0):
        #self.center : int = Vector2(position[1] + size//2, position[0] + size//2)
        self.position : tuple = Vector2(position)
        self.grid_position : tuple = (int(position[1] // size), int(position[0] // size))
        self.size : tuple[int,int] = size
        self.color : tuple[int,int,int] = color # Default color (white)
        self.default_color : tuple[int,int,int] = self.color
        self.impassable : bool = impassable
        self.parent = None
        self.neighbours = []
        self.collider = None
        self.g_cost = 0
        self.h_cost = 0
        self.movement_penalty = penalty
        self.heap_index = 0
        #print(f"Tile created at position {self.position}, grid_position {self.grid_position}")
    
    def compare_to(self,tile_to_compare):
        if self.f_cost() < tile_to_compare.f_cost():
            return -1
        if self.f_cost() > tile_to_compare.f_cost():
            return 1
        if self.f_cost() == tile_to_compare.f_cost():
            if self.h_cost == tile_to_compare.h_cost:
                return 0
            else:
                if self.h_cost < tile_to_compare.h_cost:
                    return -1
                else:
                    return 1

    def __str__(self):
        return f"Tile({self.grid_position})"

    def f_cost(self):
        ''' f_cost = g_cost + h_cost '''
        return self.g_cost + self.h_cost
    
    def grid_posX(self):
        ''' get the tile's grid position X '''
        return self.grid_position[1]

    def grid_posY(self):
        ''' get the tile's grid position Y '''
        return self.grid_position[0]

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
        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render(f"{self.grid_position}", True, (0, 0, 0))
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1, border_radius=1)  # Draw border
        screen.blit(text, (self.position[0] + self.size // 2 - text.get_width() // 2, self.position[1] + self.size // 2 - text.get_height() // 2))

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
