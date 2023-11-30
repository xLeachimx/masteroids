# File: game_config.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 29 Nov 2023
# Purpose:
#   A singleton clss for handling game configuration.
# Notes:
#   Gamepad Buttons:
#       0) X
#       1) A
#       2) B
#       3) Y
#       4) L
#       5) R
#       6)
#       7)
#       8) Select
#       9) Start

import pygame as pg


class GameConfig:
    """Singleton class for holding configuration information"""
    __config = None
    
    @staticmethod
    def create():
        GameConfig.__config = {'controller': "KEYBOARD"}
        GameConfig.__detect_snes_gamepad()
        
    @staticmethod
    def register_setting(name, value):
        if GameConfig.__config is None:
            GameConfig.create()
        GameConfig.__config[name] = value
        
    @staticmethod
    def get_setting(name):
        if GameConfig.__config is None:
            GameConfig.create()
        return GameConfig.__config[name] if name in GameConfig.__config else None
    
    @staticmethod
    def __detect_snes_gamepad():
        """Checks for and registers a Vilros USB SNES gamepad in the configuration."""
        if not pg.joystick.get_init():
            pg.joystick.init()
        if pg.joystick.get_count() == 0:
            return
        for i in range(pg.joystick.get_count()):
            stick = pg.joystick.Joystick(i)
            stick.init()
            if stick.get_name() == 'USB Gamepad':
                GameConfig.__config['controller'] = "GAMEPAD"
                GameConfig.__config['gamepad'] = stick
                GameConfig.__config['X'] = 0
                GameConfig.__config['A'] = 1
                GameConfig.__config['B'] = 2
                GameConfig.__config['Y'] = 3
                GameConfig.__config['L'] = 4
                GameConfig.__config['R'] = 5
                GameConfig.__config['SELECT'] = 8
                GameConfig.__config['START'] = 9
                GameConfig.__config['X-axis'] = 0
                GameConfig.__config['Y-axis'] = 4
                break
            stick.quit()
