# File: game_object.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 22 Nov 2023
# Purpose:
#   A base class for dealing with game objects.
# Notes:

from .vector2d import Vector2D
from .circle_collider import CircleCollider

import pygame as pg


class GameObject:
    """A simple class for building game objects"""
    # Precond:
    #   anchor is a valid Vector2D object.
    #   radius is a valid floating point number.
    #
    # Postcond:
    #   Creates a new GameObject with a CircleCollider.
    def __init__(self, anchor: Vector2D, radius: float):
        """GameObject constructor."""
        self.active = False
        self.visible = False
        self.collider = CircleCollider(anchor, radius)
    
    # Precond:
    #   delta is a floating point number indicating the time elapsed since the last update.
    #
    # Postcond:
    #   Updates the GameObject state.
    def update(self, delta: float):
        """Called each frame, if the object is active, to update the object's state."""
        pass
    
    # Precond:
    #   screen is the Pygame Surface object where the object will be drawn.
    #
    # Postcond:
    #   Abstract method for drawing the GameObject to a provided screen.
    #   Method does not draw anything by default.
    def draw(self, screen: pg.Surface):
        """Called each frame, after update if the object is visible, to draw the object to the screen."""
        pass
    
    # Precond:
    #   new_anchor is a valid Vector2D object.
    #
    # Postcond:
    #   Sets the objects anchor to the provided vector.
    def set_anchor(self, new_anchor: Vector2D):
        """Set the GameObject's anchor to a new position."""
        self.collider.move_to(new_anchor)
        
    # Precond:
    #   by is a valid Vector2D object.
    #
    # Postcond:
    #   Moves the object's anchor to by the provided vector.
    def move_anchor(self, by: Vector2D):
        """Moves the GameObject's anchor by a given vector."""
        self.collider.move(by)
        
    # Precond:
    #   to is a valid Vector2D object.
    #
    # Postcond:
    #   Moves the object's anchor to the provided vector.
    def move_anchor_to(self, to: Vector2D):
        """Set the GameObject's anchor to a new position."""
        self.collider.move_to(to)
    
    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the object's current anchor.
    def get_anchor(self) -> Vector2D:
        """Retrieve the GameObject's anchor."""
        return self.collider.get_anchor()
    
    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the true if the object is active.
    def is_active(self) -> bool:
        """Retrieve the GameObject's active state."""
        return self.active
    
    # Precond:
    #   value is a valid boolean value.
    #
    # Postcond:
    #   Sets the objects active state to the given value.
    def set_active(self, value: bool):
        """Set the GameObject's active state."""
        self.active = value
    
    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the true if the object is visible.
    def is_visible(self) -> bool:
        """Retrieve the GameObject's visible state."""
        return self.visible
    
    # Precond:
    #   value is a valid boolean value.
    #
    # Postcond:
    #   Sets the objects visible state to the given value.
    def set_visible(self, value: bool):
        """Set the GameObject's visible state."""
        self.visible = value
    
    # Precond:
    #   None.
    #
    # Postcond:
    #   Makes the object visible and active.
    def activate(self):
        """Makes the GameObject visible and active."""
        self.active = True
        self.visible = True
    
    # Precond:
    #   other is a valid GameObject.
    #
    # Postcond:
    #   Returns true if this object has collided with the given object.
    #   Returns false otherwise.
    def has_collided(self, other: 'GameObject') -> bool:
        """Detect collision between game objects"""
        return self.collider.has_collided(other.collider)
    

class MovingGameObject(GameObject):
    """A class for handling game objects that move via a constant velocity."""
    def __init__(self, anchor: Vector2D, radius: float, velocity: Vector2D):
        super(MovingGameObject, self).__init__(anchor, radius)
        self.velocity = velocity
        
    # Precond:
    #   delta is a floating point number indicating the time elapsed (in seconds) since the last update.
    #
    # Postcond:
    #  Override of the update method of moving objects.
    def update(self, delta: float):
        """Update method for a moving game object"""
        if not self.active:
            return
        self.collider.move(self.velocity.scale(delta))

    # Precond:
    #   screen_dim is a tuple of integers representing the (width, height) of the screen.
    #
    # Postcond:
    #   Returns true if the object's collider is fully in the screen.
    def in_bounds(self, screen_dim: (int, int)) -> bool:
        min_pt = self.collider.get_anchor().sub(Vector2D(self.collider.radius, self.collider.radius))
        max_pt = self.collider.get_anchor().add(Vector2D(self.collider.radius, self.collider.radius))
        return 0 <= min_pt.x < screen_dim[0] and 0 <= min_pt.y < screen_dim[1] and 0 <= max_pt.x < screen_dim[0] and\
            0 <= max_pt.y < screen_dim[1]
    
    # Precond:
    #   screen_dim is a tuple of integers representing the (width, height) of the screen.
    #
    # Postcond:
    #   Clamps the positioning of the collider to the edge of the screen.
    def clamp(self, screen_dim: (int, int)):
        x_max = screen_dim[0] - self.collider.radius
        x_min = self.collider.radius
        y_max = screen_dim[1] - self.collider.radius
        y_min = self.collider.radius
        anchor_x = min(max(x_min, self.collider.get_anchor().x), x_max)
        anchor_y = min(max(y_min, self.collider.get_anchor().y), y_max)
        if anchor_x != self.collider.get_anchor().x:
            self.velocity.x = 0
        if anchor_y != self.collider.get_anchor().y:
            self.velocity.y = 0
        self.collider.anchor = Vector2D(anchor_x, anchor_y)
        
    # Precond:
    #   screen_dim is a tuple of integers representing the (width, height) of the screen.
    #
    # Postcond:
    #   Bounces the object when it hits the edge of the screen.
    def bounce(self, screen_dim: (int, int)):
        min_pt = self.collider.get_anchor().sub(Vector2D(self.collider.radius, self.collider.radius))
        max_pt = self.collider.get_anchor().add(Vector2D(self.collider.radius, self.collider.radius))
        if min_pt.x < 0 or max_pt.x > screen_dim[0]:
            self.velocity.x = -self.velocity.x
        if min_pt.y < 0 or max_pt.y > screen_dim[1]:
            self.velocity.y = -self.velocity.y
