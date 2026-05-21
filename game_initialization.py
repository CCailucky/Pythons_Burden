import pygame

from display_manager import DisplayManager
from game_controller import GameController
from game_map import GameMap
from ui import UI


def initialize_game():
    pygame.init()
    display = DisplayManager()
    pygame.display.set_caption("Python's Burden: Escape from COMP9001")
    clock = pygame.time.Clock()

    game_map = GameMap()
    grid_font = pygame.font.Font(None, 26)
    ui = UI()
    game = GameController(game_map, ui, grid_font)

    return display, clock, game
