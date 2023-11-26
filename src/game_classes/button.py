# File: button.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 26 Nov 2023
# Purpose:
#   A simple Pygame-based button class.
# Notes:

import pygame as pg
from .vector2d import Vector2D


class Button:
    """A simply Pygame-based button class."""

    def __init__(self, label: str, min_dim: Vector2D, text_color: (int, int, int)):
        """Button constructor"""
        self.font = pg.font.SysFont("consolas", 24)
        self.padding = 10
        self.anchor = None
        self.label = label
        label_surf = self.font.render(self.label, True, text_color)
        self.dim = max(label_surf.get_width(), int(min_dim.x)) + self.padding, max(label_surf.get_height(), int(min_dim.y)) + self.padding
        self.surf = pg.Surface(self.dim, flags=pg.SRCALPHA)
        label_anchor = (self.dim[0] - label_surf.get_width())//2, (self.dim[1] - label_surf.get_height())//2
        self.surf.blit(label_surf, label_anchor)
        pg.draw.rect(self.surf, (255, 255, 255), self.surf.get_rect(), 1)
        
    def place(self, screen: pg.Surface, anchor: Vector2D):
        """Places the button at the given anchor."""
        self.anchor = anchor
        screen.blit(self.surf, self.anchor.to_int_tuple())
    
    def place_center(self, screen: pg.Surface):
        """Places the button in the center of the screen."""
        self.anchor = (screen.get_width() - self.dim[0])//2,  (screen.get_height() - self.dim[1])//2
        screen.blit(self.surf, self.anchor)
        
    def place_horizontal_center(self, screen: pg.Surface, vertical: int):
        """Places the button in the horizontal center of the screen, at a specified y-value."""
        self.anchor = (screen.get_width() - self.dim[0])//2,  vertical
        screen.blit(self.surf, self.anchor)
    
    def get_dim(self):
        """Retrieves the dimensions of the button."""
        return self.surf.get_size()
    
    def check_click(self, click_pos: (int, int)) -> bool:
        """Checks to see if a particular click is inside the button."""
        click_pos = click_pos[0] - self.anchor[0], click_pos[1] - self.anchor[1]
        return self.surf.get_rect().collidepoint(*click_pos)
    