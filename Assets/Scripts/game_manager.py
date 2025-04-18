''' Main Game Manager File'''
import random
import configparser
import pygame
from ai_player import AIPlayer
from user_player import UserPlayer
from tile import Tile
class GameManager():
    ''' main game manager class '''
    instance = None

    def __init__(self):
        if GameManager.instance is None:
            GameManager.instance = self
            self.map_size = 0
            with open('Assets/conf/game_manager.conf', 'r',encoding='ascii') as config_file:
                config = configparser.ConfigParser()
                config.read_file(config_file)
                self.tile_size = int(config.get('GameManager', 'tile_size'))
                self.player_index = int(config.get('GameManager', 'player_index'))
        self.player_index = 0
        self.map = []
        self.players = []

    def awake(self):
        '''awake function'''
        GameManager.instance = self

    def start(self):
        """Initialize the game by generating the map and players."""
        self.generate_map()
        self.generate_players()

    def update(self):
        """Update the current player's turn."""
        current_player = self.players[self.player_index]
        if current_player.hp > 0:
            current_player.turn_update()
        else:
            self.next_turn()

    def render(self, _screen):
        """Render the map and players."""
        for row in self.map:
            for tile in row:
                tile.render(_screen)
        for player in self.players:
            player.render(_screen)

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

    def generate_map(self):
        """Generate a grid-based map."""
        self.map = []

        with open('Assets/scenes/test_map.csv', 'r',encoding='ascii') as config_file:
            import csv # pylint: disable=import-outside-toplevel
            # Read the CSV file
            reader = csv.reader(config_file)
            for y,row in enumerate(reader):
                row_data = []
                for x,tile in enumerate(row):
                    impassable = int(tile)
                    tile_color = (0, 0, 0) if impassable else (255, 255, 255)
                    tile_data = Tile(position=(x * self.tile_size, y * self.tile_size), size=self.tile_size, impassable=impassable, color=tile_color)
                    row_data.append(tile_data)
                self.map.append(row_data)
        self.map_size = len(self.map)
        print(f'Generating map {self.map_size} x {self.map_size}')
    def display_map(self):
        """Display the generated map."""
        grid_display = pygame.Surface((self.map_size * self.tile_size, self.map_size * self.tile_size))

        for row in self.map:
            for tile in row:
                tile.render(grid_display)
    def generate_players(self):
        """Generate players and add them to the game."""
        p1x = random.randint(0, self.map_size - 1)
        p1y = random.randint(0, self.map_size - 1)
        p2x = random.randint(0, self.map_size - 1)
        p2y = random.randint(0, self.map_size - 1)

        # Ensure players are not placed on the same tile
        while p1x == p2x and p1y == p2y:
            print("Players are on the same tile, re-rolling positions.")
            p1x = random.randint(0, self.map_size - 1)
            p1y = random.randint(0, self.map_size - 1)
            p2x = random.randint(0, self.map_size - 1)
            p2y = random.randint(0, self.map_size - 1)
        # Ensure players are not placed on impassable tiles
        while self.map[p1x][p1y].impassable:
            print("Player 1 is on an impassable tile, re-rolling position.")
            p1x = random.randint(0, self.map_size - 1)
            p1y = random.randint(0, self.map_size - 1)
            p1_pos = self.map[p1x][p1y].center
        while self.map[p2x][p2y].impassable:
            print("Player 2 is on an impassable tile, re-rolling position.")
            p2x = random.randint(0, self.map_size - 1)
            p2y = random.randint(0, self.map_size - 1)
            p2_pos = self.map[p2x][p2y].center
        p1_pos = self.map[p1x][p1y].center
        p2_pos = self.map[p2x][p2y].center
        player1 = UserPlayer(position=(p1_pos), name="Player 1")
        player2 = AIPlayer(position=(p2_pos), name="AI Player")
        player1.color = (0, 100, 0)  # Green for user player
        player2.color = (128,0,128) # Purple for AI player
        self.players.append(player1)
        self.players.append(player2)

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    RUNNING = True
    game = GameManager()
    game.awake()
    game.start()
    GAME_X = game.map_size * game.tile_size
    GAME_Y = game.map_size * game.tile_size
    print(f"Game size: {GAME_X} x {GAME_Y}")
    screen = pygame.display.set_mode((GAME_X, GAME_Y))
    game.display_map()
    pygame.display.set_caption(f"Game Map { GAME_X // game.tile_size } x { GAME_Y // game.tile_size }")
    color_cache = (game.players[0].color,game.players[1].color)
    CLICK_FRAME_DELAY = 0
    while RUNNING:
        mouse_position = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
        for map_y in game.map:
            for map_x in map_y:
                if CLICK_FRAME_DELAY <= 0:
                    map_x.update(mouse_position)
        for event in pygame.event.get():
            match event.type:
                # quit game events
                case pygame.QUIT:
                    RUNNING = False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        RUNNING = False
                #gameplay keyboard events
                case pygame.KEYUP:
                    match event.key:
                        case pygame.K_RETURN:
                            previous_player_index = game.player_index
                            game.player_index = (game.player_index + 1) % len(game.players)
                            game.players[game.player_index].color = (255, 255, 0)
                            game.players[previous_player_index].color = color_cache[previous_player_index]
                        # reset game for testing purposes, including dynamic map file updates
                        case pygame.K_r:
                            for i in range(len(game.players)):
                                game.players.pop()
                            game.start()
                            game.player_index = 0
                            color_cache = (game.players[0].color,game.players[1].color)
                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for map_row in game.map:
                            for map_tile in map_row:
                                if map_tile.on_mouse_enter(mouse_position):
                                    if CLICK_FRAME_DELAY <= 0:
                                        map_tile.update(mouse_position, True)
                                    CLICK_FRAME_DELAY = 60
                                    break
        screen.fill((255, 255, 255))  # Clear screen with white color
        game.render(screen)
        pygame.display.flip()
        clock.tick(60)
        CLICK_FRAME_DELAY -= 1
    pygame.quit()
