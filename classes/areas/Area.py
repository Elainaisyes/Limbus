import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.Game import Game

class Area():
    def __init__(self, game: Game):
        self.game = game

