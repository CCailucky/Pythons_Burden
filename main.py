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


def move_snake(snake_body: list[tuple[int, int]], direction: tuple[int, int]) -> None:
    head_x, head_y = snake_body[0]
    move_x, move_y = direction

    new_head = (head_x + move_x, head_y + move_y)
    # check whether quantum transit is triggered
    new_head = quantum_transit(new_head)
    snake_body.insert(0, new_head)  # insert new head into snake_body[0]
    snake_body.pop()  # pop the tail


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
def draw_ui(screen, font) -> None:
    ui_rect = pygame.Rect(UI_X, UI_Y, UI_WIDTH, UI_HEIGHT)
    pygame.draw.rect(screen, UI_COLOUR, ui_rect)

    title_text = font.render("Python's Burden", True, TEXT_COLOUR)
    screen.blit(title_text, (UI_X + 20, UI_Y + 20))

    control_text = font.render("Arrow Keys: Move", True, TEXT_COLOUR)
    screen.blit(control_text, (UI_X + 20, UI_Y + 70))


def handle_events(
    game_running: bool,
    direction: tuple[int, int],
    directions: dict[str, tuple[int, int]],
) -> tuple[bool, tuple[int, int]]:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            # Change direction by arrow keys. No 180-degree turn.
            if event.key == pygame.K_UP and direction != directions["DOWN"]:
                direction = directions["UP"]
            elif event.key == pygame.K_DOWN and direction != directions["UP"]:
                direction = directions["DOWN"]
            elif event.key == pygame.K_LEFT and direction != directions["RIGHT"]:
                direction = directions["LEFT"]
            elif event.key == pygame.K_RIGHT and direction != directions["LEFT"]:
                direction = directions["RIGHT"]

    return game_running, direction


def generate_and_get_apple_position(
    snake_body: list[tuple[int, int]],
) -> tuple[int, int]:
    while True:
        position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1),
        )
        if position not in snake_body:
            return position


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python's Burden: Escape from COMP9001")
    clock = pygame.time.Clock()

    # ---arguments--- #
    game_running = True
    # font
    font = pygame.font.Font(None, 28)
    # snake information
    snake_body = [(20, 20), (19, 20), (18, 20)]
    # snake direction
    directions = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
    direction = directions["RIGHT"]  # default direction
    # apple
    apple_pos = generate_and_get_apple_position(snake_body)
    # main loop
    while game_running:
        # event handle (handle events like key press)
        game_running, direction = handle_events(game_running, direction, directions)
        move_snake(snake_body, direction)

        # draw
        screen.fill(BACKGROUND_COLOUR)
        draw_map(screen)
        draw_snake(screen, snake_body)
        draw_apple(screen, apple_pos)
        draw_ui(screen, font)
        pygame.display.flip()  # draw all

        clock.tick(20)  # FPS
    pygame.quit()


if __name__ == "__main__":
    main()
