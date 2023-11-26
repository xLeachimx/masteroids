# File: leaderboard.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 26 Nov 2023
# Purpose:
#   A simple leaderboard class which outputs to a file.
# Notes:

import os
import pygame as pg


class Leader:
    """A leader board data class"""
    
    def __init__(self, name: str, score: int):
        self.name = name
        self.score = score
    
    def encrypt(self, key: int):
        """Returns an encrypted csv version of the leader"""
        base = ",".join([self.name, str(self.score)])
        result = ""
        for ltr in base:
            result += chr(ord(ltr) ^ key)
        return result


class Leaderboard:
    SECRET_KEY = 42
    
    def __init__(self, filename: str):
        """Leaderboard constructor"""
        self.filename = filename
        self.leaders = []
        self.updated = True
        if os.path.isfile(self.filename):
            # Load file
            with open(self.filename, 'r') as fin:
                for line in fin:
                    line = line.strip()
                    if line != "":
                        self.leaders.append(Leaderboard.__decrypt_line(line))
            self.updated = False
        else:
            self.leaders = [Leader("AAA", 0) for i in range(10)]
    
    def add_leader(self, name: str, score: int):
        """Adds a new leader to the leader board, if they make the cut."""
        if score < self.leaders[-1].score:
            return
        self.updated = True
        for i in range(len(self.leaders)):
            if score > self.leaders[i].score:
                self.leaders.insert(i, Leader(name, score))
                self.leaders.pop()
                break
    
    def check_score(self, score: int) -> bool:
        """Checks whether a given score would appear on the leaderboard."""
        return score > self.leaders[-1].score
    
    def write_out(self):
        """Writes the leaderboard to its file, if needed."""
        if not self.updated:
            return
        lines = self.__encrypt()
        with open(self.filename, 'w') as fout:
            for line in lines:
                print(line, file=fout)
    
    def render(self) -> pg.Surface:
        """Renders the leaderboard into a Pygame surface for display."""
        font = pg.font.SysFont("consolas", 20)
        renders = []
        for leader in self.leaders:
            renders.append(font.render(leader.name + (5*" ") + f"{leader.score:09}", True, (255, 255, 255)))
        total_vertical = sum(map(lambda proc_line: proc_line.get_height(), renders))
        max_horizontal = max(map(lambda proc_line: proc_line.get_width(), renders))
        surf = pg.Surface((max_horizontal, total_vertical))
        vert = 0
        vert_padding = 10
        for render in renders:
            surf.blit(render, (0, vert))
            vert += render.get_height() + vert_padding
        return surf
    
    def __encrypt(self) -> [str]:
        """Encrypt the leaderboard for output."""
        result = []
        for leader in self.leaders:
            result.append(leader.encrypt(Leaderboard.SECRET_KEY))
        return result
    
    @staticmethod
    def __decrypt_line(line: str) -> Leader:
        """Decrypt a single line of an encrypted file."""
        result = ""
        for ltr in line:
            result += chr(ord(ltr) ^ Leaderboard.SECRET_KEY)
        name, score = result.split(",")
        score = int(score)
        return Leader(name, score)
