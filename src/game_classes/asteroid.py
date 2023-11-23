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
    
    ASTEROID_MIN_RADIUS = [10, 20, 30]
    ASTEROID_MAX_RADIUS = [10, 40, 60]
    ASTEROID_SPEED = [70, 50, 25]
    
    def __init__(self, size: int, anchor: Vector2D):
        """Asteroid Contructor."""
        velocity = Vector2D.ang_to_vec(radians(randint(0, 359)))
        velocity = velocity.scale(Asteroid.ASTEROID_SPEED[size])
        super(Asteroid, self).__init__(anchor, Asteroid.ASTEROID_MAX_RADIUS[size], velocity)
        self.size = size
        
    def draw(self, screen: pg.Surface):
        """Override of the draw method for the asteroid."""
        pg.draw.circle(screen, (255, 255, 255), self.collider.get_anchor().to_int_tuple(), self.collider.get_radius(), 1)
        