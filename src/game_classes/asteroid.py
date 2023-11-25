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
    ASTEROID_SECTIONS = [6, 8, 12]
    ASTEROID_SPEED = [70, 50, 25]
    ASTEROID_VALUE = [10, 100, 1000]
    
    # Precond:
    #   size is a number in the set {0, 1, 2} representing the size-class of the asteroid.
    #   anchor is a valid Vector2D object.
    #
    # Postcond:
    #   Creates a new asteroid object of the specified size.
    def __init__(self, size: int, anchor: Vector2D):
        """Asteroid Constructor."""
        velocity = Vector2D.ang_to_vec(radians(randint(0, 359)))
        velocity = velocity.scale(Asteroid.ASTEROID_SPEED[size])
        super(Asteroid, self).__init__(anchor, Asteroid.ASTEROID_MIN_RADIUS[size], velocity)
        self.size = size
        self.max_radius = Asteroid.ASTEROID_MAX_RADIUS[size]
        num_sections = Asteroid.ASTEROID_SECTIONS[self.size]
        sections = []
        sect_angle = radians(360//num_sections)
        for _ in range(num_sections):
            radius = randint(Asteroid.ASTEROID_MIN_RADIUS[self.size], Asteroid.ASTEROID_MAX_RADIUS[self.size])
            sections.append(radius)
        sqr_size = 2 * self.max_radius
        self.sprite = pg.Surface((sqr_size, sqr_size), flags=pg.SRCALPHA)
        self.sprite.fill((0, 0, 0, 0))
        sprite_center = Vector2D(*self.sprite.get_rect().center)
        for i in range(num_sections):
            ang_vec = Vector2D.ang_to_vec((i*sect_angle))
            p1 = ang_vec.scale(sections[i]).add(sprite_center).to_int_tuple()
            ang_vec = Vector2D.ang_to_vec((i-1)*sect_angle)
            p2 = ang_vec.scale(sections[i-1]).add(sprite_center).to_int_tuple()
            pg.draw.line(self.sprite, (255, 0, 0), p1, p2, 2)
        
    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a list of the asteroids created when this asteroid is destroyed.
    def split(self) -> list:
        """Splits the asteroid into smaller asteroids."""
        return []
    
    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the point value of the asteroid.
    def get_point_value(self):
        return Asteroid.ASTEROID_VALUE[self.size]
    
    # Precond:
    #   screen is the Pygame Surface object where the object will be drawn.
    #
    # Postcond:
    #   Override of the draw method for drawing the asteroid.
    def draw(self, screen: pg.Surface):
        """Override of the draw method for the asteroid."""
        if not self.visible:
            return
        anchor = self.get_anchor()
        anchor = anchor.sub(Vector2D(Asteroid.ASTEROID_MAX_RADIUS[self.size], Asteroid.ASTEROID_MAX_RADIUS[self.size]))
        screen.blit(self.sprite, anchor.to_int_tuple())
        