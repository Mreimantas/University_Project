import pygame

class Menu:


    def __init__(self, settings, screen, options, state_name):
        self.settings = settings
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 50)
        self.options = options
        self.state_name = state_name
        self.buttons = []
        self.mouse_held = False


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.buttons.clear()

        screen_width, screen_height = self.screen.get_size()

        if self.state_name == "menu":
            self.draw_main_menu(screen_width, screen_height)
        elif self.state_name == "upgrades":
            self.draw_upgrades_menu(screen_width, screen_height)
        elif self.state_name == "settings":
            self.draw_settings_menu(screen_width, screen_height)

        pygame.display.flip()


    def draw_main_menu(self, screen_width, screen_height):
        for i, option in enumerate(["Start", "Settings", "Upgrades", "Quit"]):
            text_surface = self.font.render(option, True, (255, 255, 255))
            rect = text_surface.get_rect(center=(screen_width // 2, 200 + i * 100))
            self.screen.blit(text_surface, rect)
            self.buttons.append((rect, option))

        souls_text = self.font.render(f'Souls: {self.settings.souls}', True, (255, 255, 255))
        self.screen.blit(souls_text, (10, 10))


    def draw_upgrades_menu(self, screen_width, screen_height):
        souls_text = self.font.render(f'Souls: {self.settings.souls}', True, (255, 255, 255))
        self.screen.blit(souls_text, (10, 10))

        upgrade_names = ["Health", "Speed", "Armor", "Weapon"]
        upgrade_costs = [50, 30, 40, 100]

        for i, option in enumerate(upgrade_names):
            # Upgrade name
            text_surface = self.font.render(option, True, (255, 255, 255))
            rect = text_surface.get_rect(center=(screen_width // 2, 150 + i * 120))
            self.screen.blit(text_surface, rect)
            self.buttons.append((rect, option))

            # Cost
            cost_text = self.font.render(f'Cost: {upgrade_costs[i]}', True, (200, 200, 200))
            cost_rect = cost_text.get_rect(center=(screen_width // 4, 150 + i * 120))
            self.screen.blit(cost_text, cost_rect)

            # Progression squares
            self.draw_upgrade_progression(i, screen_width // 1.5, 150 + i * 120)

        # Back button
        back_text = self.font.render("Back", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=(screen_width // 2, screen_height - 100))
        self.screen.blit(back_text, back_rect)
        self.buttons.append((back_rect, "Back"))


    def draw_settings_menu(self, screen_width, screen_height):
        for i, option in enumerate(["Fullscreen", "Back"]):
            text_surface = self.font.render(option, True, (255, 255, 255))
            rect = text_surface.get_rect(center=(screen_width // 2, 200 + i * 100))
            self.screen.blit(text_surface, rect)
            self.buttons.append((rect, option))


    def draw_upgrade_progression(self, upgrade_index, x_position, y_position):
        for j in range(3):
            color = (0, 255, 0) if self.settings.upgrades[upgrade_index] > j else (100, 100, 100)
            pygame.draw.rect(self.screen, color, (x_position + j * 40, y_position - 15, 30, 30))


    def handle_mouse_input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if not self.mouse_held and mouse_click[0]:
            for rect, option in self.buttons:
                if rect.collidepoint(mouse_pos):
                    self.process_option(option)
                    break
            self.mouse_held = True

        if not mouse_click[0]:
            self.mouse_held = False


    def process_option(self, option):
        if option == "Start":
            self.settings.game_state = "game"
        elif option == "Settings":
            self.settings.game_state = "settings"
        elif option == "Upgrades":
            self.settings.game_state = "upgrades"
        elif option == "Quit":
            self.settings.game_state = "quit"
        elif option == "Back":
            self.settings.game_state = "menu"
        elif option == "Fullscreen":
            self.settings.is_fullscreen = not self.settings.is_fullscreen
            self.screen = self.settings.apply_display_mode()
        elif option in ["Health", "Speed", "Armor", "Weapon"]:
            self.buy_upgrade(option)


    def buy_upgrade(self, upgrade_type):
        upgrade_index = ["Health", "Speed", "Armor", "Weapon"].index(upgrade_type)
        upgrade_costs = [50, 30, 40, 100]

        if self.settings.souls >= upgrade_costs[upgrade_index] and self.settings.upgrades[upgrade_index] < 3:
            self.settings.souls -= upgrade_costs[upgrade_index]
            self.settings.upgrades[upgrade_index] += 1


    def run(self):
        clock = pygame.time.Clock()
        while self.settings.game_state == self.state_name:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.settings.game_state = "quit"
            self.handle_mouse_input()
            self.draw()
            clock.tick(60)
