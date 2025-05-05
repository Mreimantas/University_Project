import pygame
import json
import os
import sys

class GameSettings:


    def __init__(self):
        self.__game_state = "menu"
        self.screen_width = 1280
        self.screen_height = 720
        self.is_fullscreen = False
        self.player_health = 100
        self.player_speed = 5
        self.player_armor = 0
        self.player_weapon = 0
        self.souls = 0
        self.upgrades = [0, 0, 0, 0]


    @property
    def game_state(self):
        return self.__game_state


    @game_state.setter
    def game_state(self, value):
        if value in ["menu", "game", "settings", "upgrades", "quit"]:
            self.__game_state = value
        else:
            raise ValueError(f"Invalid game state: {value}")


    def reset(self):
        self.player_health = 100 + self.upgrades[0] * 20 
        self.player_speed = 3 + self.upgrades[1] * 1     
        self.player_armor = self.upgrades[2] * 2 
        self.player_weapon = self.upgrades[3] 

    

    def get_settings_file_path(self):
        if getattr(sys, 'frozen', False):
            # Path to the executable if frozen
            base_path = os.path.dirname(sys.executable)
        else:
            # Path to the script if running normally
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, 'settings.json')

    def save(self):
        settings_file = self.get_settings_file_path()
        with open(settings_file, 'w') as f:
            json.dump({
                "screen_width": self.screen_width,
                "screen_height": self.screen_height,
                "is_fullscreen": self.is_fullscreen,
                "player_weapon": self.player_weapon,
                "souls": self.souls, 
                "upgrades": self.upgrades
            }, f)

    def load(self):
        settings_file = self.get_settings_file_path()
        try:
            with open(settings_file, 'r') as f:
                data = json.load(f)
                self.screen_width = data.get('screen_width', 1280)
                self.screen_height = data.get('screen_height', 720)
                self.is_fullscreen = data.get('is_fullscreen', False)
                self.player_weapon = data.get('player_weapon', 0)
                self.souls = data.get('souls', 0) 
                self.upgrades = data.get('upgrades', [0, 0, 0, 0])
        except FileNotFoundError:
            self.save()


    def apply_display_mode(self):
        flags = pygame.SCALED
        if self.is_fullscreen:
            flags |= pygame.FULLSCREEN
        return pygame.display.set_mode((1280, 720), flags)
