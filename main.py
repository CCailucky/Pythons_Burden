import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BACKGROUND_COLOUR,
    MAX_APPLES,
)
from snake import Snake
from apple import (
    AppleManager,
    check_target_completed,
)
from ui import UI
from game_map import GameMap
from events import handle_events
from item import ItemManager


# reset game
def reset_game(game_map, ui):
    occupied_positions = []
    player_snake = Snake(occupied_positions)
    collected_letters = []
    apple_manager = AppleManager(
        game_map,
        collected_letters,
        occupied_positions,
        MAX_APPLES,
    )

    item_manager = ItemManager(
        game_map,
        occupied_positions,
    )

    game_over = False
    game_win = False
    ui.reset_status_messages()
    return (
        player_snake,
        apple_manager,
        item_manager,
        collected_letters,
        occupied_positions,
        game_over,
        game_win,
    )


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
    # initialization
    (
        player_snake,
        apple_manager,
        item_manager,
        collected_letters,
        occupied_positions,
        game_over,
        game_win,
    ) = reset_game(game_map, ui)

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
                apple_manager,
                item_manager,
                collected_letters,
                occupied_positions,
                game_over,
                game_win,
            ) = reset_game(game_map, ui)

        if not game_over and not game_win:
            # update apples’ status manager
            apple_manager.update(
                game_map,
                collected_letters,
            )
            # next_head_pos for checking whether the apple is eaten
            next_head = player_snake.get_next_head_pos()
            eaten_tail_cut_item = item_manager.get_eaten_tail_cut(next_head)
            eaten_apple = apple_manager.get_eaten_apple(next_head)
            if eaten_apple == None:
                is_apple_eaten = False
            else:
                is_apple_eaten = True
            if eaten_tail_cut_item == None:
                is_tail_cut_eaten = False
            else:
                is_tail_cut_eaten = True

            # collide with the wall
            if not game_map.is_walkable(next_head):
                player_snake.lose_life()
                ui.add_status_message("Hit the wall! Life -1")
                if player_snake.is_dead():
                    game_over = True
                    ui.add_status_message("Game Over")
                    ui.add_status_message("Press R to restart")
                else:
                    player_snake.revive()
                    # spawn a new batch of apples
                    apple_manager.spawn_apples(
                        game_map,
                        collected_letters,
                    )

            # self collision
            elif player_snake.check_self_collision(next_head, is_apple_eaten):
                player_snake.lose_life()
                ui.add_status_message("self collision! Life -1")
                if player_snake.is_dead():
                    game_over = True
                    ui.add_status_message("Game Over")
                    ui.add_status_message("Press R to restart")
                else:
                    player_snake.revive()
                    # respawn a new batch of apples
                    apple_manager.spawn_apples(
                        game_map,
                        collected_letters,
                    )

            # snake move normally
            else:
                # include move and whether the snake should grow code function
                player_snake.move(next_head, is_apple_eaten)
                # include respawn apple
                if is_apple_eaten:
                    collected_letters = apple_manager.handle_apple_eaten(
                        eaten_apple,
                        game_map,
                        collected_letters,
                    )
                    ui.add_status_message(f'Eat letter "{eaten_apple.letter}"')

                if is_tail_cut_eaten:
                    cut_count = eaten_tail_cut_item.cut_count
                    old_length = len(collected_letters)
                    collected_letters = item_manager.handle_tail_cut_eaten(
                        eaten_tail_cut_item,
                        player_snake,
                        collected_letters,
                    )
                    item_manager.spawn_tail_cut(game_map)
                    removed_count = old_length - len(collected_letters)

                    if removed_count > 0:
                        ui.add_status_message(f"TailCut removed {removed_count} tail(s)")
                    else:
                        ui.add_status_message("Nothing to cut")
                        
                if check_target_completed(collected_letters):
                    game_win = True
                    ui.add_status_message("Sequence Complete! You Win!")
                    ui.add_status_message("Press R to restart")

        # draw
        screen.fill(BACKGROUND_COLOUR)
        game_map.draw(screen)
        player_snake.draw(screen, font, collected_letters)
        apple_manager.draw(screen, font)
        item_manager.draw(screen, font)
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
