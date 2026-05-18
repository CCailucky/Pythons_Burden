import pygame
from settings import DIRECTIONS


def handle_events(
    game_running: bool,
    current_direction: tuple[int, int],
    pending_direction: tuple[int, int],
    game_over: bool,
    game_started: bool,
    game_paused: bool,
    ui,
) -> tuple[bool, tuple[int, int], bool, bool, bool, bool]:
    restart_request = False
    shoot_request = False

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

            if game_started and not game_over and not game_paused:
                # Change pending direction by arrow keys.
                # Only allow one queued turn before the next snake move.
                if pending_direction == current_direction :
                    if event.key == pygame.K_UP and current_direction  != DIRECTIONS["DOWN"]:
                        pending_direction  = DIRECTIONS["UP"]
                    elif event.key == pygame.K_DOWN and current_direction  != DIRECTIONS["UP"]:
                        pending_direction  = DIRECTIONS["DOWN"]
                    elif event.key == pygame.K_LEFT and current_direction  != DIRECTIONS["RIGHT"]:
                        pending_direction  = DIRECTIONS["LEFT"]
                    elif event.key == pygame.K_RIGHT and current_direction  != DIRECTIONS["LEFT"]:
                        pending_direction  = DIRECTIONS["RIGHT"]
    return (
        game_running,
        pending_direction,
        restart_request,
        game_started,
        game_paused,
        shoot_request,
    )
