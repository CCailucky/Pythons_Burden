import pygame

from settings import (
    UI_X,
    UI_Y,
    UI_WIDTH,
    UI_HEIGHT,
    UI_COLOUR,
    UI_BORDER_COLOUR,
    UI_TEXT_COLOUR,
    UI_TITLE_COLOUR,
    UI_ACCENT_COLOUR,
    UI_MUTED_TEXT_COLOUR,
    UI_FONT_PATH,
    UI_BOLD_FONT_PATH,
    UI_FONT_SIZE,
    UI_TITLE_FONT_SIZE,
    UI_SMALL_FONT_SIZE,
    TARGET_SEQUENCE,
    MAX_MSGS,
    PAUSE_OVERLAY_ALPHA,
    PAUSE_MENU_TITLE_Y,
    PAUSE_MENU_BUTTON_WIDTH,
    PAUSE_MENU_BUTTON_HEIGHT,
    PAUSE_MENU_BUTTON_GAP,
    PAUSE_MENU_START_Y_OFFSET,
    PAUSE_MENU_HINT_OFFSET_Y,
)
from assets_loader import load_image


class UI:
    def __init__(self):
        self.font = self.load_font(UI_FONT_PATH, UI_FONT_SIZE)
        self.title_font = self.load_font(UI_BOLD_FONT_PATH, UI_TITLE_FONT_SIZE)
        self.small_font = self.load_font(UI_FONT_PATH, UI_SMALL_FONT_SIZE)

        self.status_messages = []

        self.banner_image = load_image(
            "assets/images/ui/banner.png", (UI_WIDTH - 40, 100)
        )
        self.life_panel_image = load_image("assets/images/ui/life_panel.png", (260, 80))
        self.bullet_panel_image = load_image(
            "assets/images/ui/bullet_panel.png", (260, 80)
        )
        self.win_image = load_image("assets/images/ui/win.png", (UI_WIDTH - 40, 90))
        self.lose_image = load_image("assets/images/ui/lose.png", (UI_WIDTH - 40, 90))

        self.pause_resume_button_image = load_image(
            "assets/images/ui/resume_button.png",
            (PAUSE_MENU_BUTTON_WIDTH, PAUSE_MENU_BUTTON_HEIGHT),
        )
        self.pause_reset_button_image = load_image(
            "assets/images/ui/reset_button.png",
            (PAUSE_MENU_BUTTON_WIDTH, PAUSE_MENU_BUTTON_HEIGHT),
        )
        self.pause_quit_button_image = load_image(
            "assets/images/ui/quit_button.png",
            (PAUSE_MENU_BUTTON_WIDTH, PAUSE_MENU_BUTTON_HEIGHT),
        )

    def load_font(
        self,
        font_path: str,
        font_size: int,
    ) -> pygame.font.Font:
        try:
            return pygame.font.Font(font_path, font_size)
        except FileNotFoundError:
            print(f"Missing font: {font_path}")
            return pygame.font.Font(None, font_size)

    def add_status_message(self, message: str) -> None:
        self.status_messages.append(message)
        if len(self.status_messages) > MAX_MSGS:
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
        bullet_count: int,
    ) -> None:
        self.draw_background(screen)
        self.draw_title(screen)
        self.draw_controls(screen)
        self.draw_lives(screen, lives)
        self.draw_bullets(screen, bullet_count)
        self.draw_target_sequence(screen)
        self.draw_collected_letters(screen, collected_letters)
        self.draw_status_messages(screen)
        self.draw_game_status(screen, game_over, game_win)

    def draw_background(self, screen) -> None:
        ui_rect = pygame.Rect(UI_X, UI_Y, UI_WIDTH, UI_HEIGHT)

        pygame.draw.rect(screen, UI_COLOUR, ui_rect)
        pygame.draw.rect(screen, UI_BORDER_COLOUR, ui_rect, 3)

    def draw_title(self, screen) -> None:
        screen.blit(self.banner_image, (UI_X + 20, UI_Y + 20))

    def draw_controls(self, screen) -> None:
        control_x = UI_X + 30
        control_y = UI_Y + 145
        control_text = self.small_font.render("Arrow Keys: Move", True, UI_TEXT_COLOUR)
        screen.blit(control_text, (control_x, control_y))
        pause_text = self.small_font.render("ESC: Pause / Resume", True, UI_TEXT_COLOUR)
        screen.blit(pause_text, (control_x, control_y + 28))
        start_text = self.small_font.render("SPACE: Start", True, UI_TEXT_COLOUR)
        screen.blit(start_text, (control_x, control_y + 56))

    def draw_lives(self, screen, lives: int) -> None:
        panel_x = UI_X + 30
        panel_y = UI_Y + 245

        screen.blit(self.life_panel_image, (panel_x, panel_y))

        lives_value = self.title_font.render(str(lives), True, UI_TEXT_COLOUR)
        screen.blit(lives_value, (panel_x + 140, panel_y + 23))

    def draw_bullets(self, screen, bullet_count: int) -> None:
        panel_x = UI_X + 310
        panel_y = UI_Y + 245

        screen.blit(self.bullet_panel_image, (panel_x, panel_y))

        bullet_value = self.title_font.render(
            str(bullet_count),
            True,
            UI_ACCENT_COLOUR,
        )
        screen.blit(bullet_value, (panel_x + 140, panel_y + 23))

    def draw_target_sequence(self, screen) -> None:
        target_text = self.font.render("TARGET", True, UI_ACCENT_COLOUR)
        screen.blit(target_text, (UI_X + 30, UI_Y + 360))

        target_value = self.font.render(TARGET_SEQUENCE, True, UI_TEXT_COLOUR)
        screen.blit(target_value, (UI_X + 30, UI_Y + 395))

    def draw_collected_letters(self, screen, collected_letters: list[str]) -> None:
        collected_text = self.font.render("COLLECTED", True, UI_ACCENT_COLOUR)
        screen.blit(collected_text, (UI_X + 30, UI_Y + 465))

        collected_value = self.font.render(
            "".join(collected_letters), True, UI_TEXT_COLOUR
        )
        screen.blit(collected_value, (UI_X + 30, UI_Y + 500))

    def draw_status_messages(self, screen) -> None:
        status_x = UI_X + 30
        status_y = UI_Y + 580

        status_text = self.font.render("STATUS", True, UI_ACCENT_COLOUR)
        screen.blit(status_text, (status_x, status_y))

        for i in range(len(self.status_messages)):
            message = self.status_messages[i]
            message_text = self.small_font.render(message, True, UI_TEXT_COLOUR)
            screen.blit(message_text, (status_x, status_y + 35 + i * 25))

    def draw_game_status(self, screen, game_over: bool, game_win: bool) -> None:
        banner_x = UI_X + 20
        banner_y = UI_Y + UI_HEIGHT - 115
        if game_win:
            screen.blit(self.win_image, (banner_x, banner_y))
            return
        if game_over:
            screen.blit(self.lose_image, (banner_x, banner_y))

    def draw_pause_overlay(self, screen) -> None:
        screen_width, screen_height = screen.get_size()

        # dark overlay
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, PAUSE_OVERLAY_ALPHA))
        screen.blit(overlay, (0, 0))

        # title
        title_text = self.title_font.render("GAME PAUSED", True, UI_ACCENT_COLOUR)
        title_rect = title_text.get_rect(center=(screen_width // 2, PAUSE_MENU_TITLE_Y))
        screen.blit(title_text, title_rect)

        total_height = PAUSE_MENU_BUTTON_HEIGHT * 3 + PAUSE_MENU_BUTTON_GAP * 2

        start_y = (screen_height - total_height) // 2 + PAUSE_MENU_START_Y_OFFSET
        button_x = (screen_width - PAUSE_MENU_BUTTON_WIDTH) // 2

        screen.blit(self.pause_resume_button_image, (button_x, start_y))

        screen.blit(
            self.pause_reset_button_image,
            (button_x, start_y + PAUSE_MENU_BUTTON_HEIGHT + PAUSE_MENU_BUTTON_GAP),
        )

        screen.blit(
            self.pause_quit_button_image,
            (
                button_x,
                start_y + (PAUSE_MENU_BUTTON_HEIGHT + PAUSE_MENU_BUTTON_GAP) * 2,
            ),
        )

        hint_text = self.small_font.render(
            "ESC: Resume    R: Reset    Q: Quit", True, UI_TEXT_COLOUR
        )
        hint_rect = hint_text.get_rect(
            center=(
                screen_width // 2,
                start_y + total_height + PAUSE_MENU_HINT_OFFSET_Y,
            )
        )
        screen.blit(hint_text, hint_rect)
