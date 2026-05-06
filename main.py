import pygame


from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BACKGROUND_COLOUR,
    TARGET_SEQUENCE,
    MAX_APPLES,
)
from snake import Snake
from apple import (
    Apple,
    spawn_and_get_apples,
    get_eaten_apple,
    handle_apple_eaten,
    check_target_completed,
)
from ui import UI
from game_map import GameMap
from events import handle_events


# reset game
def reset_game(game_map) -> tuple[Snake, list[Apple], list[str], bool, bool]:
    player_snake = Snake()
    collected_letters: list[str] = []

    apples = spawn_and_get_apples(
        player_snake.body,
        game_map,
        collected_letters,
        MAX_APPLES,
    )
    game_over = False
    game_win = False

    return player_snake, apples, collected_letters, game_over, game_win


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
    # game map
    game_map = GameMap()
    # font
    font = pygame.font.Font(None, 28)
    ui = UI(font)
    # snake
    player_snake = Snake()
    # collected letters
    collected_letters = []
    # apple
    apples = spawn_and_get_apples(
        player_snake.body,
        game_map,
        collected_letters,
        MAX_APPLES,
    )
    is_apple_eaten = False

    # main loop
    while game_running:

        # event handle (handle events like key press)
        game_running, player_snake.direction, restart_request = handle_events(
            game_running,
            player_snake.direction,
            game_over or game_win,
        )
        if restart_request:
            (
                player_snake,
                apples,
                collected_letters,
                game_over,
                game_win,
            ) = reset_game(game_map)
        if not game_over and not game_win:
            # next_head_pos for checking whether the apple is eaten
            next_head = player_snake.get_next_head_pos()
            eaten_apple = get_eaten_apple(next_head, apples)
            if eaten_apple == None:
                is_apple_eaten = False
            else:
                is_apple_eaten = True
            # collide with the wall
            if not game_map.is_walkable(next_head):
                player_snake.lose_life()
                if player_snake.is_dead():
                    game_over = True
                else:
                    player_snake.revive()
                    # respawn a new batch of apples
                    apples = spawn_and_get_apples(
                        player_snake.body,
                        game_map,
                        collected_letters,
                        MAX_APPLES,
                    )
            # self collision
            elif player_snake.check_self_collision(next_head, is_apple_eaten):
                player_snake.lose_life()
                if player_snake.is_dead():
                    game_over = True
                else:
                    player_snake.revive()
                    # respawn a new batch of apples
                    apples = spawn_and_get_apples(
                        player_snake.body,
                        game_map,
                        collected_letters,
                        MAX_APPLES,
                    )
            # normal move
            else:
                # include move and whether the snake should grow code function
                player_snake.move(next_head, is_apple_eaten)
                if is_apple_eaten:
                    collected_letters = handle_apple_eaten(
                        eaten_apple,
                        collected_letters,
                    )
                    # respawn a new batch of apples
                    apples = spawn_and_get_apples(
                        player_snake.body,
                        game_map,
                        collected_letters,
                        MAX_APPLES,
                    )

                    if check_target_completed(collected_letters):
                        game_win = True

        # draw
        screen.fill(BACKGROUND_COLOUR)
        game_map.draw(screen)
        player_snake.draw(screen)
        for apple in apples:
            apple.draw(screen, font)
        ui.draw(
            screen,
            player_snake.lives,
            game_over,
            game_win,
            collected_letters,
        )
        pygame.display.flip()  # draw all

        clock.tick(8)  # FPS
    pygame.quit()


if __name__ == "__main__":
    main()
