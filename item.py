import random
import pygame

from settings import (
    GRID_WIDTH,
    GRID_HEIGHT,
    GRID_SIZE,
    MAP_X,
    MAP_Y,
    ITEM_TAIL_CUT_COLOUR,
    TEXT_COLOUR,
)


class ItemTailCut:
    def __init__(
        self,
        game_map,
        occupied_positions: list[tuple[int, int]],
    ):
        self.pos = self.spawn_and_get_position(game_map, occupied_positions)

    def spawn_and_get_position(
        self,
        game_map,
        occupied_positions: list[tuple[int, int]],
    ) -> tuple[int, int]:
        while True:
            pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )

            if game_map.is_available_for_spawn(pos, occupied_positions):
                return pos

    def draw(self, screen, font) -> None:
        x, y = self.pos

        rect = pygame.Rect(
            MAP_X + x * GRID_SIZE,
            MAP_Y + y * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE,
        )

        pygame.draw.rect(screen, ITEM_TAIL_CUT_COLOUR, rect)

        text = font.render("C", True, TEXT_COLOUR)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    def check_item_eaten(self, next_head: tuple[int, int]) -> bool:
        return next_head == self.pos