import pygame

from settings import (
    GRID_SIZE,
    MAP_X,
    MAP_Y,
    MAP_WIDTH,
    MAP_HEIGHT,
    UI_X,
    UI_Y,
    UI_WIDTH,
    UI_HEIGHT,
    MAP_COLOUR,
    SNAKE_COLOUR,
    APPLE_COLOUR,
    UI_COLOUR,
    TEXT_COLOUR,
    TARGET_SEQUENCE,
)


def draw_map(screen) -> None:
    map_rect = pygame.Rect(MAP_X, MAP_Y, MAP_WIDTH, MAP_HEIGHT)
    pygame.draw.rect(screen, MAP_COLOUR, map_rect)


def draw_snake(screen, snake_body: list[tuple[int, int]]) -> None:
    for segment in snake_body:
        x, y = segment
        # start from (MAP_X, MAP_Y)
        rect = pygame.Rect(
            MAP_X + x * GRID_SIZE, MAP_Y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(screen, SNAKE_COLOUR, rect)


# similar to draw a snake
# def draw_apple(screen, font, apple_pos: tuple[int, int], apple_letter: str) -> None:
#     x, y = apple_pos

#     rect = pygame.Rect(
#         MAP_X + x * GRID_SIZE, MAP_Y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE
#     )

#     pygame.draw.rect(screen, APPLE_COLOUR, rect)
#     # draw letter
#     letter_text = font.render(apple_letter, True, TEXT_COLOUR)
#     letter_rect = letter_text.get_rect(center=rect.center)
#     screen.blit(letter_text, letter_rect)


# for test not completed
def draw_ui(
    screen,
    font,
    lives: int,
    game_over: bool,
    game_win: bool,
    collected_letters: list[str],
) -> None:
    ui_rect = pygame.Rect(UI_X, UI_Y, UI_WIDTH, UI_HEIGHT)
    pygame.draw.rect(screen, UI_COLOUR, ui_rect)

    title_text = font.render("Python's Burden", True, TEXT_COLOUR)
    screen.blit(title_text, (UI_X + 20, UI_Y + 20))

    control_text = font.render("Arrow Keys: Move", True, TEXT_COLOUR)
    screen.blit(control_text, (UI_X + 20, UI_Y + 70))

    lives_text = font.render(f"Lives: {lives}", True, TEXT_COLOUR)
    screen.blit(lives_text, (UI_X + 20, UI_Y + 120))

    target_text = font.render("Target:", True, TEXT_COLOUR)
    screen.blit(target_text, (UI_X + 20, UI_Y + 170))

    target_value = font.render(TARGET_SEQUENCE, True, TEXT_COLOUR)
    screen.blit(target_value, (UI_X + 20, UI_Y + 200))

    collected_text = font.render("Collected:", True, TEXT_COLOUR)
    screen.blit(collected_text, (UI_X + 20, UI_Y + 250))

    collected_value = font.render("".join(collected_letters), True, TEXT_COLOUR)
    screen.blit(collected_value, (UI_X + 20, UI_Y + 280))

    if game_over:
        game_over_text = font.render("Game Over", True, TEXT_COLOUR)
        screen.blit(game_over_text, (UI_X + 20, UI_Y + 170))

        restart_text = font.render("Press R to restart", True, TEXT_COLOUR)
        screen.blit(restart_text, (UI_X + 20, UI_Y + 220))
    if game_win:
        victory_text = font.render("Sequence Complete! You Win!", True, TEXT_COLOUR)
        screen.blit(victory_text, (UI_X + 20, UI_Y + 340))

        restart_text = font.render("Press R to restart", True, TEXT_COLOUR)
        screen.blit(restart_text, (UI_X + 20, UI_Y + 390))
