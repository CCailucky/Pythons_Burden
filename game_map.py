import pygame
from pathlib import Path
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
    PORTAL_COLOUR,
    INITIAL_SNAKE_BODY,
)
from assets_loader import load_grid_image, load_image

EMPTY = "empty"
WALL = "wall"
OBSTACLE = "obstacle"
PORTAL = "portal"
EXIT = "exit"


class GameMap:
    def __init__(self):
        self.grid = self.create_empty_grid()
        self.portal_positions = []
        self.portal_active = False
        self.create_walls()
        self.reachable_spawn_positions = self.get_reachable_positions(
            INITIAL_SNAKE_BODY[0]
        )
        # assets
        self.floor_tile_image = load_grid_image("assets/images/tiles/floor_tile16.png")
        self.wall_tile_image = load_grid_image("assets/images/tiles/wall_tile16.png")
        self.portal_image = load_image(
            "assets/images/portal/portal.png", (GRID_SIZE * 3, GRID_SIZE * 3)
        )

    def create_empty_grid(self) -> list[list[str]]:
        grid = []
        for y in range(GRID_HEIGHT):
            row = []
            for x in range(GRID_WIDTH):
                row.append(EMPTY)
            grid.append(row)
        return grid

    def create_walls(self) -> None:
        wall_map = [
            "###########......................................###########",
            "#..........................................................#",
            "#.#######..........................................#######.#",
            "#.#......................................................#.#",
            "#.#.###..............................................###.#.#",
            "#.#.##................................................##.#.#",
            "#.#.#..................................................#.#.#",
            "#.#......................................................#.#",
            "#.#......................................................#.#",
            "#..........................................................#",
            "#..........................................................#",
            "............................................................",
            "............................................................",
            "............................................................",
            "............................................................",
            ".................#####..#####..#...#..#####.................",
            ".................#......#...#..##.##..#...#.................",
            ".................#......#...#..#.#.#..#...#.................",
            ".................#......#...#..#...#..#####.................",
            ".................#......#...#..#...#..#.....................",
            ".................#......#...#..#...#..#.....................",
            ".................#####..#####..#...#..#.....................",
            "............................................................",
            "............................................................",
            "............................................................",
            "............................................................",
            ".................#####..#####..#####....#...................",
            ".................#...#..#...#..#...#...##...................",
            ".................#...#..#...#..#...#..#.#...................",
            ".................#####..#...#..#...#....#...................",
            ".....................#..#...#..#...#....#...................",
            ".....................#..#...#..#...#....#...................",
            ".................#####..#####..#####..#####.................",
            "............................................................",
            "............................................................",
            "............................................................",
            "............................................................",
            "............................................................",
            "............................................................",
            "............................................................",
            "............................................................",
            "............................................................",
            "............................................................",
            "............................................................",
            "............................................................",
            "............................................................",
            "............................................................",
            "............................................................",
            "............................................................",
            "#..........................................................#",
            "#..........................................................#",
            "#.#......................................................#.#",
            "#.#......................................................#.#",
            "#.#.#..................................................#.#.#",
            "#.#.##................................................##.#.#",
            "#.#.###..............................................###.#.#",
            "#.#......................................................#.#",
            "#.#######..........................................#######.#",
            "#..........................................................#",
            "###########......................................###########",
        ]
        for y in range(len(wall_map)):
            row = wall_map[y]
            for x in range(len(row)):
                if row[x] == "#":
                    self.set_grid((x, y), WALL)

    def draw(self, screen) -> None:
        map_rect = pygame.Rect(MAP_X, MAP_Y, MAP_WIDTH, MAP_HEIGHT)
        pygame.draw.rect(screen, MAP_COLOUR, map_rect)

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell_type = self.grid[y][x]

                draw_pos = (
                    MAP_X + x * GRID_SIZE,
                    MAP_Y + y * GRID_SIZE,
                )

                cell_rect = pygame.Rect(
                    draw_pos[0],
                    draw_pos[1],
                    GRID_SIZE,
                    GRID_SIZE,
                )

                # Draw floor first for all non-wall cells.
                if cell_type != WALL:
                    if self.floor_tile_image is not None:
                        screen.blit(self.floor_tile_image, draw_pos)
                    else:
                        pygame.draw.rect(screen, MAP_COLOUR, cell_rect)

                # Draw wall tile.
                if cell_type == WALL:
                    if self.wall_tile_image is not None:
                        screen.blit(self.wall_tile_image, draw_pos)
                    else:
                        pygame.draw.rect(screen, WALL_COLOUR, cell_rect)

                # Draw floor firstly, then draw portal on top of floor if it's a portal cell.
                if cell_type == PORTAL:
                    if self.floor_tile_image is not None:
                        screen.blit(self.floor_tile_image, draw_pos)
                    else:
                        pygame.draw.rect(screen, MAP_COLOUR, cell_rect)
        self.draw_portal(screen)
        
    def draw_portal(self, screen) -> None:
        if not self.portal_active:
            return
        if len(self.portal_positions) == 0:
            return

        portal_x = min(pos[0] for pos in self.portal_positions)
        portal_y = min(pos[1] for pos in self.portal_positions)

        draw_pos = (
            MAP_X + portal_x * GRID_SIZE,
            MAP_Y + portal_y * GRID_SIZE,
        )

        if self.portal_image is not None:
            screen.blit(self.portal_image, draw_pos)
            return

        # fallback: old 3x3 rect portal
        for x, y in self.portal_positions:
            rect = pygame.Rect(
                MAP_X + x * GRID_SIZE,
                MAP_Y + y * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE,
            )
            pygame.draw.rect(screen, PORTAL_COLOUR, rect)
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

    def is_available_for_spawn(
        self, pos: tuple[int, int], occupied_positions: list[tuple[int, int]]
    ) -> bool:
        return (
            self.get_grid(pos) == EMPTY
            and pos in self.reachable_spawn_positions
            and pos not in occupied_positions
        )

    # for reset / restart
    def clear_portal(self) -> None:
        for pos in self.portal_positions:
            self.set_grid(pos, EMPTY)

        self.portal_positions = []
        self.portal_active = False

    # system can place 3x3 portal or not
    def can_place_portal(
        self,
        top_left: tuple[int, int],
        occupied_positions: list[tuple[int, int]],
    ) -> bool:
        start_x, start_y = top_left

        for y in range(start_y, start_y + 3):
            for x in range(start_x, start_x + 3):
                pos = (x, y)

                if not self.is_inside_map(pos):
                    return False

                if self.get_grid(pos) != EMPTY:
                    return False

                if pos in occupied_positions:
                    return False

        return True

    # spawn a portal far away from player
    def spawn_portal_far_from_player(
        self,
        player_pos: tuple[int, int],
        occupied_positions: list[tuple[int, int]],
    ) -> bool:
        if self.portal_active:
            return True

        best_top_left = None
        best_distance = -1

        player_x, player_y = player_pos

        for y in range(GRID_HEIGHT - 2):
            for x in range(GRID_WIDTH - 2):
                top_left = (x, y)

                if self.can_place_portal(top_left, occupied_positions):
                    center_x = x + 1
                    center_y = y + 1
                    # use Manhattan distance to judge the farthest distance
                    distance = abs(center_x - player_x) + abs(center_y - player_y)

                    if distance > best_distance:
                        best_distance = distance
                        best_top_left = top_left

        if best_top_left == None:
            return False

        start_x, start_y = best_top_left

        self.portal_positions = []

        for y in range(start_y, start_y + 3):
            for x in range(start_x, start_x + 3):
                pos = (x, y)
                self.set_grid(pos, PORTAL)
                self.portal_positions.append(pos)

        self.portal_active = True
        return True

    def is_portal(self, pos: tuple[int, int]) -> bool:
        return self.get_grid(pos) == PORTAL

    # quantum_transit func is used for BFS
    def quantum_transit(self, position: tuple[int, int]) -> tuple[int, int]:
        x, y = position

        if x < 0:
            x = GRID_WIDTH - 1
        elif x >= GRID_WIDTH:
            x = 0

        if y < 0:
            y = GRID_HEIGHT - 1
        elif y >= GRID_HEIGHT:
            y = 0

        return (x, y)

    # BFS to get all reachable positions from a start position
    def get_reachable_positions(
        self, start_pos: tuple[int, int]
    ) -> set[tuple[int, int]]:
        reachable_positions = set()
        positions_to_check = [start_pos]

        while len(positions_to_check) > 0:

            # like queue pop
            current_pos = positions_to_check.pop(0)
            # already in the set, no need to check again
            if current_pos in reachable_positions:
                continue
            # not walkable, skip
            if not self.is_walkable(current_pos):
                continue

            reachable_positions.add(current_pos)

            x, y = current_pos
            neighbour_positions = [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ]

            for neighbour_pos in neighbour_positions:
                neighbour_pos = self.quantum_transit(neighbour_pos)
                if neighbour_pos not in reachable_positions:
                    positions_to_check.append(neighbour_pos)
        return reachable_positions
