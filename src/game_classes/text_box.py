# File: text_box.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 26 Nov 2023
# Purpose:
#   A simple class for creating a multiline text box.
# Notes:

import pygame as pg


class TextBox:
    def __init__(self, data: str, color: (int, int, int), line_length: int, font_size: int):
        font = pg.font.SysFont("consolas", font_size)
        provided_lines = data.split("\n")
        wrapped_text = []
        temp = ""
        for line in provided_lines:
            temp = ""
            words = line.split(" ")
            for word in words:
                if (len(word) + len(temp) + 1) < line_length:
                    temp = temp + " " + word
                else:
                    wrapped_text.append(temp)
                    temp = word
            if len(temp) != 0:
                wrapped_text.append(temp)
        rendered_text = []
        for line in wrapped_text:
            rendered_text.append(font.render(line, True, color))
        total_vertical = sum(map(lambda proc_line: proc_line.get_height(), rendered_text))
        max_horizontal = max(map(lambda proc_line: proc_line.get_width(), rendered_text))
        self.surf = pg.Surface((max_horizontal, total_vertical), flags=pg.SRCALPHA)
        vert = 0
        for line in rendered_text:
            self.surf.blit(line, (0, vert))
            vert += line.get_height()
    
    def place(self, screen: pg.Surface, anchor: (int, int)):
        screen.blit(self.surf, anchor)
        
    def place_center(self, screen: pg.Surface):
        anchor = (screen.get_width() - self.surf.get_width())//2, (screen.get_height() - self.surf.get_height())//2
        screen.blit(self.surf, anchor)
    
    def get_dim(self) -> (int, int):
        return self.surf.get_size()