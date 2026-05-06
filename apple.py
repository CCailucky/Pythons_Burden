import random
import pygame
import string
from settings import (
    GRID_WIDTH,
    GRID_HEIGHT,
    GRID_SIZE,
    MAP_X,
    MAP_Y,
    APPLE_COLOUR,
    TEXT_COLOUR,
    TARGET_SEQUENCE,
)


class Apple:
    def __init__(
        self,
        snake_body: list[tuple[int, int]],
        game_map,
        letter: str,
    ):
        self.pos = self.spawn_and_get_apple_position(snake_body, game_map)
        self.letter = letter

    # single apple
    def spawn_and_get_apple_position(
        self,
        snake_body: list[tuple[int, int]],
        game_map,
    ) -> tuple[int, int]:
        while True:
            pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
            if pos not in snake_body and game_map.is_walkable(pos):
                return pos

    def draw(self, screen, font) -> None:
        x, y = self.pos

        rect = pygame.Rect(
            MAP_X + x * GRID_SIZE,
            MAP_Y + y * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE,
        )

        pygame.draw.rect(screen, APPLE_COLOUR, rect)

        letter_text = font.render(self.letter, True, TEXT_COLOUR)
        letter_rect = letter_text.get_rect(center=rect.center)
        screen.blit(letter_text, letter_rect)

    def check_apple_eaten(self, next_head: tuple[int, int]) -> bool:
        return next_head == self.pos




# def handle_apple_eaten(
#     snake_body: list[tuple[int, int]],
#     game_map,
#     apple: Apple,
#     collected_letters: list[str],
# ) -> tuple[Apple, list[str]]:
#     # add to the collected_letters
#     collected_letters.append(apple.letter)

#     next_index = len(collected_letters)

#     if next_index < len(TARGET_SEQUENCE):
#         next_letter = TARGET_SEQUENCE[next_index]
#     else:
#         next_letter = "?"
#     new_apple = Apple(snake_body, game_map, next_letter)

#     return new_apple, collected_letters

def get_random_apple_letter() -> str:
    return random.choice(string.ascii_uppercase)  # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    
def spawn_and_get_apples(
    snake_body: list[tuple[int, int]],
    game_map,
    collected_letters: list[str],
    max_apples: int,
) -> list[Apple]:
    apples = []

    next_index = len(collected_letters)

    if next_index < len(TARGET_SEQUENCE):
        correct_letter = TARGET_SEQUENCE[next_index]
    else:
        correct_letter = "?"

    # Make sure there is at least one correct letter apple.
    apples.append(Apple(snake_body, game_map, correct_letter))
    # random apple
    while len(apples) < max_apples:
        random_letter = get_random_apple_letter()
        apples.append(Apple(snake_body, game_map, random_letter))

    return apples

def get_eaten_apple(
    next_head: tuple[int, int],
    apples: list[Apple],
) -> Apple | None:
    for apple in apples:
        if apple.check_apple_eaten(next_head):
            return apple

    return None

def handle_apple_eaten(
    eaten_apple: Apple,
    collected_letters: list[str],
) -> list[str]:
    collected_letters.append(eaten_apple.letter)
    return collected_letters

def check_target_completed(collected_letters: list[str]) -> bool:
    return "".join(collected_letters) == TARGET_SEQUENCE
