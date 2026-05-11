import random
import pygame

from settings import (
    GRID_WIDTH,
    GRID_HEIGHT,
    GRID_SIZE,
    MAP_X,
    MAP_Y,
    DIRECTIONS,
    ENEMY_SNAKE_COLOUR,
    ENEMY_INITIAL_LENGTH,
    MAX_ENEMY_SNAKES,
    ENEMY_SPAWN_INTERVAL_MS,
    ENEMY_MIN_STEPS,
    ENEMY_MAX_STEPS,
)


class EnemySnake:
    def __init__(self, game_map, occupied_positions: list[tuple[int, int]]):
        self.occupied_positions = occupied_positions
        self.direction = random.choice(list(DIRECTIONS.values()))
        self.body = self.spawn_and_get_body(game_map)
        self.alive = True
        self.steps_remaining = random.randint(ENEMY_MIN_STEPS, ENEMY_MAX_STEPS)

        for segment in self.body:
            self.occupied_positions.append(segment)

    def spawn_and_get_body(self, game_map) -> list[tuple[int, int]]:
        while True:
            direction = random.choice(list(DIRECTIONS.values()))
            move_x, move_y = direction
            # random snake head position
            head = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
            body = []
            # body spawn depends on the head direction
            # direction:right, body will spawn on the left
            for i in range(ENEMY_INITIAL_LENGTH):
                x = head[0] - move_x * i
                y = head[1] - move_y * i
                body.append((x, y))
            # check whether the body is valid or not
            valid_body = True
            for segment in body:
                if not game_map.is_inside_map(segment):
                    valid_body = False

                elif not game_map.is_walkable(segment):
                    valid_body = False

                elif segment in self.occupied_positions:
                    valid_body = False
            # if valid, spawn
            if valid_body:
                self.direction = direction
                return body

    def draw(self, screen) -> None:
        for segment in self.body:
            x, y = segment
            rect = pygame.Rect(
                MAP_X + x * GRID_SIZE,
                MAP_Y + y * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE,
            )
            pygame.draw.rect(screen, ENEMY_SNAKE_COLOUR, rect)

    def get_next_head_pos(self, direction: tuple[int, int]) -> tuple[int, int]:
        head_x, head_y = self.body[0]
        move_x, move_y = direction

        next_head = (head_x + move_x, head_y + move_y)
        next_head = self.quantum_transit(next_head)

        return next_head

    # based on the current direction to turn left or right
    def turn_left(self, direction: tuple[int, int]) -> tuple[int, int]:
        if direction == DIRECTIONS["UP"]:
            return DIRECTIONS["LEFT"]
        if direction == DIRECTIONS["LEFT"]:
            return DIRECTIONS["DOWN"]
        if direction == DIRECTIONS["DOWN"]:
            return DIRECTIONS["RIGHT"]
        return DIRECTIONS["UP"]

    def turn_right(self, direction: tuple[int, int]) -> tuple[int, int]:
        if direction == DIRECTIONS["UP"]:
            return DIRECTIONS["RIGHT"]
        if direction == DIRECTIONS["RIGHT"]:
            return DIRECTIONS["DOWN"]
        if direction == DIRECTIONS["DOWN"]:
            return DIRECTIONS["LEFT"]
        return DIRECTIONS["UP"]

    def can_move_to(self, game_map, pos: tuple[int, int]) -> bool:
        # if not game_map.is_inside_map(pos):
        #     return False
        if not game_map.is_walkable(pos):
            return False
        if pos in self.occupied_positions:
            return False
        return True

    # main move logic
    def choose_direction(self, game_map) -> bool:
        forward = self.direction
        left = self.turn_left(self.direction)
        right = self.turn_right(self.direction)

        forward_pos = self.get_next_head_pos(forward)
        left_pos = self.get_next_head_pos(left)
        right_pos = self.get_next_head_pos(right)
        # First priority: moving forward
        if self.can_move_to(game_map, forward_pos):
            self.direction = forward
            return True
        # Second priority: 
        # If cant move forward, randomly choose to try left or right.
        side_directions = [left, right]
        random.shuffle(side_directions)
        first_direction = side_directions[0]
        second_direction = side_directions[1]

        first_pos = self.get_next_head_pos(first_direction)
        second_pos = self.get_next_head_pos(second_direction)
        if self.can_move_to(game_map, first_pos):
            self.direction = first_direction
            self.steps_remaining = random.randint(ENEMY_MIN_STEPS, ENEMY_MAX_STEPS)
            return True

        if self.can_move_to(game_map, second_pos):
            self.direction = second_direction
            self.steps_remaining = random.randint(ENEMY_MIN_STEPS, ENEMY_MAX_STEPS)
            return True

        return False

    def move(self, game_map) -> None:
        if not self.alive:
            return

        if self.steps_remaining <= 0:
            possible_directions = [
                self.direction,
                self.turn_left(self.direction),
                self.turn_right(self.direction),
            ]

            self.direction = random.choice(possible_directions)
            self.steps_remaining = random.randint(ENEMY_MIN_STEPS, ENEMY_MAX_STEPS)

        can_move = self.choose_direction(game_map)

        # if cant go forward,turn left or right, the snake will die
        if not can_move:
            self.die()
            return
        # move
        next_head = self.get_next_head_pos(self.direction)

        self.body.insert(0, next_head)
        self.occupied_positions.append(next_head)

        removed_tail = self.body.pop()

        if removed_tail in self.occupied_positions:
            self.occupied_positions.remove(removed_tail)

        self.steps_remaining -= 1

    def die(self) -> None:
        self.alive = False
        for segment in self.body:
            if segment in self.occupied_positions:
                self.occupied_positions.remove(segment)

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


class EnemyManager:
    def __init__(self, occupied_positions: list[tuple[int, int]]):
        self.occupied_positions = occupied_positions
        self.enemy_snakes = []
        self.last_spawn_time = pygame.time.get_ticks()

    def spawn_enemy_snake(self, game_map) -> None:
        if len(self.enemy_snakes) >= MAX_ENEMY_SNAKES:
            return

        enemy_snake = EnemySnake(
            game_map,
            self.occupied_positions,
        )

        self.enemy_snakes.append(enemy_snake)

    def check_player_collision(self, player_next_head: tuple[int, int]) -> bool:
        for enemy_snake in self.enemy_snakes:
            if player_next_head in enemy_snake.body:
                return True
        return False
        
    def update(self, game_map) -> None:
        current_time = pygame.time.get_ticks()

        if current_time - self.last_spawn_time >= ENEMY_SPAWN_INTERVAL_MS:
            self.spawn_enemy_snake(game_map)
            self.last_spawn_time = current_time

        alive_enemies = []

        for enemy_snake in self.enemy_snakes:
            enemy_snake.move(game_map)

            if enemy_snake.alive:
                alive_enemies.append(enemy_snake)

        self.enemy_snakes = alive_enemies

    def draw(self, screen) -> None:
        for enemy_snake in self.enemy_snakes:
            enemy_snake.draw(screen)
