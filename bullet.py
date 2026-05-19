import pygame

from settings import (
    GRID_WIDTH,
    GRID_HEIGHT,
    GRID_SIZE,
    MAP_X,
    MAP_Y,
    BULLET_COLOUR,
    INITIAL_BULLETS,
    BULLET_LIFETIME_MS,
    BULLET_MOVE_INTERVAL_MS,
)


class Bullet:
    def __init__(
        self,
        pos: tuple[int, int],
        direction: tuple[int, int],
    ):
        self.pos = pos
        self.direction = direction
        self.spawn_time = pygame.time.get_ticks()
        # self.last_move_time = self.spawn_time - BULLET_MOVE_INTERVAL_MS
        self.last_move_time = self.spawn_time
        self.alive = True
        # fix bug: avoid immediately hitting player snake when shooting
        self.first_move = False

    def quantum_transit(self, position: tuple[int, int]) -> tuple[int, int]:
        x, y = position

        if x < 0:
            x = GRID_WIDTH - 1
        elif x >= GRID_WIDTH:
            x = 0

        if y < 0:
            y = GRID_HEIGHT - 1
        elif y >= GRID_HEIGHT:
            y = 0

        return (x, y)

    def move(self, game_map) -> None:
        move_x, move_y = self.direction
        next_pos = (
            self.pos[0] + move_x,
            self.pos[1] + move_y,
        )

        next_pos = self.quantum_transit(next_pos)

        # cant go through the wall
        if not game_map.is_walkable(next_pos):
            self.alive = False
            return

        self.pos = next_pos
        self.first_move = True

    def update(self, game_map) -> None:
        current_time = pygame.time.get_ticks()

        if current_time - self.spawn_time >= BULLET_LIFETIME_MS:
            self.alive = False
            return

        if current_time - self.last_move_time >= BULLET_MOVE_INTERVAL_MS:
            self.move(game_map)
            self.last_move_time = current_time

    def draw(self, screen) -> None:
        x, y = self.pos

        rect = pygame.Rect(
            MAP_X + x * GRID_SIZE,
            MAP_Y + y * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE,
        )

        pygame.draw.rect(screen, BULLET_COLOUR, rect)


class BulletManager:
    def __init__(self):
        self.bullet_count = INITIAL_BULLETS
        self.bullets = []

    def shoot(self, player_snake, direction: tuple[int, int], game_map) -> None:

        if self.bullet_count <= 0:
            return

        head_x, head_y = player_snake.body[0]
        move_x, move_y = direction

        start_pos = player_snake.quantum_transit((head_x + move_x, head_y + move_y))

        self.bullet_count -= 1

        if not game_map.is_walkable(start_pos):
            return
        bullet = Bullet(
            start_pos,
            direction,
        )

        self.bullets.append(bullet)

    def handle_bullet_hit_object(
        self,
        bullet,
        game_map,
        apple_manager,
        item_manager,
        enemy_manager,
        player_snake,
        collected_letters: list[str],
    ) -> str | None:
        if apple_manager.handle_apple_hit_by_bullet(
            bullet.pos,
            game_map,
            collected_letters,
        ):
            bullet.alive = False
            return "apple"

        if item_manager.handle_tail_cut_hit_by_bullet(bullet.pos):
            bullet.alive = False
            return "tail_cut"

        if item_manager.handle_bullet_supply_hit_by_bullet(bullet.pos):
            bullet.alive = False
            return "bullet_supply"

        if enemy_manager.handle_enemy_hit_by_bullet(bullet.pos):
            bullet.alive = False
            return "enemy"

        if bullet.pos in player_snake.body and bullet.first_move:
            bullet.alive = False
            return "player"

        return None

    def update(
        self,
        game_map,
        apple_manager,
        item_manager,
        enemy_manager,
        player_snake,
        collected_letters: list[str],
    ) -> bool:
        alive_bullets = []
        player_hit_by_bullet = False

        for bullet in self.bullets:
            bullet.update(game_map)

            hit_type = None
            if bullet.alive:
                hit_type = self.handle_bullet_hit_object(
                    bullet,
                    game_map,
                    apple_manager,
                    item_manager,
                    enemy_manager,
                    player_snake,
                    collected_letters,
                )

            if hit_type == "player":
                player_hit_by_bullet = True
            if bullet.alive:
                alive_bullets.append(bullet)
                
        self.bullets = alive_bullets
        return player_hit_by_bullet

    def add_bullets(self, amount: int) -> None:
        self.bullet_count += amount

    def draw(self, screen) -> None:
        for bullet in self.bullets:
            bullet.draw(screen)
