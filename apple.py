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


class AppleManager:
    def __init__(
        self,
        player_snake,
        game_map,
        collected_letters: list[str],
        max_apples: int,
    ):
        self.max_apples = max_apples
        self.apples = []
        self.spawn_apples(player_snake, game_map, collected_letters)

    def get_next_required_letter(self, collected_letters: list[str]) -> str:
        next_index = len(collected_letters)
        if next_index < len(TARGET_SEQUENCE):
            return TARGET_SEQUENCE[next_index]
        return "?"

    def spawn_one_apple(
        self,
        player_snake,
        game_map,
        letter: str,
    ) -> None:
        occupied_positions = self.get_occupied_positions(player_snake)

        new_apple = Apple(
            game_map,
            letter,
            occupied_positions,
        )

        self.apples.append(new_apple)

    def spawn_apples(
        self,
        player_snake,
        game_map,
        collected_letters: list[str],
    ) -> None:
        self.apples = []
        # NOT AVAILABLE POSITION FOR SPAWNING
        occupied_positions = player_snake.body.copy()
        correct_letter = self.get_next_required_letter(collected_letters)
        # Make sure there is at least one correct letter apple.
        correct_apple = Apple(
            game_map,
            correct_letter,
            occupied_positions,
        )
        self.apples.append(correct_apple)
        occupied_positions.append(correct_apple.pos)
        # Spawn random letter apples.
        while len(self.apples) < self.max_apples:
            random_letter = get_random_apple_letter()
            random_apple = Apple(
                game_map,
                random_letter,
                occupied_positions,
            )
            self.apples.append(random_apple)
            occupied_positions.append(random_apple.pos)

    def has_correct_letter(self, letter: str) -> bool:
        for apple in self.apples:
            if apple.letter == letter:
                return True

        return False

    def remove_expired_apples(self) -> None:
        valid_apples = []

        for apple in self.apples:
            if not apple.is_expired():
                valid_apples.append(apple)

        self.apples = valid_apples

    def refill_apples(
        self,
        player_snake,
        game_map,
        collected_letters: list[str],
    ) -> None:
        required_letter = self.get_next_required_letter(collected_letters)
        # refill correct letter apple
        if len(self.apples) < self.max_apples and not self.has_correct_letter(
            required_letter
        ):
            self.spawn_one_apple(player_snake, game_map, required_letter)
        # refill random letter apple
        while len(self.apples) < self.max_apples:
            random_letter = get_random_apple_letter()
            self.spawn_one_apple(player_snake, game_map, random_letter)

    def get_eaten_apple(self, next_head: tuple[int, int]) -> Apple | None:
        for apple in self.apples:
            if apple.check_apple_eaten(next_head):
                return apple
        return None

    def handle_apple_eaten(
        self,
        eaten_apple: Apple,
        player_snake,
        game_map,
        collected_letters: list[str],
    ) -> list[str]:
        if eaten_apple in self.apples:
            self.apples.remove(eaten_apple)

        collected_letters.append(eaten_apple.letter)
        self.refill_apples(
            player_snake,
            game_map,
            collected_letters,
        )
        return collected_letters

    # currently occupied positions
    def get_occupied_positions(self, player_snake) -> list[tuple[int, int]]:
        occupied_positions = player_snake.body.copy()
        for apple in self.apples:
            occupied_positions.append(apple.pos)
        return occupied_positions

    # update apples' status
    def update(
        self,
        player_snake,
        game_map,
        collected_letters: list[str],
    ) -> None:
        self.remove_expired_apples()
        self.refill_apples(player_snake, game_map, collected_letters)

    # draw all apples
    def draw(self, screen, font) -> None:
        for apple in self.apples:
            apple.draw(screen, font)


def check_target_completed(collected_letters: list[str]) -> bool:
    return "".join(collected_letters) == TARGET_SEQUENCE


def get_random_apple_letter() -> str:
    return random.choice(string.ascii_uppercase)  # ABCDEFGHIJKLMNOPQRSTUVWXYZ


# # multiple apples
# def spawn_and_get_apples(
#     snake_body: list[tuple[int, int]],
#     game_map,
#     collected_letters: list[str],
#     max_apples: int,
# ) -> list[Apple]:
#     apples = []

#     # Store all positions that apples should not spawn on.
#     occupied_positions = snake_body.copy()
#     next_index = len(collected_letters)

#     if next_index < len(TARGET_SEQUENCE):
#         correct_letter = TARGET_SEQUENCE[next_index]
#     else:
#         correct_letter = "?"
#     # Make sure there is at least one correct letter apple.
#     correct_apple = Apple(
#         game_map,
#         correct_letter,
#         occupied_positions,
#     )
#     # Make sure there is at least one correct letter apple.
#     apples.append(correct_apple)
#     occupied_positions.append(correct_apple.pos)
#     # Spawn random letter apples.
#     while len(apples) < max_apples:
#         random_letter = get_random_apple_letter()
#         random_apple = Apple(
#             game_map,
#             random_letter,
#             occupied_positions,
#         )

#         apples.append(random_apple)
#         occupied_positions.append(random_apple.pos)

#     return apples
