# File: main.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 23 Nov 2023
# Purpose:
#   Primary entry point and overarching game loop file.
# Notes:

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame as pg
from random import seed
from splash import splash_screen
from game import game
from menu import menu
from instr import instr
from board import leaderboard, leaderboard_add
from game_classes import Leaderboard, AssetManager, GameConfig


def create_icon():
    ico = pg.Surface((32, 32))
    ico.fill((0, 0, 0))
    pts = [(3, 28), (14, 3), (16, 3), (28, 28)]
    pg.draw.polygon(ico, (255, 255, 255), pts)
    return ico


def main():
    seed(42)
    # Setup pygame
    pg.init()
    screen_dim = (500, 500)
    screen = pg.display.set_mode(screen_dim)
    pg.display.set_caption("Masteroids", "Masteroids")
    pg.display.set_icon(create_icon())
    
    # Setup config
    GameConfig.register_setting("screen_dim", screen_dim)
    
    
    # Setup assets
    AssetManager.get_instance().register_sound("shooting", "assets/sfx/laser_shot.wav")
    AssetManager.get_instance().register_music("background", "assets/music/space_dust.mp3")
    AssetManager.get_instance().register_font("large", pg.font.Font("assets/fonts/Consolas.ttf", 48))
    AssetManager.get_instance().register_font("medium", pg.font.Font("assets/fonts/Consolas.ttf", 24))
    AssetManager.get_instance().register_font("small", pg.font.Font("assets/fonts/Consolas.ttf", 18))

    splash_screen(9)
    menu_selection = menu()
    while menu_selection != -1:
        if menu_selection == 0:
            score = game()
            board = Leaderboard("leader.board")
            if score == -1:
                break
            elif board.check_score(score):
                res = leaderboard_add(score)
                if res == -1:
                    break
        elif menu_selection == 1:
            res = instr()
            if res == -1:
                break
        elif menu_selection == 2:
            res = leaderboard()
            if res == -1:
                break
        menu_selection = menu()
    
    pg.quit()


if __name__ == '__main__':
    main()
