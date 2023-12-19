# File: game.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 26 Nov 2023
# Purpose:
#   A file for running an instance of the game, and required supporting functions.
# Notes:

from time import perf_counter
import pygame as pg
from game_classes import Player, Vector2D, Level, AssetManager, GameConfig
from random import seed


def create_level(player: Player, screen_dim: (int, int), difficulty: int):
    small = difficulty // 2
    medium = difficulty // 5
    large = difficulty // 7
    return Level(player, screen_dim, small, medium, large)


def create_level_label(level: int, font: pg.font.Font, screen_dim: (int, int)):
    level_label = font.render(f"LEVEL {level}", True, (255, 255, 255))
    level_anchor = (screen_dim[0] - level_label.get_width()) // 2, (screen_dim[1] - level_label.get_height()) // 2
    return level_label, level_anchor


def game():
    # Start the music
    pg.mixer.music.load(AssetManager.get_instance().get_music("background"))
    pg.mixer.music.set_volume(0.05)
    pg.mixer.music.play(-1)
    # Running constants
    screen = pg.display.get_surface()
    screen_dim = screen.get_size()
    frame_delta = 1 / 24
    frame_timer = perf_counter()
    announcement_font = AssetManager.get_instance().get_font("large")
    announcement_font.set_bold(True)
    subtitle_font = AssetManager.get_instance().get_font("small")
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
    pause_label = announcement_font.render("==PAUSED==", True, (255, 255, 255))
    pause_anchor = (screen_dim[0] - pause_label.get_width()) // 2, (screen_dim[1] - pause_label.get_height()) // 2
    level_label, level_anchor = create_level_label(level_count, announcement_font, screen_dim)
    level_dir = None
    match GameConfig.get_setting("controller"):
        case "KEYBOARD":
            level_dir = subtitle_font.render("Press SPACE to proceed", True, (255, 255, 255))
        case "GAMEPAD":
            level_dir = subtitle_font.render("Press A to proceed", True, (255, 255, 255))
    level_dir_anchor = (screen_dim[0] - level_dir.get_width()) // 2, (
              screen_dim[1] - level_dir.get_height()) // 2 + level_label.get_height()
    
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
            pg.draw.rect(screen, (255, 255, 255), screen.get_rect(), 3)
            pg.display.flip()
            # Process Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    return -1
                if GameConfig.get_setting("controller") == "KEYBOARD":
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            if game_state in ["PLAY", "PAUSED"]:
                                level.toggle_pause()
                                if game_state == "PLAY":
                                    game_state = "PAUSED"
                                    pg.mixer.music.pause()
                                else:
                                    game_state = "PLAY"
                                    pg.mixer.music.unpause()
                        if game_state == "NEW_LEVEL" and event.key == pg.K_SPACE:
                            game_state = "PLAY"
                            player.set_visible(True)
                            player.reset_cooldown()
                            level.toggle_pause()
                elif GameConfig.get_setting("controller") == "GAMEPAD":
                    if event.type == pg.JOYBUTTONDOWN:
                        if event.button == GameConfig.get_setting("START"):
                            if game_state in ["PLAY", "PAUSED"]:
                                level.toggle_pause()
                                if game_state == "PLAY":
                                    game_state = "PAUSED"
                                    pg.mixer.music.pause()
                                else:
                                    game_state = "PLAY"
                                    pg.mixer.music.unpause()
                        if game_state == "NEW_LEVEL" and event.button == GameConfig.get_setting("A"):
                            game_state = "PLAY"
                            player.set_visible(True)
                            player.reset_cooldown()
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
    pg.mixer.music.stop()
    return player.get_score()