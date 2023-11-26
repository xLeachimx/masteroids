# File: menu.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 26 Nov 2023
# Purpose:
#   A file for the menu screen and related functions.
# Notes:
#   Returns a value ot indicate which option has been selected:
#      -1: No selection/Quit
#       0: Start

import pygame as pg
from time import perf_counter
from game_classes import Button, Vector2D


def menu():
    """A function for displaying the Masteroid menu screen."""
    screen = pg.display.get_surface()
    screen_dim = screen.get_size()
    running = True
    announcement_font = pg.font.SysFont("consolas", 48, bold=True)
    masteroid_label = announcement_font.render("MASTEROIDS", True, (200, 0, 0))
    masteroid_anchor = (screen_dim[0] - masteroid_label.get_width())//2, screen_dim[1]//4 - masteroid_label.get_height()//2
    
    # Create buttons
    start_btn = Button("START", Vector2D(0, 0), (255, 255, 255))
    quit_btn = Button("QUIT", Vector2D(0, 0), (255, 255, 255))
    vert_padding = 10
    start_vert = masteroid_anchor[0] + masteroid_label.get_height() + vert_padding
    quit_vert = start_vert + start_btn.get_dim()[1] + vert_padding

    # Update accounting
    frame_delta = 1 / 24
    frame_timer = perf_counter()
    selection = -1
    while running:
        delta = perf_counter() - frame_timer
        if delta >= frame_delta:
            frame_timer = perf_counter()
            # Process Frame
            screen.fill((0, 0, 0))
            screen.blit(masteroid_label, masteroid_anchor)
            start_btn.place_horizontal_center(screen, start_vert)
            quit_btn.place_horizontal_center(screen, quit_vert)
            pg.display.flip()
            # Process Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if start_btn.check_click(event.pos):
                        selection = 0
                        running = False
                    elif quit_btn.check_click(event.pos):
                        selection = -1
                        running = False
    return selection
                
    