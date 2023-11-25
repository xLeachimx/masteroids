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
from game_classes import Player, Vector2D, Asteroid, Pellet
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
    asteroid = Asteroid(Asteroid.LARGE, Vector2D(300, 300))
    pellets = []
    
    player.set_active(True)
    asteroid.set_active(True)
    player.set_visible(True)
    asteroid.set_visible(True)
    
    # Main game loop
    while running:
        delta = perf_counter() - frame_timer
        if delta >= frame_delta:
            frame_timer = perf_counter()
            # Process Frame
            screen.fill((0, 0, 0))
            player.update(delta)
            asteroid.update(delta)
            for pellet in pellets:
                pellet.update(delta)
            player.draw(screen)
            asteroid.draw(screen)
            for pellet in pellets:
                pellet.draw(screen)
            pg.display.flip()
            # Process Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_f:
                        player.halt_ship()
            # Process Key Input
            # Rotational input
            if pg.key.get_pressed()[pg.K_a]:
                player.rotate_ccw(delta)
            elif pg.key.get_pressed()[pg.K_d]:
                player.rotate_cw(delta)
            # Throttle input
            if pg.key.get_pressed()[pg.K_w]:
                player.throttle_up(delta)
            elif pg.key.get_pressed()[pg.K_s]:
                player.throttle_down(delta)
            # Trigger input
            if pg.key.get_pressed()[pg.K_SPACE]:
                pellets.append(player.fire())
            # Process OoB behavior
            if not player.in_bounds(screen_dim):
                player.clamp(screen_dim)
            if not asteroid.in_bounds(screen_dim):
                asteroid.bounce(screen_dim)
            pellet_gc = []
            for i in range(len(pellets)):
                if not pellets[i].in_bounds(screen_dim):
                    pellet_gc.append(i)
            for i in pellet_gc[::-1]:
                pellets.pop(i)


if __name__ == '__main__':
    main()
