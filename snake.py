import pygame

from settings import (
    GRID_WIDTH,
    GRID_HEIGHT,
    GRID_SIZE,
    MAP_X,
    MAP_Y,
    SNAKE_COLOUR,
    DIRECTIONS,
)


class Snake:
    def __init__(self):
        self.body = [(20, 20), (19, 20), (18, 20), (17, 20), (16, 20)]
        self.direction = DIRECTIONS["RIGHT"]
        self.lives = 3

    def draw(self, screen) -> None:
        for segment in self.body:
            x, y = segment
            # start from (MAP_X, MAP_Y)
            rect = pygame.Rect(
                MAP_X + x * GRID_SIZE,
                MAP_Y + y * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE,
            )
            pygame.draw.rect(screen, SNAKE_COLOUR, rect)

    def move(self, next_head: tuple[int, int], should_grow: bool) -> None:
        self.body.insert(0, next_head)  # insert new head into snake_body[0]

        if not should_grow:
            self.body.pop()  # pop the tail

    def get_next_head_pos(self) -> tuple[int, int]:
        head_x, head_y = self.body[0]
        move_x, move_y = self.direction

        next_head = (head_x + move_x, head_y + move_y)
        # check whether quantum transit is triggered
        next_head = self.quantum_transit(next_head)
        return next_head

    # transit the snake from one place to another place
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

    def check_self_collision(
        self,
        next_head: tuple[int, int],
        apple_eaten: bool,
    ) -> bool:
        # tail wont disappear so the tail will be included to check the collision
        if apple_eaten:
            return next_head in self.body
        # snake_body[:-1] for NO collision with the tail, because the tail will disappear in the next move
        return next_head in self.body[:-1]

    def lose_life(self) -> None:
        self.lives -= 1
    def is_dead(self) -> bool:
        return self.lives <= 0
    # just revive, no lives reset
    def revive(self) -> None:
        self.body = [(20, 20), (19, 20), (18, 20), (17, 20), (16, 20)]
        self.direction = DIRECTIONS["RIGHT"]

    def reset(self) -> None:
        self.body = [(20, 20), (19, 20), (18, 20), (17, 20), (16, 20)]
        self.direction = DIRECTIONS["RIGHT"]
        self.lives = 3
