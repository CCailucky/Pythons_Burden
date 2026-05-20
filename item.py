import random
import pygame

from settings import (
    GRID_WIDTH,
    GRID_HEIGHT,
    GRID_SIZE,
    MAP_X,
    MAP_Y,
    ITEM_TAIL_CUT_COLOUR,
    BULLET_SUPPLY_COLOUR,
    BULLET_SUPPLY_MIN_AMOUNT,
    BULLET_SUPPLY_MAX_AMOUNT,
    MAX_BULLET_SUPPLY_ITEMS,
    BULLET_SUPPLY_SPAWN_INTERVAL_MS,
    TEXT_COLOUR,
)
from assets_loader import load_grid_image


class TailCutItem:
    def __init__(
        self,
        game_map,
        occupied_positions: list[tuple[int, int]],
        pos: tuple[int, int] | None = None,
    ):
        # tailcutitem can be assigned a specific position or a random position
        if pos is None:
            self.pos = self.spawn_and_get_position(game_map, occupied_positions)
        else:
            self.pos = pos
        self.cut_count = random.randint(1, 3)
        self.image = load_grid_image("assets/images/items/tailcut.png")

    def spawn_and_get_position(
        self,
        game_map,
        occupied_positions: list[tuple[int, int]],
    ) -> tuple[int, int]:
        while True:
            pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )

            if game_map.is_available_for_spawn(pos, occupied_positions):
                return pos

    def draw(self, screen, font) -> None:
        x, y = self.pos

        draw_pos = (
            MAP_X + x * GRID_SIZE,
            MAP_Y + y * GRID_SIZE,
        )

        rect = pygame.Rect(
            draw_pos[0],
            draw_pos[1],
            GRID_SIZE,
            GRID_SIZE,
        )

        if self.image is not None:
            screen.blit(self.image, draw_pos)
            return

        # fallback: old rectangle style
        pygame.draw.rect(screen, ITEM_TAIL_CUT_COLOUR, rect)

        text = font.render("T", True, TEXT_COLOUR)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    def check_item_eaten(self, next_head: tuple[int, int]) -> bool:
        return next_head == self.pos


class BulletSupplyItem:
    def __init__(
        self,
        game_map,
        occupied_positions: list[tuple[int, int]],
    ):
        self.pos = self.spawn_and_get_position(game_map, occupied_positions)
        self.amount = random.randint(
            BULLET_SUPPLY_MIN_AMOUNT,
            BULLET_SUPPLY_MAX_AMOUNT,
        )
        self.image = load_grid_image("assets/images/items/bulletsupply.png")

    def spawn_and_get_position(
        self,
        game_map,
        occupied_positions: list[tuple[int, int]],
    ) -> tuple[int, int]:
        while True:
            pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )

            if game_map.is_available_for_spawn(pos, occupied_positions):
                return pos

    def draw(self, screen, font) -> None:
        x, y = self.pos

        draw_pos = (
            MAP_X + x * GRID_SIZE,
            MAP_Y + y * GRID_SIZE,
        )

        rect = pygame.Rect(
            draw_pos[0],
            draw_pos[1],
            GRID_SIZE,
            GRID_SIZE,
        )

        if self.image is not None:
            screen.blit(self.image, draw_pos)
            return
        # fallback: old rectangle style
        pygame.draw.rect(screen, BULLET_SUPPLY_COLOUR, rect)
        text = font.render("B", True, TEXT_COLOUR)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    def check_item_eaten(self, next_head: tuple[int, int]) -> bool:
        return next_head == self.pos


class ItemManager:
    def __init__(
        self,
        game_map,
        occupied_positions: list[tuple[int, int]],
    ):
        self.tail_cut_items = []
        self.bullet_supply_items = []
        self.last_bullet_supply_spawn_time = pygame.time.get_ticks()
        self.occupied_positions = occupied_positions
        self.spawn_tail_cut(game_map)
        self.spawn_bullet_supply(game_map)

    def spawn_tail_cut(self, game_map) -> None:
        tail_cut_item = TailCutItem(game_map, self.occupied_positions)

        self.tail_cut_items.append(tail_cut_item)
        self.occupied_positions.append(tail_cut_item.pos)

    def spawn_bullet_supply(self, game_map) -> None:
        if len(self.bullet_supply_items) >= MAX_BULLET_SUPPLY_ITEMS:
            return
        bullet_supply_item = BulletSupplyItem(
            game_map,
            self.occupied_positions,
        )

        self.bullet_supply_items.append(bullet_supply_item)
        self.occupied_positions.append(bullet_supply_item.pos)

    def spawn_tail_cut_at_position(
        self,
        game_map,
        pos: tuple[int, int],
    ) -> None:
        tail_cut_item = TailCutItem(
            game_map,
            self.occupied_positions,
            pos,
        )

        self.tail_cut_items.append(tail_cut_item)
        self.occupied_positions.append(tail_cut_item.pos)

    def get_eaten_tail_cut(
        self,
        next_head: tuple[int, int],
    ) -> TailCutItem | None:
        for tail_cut_item in self.tail_cut_items:
            if tail_cut_item.check_item_eaten(next_head):
                return tail_cut_item

        return None

    def get_eaten_bullet_supply(
        self,
        next_head: tuple[int, int],
    ) -> BulletSupplyItem | None:
        for bullet_supply_item in self.bullet_supply_items:
            if bullet_supply_item.check_item_eaten(next_head):
                return bullet_supply_item

        return None

    def handle_tail_cut_eaten(
        self,
        eaten_tail_cut_item: TailCutItem,
        player_snake,
        collected_letters: list[str],
    ) -> list[str]:
        if eaten_tail_cut_item in self.tail_cut_items:
            self.tail_cut_items.remove(eaten_tail_cut_item)

        if eaten_tail_cut_item.pos in self.occupied_positions:
            self.occupied_positions.remove(eaten_tail_cut_item.pos)

        cut_count = eaten_tail_cut_item.cut_count
        for i in range(cut_count):
            if len(collected_letters) > 0:
                collected_letters.pop()

        player_snake.cut_tail(cut_count)

        return collected_letters

    def handle_tail_cut_eaten_by_enemy(
        self, eaten_tail_cut_item, enemy_snake, game_map
    ) -> None:
        if eaten_tail_cut_item in self.tail_cut_items:
            self.tail_cut_items.remove(eaten_tail_cut_item)

        if eaten_tail_cut_item.pos in self.occupied_positions:
            self.occupied_positions.remove(eaten_tail_cut_item.pos)

        enemy_snake.cut_tail(eaten_tail_cut_item.cut_count)
        # self.spawn_tail_cut(game_map)

    def handle_bullet_supply_eaten_by_enemy(
        self,
        eaten_bullet_supply_item: BulletSupplyItem,
    ) -> None:
        if eaten_bullet_supply_item in self.bullet_supply_items:
            self.bullet_supply_items.remove(eaten_bullet_supply_item)

        if eaten_bullet_supply_item.pos in self.occupied_positions:
            self.occupied_positions.remove(eaten_bullet_supply_item.pos)

    def handle_bullet_supply_eaten(
        self, eaten_bullet_supply_item, bullet_manager
    ) -> int:
        if eaten_bullet_supply_item in self.bullet_supply_items:
            self.bullet_supply_items.remove(eaten_bullet_supply_item)

        if eaten_bullet_supply_item.pos in self.occupied_positions:
            self.occupied_positions.remove(eaten_bullet_supply_item.pos)

        bullet_manager.add_bullets(eaten_bullet_supply_item.amount)

        return eaten_bullet_supply_item.amount

    def handle_tail_cut_hit_by_bullet(self, pos: tuple[int, int]) -> bool:
        for tail_cut_item in self.tail_cut_items:
            if tail_cut_item.pos == pos:
                self.tail_cut_items.remove(tail_cut_item)
                if tail_cut_item.pos in self.occupied_positions:
                    self.occupied_positions.remove(tail_cut_item.pos)
                return True
        return False

    def handle_bullet_supply_hit_by_bullet(self, pos: tuple[int, int]) -> bool:
        for bullet_supply_item in self.bullet_supply_items:
            if bullet_supply_item.pos == pos:
                self.bullet_supply_items.remove(bullet_supply_item)
                if bullet_supply_item.pos in self.occupied_positions:
                    self.occupied_positions.remove(bullet_supply_item.pos)
                return True
        return False

    def update(self, game_map) -> None:
        current_time = pygame.time.get_ticks()
        if (
            current_time - self.last_bullet_supply_spawn_time
            < BULLET_SUPPLY_SPAWN_INTERVAL_MS
        ):
            return
        if len(self.bullet_supply_items) >= MAX_BULLET_SUPPLY_ITEMS:
            return
        self.spawn_bullet_supply(game_map)
        self.last_bullet_supply_spawn_time = current_time

    def add_pause_duration(self, paused_duration_ms: int) -> None:
        self.last_bullet_supply_spawn_time += paused_duration_ms

    def draw(self, screen, font) -> None:
        for tail_cut_item in self.tail_cut_items:
            tail_cut_item.draw(screen, font)

        for bullet_supply_item in self.bullet_supply_items:
            bullet_supply_item.draw(screen, font)
