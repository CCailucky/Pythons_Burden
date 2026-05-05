import random

from settings import GRID_WIDTH, GRID_HEIGHT, TARGET_SEQUENCE


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


def handle_apple_eaten(
    snake_body: list[tuple[int, int]],
    apple_letter: str,
    collected_letters: str,
) -> tuple[tuple[int, int], str, str]:
    collected_letters += apple_letter
    next_index = len(collected_letters)
    if next_index < len(TARGET_SEQUENCE):
        apple_letter = TARGET_SEQUENCE[next_index]
    else:
        apple_letter = "?"
    apple_pos = spawn_and_get_apple_position(snake_body)
    return apple_pos, apple_letter, collected_letters
