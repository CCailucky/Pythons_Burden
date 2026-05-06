import pygame
from settings import DIRECTIONS
def handle_events(
    game_running: bool,
    direction: tuple[int, int],
    game_over: bool,
) -> tuple[bool, tuple[int, int], bool]:
    restart_request = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            # game is over then press r to restart the game
            if game_over and event.key == pygame.K_r:
                restart_request = True

        if not game_over and event.type == pygame.KEYDOWN:
            # Change direction by arrow keys. No 180-degree turn.
            if event.key == pygame.K_UP and direction != DIRECTIONS["DOWN"]:
                direction = DIRECTIONS["UP"]
            elif event.key == pygame.K_DOWN and direction != DIRECTIONS["UP"]:
                direction = DIRECTIONS["DOWN"]
            elif event.key == pygame.K_LEFT and direction != DIRECTIONS["RIGHT"]:
                direction = DIRECTIONS["LEFT"]
            elif event.key == pygame.K_RIGHT and direction != DIRECTIONS["LEFT"]:
                direction = DIRECTIONS["RIGHT"]

    return game_running, direction, restart_request