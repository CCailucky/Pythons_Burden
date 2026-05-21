import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WINDOW_WIDTH_RATIO,
    WINDOW_HEIGHT_RATIO,
)

# adaptive to the window screen size
class DisplayManager:
    def __init__(self):
        self.window_size = self.get_adaptive_window_size()
        self.screen = pygame.display.set_mode(self.window_size)
        self.game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def get_adaptive_window_size(self) -> tuple[int, int]:
        display_info = pygame.display.Info()

        max_width = int(display_info.current_w * WINDOW_WIDTH_RATIO)
        max_height = int(display_info.current_h * WINDOW_HEIGHT_RATIO)

        scale = min(
            max_width / SCREEN_WIDTH,
            max_height / SCREEN_HEIGHT,
            1,
        )

        window_width = int(SCREEN_WIDTH * scale)
        window_height = int(SCREEN_HEIGHT * scale)

        return window_width, window_height

    def draw_to_screen(self) -> None:
        scaled_surface = pygame.transform.scale(
            self.game_surface,
            self.window_size,
        )
        self.screen.blit(scaled_surface, (0, 0))

    def convert_mouse_pos_to_game_surface(
        self,
        mouse_pos: tuple[int, int],
    ) -> tuple[int, int]:
        scale_x = SCREEN_WIDTH / self.window_size[0]
        scale_y = SCREEN_HEIGHT / self.window_size[1]

        return (
            int(mouse_pos[0] * scale_x),
            int(mouse_pos[1] * scale_y),
        )