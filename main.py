import pygame


from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOUR, TARGET_SEQUENCE
from snake import (
    move_snake,
    get_next_head_pos,
    check_self_collision,
    reset_snake,
)
from apple import (
    spawn_and_get_apple_position,
    check_apple_eaten,
    handle_apple_eaten,
)
from draw import (
    draw_map,
    draw_snake,
    draw_apple,
    draw_ui,
)
from events import handle_events


# reset game: snake_body, direction, apple_pos, apple_letter, collected_letters, lives, game_over
def reset_game(
    directions: dict[str, tuple[int, int]],
) -> tuple[
    list[tuple[int, int]], tuple[int, int], tuple[int, int], str, str, int, bool
]:
    snake_body, direction = reset_snake(directions)
    apple_pos = spawn_and_get_apple_position(snake_body)
    apple_letter = TARGET_SEQUENCE[0]
    collected_letters = ""
    lives = 3
    game_over = False

    return (
        snake_body,
        direction,
        apple_pos,
        apple_letter,
        collected_letters,
        lives,
        game_over,
    )


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python's Burden: Escape from COMP9001")
    clock = pygame.time.Clock()

    # ---arguments--- #
    game_running = True
    game_over = False
    restart_request = False
    # font
    font = pygame.font.Font(None, 28)
    # snake information
    snake_body = [(20, 20), (19, 20), (18, 20), (17, 20), (16, 20)]
    # snake direction
    directions = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
    direction = directions["RIGHT"]  # default direction
    # apple
    apple_pos = spawn_and_get_apple_position(snake_body)
    apple_letter = TARGET_SEQUENCE[0]
    # collected letters
    collected_letters = ""
    # life
    lives = 3

    # main loop
    while game_running:

        # event handle (handle events like key press)
        game_running, direction, restart_request = handle_events(
            game_running, direction, directions, game_over
        )
        if restart_request:
            (
                snake_body,
                direction,
                apple_pos,
                apple_letter,
                collected_letters,
                lives,
                game_over,
            ) = reset_game(directions)

        if not game_over:
            # next_head_pos for checking whether the apple is eaten
            next_head = get_next_head_pos(snake_body, direction)
            apple_eaten = check_apple_eaten(next_head, apple_pos)

            # is collided
            if check_self_collision(next_head, snake_body, apple_eaten):
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    snake_body, direction = reset_snake(directions)
                    apple_pos = spawn_and_get_apple_position(snake_body)
            else:
                #move snake include whether the snake should grow code function
                move_snake(snake_body, next_head, apple_eaten)
                if apple_eaten:
                    apple_pos, apple_letter, collected_letters = handle_apple_eaten(
                        snake_body, apple_letter, collected_letters
                    )

        # draw
        screen.fill(BACKGROUND_COLOUR)
        draw_map(screen)
        draw_snake(screen, snake_body)
        draw_apple(screen, font, apple_pos, apple_letter)
        draw_ui(screen, font, lives, game_over, collected_letters)
        pygame.display.flip()  # draw all

        clock.tick(8)  # FPS
    pygame.quit()


if __name__ == "__main__":
    main()
