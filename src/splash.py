# File: splash.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 26 Nov 2023
# Purpose:
#   A file for the splash screen and related functions.
# Notes:

from time import perf_counter

import pygame as pg
from game_classes import AssetManager


# Precond:
#   length is the length of time to display the splash screen in seconds.
#
# Postcond:
#   Displays the splash screen.
def splash_screen(length: float):
    """A function for displaying the Masteroid splash screen."""
    sacgs_length = length/3
    pygame_length = length/3
    masteroids_length = length/3
    screen = pg.display.get_surface()
    running = True
    announcement_font = AssetManager.get_instance().get_font("large")
    announcement_font.set_bold(True)
    subtitle_font = AssetManager.get_instance().get_font("small")

    
    # SAGS labels
    from_label = subtitle_font.render("A game from:", True, (255, 255, 255))
    sacgs_label = announcement_font.render("SAC Game Studios", True, (255, 255, 255))
    sacgs_anchor = (screen.get_width()-sacgs_label.get_width())//2, (screen.get_height()-sacgs_label.get_height())//2
    from_anchor = sacgs_anchor[0], sacgs_anchor[1] - from_label.get_height()
    
    # Pygame labels
    with_label = subtitle_font.render("Made with:", True, (255, 255, 255))
    pygame_label = announcement_font.render("Pygame", True, (255, 255, 255))
    pygame_anchor = (screen.get_width()-pygame_label.get_width())//2, (screen.get_height()-pygame_label.get_height())//2
    with_anchor = pygame_anchor[0], pygame_anchor[1] - with_label.get_height()
    
    # Masteroids Label
    masteroid_label = announcement_font.render("MASTEROIDS", True, (200, 0, 0))
    masteroid_anchor = (screen.get_width()-masteroid_label.get_width())//2, (screen.get_height()-masteroid_label.get_height())//2
    
    frame_delta = 1 / 24
    frame_timer = perf_counter()
    while running:
        delta = perf_counter() - frame_timer
        if delta >= frame_delta:
            if sacgs_length < 0:
                if pygame_length < 0:
                    if masteroids_length < 0:
                        running = False
                    else:
                        masteroids_length -= delta
                else:
                    pygame_length -= delta
            else:
                sacgs_length -= delta
            length -= delta
            frame_timer = perf_counter()
            # Process Frame
            screen.fill((0, 0, 0))
            if sacgs_length < 0:
                if pygame_length < 0:
                    screen.blit(masteroid_label, masteroid_anchor)
                else:
                    screen.blit(with_label, with_anchor)
                    screen.blit(pygame_label, pygame_anchor)
            else:
                screen.blit(from_label, from_anchor)
                screen.blit(sacgs_label, sacgs_anchor)
            pg.display.flip()
            # Process Events
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
            if length <= 0:
                running = False
