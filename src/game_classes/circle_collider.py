# File: circle_collider.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 22 Nov 2023
# Purpose:
#   A simple collider class for determining collisions between circles.
# Notes:

from .vector2d import Vector2D


class CircleCollider:
    # Precond:
    #   anchor is a valid Vector2D representing the point at the center of the collider.
    #   radius is a floating point number.
    #
    # Postcond:
    #   Creates a new CircleCollider object.
    def __init__(self, anchor: Vector2D, radius: float):
        """CircleCollider Constructor"""
        self.anchor = anchor
        self.radius = radius
    
    # Precond:
    #   other is a valid CircleCollider object
    #
    # Postcond:
    #   Returns true if this collider and the other collider intersect.
    def has_collided(self, other: 'CircleCollider'):
        """Checks if this collider collides with another collider"""
        return self.anchor.sub(other.get_anchor()).magnitude() < (self.radius + other.radius)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the current anchor for this collider.
    def get_anchor(self) -> Vector2D:
        """Returns the anchor for this collider"""
        return self.anchor
    
    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the radius for this collider.
    def get_radius(self) -> float:
        """Returns the radius of this collider"""
        return self.radius
    
    # Precond:
    #   by is a valid Vector2D object.
    #
    # Postcond:
    #   Updates the current anchor for this collider.
    def move(self, by: Vector2D):
        """Moves the anchor by a specified amount"""
        self.anchor = self.anchor.add(by)
    
    # Precond:
    #   to is a valid Vector2D object.
    #
    # Postcond:
    #   Updates the current anchor for this collider.
    def move_to(self, to: Vector2D):
        """Changes the anchor to the provided location"""
        self.anchor = to