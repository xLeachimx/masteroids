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
            
    def run_frame(self, screen: pg.Surface, delta: float):
        # update
        self.player.update(delta)
        for asteroid in self.asteroids:
            asteroid.update(delta)
        for pellet in self.pellets:
            pellet.update(delta)
            
        # Handle out-of-bounds
        if not self.player.in_bounds(self.dim):
            self.player.clamp(self.dim)
        for asteroid in self.asteroids:
            if not asteroid.in_bounds(self.dim):
                asteroid.bounce(self.dim)
        
        # collide
        pellet_remove = []
        asteroid_remove = []
        asteroid_add = []
        for idx in range(len(self.pellets)):
            for i in range(len(self.asteroids)):
                if self.pellets[idx].has_collided(self.asteroids[i]):
                    asteroid_remove.append(i)
                    pellet_remove.append(i)
                    asteroid_add.extend(self.asteroids[i].split())
        for asteroid in self.asteroids:
            if asteroid.has_collided(self.player):
                self.lives -= 1
                self.player.move_anchor_to(Vector2D(self.dim[0]//2, self.dim[1]//2))
                
        # Garbage collection
        for i in range(len(self.pellets)):
            if not self.pellets[i].in_bounds(self.dim):
                pellet_remove.append(i)
        for i in pellet_remove[::-1]:
            self.pellets.pop(i)
        for i in asteroid_remove[::-1]:
                self.asteroids.pop(i)
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
            self.pellets.append(self.player.fire())
        
        # Draw
        self.player.draw(screen)
        for asteroid in self.asteroids:
            asteroid.draw(screen)
        for pellet in self.pellets:
            pellet.draw(screen)
    
    def win(self):
        return len(self.asteroids) == 0
    
    def lose(self):
        return self.lives == 0
    def __rand_point(self):
        return Vector2D(randint(0, self.dim[0]), randint(0, self.dim[1]))
    