import os
import sys
import pygame

# Set working directory
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
sys.path.append(current_dir)

from settings import GameSettings
from menu import Menu
from game import Game

pygame.init()

settings = GameSettings()
settings.load()
screen = settings.apply_display_mode()
pygame.display.set_caption("Roguelike Souls Game")

main_menu = Menu(settings, screen, ["Start", "Settings", "Upgrades", "Quit"], "menu")
settings_menu = Menu(settings, screen, ["Fullscreen", "Back"], "settings")
upgrades_menu = Menu(settings, screen, ["Health", "Speed", "Armor", "Weapon", "Back"], "upgrades")
game = Game(settings, screen)

def main():
    while settings.game_state != "quit":
        if settings.game_state == "menu": 
            main_menu.run()
            if settings.game_state == "game":
                game.reset() 
        elif settings.game_state == "settings":
            settings_menu.run()
        elif settings.game_state == "upgrades":
            upgrades_menu.run()
        elif settings.game_state == "game":
            game.run()

    settings.save()
    pygame.quit()

if __name__ == "__main__":
    main()