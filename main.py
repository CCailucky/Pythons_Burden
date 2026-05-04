import pygame

# ---const--- #
# grid
GRID_SIZE = 30
GRID_WIDTH = 25
GRID_HEIGHT = 20
# colour
BACKGROUND_COLOUR = (30, 30, 30)
SNAKE_COLOUR = (80, 220, 120)
# screen
SCREEN_WIDTH = GRID_SIZE * GRID_WIDTH
SCREEN_HEIGHT = GRID_SIZE * GRID_HEIGHT




def draw_snake(screen, snake_body: list[tuple[int, int]]) -> None:
    for segment in snake_body:
        x, y = segment
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, SNAKE_COLOUR, rect)


def move_snake(snake_body: list[tuple[int, int]], direction: tuple[int, int]) -> None:
    head_x, head_y = snake_body[0]
    move_x, move_y = direction

    new_head = (head_x + move_x, head_y + move_y)
    snake_body.insert(0, new_head)  # insert new head into snake_body[0]
    snake_body.pop()  # pop the tail


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python's Burden: Escape from COMP9001")
    clock = pygame.time.Clock()


    # ---arguments--- #
    game_running = True
    # snake information
    snake_body = [(5, 10), (4, 10), (3, 10)]
    # snake direction
    directions = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
    direction = directions["RIGHT"]  # default direction

    # main loop
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN:
                # change direction by up down left and right key (NO 180-DEGREE TURN)
                if event.key == pygame.K_UP and direction != directions["DOWN"]:
                    direction = directions["UP"]
                elif event.key == pygame.K_DOWN and direction != directions["UP"]:
                    direction = directions["DOWN"]
                elif event.key == pygame.K_LEFT and direction != directions["RIGHT"]:
                    direction = directions["LEFT"]
                elif event.key == pygame.K_RIGHT and direction != directions["LEFT"]:
                    direction = directions["RIGHT"]
        move_snake(snake_body, direction)
        screen.fill(BACKGROUND_COLOUR)
        draw_snake(screen, snake_body)
        pygame.display.flip()  # draw all
        clock.tick(5)  # FPS = 5
    pygame.quit()


if __name__ == "__main__":
    main()
