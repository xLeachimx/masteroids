# File: main.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 23 Nov 2023
# Purpose:
#   Primary entry point and overarching game loop file.
# Notes:

import pygame as pg
from time import perf_counter
from game_classes import Player, Vector2D, Asteroid, Pellet, Level
from random import seed
from math import radians

def main():
    # Setup pygame
    pg.init()
    screen_dim = (500, 500)
    screen = pg.display.set_mode(screen_dim)
    frame_delta = 1/24
    frame_timer = perf_counter()
    running = True
    
    # Setup GameObjects
    player = Player(Vector2D(250, 250))
    level = Level(player, screen_dim, 0, 0, 1)
    player.set_active(True)
    player.set_visible(True)
    
    # Main game loop
    while running:
        delta = perf_counter() - frame_timer
        if delta >= frame_delta:
            frame_timer = perf_counter()
            # Process Frame
            screen.fill((0, 0, 0))
            level.run_frame(screen, delta)
            pg.display.flip()
            # Process Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False


if __name__ == '__main__':
    main()
