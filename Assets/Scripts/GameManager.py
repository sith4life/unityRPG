import random
import pygame
from game_engine import GameObject, Color, Vector2, Vector3, Debug
from tile import Tile
from player import Player, UserPlayer, AIPlayer
from tile_highlight import TileHighlight
from tile_path_finder import TilePathFinder

class GameManager(GameObject):
    instance = None

    def __init__(self):
        if GameManager.instance is None:
            GameManager.instance = self
        self.map_size = 11
        self.player_index = 0
        self.map = []
        self.players = []

    def awake(self):
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

    def render(self, screen):
        """Render the map and players."""
        for row in self.map:
            for tile in row:
                tile.render(screen)
        for player in self.players:
            player.render(screen)

    def next_turn(self):
        """Move to the next player's turn."""
        self.player_index = (self.player_index + 1) % len(self.players)

    def move_current_player(self, destination_tile):
        """Move the current player to the specified tile."""
        current_player = self.players[self.player_index]
        if not destination_tile.im_passable:
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
        for i in range(self.map_size):
            row = []
            for j in range(self.map_size):
                tile = Tile(position=(i * 50, j * 50))  # Example tile size of 50x50 pixels
                tile.grid_position = (i, j)
                row.append(tile)
            self.map.append(row)

    def generate_players(self):
        """Generate players and add them to the game."""
        player1 = UserPlayer(position=(50, 50), name="Player 1")
        player2 = AIPlayer(position=(450, 450), name="AI Player")
        self.players.append(player1)
        self.players.append(player2)