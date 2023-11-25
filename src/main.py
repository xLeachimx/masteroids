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
from time import perf_counter
from game_classes import Player, Vector2D, Level
from random import seed
from math import radians


def create_level(player: Player, screen_dim: (int, int), difficulty: int):
    small = difficulty // 2
    medium = difficulty // 5
    large = difficulty // 7
    return Level(player, screen_dim, small, medium, large)


def create_level_label(level: int, font: pg.font.Font, screen_dim: (int, int)):
    level_label = font.render(f"LEVEL {level}", False, (255, 255, 255))
    level_anchor = (screen_dim[0] - level_label.get_width()) // 2, (screen_dim[1] - level_label.get_height()) // 2
    return level_label, level_anchor


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
    frame_delta = 1 / 24
    frame_timer = perf_counter()
    announcement_font = pg.font.SysFont("consolas", 48, bold=True)
    subtitle_font = pg.font.SysFont("consolas", 12, bold=True)
    running = True
    
    # Setup GameObjects
    player = Player(Vector2D(250, 250))
    difficulty = 10
    level_count = 1
    level = create_level(player, screen_dim, difficulty)
    player.set_active(True)
    player.set_visible(True)
    
    # Basic Game state handling and text
    game_state = "NEW_LEVEL"
    pause_label = announcement_font.render("==PAUSED==", False, (255, 255, 255))
    pause_anchor = (screen_dim[0] - pause_label.get_width()) // 2, (screen_dim[1] - pause_label.get_height()) // 2
    level_label, level_anchor = create_level_label(level_count, announcement_font, screen_dim)
    level_dir = subtitle_font.render("Press SPACE to proceed", False, (255, 255, 255))
    level_dir_anchor = (screen_dim[0] - level_dir.get_width()) // 2, (
              screen_dim[1] - level_dir.get_height()) // 2 + level_label.get_height()
    
    splash_screen(8)
    # Main game loop
    while running:
        delta = perf_counter() - frame_timer
        if delta >= frame_delta:
            frame_timer = perf_counter()
            # Process Frame
            screen.fill((0, 0, 0))
            level.run_frame(screen, delta)
            if game_state == "PAUSED":
                screen.blit(pause_label, pause_anchor)
            elif game_state == "NEW_LEVEL":
                player.set_visible(False)
                screen.blit(level_label, level_anchor)
                screen.blit(level_dir, level_dir_anchor)
            pg.display.flip()
            # Process Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        if game_state in ["PLAY", "PAUSED"]:
                            level.toggle_pause()
                            if game_state == "PLAY":
                                game_state = "PAUSED"
                            else:
                                game_state = "PLAY"
                    if game_state == "NEW_LEVEL" and event.key == pg.K_SPACE:
                        game_state = "PLAY"
                        player.set_visible(True)
                        level.toggle_pause()
            if level.win():
                difficulty += 1
                level_count += 1
                level_label, level_anchor = create_level_label(level_count, announcement_font, screen_dim)
                level = create_level(player, screen_dim, difficulty)
                game_state = "NEW_LEVEL"
            elif level.lose():
                running = False
                game_state = "LOST"



def splash_screen(length: float):
    sacgs_length = length/2
    screen = pg.display.get_surface()
    running = True
    announcement_font = pg.font.SysFont("consolas", 48, bold=True)
    subtitle_font = pg.font.SysFont("consolas", 18, bold=True)
    
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
    
    frame_delta = 1 / 24
    frame_timer = perf_counter()
    while running:
        delta = perf_counter() - frame_timer
        if delta >= frame_delta:
            length -= delta
            frame_timer = perf_counter()
            # Process Frame
            screen.fill((0, 0, 0))
            if length < sacgs_length:
                screen.blit(from_label, from_anchor)
                screen.blit(sacgs_label, sacgs_anchor)
            else:
                screen.blit(with_label, with_anchor)
                screen.blit(pygame_label, pygame_anchor)
            pg.display.flip()
            # Process Events
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
            if length <= 0:
                running = False


if __name__ == '__main__':
    main()
