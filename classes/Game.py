import pygame, random

from constants import WIDTH, HEIGHT, FPS, GAME_NAME
from classes.ClickButton import ClickButton

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.running = True

        self.points = 0
        self.clicks_per_click = 1
        self.clicks_per_second = 0

        self.click_button_image = pygame.image.load("assets/images/dante_button.png").convert_alpha()
        self.click_button = ClickButton(self.click_button_image, WIDTH//2, HEIGHT//2, self.window, self, scale=1.5)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and pygame.Rect.collidepoint(self.click_button.rect, pygame.mouse.get_pos()):
                    self.click_button.click()

            

    def update(self):
        self.click_button.loop()


    def draw(self):
        self.window.fill((0, 0, 0))
        self.click_button.draw()

        pygame.display.update()