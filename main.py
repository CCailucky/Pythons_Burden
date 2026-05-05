import pygame
import random

# ---const--- #
# grid
GRID_SIZE = 20
GRID_WIDTH = 40
GRID_HEIGHT = 40
# colour
BACKGROUND_COLOUR = (30, 30, 30)
SNAKE_COLOUR = (80, 220, 120)
MAP_COLOUR = (20, 20, 20)
UI_COLOUR = (245, 245, 245)
TEXT_COLOUR = (30, 30, 30)
APPLE_COLOUR = (220, 60, 60)
# --- layout --- #
LEFT_MARGIN = 40
TOP_MARGIN = 40
RIGHT_MARGIN = 40
BOTTOM_MARGIN = 40
UI_GAP = 40
# MAP width
MAP_WIDTH = GRID_SIZE * GRID_WIDTH  # 800
MAP_HEIGHT = GRID_SIZE * GRID_HEIGHT  # 800
# map left top corner
MAP_X = LEFT_MARGIN
MAP_Y = TOP_MARGIN
# UI
UI_WIDTH = MAP_WIDTH // 2
UI_HEIGHT = MAP_HEIGHT
UI_X = MAP_X + MAP_WIDTH + UI_GAP
UI_Y = MAP_Y
# screen
SCREEN_WIDTH = LEFT_MARGIN + MAP_WIDTH + UI_GAP + UI_WIDTH + RIGHT_MARGIN
SCREEN_HEIGHT = TOP_MARGIN + MAP_HEIGHT + BOTTOM_MARGIN


def move_snake(
    snake_body: list[tuple[int, int]], next_head: tuple[int, int], should_grow: bool
) -> None:
    snake_body.insert(0, next_head)  # insert new head into snake_body[0]
    if not should_grow:
        snake_body.pop()  # pop the tail


def get_next_head_pos(
    snake_body: list[tuple[int, int]], direction: tuple[int, int]
) -> tuple[int, int]:
    head_x, head_y = snake_body[0]
    move_x, move_y = direction

    next_head = (head_x + move_x, head_y + move_y)
    # check whether quantum transit is triggered
    next_head = quantum_transit(next_head)

    return next_head


# transit the snake from one place to another place
def quantum_transit(position: tuple[int, int]) -> tuple[int, int]:
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


def draw_map(screen) -> None:
    map_rect = pygame.Rect(MAP_X, MAP_Y, MAP_WIDTH, MAP_HEIGHT)
    pygame.draw.rect(screen, MAP_COLOUR, map_rect)


def draw_snake(screen, snake_body: list[tuple[int, int]]) -> None:
    for segment in snake_body:
        x, y = segment
        # start from (MAP_X, MAP_Y)
        rect = pygame.Rect(
            MAP_X + x * GRID_SIZE, MAP_Y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(screen, SNAKE_COLOUR, rect)


# similar to draw a snake
def draw_apple(screen, apple_pos: tuple[int, int]) -> None:
    x, y = apple_pos

    rect = pygame.Rect(
        MAP_X + x * GRID_SIZE, MAP_Y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE
    )

    pygame.draw.rect(screen, APPLE_COLOUR, rect)


# for test not completed
def draw_ui(screen, font, lives: int, game_over: bool) -> None:
    ui_rect = pygame.Rect(UI_X, UI_Y, UI_WIDTH, UI_HEIGHT)
    pygame.draw.rect(screen, UI_COLOUR, ui_rect)

    title_text = font.render("Python's Burden", True, TEXT_COLOUR)
    screen.blit(title_text, (UI_X + 20, UI_Y + 20))

    control_text = font.render("Arrow Keys: Move", True, TEXT_COLOUR)
    screen.blit(control_text, (UI_X + 20, UI_Y + 70))

    lives_text = font.render(f"Lives: {lives}", True, TEXT_COLOUR)
    screen.blit(lives_text, (UI_X + 20, UI_Y + 120))

    if game_over:
        game_over_text = font.render("Game Over", True, TEXT_COLOUR)
        screen.blit(game_over_text, (UI_X + 20, UI_Y + 170))


def handle_events(
    game_running: bool,
    direction: tuple[int, int],
    directions: dict[str, tuple[int, int]],
    game_over: bool,
) -> tuple[bool, tuple[int, int], bool]:
    restart_request = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            # game is over then press r to restart the game
            if game_over and event.key == pygame.K_r:
                restart_request = True

        if not game_over and event.type == pygame.KEYDOWN:
            # Change direction by arrow keys. No 180-degree turn.
            if event.key == pygame.K_UP and direction != directions["DOWN"]:
                direction = directions["UP"]
            elif event.key == pygame.K_DOWN and direction != directions["UP"]:
                direction = directions["DOWN"]
            elif event.key == pygame.K_LEFT and direction != directions["RIGHT"]:
                direction = directions["LEFT"]
            elif event.key == pygame.K_RIGHT and direction != directions["LEFT"]:
                direction = directions["RIGHT"]

    return game_running, direction, restart_request


def spawn_and_get_apple_position(
    snake_body: list[tuple[int, int]],
) -> tuple[int, int]:
    while True:
        position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1),
        )
        if position not in snake_body:
            return position


def check_apple_eaten(next_head: tuple[int, int], apple_pos: tuple[int, int]) -> bool:
    return next_head == apple_pos


def check_self_collision(
    next_head: tuple[int, int], snake_body: list[tuple[int, int]], apple_eaten: bool
) -> bool:
    # tail wont disappear so the tail will be included to check the collision
    if apple_eaten:
        return next_head in snake_body
    # snake_body[:-1] for NO collision with the tail, because the tail will disappear in the next move
    return next_head in snake_body[:-1]


def reset_snake(
    directions: dict[str, tuple[int, int]],
) -> tuple[list[tuple[int, int]], tuple[int, int]]:
    snake_body = [(20, 20), (19, 20), (18, 20), (17, 20), (16, 20)]
    direction = directions["RIGHT"]

    return snake_body, direction


def reset_game(
    directions: dict[str, tuple[int, int]],
) -> tuple[list[tuple[int, int]], tuple[int, int], tuple[int, int], int, bool]:
    snake_body, direction = reset_snake(directions)
    apple_pos = spawn_and_get_apple_position(snake_body)
    lives = 3
    game_over = False

    return snake_body, direction, apple_pos, lives, game_over


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python's Burden: Escape from COMP9001")
    clock = pygame.time.Clock()

    # ---arguments--- #
    game_running = True
    game_over = False
    restart_request = False
    # font
    font = pygame.font.Font(None, 28)
    # snake information
    snake_body = [(20, 20), (19, 20), (18, 20), (17, 20), (16, 20)]
    # snake direction
    directions = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
    direction = directions["RIGHT"]  # default direction
    # apple
    apple_pos = spawn_and_get_apple_position(snake_body)
    # life
    lives = 3

    # main loop
    while game_running:

        # event handle (handle events like key press)
        game_running, direction, restart_request = handle_events(
            game_running, direction, directions, game_over
        )
        if restart_request:
            snake_body, direction, apple_pos, lives, game_over = reset_game(directions)
        if not game_over:
            # next_head_pos for checking whether the apple is eaten
            next_head = get_next_head_pos(snake_body, direction)
            apple_eaten = check_apple_eaten(next_head, apple_pos)
            # is collided
            if check_self_collision(next_head, snake_body, apple_eaten):
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    snake_body, direction = reset_snake(directions)
                    apple_pos = spawn_and_get_apple_position(snake_body)
            else:
                move_snake(snake_body, next_head, apple_eaten)
                if apple_eaten:
                    apple_pos = spawn_and_get_apple_position(snake_body)

        # draw
        screen.fill(BACKGROUND_COLOUR)
        draw_map(screen)
        draw_snake(screen, snake_body)
        draw_apple(screen, apple_pos)
        draw_ui(screen, font, lives, game_over)
        pygame.display.flip()  # draw all

        clock.tick(8)  # FPS
    pygame.quit()


if __name__ == "__main__":
    main()
