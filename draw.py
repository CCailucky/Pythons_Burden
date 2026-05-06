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
