import pygame
from settings import (
    DIRECTIONS,
    SCREEN_START_INTERFACE,
    SCREEN_RULES_INTERFACE,
    SCREEN_GAME,
)


def handle_input_events(
    game_running: bool,
    current_direction: tuple[int, int],
    pending_direction: tuple[int, int],
    game_over: bool,
    game_started: bool,
    game_paused: bool,
    ui,
    display,
    current_screen: str,
) -> tuple[bool, tuple[int, int], bool, bool, bool, bool, str | None]:
    restart_request = False
    shoot_request = False
    menu_action = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        # KEYBOARD EVENTS
        if event.type == pygame.KEYDOWN:

            # Start interface: no keyboard control
            if current_screen == SCREEN_START_INTERFACE:
                continue
            # Rules interface: no keyboard control
            if current_screen == SCREEN_RULES_INTERFACE:
                continue
            # Game interface: keyboard control
            if current_screen == SCREEN_GAME:
                # game over / win -> R restart
                if game_over and event.key == pygame.K_r:
                    menu_action = "reset"
                # ESC pause / resume
                elif game_started and not game_over and event.key == pygame.K_ESCAPE:
                    if game_paused:
                        menu_action = "resume"
                    else:
                        menu_action = "pause"
                # Pause Menu for reset and quit
                elif game_started and game_paused:
                    if event.key == pygame.K_r:
                        menu_action = "reset"
                    elif event.key == pygame.K_q:
                        menu_action = "quit"
                # F to shoot bullet
                elif (
                    game_started
                    and not game_over
                    and not game_paused
                    and event.key == pygame.K_f
                ):
                    shoot_request = True

                # movement
                if game_started and not game_over and not game_paused:
                    # Change pending direction by arrow keys.
                    # Only allow one queued turn before the next snake move.
                    if pending_direction == current_direction:
                        if (
                            event.key == pygame.K_UP
                            and current_direction != DIRECTIONS["DOWN"]
                        ):
                            pending_direction = DIRECTIONS["UP"]
                        elif (
                            event.key == pygame.K_DOWN
                            and current_direction != DIRECTIONS["UP"]
                        ):
                            pending_direction = DIRECTIONS["DOWN"]
                        elif (
                            event.key == pygame.K_LEFT
                            and current_direction != DIRECTIONS["RIGHT"]
                        ):
                            pending_direction = DIRECTIONS["LEFT"]
                        elif (
                            event.key == pygame.K_RIGHT
                            and current_direction != DIRECTIONS["LEFT"]
                        ):
                            pending_direction = DIRECTIONS["RIGHT"]
        # MOUSE EVENTS
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = display.convert_mouse_pos_to_game_surface(event.pos)
            screen_width, screen_height = display.game_surface.get_size()
            # START INTERFACE (MOUSE EVENTS)
            if current_screen == SCREEN_START_INTERFACE:
                start_rect, rules_rect, quit_rect = ui.get_start_interface_button_rects(
                    screen_width, screen_height
                )
                if start_rect.collidepoint(mouse_pos):
                    menu_action = "start"
                elif rules_rect.collidepoint(mouse_pos):
                    menu_action = "rules"
                elif quit_rect.collidepoint(mouse_pos):
                    menu_action = "quit"
            # RULES INTERFACE (MOUSE EVENTS)
            elif current_screen == SCREEN_RULES_INTERFACE:
                back_rect, prev_rect, next_rect = ui.get_rules_interface_button_rects(
                    screen_width, screen_height
                )
                if back_rect.collidepoint(mouse_pos):
                    menu_action = "back"
                elif prev_rect.collidepoint(mouse_pos):
                    menu_action = "prev_rules"
                elif next_rect.collidepoint(mouse_pos):
                    menu_action = "next_rules"
            # PAUSE INTERFACE (MOUSE EVENTS)
            elif (
                current_screen == SCREEN_GAME
                and game_started
                and game_paused
                and not game_over
            ):
                # convert to game surface coordinate
                resume_rect, reset_rect, quit_rect = ui.get_pause_menu_button_rects(
                    screen_width, screen_height
                )

                if resume_rect.collidepoint(mouse_pos):
                    menu_action = "resume"

                elif reset_rect.collidepoint(mouse_pos):
                    menu_action = "reset"

                elif quit_rect.collidepoint(mouse_pos):
                    menu_action = "quit"
    return (
        game_running,
        pending_direction,
        restart_request,
        game_started,
        game_paused,
        shoot_request,
        menu_action,
    )
