import random

from settings import GRID_WIDTH, GRID_HEIGHT

def spawn_and_get_apple_position(
    snake_body: list[tuple[int, int]],
) -> tuple[int, int]:
    while True:
        position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1),
        )
        if position not in snake_body:
            return position


def check_apple_eaten(next_head: tuple[int, int], apple_pos: tuple[int, int]) -> bool:
    return next_head == apple_pos
