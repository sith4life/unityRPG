''' Main Game Manager File'''
import os
import random
import configparser
import pygame
from ai_player import AIPlayer
from user_player import UserPlayer
from player import Player
from tile import Tile
import a_star
class GameManager():
    ''' main game manager class '''
    instance = None

    def __init__(self):
        pygame.init()

        if GameManager.instance is None:
            GameManager.instance = self
            self.map_size = 0
            with open(os.path.join(os.path.dirname(__file__),'../conf/game_manager.conf'), 'r',encoding='ascii') as config_file:
                config = configparser.ConfigParser()
                config.read_file(config_file)
                self.tile_size = int(config.get('GameManager', 'tile_size'))
                self.player_index = int(config.get('GameManager', 'player_index'))
        self.player_index = 0
        self.map = []
        self.players = []
        self.path = []
        self.current_positions = []
        self.last_positions = []
        self.running = True
        self.clock = pygame.time.Clock()
        # frame rate independence for smoother gameplay across devices
        self.delta_time = 0
        self.prev_time = 0
        self.awake()
        self.start()
        self.setup_env()

    def awake(self):
        '''awake function'''
        GameManager.instance = self
        self.generate_map()

    def start(self):
        """Initialize the game by generating the map and players."""
        self.generate_players()

    def update(self):
        """Update the current player's turn."""
        self.players[self.player_index].update(self.delta_time)
    
    def get_delta_time(self):
        self.delta_time = self.clock.tick(60)  / 1000.0

    def render(self):
        """Render only visible tiles and players."""
        grid_display = pygame.Surface((self.map_size * self.tile_size, self.map_size * self.tile_size))
        # truncate the path based on the player's movement range
        draw_path = self.path[:self.players[self.player_index].movement_range]
        for row in self.map:
            for tile in row:
                if not draw_path:
                    tile.color = tile.default_color
                else:
                    if tile in draw_path:
                        tile.color = (255, 0, 0)
                    else:
                        tile.color = tile.default_color
                tile.render(grid_display)
        self.screen.blit(grid_display, (0, 0))
        for player in self.players:
            player.render(self.screen)
        
        pygame.display.flip()

    def next_turn(self):
        """Move to the next player's turn."""
        self.player_index = (self.player_index + 1) % len(self.players)

    def move_current_player(self, destination_tile):
        """Move the current player to the specified tile."""
        current_player = self.players[self.player_index]
        if not destination_tile.impassable:
            current_player.move_to(destination_tile.position)
            current_player.grid_position = destination_tile.grid_position

    def attack_with_current_player(self, target_tile):
        """Attack a target on the specified tile."""
        current_player = self.players[self.player_index]
        target = next((p for p in self.players if p.grid_position == target_tile.grid_position), None)
        if target:
            current_player.attack(target)

    def get_neighbours(self, tile):
        """Get the neighbouring tiles of a given tile."""
        neighbours = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                neighbour_x = tile.grid_posX() + x
                neighbour_y = tile.grid_posY() + y

                if 0 <= neighbour_x < self.map_size and 0 <= neighbour_y < self.map_size:
                    if abs(x) + abs(y) == 2:  # Diagonal movement
                        if self.map[tile.grid_posY()][neighbour_x].impassable or self.map[neighbour_y][tile.grid_posX()].impassable:
                            continue
                    neighbours.append(self.map[neighbour_y][neighbour_x])
        return neighbours
    def game_loop(self):
        while self.running:
            self.get_delta_time()
            self.get_events()
            self.pathfinding()
            self.update()
            self.render()
        pygame.quit()
    
    def generate_map(self):
        """Generate a grid-based map."""
        self.map = []

        with open(os.path.join(os.path.dirname(__file__),'../scenes/complex_map.csv'), 'r',encoding='ascii') as config_file:
            import csv # pylint: disable=import-outside-toplevel
            # Read the CSV file
            reader = csv.reader(config_file)
            for y,row in enumerate(reader):
                row_data = []
                for x,tile in enumerate(row):
                    impassable = 1 if int(tile) == 1 else 0
                    penalty = int(tile) if tile != 1 else 0
                    match penalty:
                        case 4: tile_color = (0,0,255)
                        case 3: tile_color = (165,42,42)
                        case 2: tile_color = (0, 255, 0)
                        case _: tile_color = (0, 0, 0) if impassable else (211, 211, 211)
                    tile_data = Tile(position=(x * self.tile_size, y * self.tile_size), size=self.tile_size, impassable=impassable, color=tile_color, penalty=penalty)
                    row_data.append(tile_data)
                self.map.append(row_data)
        self.map_size = len(self.map)
        print(f'Generating map {self.map_size} x {self.map_size}')
    def get_mouse(self):
        self.mouse_position = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
        self.mouse_pos_x = self.mouse_position[1] // game.tile_size
        self.mouse_pos_y = self.mouse_position[0] // game.tile_size

    def get_events(self):
        self.get_mouse()
        for event in pygame.event.get():
            match event.type:
                # quit game events
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                case pygame.KEYUP:
                    match event.key:
                        case pygame.K_RETURN:
                            previous_player_index = self.player_index
                            self.player_index = (game.player_index + 1) % len(game.players)
                            self.players[game.player_index].color = (255, 255, 0)
                            self.players[previous_player_index].color = self.players[previous_player_index].default_color
                        # reset game for testing purposes, including dynamic map file updates
                        case pygame.K_r:
                            for i in range(len(game.players)):
                                self.players.pop()
                            self.start()
                            self.player_index = 0
                            color_cache = (game.players[0].color,game.players[1].color)
                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click_position = ( self.mouse_position[1] // self.tile_size, self.mouse_position[0]  // self.tile_size)

                        if self.path:
                           if any(tile.grid_position == click_position for tile in self.path):
                                self.players[game.player_index].move_to(game)
                                self.next_turn()
                                CLICK_FRAME_DELAY = 60
    def generate_players(self):
        """Generate players and add them to the game."""
        while True:
            p1x = random.randint(0, self.map_size - 1)
            p1y = random.randint(0, self.map_size - 1)
            p2x = random.randint(0, self.map_size - 1)
            p2y = random.randint(0, self.map_size - 1)

            while self.map[p1x][p1y].impassable:
                print("Player 1 is on an impassable tile, re-rolling position.")
                p1x = random.randint(0, self.map_size - 1)
                p1y = random.randint(0, self.map_size - 1)
            while self.map[p2x][p2y].impassable:
                print("Player 2 is on an impassable tile, re-rolling position.")
                p2x = random.randint(0, self.map_size - 1)
                p2y = random.randint(0, self.map_size - 1)
            # Ensure players are not placed on the same tile
            if p1x != p2x or p1y != p2y:
                break  # Valid positions found
        p1_pos = self.map[p1x][p1y].position + (self.tile_size // 2, self.tile_size // 2)
        p2_pos = self.map[p2x][p2y].position + (self.tile_size // 2, self.tile_size // 2)
        player1 = Player(position=(p1_pos), name="Player 1", color=(0, 100, 0))
        player2 = Player(position=(p2_pos), name="AI Player", color=(128, 0, 128))
        self.players.append(player1)
        self.players.append(player2)

    def setup_env(self):
        GAME_X = self.map_size * self.tile_size
        GAME_Y = self.map_size * self.tile_size
        print(f"Game size: {GAME_X} x {GAME_Y}")
        self.screen = pygame.display.set_mode((GAME_X, GAME_Y))
        pygame.display.set_caption(f"Game Map { GAME_X // self.tile_size } x { GAME_Y // self.tile_size }")

    def pathfinding(self):
        if not self.players[self.player_index].moving:
            if (self.mouse_pos_x == 0 and self.mouse_pos_y == 0 and self.last_positions == [None,None]) or self.map[self.mouse_pos_x][self.mouse_pos_y].impassable:
                path_to = self.players[self.player_index].grid_position
            else:
                path_to = (self.mouse_pos_x,self.mouse_pos_y)
            self.current_positions = [
                path_to,
                self.players[self.player_index].grid_position
            ]

            if self.current_positions != self.last_positions:
                full_path = a_star.find_path(
                    self.map[int(self.players[self.player_index].grid_position[0])][int(self.players[self.player_index].grid_position[1])],
                    self.map[path_to[0]][path_to[1]],
                    self
                )
                # Limit the path to the player's movement range
                self.path = full_path[:int(self.players[self.player_index].movement_range)]
                self.last_positions = self.current_positions

if __name__ == '__main__':
    game = GameManager()
    
    while game.running:
        game.game_loop()

    
