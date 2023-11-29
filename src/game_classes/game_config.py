# File: game_config.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 29 Nov 2023
# Purpose:
#   A singleton clss for handling game configuration.
# Notes:

import pygame as pg


class GameConfig:
    __INSTANCE = None
    
    @staticmethod
    def get_instance():
        if GameConfig.__INSTANCE is None:
            GameConfig.__INSTANCE = GameConfig()
        return GameConfig.__INSTANCE
    
    @staticmethod
    def destroy():
        del GameConfig.__INSTANCE
        GameConfig.__INSTANCE = None
    
    def __init__(self):
        """Setups the GameConfig object"""
        self.config = {'controller': "KEYBOARD"}
        self.__detect_SNES_gamepad()
        
    def register_setting(self, name, value):
        self.config[name] = value
        
    def get_setting(self, name, value):
        return self.config[name] if name in self.config else None
    
    def __detect_SNES_gamepad(self):
        """Checks for and registers a Vilros USB SNES gamepad in the configuration."""
        if not pg.joystick.get_init():
            pg.joystick.init()
        if pg.joystick.get_count() == 0:
            return
        for i in range(pg.joystick.get_count()):
            stick = pg.joystick.Joystick(i)
            stick.init()
            if stick.get_name() == 'USB Gamepad':
                self.config['controller'] = "GAMEPAD"
                self.config['gamepad'] = stick
                break
            stick.quit()
