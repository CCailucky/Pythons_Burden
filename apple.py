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
    APPLE_LIFETIME_MS,
    APPLE_LIFETIME_RANDOM_RANGE_MS,
)


class Apple:
    def __init__(
        self,
        game_map,
        letter: str,
        occupied_positions: list[tuple[int, int]],
    ):
        self.pos = self.spawn_and_get_apple_position(game_map, occupied_positions)
        self.letter = letter
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = self.get_random_lifetime()

    # single apple
    def spawn_and_get_apple_position(
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

        pygame.draw.rect(screen, APPLE_COLOUR, rect)

        letter_text = font.render(self.letter, True, TEXT_COLOUR)
        letter_rect = letter_text.get_rect(center=rect.center)
        screen.blit(letter_text, letter_rect)

    def check_apple_eaten(self, next_head: tuple[int, int]) -> bool:
        return next_head == self.pos

    def get_random_lifetime(self) -> int:
        return random.randint(
            APPLE_LIFETIME_MS - APPLE_LIFETIME_RANDOM_RANGE_MS,
            APPLE_LIFETIME_MS + APPLE_LIFETIME_RANDOM_RANGE_MS,
        )

    def is_expired(self) -> bool:
        current_time = pygame.time.get_ticks()
        return current_time - self.spawn_time >= self.lifetime


#
#
#
#
#
#


class AppleManager:
    def __init__(
        self,
        game_map,
        collected_letters: list[str],
        occupied_positions: list[tuple[int, int]],
        max_apples: int,
    ):
        self.max_apples = max_apples
        self.apples = []
        self.occupied_positions = occupied_positions
        self.spawn_apples(game_map, collected_letters)
    def get_next_required_letter(self, collected_letters: list[str]) -> str:
        next_index = len(collected_letters)
        if next_index < len(TARGET_SEQUENCE):
            return TARGET_SEQUENCE[next_index]
        return "?"
# after spawning, occupied_positions must be updated
    def spawn_one_apple(
        self,
        game_map,
        letter: str,
    ) -> None:
        new_apple = Apple(
            game_map,
            letter,
            self.occupied_positions,
        )

        self.apples.append(new_apple)
        self.occupied_positions.append(new_apple.pos)

    # used when initialize apple manager OR restart the game
    def spawn_apples(
        self,
        game_map,
        collected_letters: list[str],
    ) -> None:
        # Remove old apple positions from occupied_positions
        for apple in self.apples:
            if apple.pos in self.occupied_positions:
                self.occupied_positions.remove(apple.pos)

        self.apples = []

        correct_letter = self.get_next_required_letter(collected_letters)
        # Make sure there is at least one correct letter apple.
        self.spawn_one_apple(
            game_map,
            correct_letter,
        )
        # Spawn random letter apples.
        while len(self.apples) < self.max_apples:
            random_letter = get_random_apple_letter()
            self.spawn_one_apple(
                game_map,
                random_letter,
            )

    def has_correct_letter(self, correct_letter: str) -> bool:
        for apple in self.apples:
            if apple.letter == correct_letter:
                return True
        return False

    def remove_expired_apples(self) -> None:
        valid_apples = []

        for apple in self.apples:
            if apple.is_expired():
                if apple.pos in self.occupied_positions:
                    self.occupied_positions.remove(apple.pos)
            else:
                valid_apples.append(apple)

        self.apples = valid_apples

    def refill_apples(
        self,
        game_map,
        collected_letters: list[str],
    ) -> None:
        required_letter = self.get_next_required_letter(collected_letters)
        # refill correct letter apple
        if len(self.apples) < self.max_apples and not self.has_correct_letter(
            required_letter
        ):
            self.spawn_one_apple(
                game_map,
                required_letter
            )
        # refill random letter apple
        while len(self.apples) < self.max_apples:
            random_letter = get_random_apple_letter()

            self.spawn_one_apple(
                game_map,
                random_letter,
            )

    # update apples' status
    def update(
        self,
        game_map,
        collected_letters: list[str],
    ) -> None:
        self.remove_expired_apples()
        self.refill_apples(game_map, collected_letters)

    def get_eaten_apple(self, next_head: tuple[int, int]) -> Apple | None:
        for apple in self.apples:
            if apple.check_apple_eaten(next_head):
                return apple
        return None

    def handle_apple_eaten(
        self,
        eaten_apple: Apple,
        game_map,
        collected_letters: list[str],
    ) -> list[str]:
        if eaten_apple in self.apples:
            self.apples.remove(eaten_apple)
        if eaten_apple.pos in self.occupied_positions:
            self.occupied_positions.remove(eaten_apple.pos)
        collected_letters.append(eaten_apple.letter)
        self.refill_apples(
            game_map,
            collected_letters
        )

        return collected_letters

    # draw all apples
    def draw(self, screen, font) -> None:
        for apple in self.apples:
            apple.draw(screen, font)


def check_target_completed(collected_letters: list[str]) -> bool:
    return "".join(collected_letters) == TARGET_SEQUENCE


def get_random_apple_letter() -> str:
    return random.choice(string.ascii_uppercase)  # ABCDEFGHIJKLMNOPQRSTUVWXYZ
