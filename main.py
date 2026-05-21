import pygame

from settings import FPS
from game_initialization import initialize_game


def main():
    display, clock, game = initialize_game()
    game_running = True
    # input->logic->draw :)
    while game_running:
        # input
        game_running = game.handle_events(game_running, display)
        # logic
        game.update()
        # draw
        game.draw(display.game_surface)
        display.draw_to_screen()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
