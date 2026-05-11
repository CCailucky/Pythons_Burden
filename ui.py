import pygame

from settings import (
    GRID_SIZE,
    MAP_X,
    MAP_Y,
    MAP_WIDTH,
    MAP_HEIGHT,
    UI_X,
    UI_Y,
    UI_WIDTH,
    UI_HEIGHT,
    MAP_COLOUR,
    SNAKE_COLOUR,
    APPLE_COLOUR,
    UI_COLOUR,
    TEXT_COLOUR,
    TARGET_SEQUENCE,
)


class UI:
    def __init__(self, font):
        self.font = font
        self.status_messages = []  # 5 msgs

    def add_status_message(self, message: str) -> None:
        self.status_messages.append(message)
        if len(self.status_messages) > 5:
            self.status_messages.pop(0)

    def reset_status_messages(self) -> None:
        self.status_messages = []
        self.add_status_message("Press SPACE to start")

    def draw(
        self,
        screen,
        lives: int,
        game_over: bool,
        game_win: bool,
        collected_letters: list[str],
    ) -> None:
        self.draw_background(screen)
        self.draw_title(screen)
        self.draw_controls(screen)
        self.draw_lives(screen, lives)
        self.draw_target_sequence(screen)
        self.draw_collected_letters(screen, collected_letters)
        self.draw_status_messages(screen)
        #self.draw_game_status(screen, game_over, game_win)

    def draw_background(self, screen) -> None:
        ui_rect = pygame.Rect(UI_X, UI_Y, UI_WIDTH, UI_HEIGHT)
        pygame.draw.rect(screen, UI_COLOUR, ui_rect)

    def draw_title(self, screen) -> None:
        title_text = self.font.render("Python's Burden", True, TEXT_COLOUR)
        screen.blit(title_text, (UI_X + 20, UI_Y + 20))

    def draw_controls(self, screen) -> None:
        control_text = self.font.render("Arrow Keys: Move", True, TEXT_COLOUR)
        screen.blit(control_text, (UI_X + 20, UI_Y + 70))

        pause_text = self.font.render("P: Pause / Resume", True, TEXT_COLOUR)
        screen.blit(pause_text, (UI_X + 20, UI_Y + 100))

        start_text = self.font.render("SPACE: Start", True, TEXT_COLOUR)
        screen.blit(start_text, (UI_X + 20, UI_Y + 130))

    def draw_lives(self, screen, lives: int) -> None:
        lives_text = self.font.render(f"Lives: {lives}", True, TEXT_COLOUR)
        screen.blit(lives_text, (UI_X + 20, UI_Y + 170))

    def draw_target_sequence(self, screen) -> None:
        target_text = self.font.render("Target:", True, TEXT_COLOUR)
        screen.blit(target_text, (UI_X + 20, UI_Y + 2200))

        target_value = self.font.render(TARGET_SEQUENCE, True, TEXT_COLOUR)
        screen.blit(target_value, (UI_X + 20, UI_Y + 250))

    def draw_collected_letters(
        self,
        screen,
        collected_letters: list[str],
    ) -> None:
        collected_text = self.font.render("Collected:", True, TEXT_COLOUR)
        screen.blit(collected_text, (UI_X + 20, UI_Y + 300))

        collected_value = self.font.render(
            "".join(collected_letters),
            True,
            TEXT_COLOUR,
        )
        screen.blit(collected_value, (UI_X + 20, UI_Y + 330))

    def draw_status_messages(self, screen) -> None:
        status_text = self.font.render("Status:", True, TEXT_COLOUR)
        screen.blit(status_text, (UI_X + 20, UI_Y + 390))

        for i in range(len(self.status_messages)):
            message = self.status_messages[i]
            message_text = self.font.render(message, True, TEXT_COLOUR)
            screen.blit(message_text, (UI_X + 20, UI_Y + 420 + i * 30))

    # def draw_game_status(
    #     self,
    #     screen,
    #     game_over: bool,
    #     game_win: bool,
    # ) -> None:
    #     if game_over:
    #         game_over_text = self.font.render("Game Over", True, TEXT_COLOUR)
    #         screen.blit(game_over_text, (UI_X + 20, UI_Y + 520))

    #         restart_text = self.font.render("Press R to restart", True, TEXT_COLOUR)
    #         screen.blit(restart_text, (UI_X + 20, UI_Y + 550))

    #     if game_win:
    #         victory_text = self.font.render(
    #             "Sequence Complete! You Win!",
    #             True,
    #             TEXT_COLOUR,
    #         )
    #         screen.blit(victory_text, (UI_X + 20, UI_Y + 520))

    #         restart_text = self.font.render("Press R to restart", True, TEXT_COLOUR)
    #         screen.blit(restart_text, (UI_X + 20, UI_Y + 550))
