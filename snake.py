import pygame

from settings import (
    GRID_WIDTH,
    GRID_HEIGHT,
    GRID_SIZE,
    MAP_X,
    MAP_Y,
    SNAKE_COLOUR,
    TEXT_COLOUR,
    DIRECTIONS,
    INITIAL_SNAKE_BODY,
    INITIAL_LIVES,
)
from assets_loader import (
    load_grid_image,
    rotate_snake_image_by_direction,
    get_snake_tail_direction,
)


class Snake:
    def __init__(self, occupied_positions: list[tuple[int, int]]):
        self.direction = DIRECTIONS["RIGHT"]
        self.body = INITIAL_SNAKE_BODY.copy()
        self.lives = INITIAL_LIVES
        self.occupied_positions = occupied_positions
        self.is_invincible = False
        self.invincible_start_time = 0
        self.invincible_duration_ms = 3000

        for segment in self.body:
            if segment not in self.occupied_positions:
                self.occupied_positions.append(segment)

        self.head_image = load_grid_image("assets/images/snake/PlayerSnakeHead.png")
        self.body_image = load_grid_image("assets/images/snake/PlayerSnakeBody.png")
        self.tail_image = load_grid_image("assets/images/snake/PlayerSnakeTail16.png")

    def move(self, next_head: tuple[int, int], should_grow: bool) -> None:
        self.body.insert(0, next_head)  # insert new head into snake_body[0]

        # always add the new head position, one pos belongs to item, one pos belongs to the snake
        self.occupied_positions.append(next_head)

        if not should_grow:
            removed_tail = self.body.pop()
            if removed_tail in self.occupied_positions:
                self.occupied_positions.remove(removed_tail)

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

    def start_invincible(self) -> None:
        self.is_invincible = True
        self.invincible_start_time = pygame.time.get_ticks()

    def update_invincible(self, enemy_manager) -> None:
        if not self.is_invincible:
            return

        current_time = pygame.time.get_ticks()
        is_invincible_time_passed = (
            current_time - self.invincible_start_time >= self.invincible_duration_ms
        )

        if is_invincible_time_passed and not enemy_manager.check_player_body_overlap(
            self.body
        ):
            self.is_invincible = False

    def handle_bullet_hit(self) -> bool:
        if self.is_invincible:
            return False
        self.lose_life()
        return True

    def lose_life(self) -> None:
        self.lives -= 1

    def is_dead(self) -> bool:
        return self.lives <= 0

    # not allowed to be over grid_width
    def create_respawn_body(self, length: int) -> list[tuple[int, int]]:
        head_y = GRID_HEIGHT * 3 // 4

        if length <= GRID_WIDTH:
            head_x = length - 1
        else:
            head_x = GRID_WIDTH - 1
        body = []
        for i in range(length):
            x = head_x - i
            if x < 0:
                x = 0
            body.append((x, head_y))

        return body

    # just revive, no lives reset
    def revive(self) -> None:
        current_length = len(self.body)
        for segment in self.body:
            if segment in self.occupied_positions:
                self.occupied_positions.remove(segment)
        self.body = self.create_respawn_body(current_length)
        self.direction = DIRECTIONS["RIGHT"]
        for segment in self.body:
            if segment not in self.occupied_positions:
                self.occupied_positions.append(segment)

    def reset(self) -> None:
        for segment in self.body:
            if segment in self.occupied_positions:
                self.occupied_positions.remove(segment)
        self.body = INITIAL_SNAKE_BODY.copy()
        self.direction = DIRECTIONS["RIGHT"]
        for segment in self.body:
            if segment not in self.occupied_positions:
                self.occupied_positions.append(segment)
        self.lives = INITIAL_LIVES

    def cut_tail(self, cut_count: int) -> None:
        for i in range(cut_count):
            if len(self.body) > 1:
                removed_tail = self.body.pop()
                if removed_tail in self.occupied_positions:
                    self.occupied_positions.remove(removed_tail)

    def draw_snake_image(
        self, screen, image: pygame.Surface | None, rect: pygame.Rect
    ) -> None:
        if image is None:
            pygame.draw.rect(screen, SNAKE_COLOUR, rect)
            return
        if self.is_invincible:
            transparent_image = image.copy()
            transparent_image.set_alpha(120)
            screen.blit(transparent_image, rect)
        else:
            screen.blit(image, rect)

    def add_pause_duration(self, paused_duration_ms: int) -> None:
        if self.is_invincible:
            self.invincible_start_time += paused_duration_ms

    def draw(self, screen, font, collected_letters: list[str]) -> None:

        # get index and segment
        for index, segment in enumerate(self.body):
            x, y = segment

            rect = pygame.Rect(
                MAP_X + x * GRID_SIZE,
                MAP_Y + y * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE,
            )

            # draw head
            if index == 0:
                image = rotate_snake_image_by_direction(
                    self.head_image,
                    self.direction,
                )
                self.draw_snake_image(screen, image, rect)
            # draw tail
            elif index == len(self.body) - 1:
                if len(self.body) >= 2:
                    tail_direction = get_snake_tail_direction(
                        self.body[-2],
                        self.body[-1],
                    )
                else:
                    tail_direction = self.direction
                image = rotate_snake_image_by_direction(
                    self.tail_image,
                    tail_direction,
                )
                self.draw_snake_image(screen, image, rect)
            # draw body
            else:
                self.draw_snake_image(screen, self.body_image, rect)

            # index 0 is the snake head, so no letter on the head.

            if index > 0:
                letter_index = index - 1

                if letter_index < len(collected_letters):
                    letter = collected_letters[letter_index]
                    letter_text = font.render(letter, True, TEXT_COLOUR)
                    letter_rect = letter_text.get_rect(center=rect.center)
                    screen.blit(letter_text, letter_rect)
