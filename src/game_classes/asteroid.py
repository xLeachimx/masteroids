# File: asteroid.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 23 Nov 2023
# Purpose:
#   A simple class for handling procedurally generated asteroids.
# Notes:

from .game_object import MovingGameObject
from .vector2d import Vector2D
from random import randint
from math import radians

import pygame as pg


class Asteroid(MovingGameObject):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2
    
    ASTEROID_MIN_RADIUS = [5, 10, 20]
    ASTEROID_MAX_RADIUS = [10, 20, 30]
    ASTEROID_SPEED = [70, 50, 25]
    
    def __init__(self, size: int, anchor: Vector2D):
        """Asteroid Contructor."""
        velocity = Vector2D.ang_to_vec(radians(randint(0, 359)))
        velocity = velocity.scale(Asteroid.ASTEROID_SPEED[size])
        super(Asteroid, self).__init__(anchor, Asteroid.ASTEROID_MAX_RADIUS[size], velocity)
        self.size = size
        num_sections = (2**size) + 6
        sections = []
        sect_angle = radians(360//num_sections)
        for _ in range(num_sections):
            radius = randint(Asteroid.ASTEROID_MIN_RADIUS[self.size], Asteroid.ASTEROID_MAX_RADIUS[self.size])
            sections.append(radius)
        sqr_size = 2 * self.collider.get_radius()
        self.sprite = pg.Surface((sqr_size, sqr_size))
        self.sprite.fill((0, 0, 0))
        points = []
        sprite_center = Vector2D(*self.sprite.get_rect().center)
        for i in range(num_sections):
            ang_vec = Vector2D.ang_to_vec((i*sect_angle))
            p1 = ang_vec.scale(sections[i]).add(sprite_center).to_int_tuple()
            ang_vec = Vector2D.ang_to_vec((i-1)*sect_angle)
            p2 = ang_vec.scale(sections[i-1]).add(sprite_center).to_int_tuple()
            pg.draw.line(self.sprite, (255, 255, 255), p1, p2)
        
    def draw(self, screen: pg.Surface):
        """Override of the draw method for the asteroid."""
        # pg.draw.circle(screen, (255, 255, 255), self.collider.get_anchor().to_int_tuple(), self.collider.get_radius(), 1)
        anchor = self.get_anchor()
        anchor = anchor.sub(Vector2D(Asteroid.ASTEROID_MAX_RADIUS[self.size], Asteroid.ASTEROID_MAX_RADIUS[self.size]))
        screen.blit(self.sprite, anchor.to_int_tuple())
        