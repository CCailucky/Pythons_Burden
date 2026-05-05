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
def draw_apple(screen, apple_pos: tuple[int, int]) -> None:
    x, y = apple_pos

    rect = pygame.Rect(
        MAP_X + x * GRID_SIZE, MAP_Y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE
    )

    pygame.draw.rect(screen, APPLE_COLOUR, rect)


# for test not completed
def draw_ui(screen, font, lives: int, game_over: bool) -> None:
    ui_rect = pygame.Rect(UI_X, UI_Y, UI_WIDTH, UI_HEIGHT)
    pygame.draw.rect(screen, UI_COLOUR, ui_rect)

    title_text = font.render("Python's Burden", True, TEXT_COLOUR)
    screen.blit(title_text, (UI_X + 20, UI_Y + 20))

    control_text = font.render("Arrow Keys: Move", True, TEXT_COLOUR)
    screen.blit(control_text, (UI_X + 20, UI_Y + 70))

    lives_text = font.render(f"Lives: {lives}", True, TEXT_COLOUR)
    screen.blit(lives_text, (UI_X + 20, UI_Y + 120))

    if game_over:
        game_over_text = font.render("Game Over", True, TEXT_COLOUR)
        screen.blit(game_over_text, (UI_X + 20, UI_Y + 170))
        
        restart_text = font.render("Press R to restart", True, TEXT_COLOUR)
        screen.blit(restart_text, (UI_X + 20, UI_Y + 220))