import pygame
from settings import (
    GRID_WIDTH,
    GRID_HEIGHT,
    GRID_SIZE,
    MAP_X,
    MAP_Y,
    MAP_WIDTH,
    MAP_HEIGHT,
    MAP_COLOUR,
)

EMPTY = "empty"
WALL = "wall"
OBSTACLE = "obstacle"
PORTAL = "portal"
EXIT = "exit"


class GameMap:
    def __init__(self):
        self.grid = self.create_empty_grid()

    def create_empty_grid(self) -> list[list[str]]:
        grid = []
        for y in range(GRID_HEIGHT):
            row = []
            for x in range(GRID_WIDTH):
                row.append(EMPTY)
            grid.append(row)
        return grid

    def draw(self, screen) -> None:
        map_rect = pygame.Rect(MAP_X, MAP_Y, MAP_WIDTH, MAP_HEIGHT)
        pygame.draw.rect(screen, MAP_COLOUR, map_rect)

    def is_inside_map(self, pos: tuple[int, int]) -> bool:
        x, y = pos

        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

    def get_grid(self, pos: tuple[int, int]) -> str:
        x, y = pos
        return self.grid[y][x]

    def set_grid(self, pos: tuple[int, int], cell_type: str) -> None:
        x, y = pos
        self.grid[y][x] = cell_type

    # waiting for modifying
    def is_walkable(self, pos: tuple[int, int]) -> bool:
        cell_type = self.get_grid(pos)

        return cell_type in [EMPTY, PORTAL, EXIT]
