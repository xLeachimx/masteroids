# File: vector2d.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 22 Nov 2023
# Purpose:
#   A simple, immutable two-dimensional vector class.
# Notes:

from math import sqrt, sin, cos


class Vector2D:
    """An immutable 2D vector class"""
    
    # Precond:
    #   x is the x value of the 2D vector.
    #   y is the y value of the 2D vector.
    #
    # Postcond:
    #   Constructs a new Vector2D object.
    def __init__(self, x: float, y: float):
        """Vector2D constructor"""
        self.x = x
        self.y = y
    
    # Precond:
    #   other is a valid Vector2D object
    #
    # Postcond:
    #   Returns a new Vector2D which is the result of adding this vector with the given vector.
    def add(self, other: 'Vector2D') -> 'Vector2D':
        """Adds two 2D vectors"""
        return Vector2D(self.x + other.x, self.y + other.y)
    
    # Precond:
    #   other is a valid Vector2D object
    #
    # Postcond:
    #   Returns a new Vector2D which is the result of subtracting this vector by the given vector.
    def sub(self, other: 'Vector2D') -> 'Vector2D':
        """Subtracts two 2D vectors"""
        return Vector2D(self.x - other.x, self.y - other.y)
    
    # Precond:
    #   factor is a floating-point value
    #
    # Postcond:
    #   Returns a new Vector2D which this vector scaled by the given factor.
    def scale(self, factor: float) -> 'Vector2D':
        """Scales a 2D vector by a constant value"""
        return Vector2D(factor * self.x, factor * self.y)
    
    # Precond:
    #   other is a valid Vector2D object
    #
    # Postcond:
    #   Returns the dot product of this vector with the given vector.
    def dot(self, other: 'Vector2D') -> float:
        """Performs the dot product of two 2D vectors"""
        return (self.x * other.x) + (self.y + other.y)
    
    # Precond:
    #   None
    #
    # Postcond:
    #   Returns the magnitude of this vector.
    def magnitude(self) -> float:
        return sqrt((self.x * self.x) + (self.y * self.y))
    
    # Precond:
    #   None
    #
    # Postcond:
    #   Returns a new Vector2D which faced the inverse direction of this vector.
    def inverse(self) -> 'Vector2D':
        """Inverts the direction of the vector"""
        return self.scale(-1)
    
    # Precond:
    #   None
    #
    # Postcond:
    #   Returns a new Vector2D which is the unit vector of this vector.
    def unit(self) -> 'Vector2D':
        """Compute the unit vector of the vector"""
        return self.scale(1 / self.magnitude())
    
    # Precond:
    #   None
    #
    # Postcond:
    #   Returns the vector as an integer tuple.
    def to_int_tuple(self):
        """Convert the vector into an integer tuple."""
        return int(self.x), int(self.y)
    
    # Precond:
    #   None
    #
    # Postcond:
    #   Returns the vector as a tuple.
    def to_tuple(self):
        """Convert the vector into an integer tuple."""
        return self.x, self.y
    
    # =========================
    #   Static Methods
    # =========================
    
    # Precond:
    #   angle is a floating point value representing the angle to convert (in radians.)
    #
    # Postcond:
    #   Returns a unit vector pointing in the specified direction.
    @staticmethod
    def ang_to_vec(angle: float) -> 'Vector2D':
        return Vector2D(cos(angle), sin(angle))
