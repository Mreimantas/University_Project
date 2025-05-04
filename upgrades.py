import pygame

class UpgradesMenu:


    def __init__(self, settings, screen, state_name):
        self.settings = settings
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 50)
        self.state_name = state_name
        self.buttons = []
        self.mouse_held = False
        self.upgrade_prices = {
            "Health": 50,
            "Speed": 50,
            "Armor": 50,
            "Weapon": 50
        }


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.buttons.clear()

        screen_width, screen_height = self.screen.get_size()

        souls_text = self.font.render(f"Souls: {self.settings.souls}", True, (255, 255, 255))
        self.screen.blit(souls_text, (10, 10))

        for i, option in enumerate(self.upgrade_prices):
            required_souls = self.upgrade_prices[option]
            upgrade_status = self.settings.upgrades[option]
            text_surface = self.font.render(f"{option} - {required_souls} Souls", True, (255, 255, 255))
            rect = text_surface.get_rect(center=(screen_width // 2, 200 + i * 100))
            self.screen.blit(text_surface, rect)

            self.draw_progression(option, 3, rect.x + 250, rect.y)

            self.buttons.append((rect, option))

        back_text = self.font.render("Back", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=(screen_width // 2, screen_height - 100))
        self.screen.blit(back_text, back_rect)
        self.buttons.append((back_rect, "Back"))

        pygame.display.flip()


    def draw_progression(self, option, max_level, x, y):
        for i in range(max_level):
            color = (0, 255, 0) if i < self.settings.upgrades[option] else (255, 255, 255)
            pygame.draw.rect(self.screen, color, (x + i * 40, y, 30, 30))


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
        if option == "Back":
            self.settings.game_state = "menu"
        else:
            self.attempt_upgrade(option)


    def attempt_upgrade(self, option):
        required_souls = self.upgrade_prices[option]
        if self.settings.souls >= required_souls and self.settings.upgrades[option] < 3:
            self.settings.souls -= required_souls
            self.settings.upgrades[option] += 1
            self.settings.save()


    def run(self):
        clock = pygame.time.Clock()
        while self.settings.game_state == self.state_name:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.settings.game_state = "quit"

            self.handle_mouse_input()
            self.draw()
            clock.tick(60)
