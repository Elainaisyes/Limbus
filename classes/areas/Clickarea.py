import pygame
from constants import WIDTH, HEIGHT
from classes.ClickButton import ClickButton
from util.lerp import lerp, lerp_color

class Clickarea():
    def __init__(self, game):
        self.game = game
        self.click_button_image = pygame.image.load("assets/images/dante_button.png").convert_alpha()
        self.click_button = ClickButton(self.click_button_image, WIDTH//2, HEIGHT//2, self.game.window, self.game, scale=1.5, area=self)

    def loop(self):
        self.click_button.loop()
        self.target_background_color = (120,120,120) if not self.game.in_rush else (180,180,80)
        self.target_text_color = (255,255, 180 if self.game.in_rush else 80)
        self.coins_text_color = (255, 255, 80 if self.game.in_rush else 180)
        self.game.background.set_color(lerp_color(self.game.background.color, self.target_background_color, 0.1))
        self.coins_text_color = lerp_color(self.coins_text_color, self.target_text_color, 0.1)

    def draw(self):
        coins_text_icon = self.game.gold_coin_image if self.game.in_rush else self.game.coin_image
        num_display = f"{self.game.coins:,.2f}" if not self.game.coins.is_integer() else f"{self.game.coins:,}"
        self.game.draw_text(f"Coins: {num_display}", self.game.font, (WIDTH//2, 48), 1.5, centered=True, icon=coins_text_icon, 
                            color=self.coins_text_color, icon_color=self.coins_text_color)

        self.click_button.draw()