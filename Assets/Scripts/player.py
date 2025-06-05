import pygame

class Player:
    def __init__(self, position=(0, 0), name="Player",is_ai=False, size=50, color=(255, 255, 255)):
        """Initialize the player with position, name, and AI status."""
        self.moving = False
        self.target_positions = []
        self.attacking = False
        self.is_ai = is_ai

        self.path = []
        self.position_queue = []
        self.target = None
        self.target_position = None
        self.move_speed = 200.0  # Speed of the player
        self.attack_speed = 1.0  # Attack speed of the player
        self.attack_range = 1.0  # Attack range of the player
        self.movement_range = 4  # Movement range of the player
        self.action_points = 2  # Action points for the player
        self.attacking = False
        self.moving = False

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
        self.color = color  # Default color (white)
        self.radius = 15  # Radius for rendering the player as a circle
        self.transform = pygame.Rect(position[1],position[0],self.radius,self.radius)
        self.position = pygame.math.Vector2(position)
        self.grid_position : tuple = (int(position[1] // size), int(position[0] // size))

    def update(self, delta_time):
        """Update the player's position based on delta time."""
        if self.moving and self.current_target:
            # Calculate the direction vector toward the target
            direction = self.current_target - self.position
            print(direction)
            distance_to_move = self.move_speed * delta_time  # Movement increment based on delta time

            print(f"Position: {self.position}, Target: {self.current_target}, Direction: {direction}, Distance to Move: {distance_to_move}")  # Debug print
            
            if direction.length() > 0:  # Avoid division by zero
                direction = direction.normalize()  # Normalize the direction vector

            # Move toward the target
            if direction.length() > distance_to_move:
                self.position += direction * distance_to_move
            else:
                # Snap to the target only when fully reached
                self.position = self.current_target
                self.grid_position = (int(self.position.y // 50), int(self.position.x // 50))
                if self.target_positions:
                    self.current_target = self.target_positions.pop(0)
                else:
                    self.moving = False
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
        pygame.draw.circle(screen, self.color, (round(self.position.x), round(self.position.y)), self.radius)

    def move_to(self, map):
        """Set the path for the player to follow."""
        tile_size = map.tile_size
        path = map.path
        self.target_positions = [pygame.math.Vector2(tile.position) + (map.tile_size // 2, map.tile_size // 2) for tile in map.path]
        print(f"Target Positions: {self.target_positions}")  # Debug print
        if self.target_positions:
            self.current_target = self.target_positions.pop(0)
            self.moving = True
        else:
            self.moving = False
            

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