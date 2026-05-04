import pygame


def main():
    pygame.init()

    screen = pygame.display.set_mode((750, 600)) # width 750 height 600
    pygame.display.set_caption("Python's Burden: Escape from COMP9001")

    game_running = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        screen.fill((30, 30, 30))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()