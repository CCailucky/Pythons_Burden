import pygame

from settings import (
    BACKGROUND_COLOUR,
    MAX_APPLES,
    SNAKE_MOVE_INTERVAL_MS,
    SCREEN_START_INTERFACE,
    SCREEN_RULES_INTERFACE,
    SCREEN_GAME,
)
from snake import Snake
from apple import (
    AppleManager,
    check_target_completed,
)
from item import ItemManager
from enemy import EnemyManager
from bullet import BulletManager
from input_events import handle_input_events


# game_controller is used for:
# 1.reset the game
# 2.control all the instances
# 3.time offset control
# 4.draw
class GameController:
    def __init__(self, game_map, ui, grid_font):
        self.game_map = game_map
        self.ui = ui
        self.grid_font = grid_font
        self.reset()
        self.game_started = False
        self.current_screen = SCREEN_START_INTERFACE
        self.rules_page_index = 0

    ################################# RESET #################################
    # reset the game
    def reset(self) -> None:
        self.game_map.clear_portal()
        self.collected_letters = []
        self.occupied_positions = []
        self.player_snake = Snake(self.occupied_positions)
        self.pending_direction = self.player_snake.direction
        self.last_game_tick_time = pygame.time.get_ticks()

        # instances
        self.apple_manager = AppleManager(
            self.game_map, self.collected_letters, self.occupied_positions, MAX_APPLES
        )
        self.item_manager = ItemManager(self.game_map, self.occupied_positions)
        self.enemy_manager = EnemyManager(self.occupied_positions)
        self.bullet_manager = BulletManager()
        # game status
        self.game_over = False
        self.game_win = False
        self.game_started = False
        self.game_paused = False
        self.shoot_request = False
        self.pause_start_time = None
        # game ui msgs
        self.ui.reset_status_messages()

    ################################# HANDLE #################################

    # send msgs and handle player's life status
    def handle_player_damage(self, message: str) -> None:
        self.player_snake.lose_life()
        self.ui.add_status_message(message)

        if self.player_snake.is_dead():
            self.game_over = True
            self.ui.add_status_message("Game Over")
            self.ui.add_status_message("Press R to restart")
            return

        self.player_snake.revive()
        self.pending_direction = self.player_snake.direction
        self.player_snake.start_invincible()
        self.apple_manager.spawn_apples(
            self.game_map,
            self.collected_letters,
        )

    def handle_bullet_hit_player(self) -> None:
        is_damage_taken = self.player_snake.handle_bullet_hit()

        if not is_damage_taken:
            self.ui.add_status_message("Bullet blocked by invincibility")
            return

        self.ui.add_status_message("Hit by your own bullet! Life -1")

        if self.player_snake.is_dead():
            self.game_over = True
            self.ui.add_status_message("Game Over")
            self.ui.add_status_message("Press R to restart")
            return

        self.player_snake.revive()
        self.pending_direction = self.player_snake.direction
        self.player_snake.start_invincible()
        self.apple_manager.spawn_apples(
            self.game_map,
            self.collected_letters,
        )

    # what will the player snake eat in the next move
    def get_eaten_objects(self, next_head: tuple[int, int]):
        eaten_tail_cut_item = self.item_manager.get_eaten_tail_cut(next_head)
        eaten_bullet_supply_item = self.item_manager.get_eaten_bullet_supply(next_head)
        eaten_apple = self.apple_manager.get_eaten_apple(next_head)

        return eaten_tail_cut_item, eaten_bullet_supply_item, eaten_apple

    def handle_player_collision(
        self, next_head: tuple[int, int], is_apple_eaten: bool
    ) -> bool:
        # handle collide with wall
        if not self.game_map.is_walkable(next_head):
            self.handle_player_damage("Hit the wall! Life -1")
            return True
        # handle collide with itself
        if self.player_snake.check_self_collision(next_head, is_apple_eaten):
            self.handle_player_damage("self collision! Life -1")
            return True
        # handle collide with enemy snake
        if (
            not self.player_snake.is_invincible
            and self.enemy_manager.check_player_collision(next_head)
        ):
            self.handle_player_damage("Hit enemy snake! Life -1")
            return True

        return False

    def handle_player_pickups(
        self,
        eaten_apple,
        eaten_bullet_supply_item,
        eaten_tail_cut_item,
    ) -> None:
        if eaten_apple is not None:
            self.collected_letters = self.apple_manager.handle_apple_eaten(
                eaten_apple,
                self.game_map,
                self.collected_letters,
            )
            self.ui.add_status_message(f'Eat letter "{eaten_apple.letter}"')

        if eaten_bullet_supply_item is not None:
            bullet_amount = self.item_manager.handle_bullet_supply_eaten(
                eaten_bullet_supply_item,
                self.bullet_manager,
            )
            self.ui.add_status_message(f"Bullet supply +{bullet_amount}")

        if eaten_tail_cut_item is not None:
            old_length = len(self.collected_letters)

            self.collected_letters = self.item_manager.handle_tail_cut_eaten(
                eaten_tail_cut_item,
                self.player_snake,
                self.collected_letters,
            )

            removed_count = old_length - len(self.collected_letters)

            if removed_count > 0:
                self.ui.add_status_message(f"TailCut removed {removed_count} tail(s)")
            else:
                self.ui.add_status_message("Nothing to cut")

    def handle_events(self, game_running: bool, display) -> bool:
        (
            game_running,
            self.pending_direction,
            restart_request,
            self.game_started,
            self.game_paused,
            self.shoot_request,
            menu_action,
        ) = handle_input_events(
            game_running,
            self.player_snake.direction,
            self.pending_direction,
            self.game_over or self.game_win,
            self.game_started,
            self.game_paused,
            self.ui,
            display,
            self.current_screen,
        )
        # handle button event
        game_running = self.handle_menu_action(menu_action, game_running)

        self.handle_pause_time_offset()

        if restart_request:
            self.reset()

        return game_running

    def handle_menu_action(self, menu_action: str | None, game_running: bool) -> bool:
        if menu_action is None:
            return game_running
        if menu_action == "start":
            self.reset()
            self.current_screen = SCREEN_GAME
            self.game_started = True
            self.ui.add_status_message("Game started!")
        elif menu_action == "pause":
            self.game_paused = True
            self.ui.add_status_message("Game paused")
        elif menu_action == "resume":
            self.game_paused = False
            self.ui.add_status_message("Game resumed")
        elif menu_action == "reset":
            self.reset()
            self.current_screen = SCREEN_GAME
            self.game_started = True
            self.ui.add_status_message("Game restarted!")
        elif menu_action == "quit":
            game_running = False
        # RULES PART
        elif menu_action == "rules":
            self.current_screen = SCREEN_RULES_INTERFACE
            self.rules_page_index = 0
        elif menu_action == "back":
            self.current_screen = SCREEN_START_INTERFACE
            self.rules_page_index = 0
        elif menu_action == "next_rules":
            if self.rules_page_index < self.ui.get_rules_page_count() - 1:
                self.rules_page_index += 1
        elif menu_action == "prev_rules":
            if self.rules_page_index > 0:
                self.rules_page_index -= 1
        return game_running

    def handle_pause_time_offset(self) -> None:
        if self.game_paused:
            if self.pause_start_time is None:
                self.pause_start_time = pygame.time.get_ticks()
            return

        if self.pause_start_time is not None:
            paused_duration = pygame.time.get_ticks() - self.pause_start_time

            self.last_game_tick_time += paused_duration
            self.player_snake.add_pause_duration(paused_duration)
            self.apple_manager.add_pause_duration(paused_duration)
            self.item_manager.add_pause_duration(paused_duration)
            self.enemy_manager.add_pause_duration(paused_duration)
            self.bullet_manager.add_pause_duration(paused_duration)

            self.pause_start_time = None

    def handle_portal(self) -> None:
        if check_target_completed(self.collected_letters):
            if not self.game_map.portal_active:
                portal_spawned = self.game_map.spawn_portal_far_from_player(
                    self.player_snake.body[0],
                    self.occupied_positions,
                )

                if portal_spawned:
                    self.ui.add_status_message("Sequence complete! Portal opened!")
        else:
            if self.game_map.portal_active:
                self.game_map.clear_portal()
                self.ui.add_status_message("Portal closed! Sequence is incomplete.")

        if self.game_map.portal_active and self.game_map.is_portal(
            self.player_snake.body[0]
        ):
            self.game_win = True
            self.ui.add_status_message("You entered the portal! You Win!")
            self.ui.add_status_message("Press R to restart")

    ################################# MAIN UPDATE #################################
    # check whether the game is normally running
    def can_update_game(self) -> bool:
        return (
            self.current_screen == SCREEN_GAME
            and self.game_started
            and not self.game_paused
            and not self.game_over
            and not self.game_win
        )

    def can_draw_pause_overlay(self) -> bool:
        return (
            self.current_screen == SCREEN_GAME
            and self.game_started
            and self.game_paused
            and not self.game_over
            and not self.game_win
        )

    # for main.py to update the game logic
    def update(self) -> None:
        if not self.can_update_game():
            return
        current_time = pygame.time.get_ticks()
        self.update_realtime_systems()
        # if the game is over, the snake_tick shouldnt execute in the next frame
        if not self.can_update_game():
            return
        self.update_snake_tick(current_time)

    # update non-snake part
    def update_realtime_systems(self) -> None:
        self.item_manager.update(self.game_map)

        if self.shoot_request:
            self.bullet_manager.shoot(
                self.player_snake,
                self.pending_direction,
                self.game_map,
            )

        is_player_hit_by_bullet = self.bullet_manager.update(
            self.game_map,
            self.apple_manager,
            self.item_manager,
            self.enemy_manager,
            self.player_snake,
            self.collected_letters,
        )

        if is_player_hit_by_bullet:
            self.handle_bullet_hit_player()

        self.shoot_request = False

    # update enemyAI part
    def update_enemy_systems(self) -> None:
        self.enemy_manager.update(
            self.game_map,
            self.apple_manager,
            self.item_manager,
            self.collected_letters,
        )

        self.enemy_manager.handle_enemy_drops(
            self.game_map,
            self.apple_manager,
            self.item_manager,
            self.collected_letters,
            self.ui,
        )

        self.player_snake.update_invincible(self.enemy_manager)

    # update player-snake part(related to player snake)
    def update_snake_tick(self, current_time: int) -> None:
        # check the tick time
        if current_time - self.last_game_tick_time < SNAKE_MOVE_INTERVAL_MS:
            return
        # assign the pending direction to snake's true direction
        self.last_game_tick_time = current_time
        self.player_snake.direction = self.pending_direction
        # update apples
        self.apple_manager.update(self.game_map, self.collected_letters)
        # calculate the pos of player snake's next head
        next_head = self.player_snake.get_next_head_pos()
        # check what was eaten in the next head
        eaten_tail_cut_item, eaten_bullet_supply_item, eaten_apple = (
            self.get_eaten_objects(next_head)
        )
        # is_apple_eaten is used in player self-collision
        is_apple_eaten = eaten_apple is not None
        # update enemies
        self.update_enemy_systems()
        # check the player collision
        has_collision = self.handle_player_collision(next_head, is_apple_eaten)
        # if the player snake collides, the rest of the code wont execute.
        if has_collision:
            return
        # player snake normally move
        self.player_snake.move(next_head, is_apple_eaten)
        # handle what the player snake eats
        self.handle_player_pickups(
            eaten_apple, eaten_bullet_supply_item, eaten_tail_cut_item
        )
        # check whether the exit portal needs to be activated
        self.handle_portal()

    ################################# DRAW #################################
    def draw(self, surface) -> None:
        # start interface
        if self.current_screen == SCREEN_START_INTERFACE:
            self.ui.draw_start_interface(surface)
            return
        # rule interface
        if self.current_screen == SCREEN_RULES_INTERFACE:
            self.ui.draw_rules_interface(surface, self.rules_page_index)
            return
        surface.fill(BACKGROUND_COLOUR)

        self.game_map.draw(surface)
        self.player_snake.draw(
            surface,
            self.grid_font,
            self.collected_letters,
        )
        self.apple_manager.draw(surface, self.grid_font)
        self.item_manager.draw(surface, self.grid_font)
        self.enemy_manager.draw(surface)
        self.bullet_manager.draw(surface)

        self.ui.draw(
            surface,
            self.player_snake.lives,
            self.game_over,
            self.game_win,
            self.collected_letters,
            self.bullet_manager.bullet_count,
        )
        if self.can_draw_pause_overlay():
            self.ui.draw_pause_overlay(surface)
