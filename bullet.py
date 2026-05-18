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
        # when spawned, immediately move to the next grid, in order to avoid spawn in the snake's head
        self.last_move_time = self.spawn_time - BULLET_MOVE_INTERVAL_MS
        self.alive = True

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

    def move(self) -> None:
        move_x, move_y = self.direction
        next_pos = (
            self.pos[0] + move_x,
            self.pos[1] + move_y,
        )

        next_pos = self.quantum_transit(next_pos)
        self.pos = next_pos

    def update(self) -> None:
        current_time = pygame.time.get_ticks()

        if current_time - self.spawn_time >= BULLET_LIFETIME_MS:
            self.alive = False
            return

        while current_time - self.last_move_time >= BULLET_MOVE_INTERVAL_MS:
            self.move()
            self.last_move_time += BULLET_MOVE_INTERVAL_MS

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

    def shoot(self, player_snake, direction: tuple[int, int]) -> None:

        if self.bullet_count <= 0:
            return

        head_x, head_y = player_snake.body[0]
        move_x, move_y = direction

        start_pos = player_snake.quantum_transit((head_x + move_x, head_y + move_y))

        bullet = Bullet(
            start_pos,
            direction,
        )

        self.bullets.append(bullet)
        self.bullet_count -= 1

    def update(self) -> None:
        alive_bullets = []

        for bullet in self.bullets:
            bullet.update()

            if bullet.alive:
                alive_bullets.append(bullet)

        self.bullets = alive_bullets

    def draw(self, screen) -> None:
        for bullet in self.bullets:
            bullet.draw(screen)
