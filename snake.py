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


class Snake:
    def __init__(self, occupied_positions: list[tuple[int, int]]):
        self.direction = DIRECTIONS["RIGHT"]
        self.body = INITIAL_SNAKE_BODY.copy()
        self.lives = INITIAL_LIVES
        self.occupied_positions = occupied_positions
        for segment in self.body:
            if segment not in self.occupied_positions:
                self.occupied_positions.append(segment)

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

    def lose_life(self) -> None:
        self.lives -= 1

    def is_dead(self) -> bool:
        return self.lives <= 0

    # not allowed to be over grid_width
    def create_respawn_body(self, length: int) -> list[tuple[int, int]]:
        head_y = 20

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

    # def draw(self, screen) -> None:
    #     for segment in self.body:
    #         x, y = segment
    #         # start from (MAP_X, MAP_Y)
    #         rect = pygame.Rect(
    #             MAP_X + x * GRID_SIZE,
    #             MAP_Y + y * GRID_SIZE,
    #             GRID_SIZE,
    #             GRID_SIZE,
    #         )
    #         pygame.draw.rect(screen, SNAKE_COLOUR, rect)

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

            pygame.draw.rect(screen, SNAKE_COLOUR, rect)

            # index 0 is the snake head, so no letter on the head.
            if index > 0:
                letter_index = index - 1

                if letter_index < len(collected_letters):
                    letter = collected_letters[letter_index]
                    letter_text = font.render(letter, True, TEXT_COLOUR)
                    letter_rect = letter_text.get_rect(center=rect.center)
                    screen.blit(letter_text, letter_rect)
