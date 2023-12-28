# File: instr.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 26 Nov 2023
# Purpose:
#   A file for the instruction screen and related functions.
# Notes:

from time import perf_counter
from game_classes import TextBox, Button, GameConfig
import pygame as pg

def instr():
    """A function for displaying the Masteroid instruction screen."""
    screen = pg.display.get_surface()
    screen_dim = screen.get_size()
    running = True
    controls = ""
    if GameConfig.get_setting("controller") == "KEYBOARD":
        controls = """Controls
        
        W     Accelerate the ship forward.
        
        A     Rotate the ship counterclockwise.
        
        S     Accelerate the ship backward.
        
        D     Rotate the ship clockwise.
        
        F     Halt all ship velocity.
        
        Esc   Pause/unpause the game, exit menus.
        
        Space Fire weapons, start level
        """
    elif GameConfig.get_setting("controller") == "GAMEPAD":
        controls = """Controls
        
        UP        Accelerate the ship forward.
        
        LEFT      Rotate the ship counterclockwise.
        
        DOWN      Accelerate the ship backward.
        
        RIGHT     Rotate the ship clockwise.
        
        B         Halt all ship velocity.
        
        START     Pause/unpause the game, exit menus.
        
        A         Fire weapons, start level
        """
    controls_text = TextBox(controls, (255, 255, 255), 60, "small")
    instructions = """How to play:
    
    You are playing as a ship tasked with destroying all the asteroids in the area.
    
    Clean up the asteroids in the level to move to the next one.
    
    Keep playing until you run out of lives, you might even get onto the leaderboard.
    """
    instr_text = TextBox(instructions, (255, 255, 255), 40, "small")
    
    controls_btn = Button("Controls", None, (255, 255, 255))
    controls_anchor = 0, 0
    instr_btn = Button("Instructions", None, (255, 255, 255))
    instr_anchor = screen.get_width() - instr_btn.get_dim()[0], 0
    back_btn = Button("Back", None, (255, 0, 0))
    back_anchor = screen.get_width() - back_btn.get_dim()[0], screen.get_height() - back_btn.get_dim()[1]

    # Update accounting
    frame_delta = 1 / 24
    frame_timer = perf_counter()
    display = "CONTR"
    while running:
        delta = perf_counter() - frame_timer
        if delta >= frame_delta:
            frame_timer = perf_counter()
            # Process Frame
            screen.fill((0, 0, 0))
            controls_btn.place(screen, controls_anchor)
            instr_btn.place(screen, instr_anchor)
            if GameConfig.get_setting("controller") == "KEYBOARD":
                back_btn.place(screen, back_anchor)
            if display == "CONTR":
                controls_text.place_center(screen)
            elif display == "INSTR":
                instr_text.place_center(screen)
            pg.display.flip()
            # Process Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    return -1
                if GameConfig.get_setting("controller") == "KEYBOARD":
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            running = False
                    elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        if controls_btn.check_click(event.pos):
                            display = "CONTR"
                        elif instr_btn.check_click(event.pos):
                            display = "INSTR"
                        elif back_btn.check_click(event.pos):
                            running = False
                elif GameConfig.get_setting("controller") == "GAMEPAD":
                    if event.type == pg.JOYBUTTONDOWN:
                        if event.button == GameConfig.get_setting("L"):
                            display = "CONTR"
                        elif event.button == GameConfig.get_setting("R"):
                            display = "INSTR"
                        elif event.button == GameConfig.get_setting("B"):
                            running = False
    return 0
