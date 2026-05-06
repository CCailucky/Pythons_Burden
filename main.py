import pygame


from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOUR, TARGET_SEQUENCE
from snake import Snake
from apple import (
    Apple,
    handle_apple_eaten,
    check_target_completed,
)
from draw import (
    draw_map,
    draw_ui,
)
from events import handle_events


# reset game: snake_body, direction, apple_pos, apple_letter, collected_letters, lives, game_over
def reset_game(
    directions: dict[str, tuple[int, int]],
) -> tuple[Snake, Apple, list[str], bool, bool]:
    player_snake = Snake(directions)
    apple = Apple(player_snake.body, TARGET_SEQUENCE[0])
    collected_letters: list[str] = []
    game_over = False
    game_win = False

    return player_snake, apple, collected_letters, game_over, game_win


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python's Burden: Escape from COMP9001")
    clock = pygame.time.Clock()

    # ---arguments--- #
    game_running = True
    game_over = False
    game_win = False
    restart_request = False
    # font
    font = pygame.font.Font(None, 28)
    # snake information
    directions = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
    player_snake = Snake(directions)
    # apple
    apple = Apple(player_snake.body, TARGET_SEQUENCE[0])
    # collected letters
    collected_letters = []

    # main loop
    while game_running:

        # event handle (handle events like key press)
        game_running, player_snake.direction, restart_request = handle_events(
            game_running,
            player_snake.direction,
            directions,
            game_over or game_win,
        )
        if restart_request:
            (
                player_snake,
                apple,
                collected_letters,
                game_over,
                game_win,
            ) = reset_game(directions)

        if not game_over and not game_win:
            # next_head_pos for checking whether the apple is eaten
            next_head = player_snake.get_next_head_pos()
            apple_eaten = apple.check_apple_eaten(next_head)

            if player_snake.check_self_collision(next_head, apple_eaten):
                player_snake.lose_life()

                if player_snake.lives <= 0:
                    game_over = True
                else:
                    player_snake.revive()
                    apple = Apple(player_snake.body, apple.letter)
            else:
                # include move and whether the snake should grow code function
                player_snake.move(next_head, apple_eaten)
                if apple_eaten:
                    apple, collected_letters = handle_apple_eaten(
                        player_snake.body,
                        apple,
                        collected_letters,
                    )
                    if check_target_completed(collected_letters):
                        game_win = True

        # draw
        screen.fill(BACKGROUND_COLOUR)
        draw_map(screen)
        player_snake.draw(screen)
        apple.draw(screen, font)
        draw_ui(
            screen, font, player_snake.lives, game_over, game_win, collected_letters
        )
        pygame.display.flip()  # draw all

        clock.tick(8)  # FPS
    pygame.quit()


if __name__ == "__main__":
    main()
