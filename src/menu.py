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
#       1: Instructions
#       2: Leaderboard

import pygame as pg
from time import perf_counter
from game_classes import Button, AssetManager, GameConfig


def pointer_points(btn: Button, width: int, height: int, padding: int):
    pointer_anchor = list(btn.get_anchor())
    pointer_anchor[0] -= width + padding
    pointer_anchor[1] += (btn.get_dim()[1] - height)//2
    p1 = pointer_anchor
    p2 = pointer_anchor[0] + width, pointer_anchor[1] + height//2
    p3 = pointer_anchor[0], pointer_anchor[1] + height
    return [p1, p2, p3]

def menu():
    """A function for displaying the Masteroid menu screen."""
    screen = pg.display.get_surface()
    screen_dim = screen.get_size()
    running = True
    announcement_font = AssetManager.get_instance().get_font("large")
    announcement_font.set_bold(True)
    masteroid_label = announcement_font.render("MASTEROIDS", True, (200, 0, 0))
    masteroid_anchor = (screen_dim[0] - masteroid_label.get_width())//2, screen_dim[1]//4 - masteroid_label.get_height()//2
    
    # Create buttons
    start_btn = Button("START", None, (255, 255, 255))
    instr_btn = Button("INSTRUCTIONS", None, (255, 255, 255))
    leader_btn = Button("LEADERBOARD", None, (255, 255, 255))
    quit_btn = Button("QUIT", None, (255, 255, 255))
    vert_padding = 10
    start_vert = masteroid_anchor[0] + masteroid_label.get_height() + vert_padding
    instr_vert = start_vert + start_btn.get_dim()[1] + vert_padding
    leader_vert = instr_vert + instr_btn.get_dim()[1] + vert_padding
    quit_vert = leader_vert + leader_btn.get_dim()[1] + vert_padding
    
    # Selector for when gamepad is used.
    selector = 0
    selector_width = 5
    buttons = [(start_btn, start_vert), (instr_btn, instr_vert), (leader_btn, leader_vert), (quit_btn, quit_vert)]

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
            instr_btn.place_horizontal_center(screen, instr_vert)
            leader_btn.place_horizontal_center(screen, leader_vert)
            quit_btn.place_horizontal_center(screen, quit_vert)
            if GameConfig.get_setting("controller") == "GAMEPAD":
                pts = pointer_points(buttons[selector][0], 10, 15, 5)
                pg.draw.polygon(screen, (0, 0, 255), pts)
            pg.display.flip()
            # Process Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if GameConfig.get_setting("controller") == "KEYBOARD":
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        running = False
                        if start_btn.check_click(event.pos):
                            selection = 0
                        elif instr_btn.check_click(event.pos):
                            selection = 1
                        elif leader_btn.check_click(event.pos):
                            selection = 2
                        elif quit_btn.check_click(event.pos):
                            selection = -1
                        else:
                            running = True
                elif GameConfig.get_setting("controller") == "GAMEPAD":
                    if event.type == pg.JOYBUTTONDOWN and event.button == GameConfig.get_setting("A"):
                        running = False
                        if selector == len(buttons)-1:
                            selection = -1
                        else:
                            selection = selector
                    elif event.type == pg.JOYAXISMOTION:
                        if event.axis == GameConfig.get_setting("Y-axis"):
                            if round(event.value) == -1:
                                selector -= 1
                            elif round(event.value) == 1:
                                selector += 1
                            selector = selector % len(buttons)
                                
    return selection
                
    