import pygame, random

from constants import WIDTH, HEIGHT, FPS, GAME_NAME, ARROW, HOVER, CLICK
from classes.Basic_Image import Basic_Image
from classes.Particle import Particle
from classes.ClickButton import ClickButton
from util.audio_manager import Audio_Manager
from util.draw_trail import draw_trail
from util.draw_text import draw_text

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        pygame.mixer.set_num_channels(128)
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.running = True
        self.fullscreen = False

        self.mouse_pos = pygame.mouse.get_pos()

        self.SECOND_INTERVAL = pygame.event.custom_type()
        pygame.time.set_timer(self.SECOND_INTERVAL, 1000)

        self.audio_manager = Audio_Manager()
        self.font = pygame.font.Font('assets/fonts/pixeloid.sans-bold.ttf', 32)
        self.font_light = pygame.font.Font('assets/fonts/pixeloid.sans.ttf', 32)

        self.location = "clickarea"

        self.coins = 0
        self.coins_per_click = 1
        self.coins_per_second = 0

        self.coin_image = pygame.image.load('assets/images/coin.png').convert_alpha()

        self.background = Basic_Image(pygame.image.load("assets/images/backgrounds/clickarea.png").convert_alpha(), WIDTH//2, HEIGHT//2, self.window, self, color=(120,120,120), width=WIDTH, height=HEIGHT)

        self.click_button_image = pygame.image.load("assets/images/dante_button.png").convert_alpha()
        self.click_button = ClickButton(self.click_button_image, WIDTH//2, HEIGHT//2, self.window, self, scale=1.5)
        self.mouse_trail = pygame.sprite.Group()
        self.mouse_trail_color = (255, 255, 180)

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
                if event.key == pygame.K_f:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                    else:
                        self.window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and pygame.Rect.collidepoint(self.click_button.rect, self.mouse_pos):
                    self.click_button.click()
            if event.type == pygame.MOUSEMOTION:
                if self.location == "clickarea":
                    self.set_cursor_hover(self.click_button.rect)
            if event.type == self.SECOND_INTERVAL:
                self.coins += self.coins_per_second

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        Particle(self.mouse_pos[0], self.mouse_pos[1], 5, 0, 0, 30, (255, 255, 255), 255, self.mouse_trail)
        for particle in self.mouse_trail:
            particle.loop()
        self.click_button.loop()

    def set_cursor_hover(self, rect):
        if rect.collidepoint(self.mouse_pos):
            pygame.mouse.set_cursor(HOVER)
        else:
            pygame.mouse.set_cursor(ARROW)

    def draw_text(self, text, font, position, scale=1, color=(255, 255, 255), centered=False, icon=None, icon_at_end=False, icon_color=(255,255,255), icon_rotation=0):
        draw_text(self.window, text, font, position, scale, color, centered, icon, icon_at_end, icon_color, icon_rotation)

    def draw(self):
        self.window.fill((0, 0, 0))
        self.background.draw()

        self.draw_text(f"Coins: {self.coins}", self.font, (WIDTH//2, 48), 1.5, centered=True, icon=self.coin_image, color=(255, 255, 180))

        self.click_button.draw()
        draw_trail(self.window, pygame.math.Vector2(self.mouse_pos), self.mouse_trail, self.mouse_trail_color)
        pygame.display.update()