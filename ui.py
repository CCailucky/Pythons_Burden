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
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    # start interface
    START_MENU_BUTTON_WIDTH,
    START_MENU_BUTTON_HEIGHT,
    START_MENU_BUTTON_GAP,
    START_MENU_BUTTON_BOTTOM_MARGIN,
    # rule interface 1
    RULES_PAGE_COUNT,
    RULES_OVERLAY_ALPHA,
    RULES_BACK_BUTTON_WIDTH,
    RULES_BACK_BUTTON_HEIGHT,
    RULES_BACK_BUTTON_X,
    RULES_BACK_BUTTON_Y,
    RULES_NAV_BUTTON_WIDTH,
    RULES_NAV_BUTTON_HEIGHT,
    RULES_NAV_BUTTON_SIDE_MARGIN,
    RULES_NAV_BUTTON_BOTTOM_MARGIN,
    RULES_TITLE_Y,
    RULES_STORY_START_Y,
    RULES_STORY_LINE_GAP,
    RULES_INTRO_FONT_SIZE,
    # rule interface 2
    RULES_ITEM_ICON_SIZE,
    RULES_ITEM_TEXT_OFFSET_X,
    RULES_ITEM_LEFT_X,
    RULES_ITEM_RIGHT_X,
    RULES_ITEM_START_Y,
    RULES_ITEM_ROW_GAP,
    RULES_ITEM_TITLE_LINE_GAP,
    RULES_ITEM_DESC_LINE_GAP,
    # rules interface 3 and 4 images
    RULES_MECHANIC_IMAGE_WIDTH,
    RULES_MECHANIC_IMAGE_HEIGHT,
    RULES_PAGE_TWO_COL_LEFT_X,
    RULES_PAGE_TWO_COL_RIGHT_X,
    RULES_PAGE_IMAGE_TOP_Y,
    RULES_PAGE_THREE_COL_LEFT_X,
    RULES_PAGE_THREE_COL_MIDDLE_X,
    RULES_PAGE_THREE_COL_RIGHT_X,
    RULES_IMAGE_TITLE_OFFSET_Y,
    RULES_IMAGE_DESC_OFFSET_Y,
    RULES_IMAGE_DESC_LINE_GAP,
    RULES_BOTTOM_INFO_Y,
)
from assets_loader import load_image


class UI:
    def __init__(self):
        self.font = self.load_font(UI_FONT_PATH, UI_FONT_SIZE)
        self.title_font = self.load_font(UI_BOLD_FONT_PATH, UI_TITLE_FONT_SIZE)
        self.small_font = self.load_font(UI_FONT_PATH, UI_SMALL_FONT_SIZE)
        self.rules_intro_font = self.load_font(UI_FONT_PATH, RULES_INTRO_FONT_SIZE)
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
        # GAME UI
        # button
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
        # icon
        self.letter_icon = load_image("assets/images/apples/A.png", (16, 16))
        self.wildcard_icon = load_image(
            "assets/images/apples/golden_apple.png", (16, 16)
        )
        self.bullet_supply_icon = load_image(
            "assets/images/items/bulletsupply.png", (16, 16)
        )
        self.tail_cut_icon = load_image("assets/images/items/tailcut.png", (16, 16))
        # START INTERFACE
        self.start_interface_image = load_image(
            "assets/images/ui/start_interface.png", (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        self.start_button_image = load_image(
            "assets/images/ui/start_button.png",
            (START_MENU_BUTTON_WIDTH, START_MENU_BUTTON_HEIGHT),
        )

        self.rules_button_image = load_image(
            "assets/images/ui/rules_button.png",
            (START_MENU_BUTTON_WIDTH, START_MENU_BUTTON_HEIGHT),
        )

        self.quit_button2_image = load_image(
            "assets/images/ui/quit_button2.png",
            (START_MENU_BUTTON_WIDTH, START_MENU_BUTTON_HEIGHT),
        )

        # RULES INTERFACE 1
        self.back_button_image = load_image(
            "assets/images/ui/back_button.png",
            (RULES_BACK_BUTTON_WIDTH, RULES_BACK_BUTTON_HEIGHT),
        )

        self.prev_button_image = load_image(
            "assets/images/ui/prev_button.png",
            (RULES_NAV_BUTTON_WIDTH, RULES_NAV_BUTTON_HEIGHT),
        )

        self.next_button_image = load_image(
            "assets/images/ui/next_button.png",
            (RULES_NAV_BUTTON_WIDTH, RULES_NAV_BUTTON_HEIGHT),
        )
        # RULES INTERFACE 2
        self.rules_letter_icon = load_image(
            "assets/images/apples/A.png",
            (RULES_ITEM_ICON_SIZE, RULES_ITEM_ICON_SIZE),
        )

        self.rules_wildcard_icon = load_image(
            "assets/images/apples/golden_apple.png",
            (RULES_ITEM_ICON_SIZE, RULES_ITEM_ICON_SIZE),
        )

        self.rules_bullet_icon = load_image(
            "assets/images/items/bullet.png",
            (RULES_ITEM_ICON_SIZE, RULES_ITEM_ICON_SIZE),
        )

        self.rules_bullet_supply_icon = load_image(
            "assets/images/items/bulletsupply.png",
            (RULES_ITEM_ICON_SIZE, RULES_ITEM_ICON_SIZE),
        )

        self.rules_tail_cut_icon = load_image(
            "assets/images/items/tailcut.png",
            (RULES_ITEM_ICON_SIZE, RULES_ITEM_ICON_SIZE),
        )
        # RULES INTERFACE 3 AND 4
        self.rules_bullet_enemy_image = load_image(
            "assets/images/intro/bullet_vs_enemy.png",
            (RULES_MECHANIC_IMAGE_WIDTH, RULES_MECHANIC_IMAGE_HEIGHT),
        )

        self.rules_bullet_enemy_2_image = load_image(
            "assets/images/intro/bullet_vs_enemy2.png",
            (RULES_MECHANIC_IMAGE_WIDTH, RULES_MECHANIC_IMAGE_HEIGHT),
        )

        self.rules_eat_letter_image = load_image(
            "assets/images/intro/eat_letter.png",
            (RULES_MECHANIC_IMAGE_WIDTH, RULES_MECHANIC_IMAGE_HEIGHT),
        )

        self.rules_target_image = load_image(
            "assets/images/intro/target.png",
            (RULES_MECHANIC_IMAGE_WIDTH, RULES_MECHANIC_IMAGE_HEIGHT),
        )

        self.rules_exit_portal_image = load_image(
            "assets/images/intro/exit_portal.png",
            (RULES_MECHANIC_IMAGE_WIDTH, RULES_MECHANIC_IMAGE_HEIGHT),
        )

        self.rules_heart_icon = load_image(
            "assets/images/intro/heart.png",
            (RULES_ITEM_ICON_SIZE, RULES_ITEM_ICON_SIZE),
        )
        self.rules_quantum_teleport_icon = load_image(
            "assets/images/intro/teleport.png",
            (RULES_ITEM_ICON_SIZE, RULES_ITEM_ICON_SIZE),
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

    def get_pause_menu_button_rects(
        self, screen_width: int, screen_height: int
    ) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect]:
        total_height = PAUSE_MENU_BUTTON_HEIGHT * 3 + PAUSE_MENU_BUTTON_GAP * 2

        start_y = (screen_height - total_height) // 2 + PAUSE_MENU_START_Y_OFFSET
        button_x = (screen_width - PAUSE_MENU_BUTTON_WIDTH) // 2

        resume_rect = pygame.Rect(
            button_x, start_y, PAUSE_MENU_BUTTON_WIDTH, PAUSE_MENU_BUTTON_HEIGHT
        )

        reset_rect = pygame.Rect(
            button_x,
            start_y + PAUSE_MENU_BUTTON_HEIGHT + PAUSE_MENU_BUTTON_GAP,
            PAUSE_MENU_BUTTON_WIDTH,
            PAUSE_MENU_BUTTON_HEIGHT,
        )

        quit_rect = pygame.Rect(
            button_x,
            start_y + (PAUSE_MENU_BUTTON_HEIGHT + PAUSE_MENU_BUTTON_GAP) * 2,
            PAUSE_MENU_BUTTON_WIDTH,
            PAUSE_MENU_BUTTON_HEIGHT,
        )

        return resume_rect, reset_rect, quit_rect

    def get_start_interface_button_rects(
        self, screen_width: int, screen_height: int
    ) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect]:
        total_height = START_MENU_BUTTON_HEIGHT * 3 + START_MENU_BUTTON_GAP * 2

        start_y = screen_height - total_height - START_MENU_BUTTON_BOTTOM_MARGIN
        button_x = (screen_width - START_MENU_BUTTON_WIDTH) // 2

        start_rect = pygame.Rect(
            button_x, start_y, START_MENU_BUTTON_WIDTH, START_MENU_BUTTON_HEIGHT
        )

        rules_rect = pygame.Rect(
            button_x,
            start_y + START_MENU_BUTTON_HEIGHT + START_MENU_BUTTON_GAP,
            START_MENU_BUTTON_WIDTH,
            START_MENU_BUTTON_HEIGHT,
        )

        quit_rect = pygame.Rect(
            button_x,
            start_y + (START_MENU_BUTTON_HEIGHT + START_MENU_BUTTON_GAP) * 2,
            START_MENU_BUTTON_WIDTH,
            START_MENU_BUTTON_HEIGHT,
        )

        return start_rect, rules_rect, quit_rect

    def get_rules_interface_button_rects(
        self, screen_width: int, screen_height: int
    ) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect]:
        back_rect = pygame.Rect(
            RULES_BACK_BUTTON_X,
            RULES_BACK_BUTTON_Y,
            RULES_BACK_BUTTON_WIDTH,
            RULES_BACK_BUTTON_HEIGHT,
        )
        prev_rect = pygame.Rect(
            RULES_NAV_BUTTON_SIDE_MARGIN,
            screen_height - RULES_NAV_BUTTON_HEIGHT - RULES_NAV_BUTTON_BOTTOM_MARGIN,
            RULES_NAV_BUTTON_WIDTH,
            RULES_NAV_BUTTON_HEIGHT,
        )
        next_rect = pygame.Rect(
            screen_width - RULES_NAV_BUTTON_WIDTH - RULES_NAV_BUTTON_SIDE_MARGIN,
            screen_height - RULES_NAV_BUTTON_HEIGHT - RULES_NAV_BUTTON_BOTTOM_MARGIN,
            RULES_NAV_BUTTON_WIDTH,
            RULES_NAV_BUTTON_HEIGHT,
        )
        return back_rect, prev_rect, next_rect

    def get_rules_page_count(self) -> int:
        return RULES_PAGE_COUNT

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
        self.draw_controls_separator(screen)
        self.draw_item_intro(screen)
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
        shoot_text = self.small_font.render("F: Shoot Bullet", True, UI_TEXT_COLOUR)
        screen.blit(shoot_text, (control_x, control_y + 56))
        restart_text = self.small_font.render("R: Restart (Game Over)", True, UI_TEXT_COLOUR)
        screen.blit(restart_text, (control_x, control_y + 84))
    def draw_controls_separator(self, screen) -> None:
        line_x = UI_X + 255
        line_top = UI_Y + 145
        line_bottom = UI_Y + 270

        pygame.draw.line(
            screen, UI_BORDER_COLOUR, (line_x, line_top), (line_x, line_bottom), 2
        )

    def draw_item_intro(self, screen) -> None:
        icon_x = UI_X + 285
        text_x = icon_x + 42
        start_y = UI_Y + 145
        row_gap = 28

        items = [
            (self.letter_icon, " : Letter"),
            (self.wildcard_icon, " : Wildcard Letter"),
            (self.bullet_supply_icon, " : Bullet Supply"),
            (self.tail_cut_icon, " : Cut 1-3 tail letters"),
        ]

        for i, (icon, text) in enumerate(items):
            row_y = start_y + i * row_gap

            screen.blit(icon, (icon_x, row_y + 4))

            text_surface = self.small_font.render(text, True, UI_TEXT_COLOUR)
            screen.blit(text_surface, (text_x, row_y))

    def draw_lives(self, screen, lives: int) -> None:
        panel_x = UI_X + 30
        panel_y = UI_Y + 305

        screen.blit(self.life_panel_image, (panel_x, panel_y))

        lives_value = self.title_font.render(str(lives), True, UI_TEXT_COLOUR)
        screen.blit(lives_value, (panel_x + 140, panel_y + 23))

    def draw_bullets(self, screen, bullet_count: int) -> None:
        panel_x = UI_X + 310
        panel_y = UI_Y + 305

        screen.blit(self.bullet_panel_image, (panel_x, panel_y))

        bullet_value = self.title_font.render(
            str(bullet_count),
            True,
            UI_ACCENT_COLOUR,
        )
        screen.blit(bullet_value, (panel_x + 140, panel_y + 23))

    def draw_target_sequence(self, screen) -> None:
        target_text = self.font.render("TARGET", True, UI_ACCENT_COLOUR)
        screen.blit(target_text, (UI_X + 30, UI_Y + 430))

        target_value = self.font.render(TARGET_SEQUENCE, True, UI_TEXT_COLOUR)
        screen.blit(target_value, (UI_X + 30, UI_Y + 465))

    def draw_collected_letters(self, screen, collected_letters: list[str]) -> None:
        collected_text = self.font.render("COLLECTED", True, UI_ACCENT_COLOUR)
        screen.blit(collected_text, (UI_X + 30, UI_Y + 540))

        collected_value = self.font.render(
            "".join(collected_letters), True, UI_TEXT_COLOUR
        )
        screen.blit(collected_value, (UI_X + 30, UI_Y + 575))

    def draw_status_messages(self, screen) -> None:
        status_x = UI_X + 30
        status_y = UI_Y + 660

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

        # get button rects
        resume_rect, reset_rect, quit_rect = self.get_pause_menu_button_rects(
            screen_width, screen_height
        )

        # draw buttons
        screen.blit(self.pause_resume_button_image, resume_rect)
        screen.blit(self.pause_reset_button_image, reset_rect)
        screen.blit(self.pause_quit_button_image, quit_rect)

        # keyboard hints
        hint_y = quit_rect.bottom + PAUSE_MENU_HINT_OFFSET_Y

        hint_text = self.small_font.render(
            "ESC: Resume    R: Reset    Q: Quit",
            True,
            UI_TEXT_COLOUR,
        )
        hint_rect = hint_text.get_rect(center=(screen_width // 2, hint_y))
        screen.blit(hint_text, hint_rect)

    def draw_start_interface(self, screen) -> None:
        screen_width, screen_height = screen.get_size()

        screen.blit(self.start_interface_image, (0, 0))

        start_rect, rules_rect, quit_rect = self.get_start_interface_button_rects(
            screen_width,
            screen_height,
        )

        screen.blit(self.start_button_image, start_rect)
        screen.blit(self.rules_button_image, rules_rect)
        screen.blit(self.quit_button2_image, quit_rect)

    def draw_rules_interface(self, screen, rules_page_index: int) -> None:
        screen_width, screen_height = screen.get_size()

        # draw start interface as background
        screen.blit(self.start_interface_image, (0, 0))

        # dark overlay
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, RULES_OVERLAY_ALPHA))
        screen.blit(overlay, (0, 0))

        # buttons
        back_rect, prev_rect, next_rect = self.get_rules_interface_button_rects(
            screen_width, screen_height
        )

        screen.blit(self.back_button_image, back_rect)
        screen.blit(self.prev_button_image, prev_rect)
        screen.blit(self.next_button_image, next_rect)

        # index protection
        if rules_page_index < 0:
            rules_page_index = 0
        elif rules_page_index >= self.get_rules_page_count():
            rules_page_index = self.get_rules_page_count() - 1

        # draw different rules page by index
        if rules_page_index == 0:
            self.draw_rules_intro_page(screen)
        elif rules_page_index == 1:
            self.draw_rules_controls_items_page(screen)
        elif rules_page_index == 2:
            self.draw_rules_sequence_escape_page(screen)
        elif rules_page_index == 3:
            self.draw_rules_fight_survival_page(screen)

    # common func
    def draw_rules_page_title(self, screen, title: str) -> None:
        screen_width, screen_height = screen.get_size()

        title_text = self.title_font.render(title, True, UI_ACCENT_COLOUR)
        title_rect = title_text.get_rect(center=(screen_width // 2, RULES_TITLE_Y))
        screen.blit(title_text, title_rect)

    # page 1
    def draw_rules_intro_page(self, screen) -> None:
        screen_width, screen_height = screen.get_size()

        self.draw_rules_page_title(screen, "INTRODUCTION")

        story_lines = [
            "Python, a little snake, accidentally enters the COMP9001 maze.",
            "Collect letters and defeat guardian snakes.",
            "Complete the key sequence to open the escape portal.",
            "Enter the portal and escape from COMP9001!",
        ]

        for i, line in enumerate(story_lines):
            line_text = self.rules_intro_font.render(line, True, UI_TEXT_COLOUR)
            line_rect = line_text.get_rect(
                center=(
                    screen_width // 2,
                    RULES_STORY_START_Y + i * RULES_STORY_LINE_GAP,
                )
            )
            screen.blit(line_text, line_rect)

    # a helper to draw icons and descriptions
    def draw_rules_icon_item(self, screen, icon, title, lines, x, y) -> None:
        screen.blit(icon, (x, y))

        text_x = x + RULES_ITEM_TEXT_OFFSET_X

        title_surface = self.font.render(title, True, UI_ACCENT_COLOUR)
        screen.blit(title_surface, (text_x, y))

        for i, line in enumerate(lines):
            line_surface = self.small_font.render(line, True, UI_TEXT_COLOUR)
            screen.blit(
                line_surface,
                (
                    text_x,
                    y + RULES_ITEM_TITLE_LINE_GAP + i * RULES_ITEM_DESC_LINE_GAP,
                ),
            )

    # page 2
    def draw_rules_controls_items_page(self, screen) -> None:
        screen_width, screen_height = screen.get_size()

        title_text = self.title_font.render("CONTROLS & ITEMS", True, UI_ACCENT_COLOUR)
        title_rect = title_text.get_rect(center=(screen_width // 2, RULES_TITLE_Y))
        screen.blit(title_text, title_rect)

        self.draw_rules_icon_item(
            screen,
            self.rules_bullet_icon,
            "Controls",
            [
                "Arrow Keys: Move Python.",
                "F: Shoot a bullet.",
                "ESC: Open the pause menu.",
            ],
            RULES_ITEM_LEFT_X,
            RULES_ITEM_START_Y,
        )

        self.draw_rules_icon_item(
            screen,
            self.rules_letter_icon,
            "Letter",
            [
                "Collect letters in the correct order.",
                "Eating one grows Python by 1 segment.",
            ],
            RULES_ITEM_RIGHT_X,
            RULES_ITEM_START_Y,
        )

        self.draw_rules_icon_item(
            screen,
            self.rules_wildcard_icon,
            "Wildcard Letter",
            [
                "Becomes the next required letter.",
            ],
            RULES_ITEM_LEFT_X,
            RULES_ITEM_START_Y + RULES_ITEM_ROW_GAP,
        )

        self.draw_rules_icon_item(
            screen,
            self.rules_bullet_supply_icon,
            "Bullet Supply",
            [
                "Adds extra bullets.",
                "Respawns over time.",
            ],
            RULES_ITEM_RIGHT_X,
            RULES_ITEM_START_Y + RULES_ITEM_ROW_GAP,
        )

        self.draw_rules_icon_item(
            screen,
            self.rules_tail_cut_icon,
            "TailCut",
            [
                "Removes 1-3 collected letters.",
                "Also cuts Python's tail.",
            ],
            RULES_ITEM_LEFT_X,
            RULES_ITEM_START_Y + RULES_ITEM_ROW_GAP * 2,
        )

    # page 3
    def draw_rules_sequence_escape_page(self, screen) -> None:
        screen_width, screen_height = screen.get_size()

        title_text = self.title_font.render("SEQUENCE & ESCAPE", True, UI_ACCENT_COLOUR)
        title_rect = title_text.get_rect(center=(screen_width // 2, RULES_TITLE_Y))
        screen.blit(title_text, title_rect)

        image_y = RULES_PAGE_IMAGE_TOP_Y

        x1 = RULES_PAGE_THREE_COL_LEFT_X
        x2 = RULES_PAGE_THREE_COL_MIDDLE_X
        x3 = RULES_PAGE_THREE_COL_RIGHT_X

        screen.blit(self.rules_eat_letter_image, (x1, image_y))
        screen.blit(self.rules_target_image, (x2, image_y))
        screen.blit(self.rules_exit_portal_image, (x3, image_y))

        title_1 = self.font.render("Collect letters", True, UI_ACCENT_COLOUR)
        screen.blit(title_1, (x1, image_y + RULES_IMAGE_TITLE_OFFSET_Y))

        desc_1 = [
            "Collect a letter",
            "Python grows by 1 segment.",
        ]

        title_2 = self.font.render("Target Sequence", True, UI_ACCENT_COLOUR)
        screen.blit(title_2, (x2, image_y + RULES_IMAGE_TITLE_OFFSET_Y))

        desc_2 = [
            "Try to collect letters in order",
            "to match the target sequence",
        ]

        title_3 = self.font.render("Escape Portal", True, UI_ACCENT_COLOUR)
        screen.blit(title_3, (x3, image_y + RULES_IMAGE_TITLE_OFFSET_Y))

        desc_3 = [
            "Complete the sequence.",
            "Enter the portal to win.",
        ]

        for i, line in enumerate(desc_1):
            text = self.small_font.render(line, True, UI_TEXT_COLOUR)
            screen.blit(
                text,
                (
                    x1,
                    image_y + RULES_IMAGE_DESC_OFFSET_Y + i * RULES_IMAGE_DESC_LINE_GAP,
                ),
            )

        for i, line in enumerate(desc_2):
            text = self.small_font.render(line, True, UI_TEXT_COLOUR)
            screen.blit(
                text,
                (
                    x2,
                    image_y + RULES_IMAGE_DESC_OFFSET_Y + i * RULES_IMAGE_DESC_LINE_GAP,
                ),
            )

        for i, line in enumerate(desc_3):
            text = self.small_font.render(line, True, UI_TEXT_COLOUR)
            screen.blit(
                text,
                (
                    x3,
                    image_y + RULES_IMAGE_DESC_OFFSET_Y + i * RULES_IMAGE_DESC_LINE_GAP,
                ),
            )

    # page 4
    def draw_rules_fight_survival_page(self, screen) -> None:
        screen_width, screen_height = screen.get_size()

        title_text = self.title_font.render("FIGHT & SURVIVAL", True, UI_ACCENT_COLOUR)
        title_rect = title_text.get_rect(center=(screen_width // 2, RULES_TITLE_Y))
        screen.blit(title_text, title_rect)

        left_x = RULES_PAGE_TWO_COL_LEFT_X
        right_x = RULES_PAGE_TWO_COL_RIGHT_X
        image_y = RULES_PAGE_IMAGE_TOP_Y

        screen.blit(self.rules_bullet_enemy_image, (left_x, image_y))
        screen.blit(self.rules_bullet_enemy_2_image, (right_x, image_y))

        left_title = self.font.render("Hit Head / 1st Body", True, UI_ACCENT_COLOUR)
        screen.blit(left_title, (left_x, image_y + RULES_IMAGE_TITLE_OFFSET_Y))

        left_desc = self.small_font.render(
            "Defeat the guardian snake.",
            True,
            UI_TEXT_COLOUR,
        )
        screen.blit(left_desc, (left_x, image_y + RULES_IMAGE_DESC_OFFSET_Y))

        right_title = self.font.render("Hit Other Body Parts", True, UI_ACCENT_COLOUR)
        screen.blit(right_title, (right_x, image_y + RULES_IMAGE_TITLE_OFFSET_Y))

        right_desc = self.small_font.render(
            "Cut from the hit point to the tail.",
            True,
            UI_TEXT_COLOUR,
        )
        screen.blit(right_desc, (right_x, image_y + RULES_IMAGE_DESC_OFFSET_Y))

        info_y = RULES_BOTTOM_INFO_Y

        screen.blit(self.rules_bullet_icon, (left_x, info_y))
        bullet_text_1 = self.small_font.render(
            "Bullets can destroy letters, items, and guardian snakes.",
            True,
            UI_TEXT_COLOUR,
        )
        screen.blit(bullet_text_1, (left_x + 80, info_y + 10))

        screen.blit(self.rules_heart_icon, (left_x, info_y + 80))
        heart_text_1 = self.small_font.render(
            "Python loses 1 life when hitting walls, itself, or enemies.",
            True,
            UI_TEXT_COLOUR,
        )
        screen.blit(heart_text_1, (left_x + 80, info_y + 90))
        

        screen.blit(self.rules_quantum_teleport_icon, (left_x, info_y + 160))
        teleport_text = self.small_font.render(
            "Quantum Teleport: pass through one edge and reappear from the opposite side.",
            True,
            UI_TEXT_COLOUR,
        )
        screen.blit(teleport_text, (left_x + 80, info_y + 170))