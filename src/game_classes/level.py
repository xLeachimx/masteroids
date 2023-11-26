# File: level.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 23 Nov 2023
# Purpose:
#   A simple level class for handling a single asteroids level.
# Notes:

from .player import Player
from .asteroid import Asteroid
from .pellet import Pellet
from .vector2d import Vector2D

from random import randint
import pygame as pg


class Level:
    def __init__(self, player: Player, screen_dim: (int, int), small: int, medium: int, large: int):
        self.dim = screen_dim
        self.player = player
        self.player.move_anchor_to(Vector2D(screen_dim[0]//2, screen_dim[1]//2))
        self.player.halt_ship()
        self.player.reset_facing()
        self.lives = 3
        self.asteroids = []
        self.pellets = []
        for i in range(small):
            self.asteroids.append(Asteroid(Asteroid.SMALL, self.__rand_point()))
            self.asteroids[-1].clamp(self.dim)
            self.asteroids[-1].activate()
        for i in range(medium):
            self.asteroids.append(Asteroid(Asteroid.MEDIUM, self.__rand_point()))
            self.asteroids[-1].clamp(self.dim)
            self.asteroids[-1].activate()
        for i in range(large):
            self.asteroids.append(Asteroid(Asteroid.LARGE, self.__rand_point()))
            self.asteroids[-1].clamp(self.dim)
            self.asteroids[-1].activate()
        
        #Setup HUD elements
        self.font = pg.font.SysFont("consolas", 30)
        self.paused = True
        
        # setup initial i-frames (measured in seconds)
        self.i_frames = 3
        self.i_blink_count = 0

    def run_frame(self, screen: pg.Surface, delta: float):
        if not self.paused:
            self.handle_i_frames(delta)
            
            # update
            self.player.update(delta)
            for asteroid in self.asteroids:
                asteroid.update(delta)
            for pellet in self.pellets:
                pellet.update(delta)
                
            # Handle out-of-bounds
            if not self.player.in_bounds(self.dim):
                self.player.bounce(self.dim)
            for asteroid in self.asteroids:
                if not asteroid.in_bounds(self.dim):
                    asteroid.bounce(self.dim)
            
            # collide
            pellet_remove = set()
            asteroid_remove = set()
            asteroid_add = []
            for idx in range(len(self.pellets)):
                for i in range(len(self.asteroids)):
                    if self.pellets[idx].has_collided(self.asteroids[i]):
                        asteroid_remove.add(i)
                        pellet_remove.add(idx)
                        asteroid_add.extend(self.asteroids[i].split())
                        self.player.add_score(self.asteroids[i].get_point_value())
            if self.i_frames <= 0:
                for asteroid in self.asteroids:
                    if asteroid.has_collided(self.player):
                        self.lives -= 1
                        self.player.move_anchor_to(Vector2D(self.dim[0]//2, self.dim[1]//2))
                        self.player.halt_ship()
                        self.i_frames = 1
                        self.i_blink_count = 0
                        break
                    
            # Garbage collection
            for i in range(len(self.pellets)):
                if not self.pellets[i].in_bounds(self.dim):
                    pellet_remove.add(i)
            asteroid_remove = list(asteroid_remove)
            pellet_remove = list(pellet_remove)
            asteroid_remove.sort(reverse=True)
            pellet_remove.sort(reverse=True)
            for i in pellet_remove:
                self.pellets.pop(i)
            for i in asteroid_remove:
                self.asteroids.pop(i)
            del pellet_remove
            del asteroid_remove
            self.asteroids.extend(asteroid_add)
            
            # Process Key Input
            # Rotational input
            if pg.key.get_pressed()[pg.K_a]:
                self.player.rotate_ccw(delta)
            elif pg.key.get_pressed()[pg.K_d]:
                self.player.rotate_cw(delta)
            # Throttle input
            if pg.key.get_pressed()[pg.K_f]:
                self.player.halt_ship()
            elif pg.key.get_pressed()[pg.K_w]:
                self.player.throttle_up(delta)
            elif pg.key.get_pressed()[pg.K_s]:
                self.player.throttle_down(delta)
            # Trigger input
            if pg.key.get_pressed()[pg.K_SPACE]:
                pellet = self.player.fire()
                if pellet is not None:
                    self.pellets.append(pellet)
        
        # Draw
        self.player.draw(screen)
        for asteroid in self.asteroids:
            asteroid.draw(screen)
        for pellet in self.pellets:
            pellet.draw(screen)
        
        # Draw HUD
        score_text = self.font.render(f"{self.player.get_score():09}", True, (255, 255, 255))
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        screen.blit(score_text, (self.dim[0] - score_text.get_width(), 0))
        screen.blit(lives_text, (0, 0))

    def win(self):
        return len(self.asteroids) == 0
    
    def lose(self):
        return self.lives == 0
    
    def pause(self):
        self.paused = True
        
    def resume(self):
        self.paused = False
        
    def toggle_pause(self):
        self.paused = not self.paused

    def handle_i_frames(self, delta: float):
        if self.i_frames <= 0:
           return
        self.i_frames = max(self.i_frames - delta, 0)
        # Blink while we have i-frames
        if self.i_frames > 0:
            self.i_blink_count += 1
            if (self.i_blink_count % 5) == 0:
                self.player.set_visible(not self.player.is_visible())
        else:
            self.player.set_visible(True)
        pass

    def __rand_point(self):
        return Vector2D(randint(0, self.dim[0]), randint(0, self.dim[1]))
    