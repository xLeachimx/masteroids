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
    board.write_out()
    return 0


def leaderboard_add(score: int):
    """A function for adding an entry to the leaderboard screen."""
    screen = pg.display.get_surface()
    screen_dim = screen.get_size()
    running = True
    name = "AAA"
    char_index = 0
    blink_freq = 0.25
    blink_timer = blink_freq
    blink = False
    font = pg.font.SysFont("consolas", 28)
    dir_font = pg.font.SysFont("consolas", 14)
    dir_text = dir_font.render("Press Enter When Done", True, (255, 255, 255))
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
            # Render text with blinking
            temp_text = name
            blink_timer -= delta
            if blink_timer <= 0:
                blink = not blink
                blink_timer = blink_freq
            if blink:
                temp_text = temp_text[:char_index] + "_" + temp_text[char_index+1:]
            text = (" "*5).join([temp_text, f"{score:09}"])
            text_render = font.render(text, True, (255, 255, 255))
            text_anchor = (screen_dim[0] - text_render.get_width())//2, (screen_dim[1] - text_render.get_height())//2
            dir_anchor = text_anchor[0], text_anchor[1] + text_render.get_height() + 10
            screen.blit(text_render, text_anchor)
            screen.blit(dir_text, dir_anchor)
            pg.display.flip()
            # Process Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    return -1
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                    elif event.key == pg.K_RETURN:
                        board.add_leader(name, score)
                        running = False
                    elif event.key in [pg.K_LEFT, pg.K_a]:
                        char_index -= 1
                        char_index = char_index % 3
                    elif event.key in [pg.K_RIGHT, pg.K_d]:
                        char_index += 1
                        char_index = char_index % 3
                    elif event.key in [pg.K_UP, pg.K_w]:
                        next_char = chr(ord(name[char_index])+1)
                        if ord(next_char) > ord("Z"):
                            next_char = "A"
                        name = name[:char_index] + next_char + name[char_index+1:]
                    elif event.key in [pg.K_DOWN, pg.K_s]:
                        next_char = chr(ord(name[char_index])-1)
                        if ord(next_char) < ord("A"):
                            next_char = "Z"
                        name = name[:char_index] + next_char + name[char_index+1:]
    board.write_out()
    return 0