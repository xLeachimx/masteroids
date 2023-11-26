# File: board.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 26 Nov 2023
# Purpose:
#   A file for the leaderboard screen and related functions.
# Notes:

import pygame as pg
from game_classes import Button, Leaderboard
from time import perf_counter


def leaderboard():
    """A function for displaying the Masteroid leaderboard screen."""
    screen = pg.display.get_surface()
    screen_dim = screen.get_size()
    running = True
    back_btn = Button("Back", None, (255, 0, 0))
    back_anchor = screen.get_width() - back_btn.get_dim()[0], screen.get_height() - back_btn.get_dim()[1]
    board = Leaderboard("leader.board")

    # Update accounting
    frame_delta = 1 / 24
    frame_timer = perf_counter()
    while running:
        delta = perf_counter() - frame_timer
        if delta >= frame_delta:
            frame_timer = perf_counter()
            # Process Frame
            screen.fill((0, 0, 0))
            leader_render = board.render()
            leader_anchor = (screen_dim[0] - leader_render.get_width())//2, (screen_dim[1] - leader_render.get_height())//2
            screen.blit(leader_render, leader_anchor)
            back_btn.place(screen, back_anchor)
            pg.display.flip()
            # Process Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    return -1
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if back_btn.check_click(event.pos):
                        running = False
    return 0
