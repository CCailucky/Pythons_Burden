import pygame
from settings import DIRECTIONS


def handle_events(
    game_running: bool,
    direction: tuple[int, int],
    game_over: bool,
    game_started: bool,
    game_paused: bool,
    ui,
) -> tuple[bool, tuple[int, int], bool, bool, bool, bool]:
    restart_request = False
    # shoot bullet
    shoot_request = False
    # avoid multiple actions in one frame
    direction_changed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            # press space to start the game
            if game_started == False and event.key == pygame.K_SPACE:
                game_started = True
                game_paused = False
                ui.add_status_message("Game started!")
            # press p to pause the game
            if game_started == True and not game_over and event.key == pygame.K_p:
                game_paused = not game_paused
                if game_paused:
                    ui.add_status_message("Game paused")
                else:
                    ui.add_status_message("Game resumed")
            # press f to fire a bullet
            if (
                game_started == True
                and not game_over
                and not game_paused
                and event.key == pygame.K_f
            ):
                shoot_request = True

            # game is over then press r to restart the game
            if game_over and event.key == pygame.K_r:
                restart_request = True

        if (
            event.type == pygame.KEYDOWN
            and game_started
            and not game_over
            and not game_paused
            and not direction_changed
        ):
            # Change direction by arrow keys. No 180-degree turn.
            if event.key == pygame.K_UP and direction != DIRECTIONS["DOWN"]:
                direction = DIRECTIONS["UP"]
                direction_changed = True
            elif event.key == pygame.K_DOWN and direction != DIRECTIONS["UP"]:
                direction = DIRECTIONS["DOWN"]
                direction_changed = True
            elif event.key == pygame.K_LEFT and direction != DIRECTIONS["RIGHT"]:
                direction = DIRECTIONS["LEFT"]
                direction_changed = True
            elif event.key == pygame.K_RIGHT and direction != DIRECTIONS["LEFT"]:
                direction = DIRECTIONS["RIGHT"]
                direction_changed = True
    return (
        game_running,
        direction,
        restart_request,
        game_started,
        game_paused,
        shoot_request,
    )
