# File: pellet.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 25 Nov 2023
# Purpose:
#   A class for handling the pellet shot by the player's ship.
# Notes:

from .game_object import MovingGameObject
from .vector2d import Vector2D

import pygame as pg


class Pellet(MovingGameObject):
    """A class for handling Player ship pellets."""
    SPEED = 100
    RADIUS = 3
    
    def __init__(self, anchor: Vector2D, direction: Vector2D):
        super(Pellet, self).__init__(anchor, Pellet.RADIUS, direction.scale(Pellet.SPEED))
    
    def draw(self, screen: pg.Surface):
        if not self.visible:
            return
        pg.draw.circle(screen, (0, 255, 0), self.collider.get_anchor().to_int_tuple(), Pellet.RADIUS)
    