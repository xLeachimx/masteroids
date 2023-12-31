# File: player.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 22 Nov 2023
# Purpose:
#   A player game object class
# Notes:

from .game_object import MovingGameObject
from .vector2d import Vector2D
from .pellet import Pellet
from .asset_manager import AssetManager
from math import radians

import pygame as pg


class Player(MovingGameObject):
    """A simple class for dealing with the player's ship."""
    # Player constants
    SHIP_RADIUS = 10
    SHIP_ACCELERATION = 33
    SHIP_MAX_VELOCITY = 90
    SHIP_ANGULAR_SPEED = radians(180)
    COOLDOWN_TIMER = 0.4
    
    def __init__(self, anchor: Vector2D):
        """Player constructor."""
        super(Player, self).__init__(anchor, Player.SHIP_RADIUS, Vector2D(0, 0))
        self.facing = 0
        self.score = 0
        self.cooldown = 0
    
    def throttle_up(self, delta: float):
        """Apply acceleration in the direction of facing."""
        facing_vector = Vector2D.ang_to_vec(self.facing).scale(delta).scale(Player.SHIP_ACCELERATION)
        self.velocity = self.velocity.add(facing_vector)
        if self.velocity.magnitude() >= Player.SHIP_MAX_VELOCITY:
            self.velocity = self.velocity.unit().scale(Player.SHIP_MAX_VELOCITY)
    
    def throttle_down(self, delta: float):
        """Apply acceleration in the inverse direction of facing."""
        facing_vector = Vector2D.ang_to_vec(self.facing).scale(delta).scale(Player.SHIP_ACCELERATION)
        self.velocity = self.velocity.sub(facing_vector)
        if self.velocity.magnitude() >= Player.SHIP_MAX_VELOCITY:
            self.velocity = self.velocity.unit().scale(Player.SHIP_MAX_VELOCITY)
    
    def halt_ship(self):
        """Set the ship's velocity to zero."""
        self.velocity = Vector2D(0, 0)
        
    def reset_facing(self):
        """Resets the ship's facing to zero."""
        self.facing = 0
    
    def rotate_cw(self, delta: float):
        """Rotate the ship clockwise."""
        self.facing += delta * Player.SHIP_ANGULAR_SPEED
    
    def rotate_ccw(self, delta: float):
        """Rotate the ship counterclockwise."""
        self.facing -= delta * Player.SHIP_ANGULAR_SPEED
    
    def get_score(self) -> int:
        """Retrieve the player's score."""
        return self.score
    
    def add_score(self, incr: int) -> int:
        """Add to and retrieve the player's score."""
        self.score += incr
        return self.score
    
    def fire(self):
        """Spawn and return new pellet object in front of the player's ship."""
        if self.cooldown > 0:
            return None
        pellet_anchor = Vector2D.ang_to_vec(self.facing).scale(Player.SHIP_RADIUS)
        pellet = Pellet(pellet_anchor.add(self.get_anchor()), pellet_anchor.unit())
        pellet.activate()
        AssetManager.get_instance().get_sound("shooting").play()
        self.cooldown = Player.COOLDOWN_TIMER
        return pellet
    
    def reset_cooldown(self):
        self.cooldown = Player.COOLDOWN_TIMER
    
    # =======================
    #   Overridden methods
    # =======================
    
    # Precond:
    #   delta is a floating point number indicating the time elapsed (in seconds) since the last update.
    #
    # Postcond:
    #  Override of the update method of moving objects.
    def update(self, delta: float):
        """Update method for a moving game object"""
        if not self.active:
            return
        self.cooldown -= delta
        super(Player, self).update(delta)
    
    # Precond:
    #   screen is the Pygame Surface object where the object will be drawn.
    #
    # Postcond:
    #   Override of the draw method for drawing the player's ship.
    def draw(self, screen: pg.Surface):
        """Override of the draw method for the Player's ship."""
        if not self.visible:
            return
        anchor = self.get_anchor()
        anchor = anchor.sub(Vector2D(Player.SHIP_RADIUS, Player.SHIP_RADIUS))
        sprite = pg.Surface((2*Player.SHIP_RADIUS + 1, 2*Player.SHIP_RADIUS + 1), flags=pg.SRCALPHA)
        sprite.fill((0, 0, 0, 0))
        sprite_center = Vector2D(*sprite.get_rect().center)
        p1 = Vector2D.ang_to_vec(self.facing).scale(Player.SHIP_RADIUS).add(sprite_center)
        p2 = Vector2D.ang_to_vec(self.facing + radians(120)).scale(Player.SHIP_RADIUS//2).add(sprite_center)
        p3 = Vector2D.ang_to_vec(self.facing - radians(120)).scale(Player.SHIP_RADIUS//2).add(sprite_center)
        pg.draw.circle(sprite, (255, 255, 255), sprite_center.to_int_tuple(), Player.SHIP_RADIUS, 1)
        pg.draw.polygon(sprite, (255, 255, 255), [p1.to_int_tuple(), p2.to_int_tuple(), p3.to_int_tuple()])
        screen.blit(sprite, anchor.to_int_tuple())