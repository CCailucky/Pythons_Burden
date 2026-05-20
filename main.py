import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BACKGROUND_COLOUR,
    MAX_APPLES,
    FPS,
    SNAKE_MOVE_INTERVAL_MS,
    WINDOW_WIDTH_RATIO,
    WINDOW_HEIGHT_RATIO,
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
from enemy import EnemyManager
from bullet import BulletManager


# reset game
def reset_game(game_map, ui):

    game_map.clear_portal()
    occupied_positions = []
    player_snake = Snake(occupied_positions)
    # pending direction
    pending_direction = player_snake.direction
    # last tick time
    last_game_tick_time = pygame.time.get_ticks()
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
    enemy_manager = EnemyManager(occupied_positions)
    bullet_manager = BulletManager()
    game_over = False
    game_win = False
    game_started = False
    game_paused = False
    ui.reset_status_messages()
    return (
        player_snake,
        pending_direction,
        last_game_tick_time,
        apple_manager,
        item_manager,
        enemy_manager,
        bullet_manager,
        collected_letters,
        occupied_positions,
        game_over,
        game_win,
        game_started,
        game_paused,
    )


# adaptive to the window screen size
def get_adaptive_window_size() -> tuple[int, int]:
    display_info = pygame.display.Info()

    max_width = int(display_info.current_w * WINDOW_WIDTH_RATIO)
    max_height = int(display_info.current_h * WINDOW_HEIGHT_RATIO)

    scale = min(max_width / SCREEN_WIDTH, max_height / SCREEN_HEIGHT, 1)

    window_width = int(SCREEN_WIDTH * scale)
    window_height = int(SCREEN_HEIGHT * scale)

    return window_width, window_height


def main():
    pygame.init()
    window_size = get_adaptive_window_size()
    screen = pygame.display.set_mode(window_size)
    game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python's Burden: Escape from COMP9001")
    clock = pygame.time.Clock()

    # ---arguments--- #
    game_running = True
    restart_request = False
    pause_start_time = None
    # game map
    game_map = GameMap()
    # font
    grid_font = pygame.font.Font(None, 26)
    ui = UI()
    # initialization
    (
        player_snake,
        pending_direction,
        last_game_tick_time,
        apple_manager,
        item_manager,
        enemy_manager,
        bullet_manager,
        collected_letters,
        occupied_positions,
        game_over,
        game_win,
        game_started,
        game_paused,
    ) = reset_game(game_map, ui)

    # main loop
    while game_running:

        # event handle (handle events like key press)
        (
            game_running,
            pending_direction,
            restart_request,
            game_started,
            game_paused,
            shoot_request,
        ) = handle_events(
            game_running,
            player_snake.direction,
            pending_direction,
            game_over or game_win,
            game_started,
            game_paused,
            ui,
        )
        # for time offset when pausing the game(fix the correct start time after pausing)
        if game_paused:
            if pause_start_time is None:
                pause_start_time = pygame.time.get_ticks()
        else:
            if pause_start_time is not None:
                paused_duration = pygame.time.get_ticks() - pause_start_time

                last_game_tick_time += paused_duration
                player_snake.add_pause_duration(paused_duration)
                apple_manager.add_pause_duration(paused_duration)
                item_manager.add_pause_duration(paused_duration)
                enemy_manager.add_pause_duration(paused_duration)
                bullet_manager.add_pause_duration(paused_duration)
                pause_start_time = None

        if restart_request:
            (
                player_snake,
                pending_direction,
                last_game_tick_time,
                apple_manager,
                item_manager,
                enemy_manager,
                bullet_manager,
                collected_letters,
                occupied_positions,
                game_over,
                game_win,
                game_started,
                game_paused,
            ) = reset_game(game_map, ui)

        if game_started and not game_paused and not game_over and not game_win:
            current_time = pygame.time.get_ticks()
            item_manager.update(game_map)
            # shoot bullet from the next position based on pending_direction
            if shoot_request:
                bullet_manager.shoot(player_snake, pending_direction, game_map)

            # update bullet status every frame
            is_player_hit_by_bullet = bullet_manager.update(
                game_map,
                apple_manager,
                item_manager,
                enemy_manager,
                player_snake,
                collected_letters,
            )
            # handle bullet hits player snake
            if is_player_hit_by_bullet:
                is_damage_taken = player_snake.handle_bullet_hit()

                if not is_damage_taken:
                    ui.add_status_message("Bullet blocked by invincibility")
                else:
                    ui.add_status_message("Hit by your own bullet! Life -1")

                    if player_snake.is_dead():
                        game_over = True
                        ui.add_status_message("Game Over")
                        ui.add_status_message("Press R to restart")
                    else:
                        player_snake.revive()
                        pending_direction = player_snake.direction
                        player_snake.start_invincible()
                        apple_manager.spawn_apples(
                            game_map,
                            collected_letters,
                        )

            if current_time - last_game_tick_time >= SNAKE_MOVE_INTERVAL_MS:
                last_game_tick_time = current_time
                # apply the queued direction once per snake move
                player_snake.direction = pending_direction
                # update apples’ status manager
                apple_manager.update(game_map, collected_letters)
                # next_head_pos for checking whether the apple is eaten
                next_head = player_snake.get_next_head_pos()

                eaten_tail_cut_item = item_manager.get_eaten_tail_cut(next_head)
                eaten_bullet_supply_item = item_manager.get_eaten_bullet_supply(
                    next_head
                )
                eaten_apple = apple_manager.get_eaten_apple(next_head)

                is_apple_eaten = eaten_apple != None
                is_tail_cut_eaten = eaten_tail_cut_item != None
                is_bullet_supply_eaten = eaten_bullet_supply_item != None

                # update enemy snake
                enemy_manager.update(
                    game_map,
                    apple_manager,
                    item_manager,
                    collected_letters,
                )
                enemy_manager.handle_enemy_drops(
                    game_map,
                    apple_manager,
                    item_manager,
                    collected_letters,
                    ui,
                )
                player_snake.update_invincible(enemy_manager)

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
                        pending_direction = player_snake.direction
                        # enter invincible mode for 3 secs
                        player_snake.start_invincible()
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
                        pending_direction = player_snake.direction
                        # enter invincible mode for 3 secs
                        player_snake.start_invincible()
                        # respawn a new batch of apples
                        apple_manager.spawn_apples(
                            game_map,
                            collected_letters,
                        )

                # collide with the enemy snake (when the snake becomes invincible, colliding with the enemy snakes has no effect)
                elif (
                    not player_snake.is_invincible
                    and enemy_manager.check_player_collision(next_head)
                ):
                    player_snake.lose_life()
                    ui.add_status_message("Hit enemy snake! Life -1")

                    if player_snake.is_dead():
                        game_over = True
                        ui.add_status_message("Game Over")
                        ui.add_status_message("Press R to restart")
                    else:
                        player_snake.revive()
                        pending_direction = player_snake.direction
                        player_snake.start_invincible()
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
                            eaten_apple, game_map, collected_letters
                        )
                        ui.add_status_message(f'Eat letter "{eaten_apple.letter}"')

                    if is_bullet_supply_eaten:
                        bullet_amount = item_manager.handle_bullet_supply_eaten(
                            eaten_bullet_supply_item, bullet_manager
                        )
                        ui.add_status_message(f"Bullet supply +{bullet_amount}")

                    if is_tail_cut_eaten:
                        cut_count = eaten_tail_cut_item.cut_count
                        old_length = len(collected_letters)
                        collected_letters = item_manager.handle_tail_cut_eaten(
                            eaten_tail_cut_item, player_snake, collected_letters
                        )

                        removed_count = old_length - len(collected_letters)

                        if removed_count > 0:
                            ui.add_status_message(
                                f"TailCut removed {removed_count} tail(s)"
                            )
                        else:
                            ui.add_status_message("Nothing to cut")

                    # for portal
                    if check_target_completed(collected_letters):
                        if not game_map.portal_active:
                            portal_spawned = game_map.spawn_portal_far_from_player(
                                player_snake.body[0],
                                occupied_positions,
                            )

                            if portal_spawned:
                                ui.add_status_message(
                                    "Sequence complete! Portal opened!"
                                )
                    else:
                        if game_map.portal_active:
                            game_map.clear_portal()
                            ui.add_status_message(
                                "Portal closed! Sequence is incomplete."
                            )

                    if game_map.portal_active and game_map.is_portal(
                        player_snake.body[0]
                    ):
                        game_win = True
                        ui.add_status_message("You entered the portal! You Win!")
                        ui.add_status_message("Press R to restart")
        # draw
        game_surface.fill(BACKGROUND_COLOUR)

        game_map.draw(game_surface)
        player_snake.draw(game_surface, grid_font, collected_letters)
        apple_manager.draw(game_surface, grid_font)
        item_manager.draw(game_surface, grid_font)
        enemy_manager.draw(game_surface)
        bullet_manager.draw(game_surface)
        ui.draw(
            game_surface,
            player_snake.lives,
            game_over,
            game_win,
            collected_letters,
            bullet_manager.bullet_count,
        )
        # scale game_surface to window size
        scaled_surface = pygame.transform.scale(game_surface, window_size)
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()  # draw all

        clock.tick(FPS)  # FPS
    pygame.quit()


if __name__ == "__main__":
    main()
