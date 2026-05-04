import pygame

# const
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

def draw_snake(screen, snake_body):
    for segment in snake_body:
        x, y = segment

        rect = pygame.Rect(
            x * GRID_SIZE,
            y * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )

        pygame.draw.rect(screen, SNAKE_COLOUR, rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python's Burden: Escape from COMP9001")

    # snake info
    snake_body = [(5, 10), (4, 10), (3, 10)]

    game_running = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False


        screen.fill(BACKGROUND_COLOUR)
        draw_snake(screen, snake_body)


        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
