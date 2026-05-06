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
    WALL_COLOUR,
)

EMPTY = "empty"
WALL = "wall"
OBSTACLE = "obstacle"
PORTAL = "portal"
EXIT = "exit"


class GameMap:
    def __init__(self):
        self.grid = self.create_empty_grid()
        self.create_test_walls()
    def create_empty_grid(self) -> list[list[str]]:
        grid = []
        for y in range(GRID_HEIGHT):
            row = []
            for x in range(GRID_WIDTH):
                row.append(EMPTY)
            grid.append(row)
        return grid


    def create_test_walls(self) -> None:
        for x in range(10, 20):
            self.set_grid((x, x), WALL)

    def draw(self, screen) -> None:
        map_rect = pygame.Rect(MAP_X, MAP_Y, MAP_WIDTH, MAP_HEIGHT)
        pygame.draw.rect(screen, MAP_COLOUR, map_rect)

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell_type = self.grid[y][x]

                if cell_type == WALL:
                    wall_rect = pygame.Rect(
                        MAP_X + x * GRID_SIZE,
                        MAP_Y + y * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE,
                    )
                    pygame.draw.rect(screen, WALL_COLOUR, wall_rect)

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
