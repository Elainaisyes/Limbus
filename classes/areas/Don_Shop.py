import pygame, random
from constants import WIDTH, HEIGHT
from util.lerp import lerp, lerp_color
from classes.areas.Area import Area
from classes.Basic_Image import Basic_Image

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.Game import Game

class Don_Shop(Area):
    def __init__(self, game: Game):
        super().__init__(game)
        self.don = Basic_Image(pygame.image.load("assets/images/character_sprites/don/default.png").convert_alpha(), WIDTH-200, HEIGHT-400, self.game.window, self.game, scale=0.4)
        self.next_id = 0

    def loop(self):
        for i in range(1):
            self.next_id += 1
            self.game.set_typewriter_text(f"shop_text_{self.next_id}", f"H{"i" * random.randint(1,5)}", (random.randint(0,self.game.width), random.randint(0,self.game.height)), rotation=random.randint(0,360)
                                          ,lifetime=2, color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))

    def draw(self):
        self.don.draw()