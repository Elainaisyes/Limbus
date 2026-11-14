import pygame, random

from constants import WIDTH, HEIGHT, FPS, GAME_NAME, ARROW, HOVER, BACKGROUNDS
from classes.Basic_Image import Basic_Image
from classes.Particle import Particle
from classes.areas.Clickarea import Clickarea
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


        self.area = "clickarea"

        self.coins = 0
        self.coins_per_click = 1
        self.coins_per_second = 0

        self.in_rush = False

        self.coin_image = pygame.image.load('assets/images/coin.png').convert_alpha()
        self.gold_coin_image = pygame.image.load('assets/images/gold_coin.png').convert_alpha()

        self.mouse_trail = pygame.sprite.Group()

        self.set_background("clickarea", "default")

        self.click_area = Clickarea(self)

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
                if event.key == pygame.K_p:
                    self.set_background("brown_square", "boss")
                if event.key == pygame.K_f:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                    else:
                        self.window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and pygame.Rect.collidepoint(self.click_area.click_button.rect, self.mouse_pos):
                    self.click_area.click_button.click()
            if event.type == pygame.MOUSEMOTION:
                if self.area == "clickarea":
                    self.set_cursor_hover(self.click_area.click_button.rect)
            if event.type == self.SECOND_INTERVAL:
                self.coins += self.coins_per_second

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        Particle(self.mouse_pos[0], self.mouse_pos[1], 5, 0, 0, 30, (255, 255, 255), 255, self.mouse_trail)
        for particle in self.mouse_trail:
            particle.loop()
        self.click_area.loop()

    def set_background(self, area, type, start_time=0.0, resume=True):
        config = BACKGROUNDS[area][type]
        image = pygame.image.load(config["bg_image"]).convert_alpha()
        self.background = Basic_Image(image, WIDTH//2, HEIGHT//2, self.window, self, color=(120,120,120), width=WIDTH, height=HEIGHT)
        self.area = area
        self.background_type = type
        self.background_config = config
        self.mouse_trail_color = config["trail_color"]
        self.audio_manager.play_bgm(config["bgm_name"], start=start_time, resume=resume)

    def set_cursor_hover(self, rect):
        if rect.collidepoint(self.mouse_pos):
            pygame.mouse.set_cursor(HOVER)
        else:
            pygame.mouse.set_cursor(ARROW)

    def color_offset(self, color, amount=100):
        return tuple(min(255, max(0, value - amount)) for value in color)

    def draw_text(self, text, font, position, scale=1, alpha=255, color=(255, 255, 255), centered=False, icon=None, icon_at_end=False, icon_color=(255,255,255), icon_rotation=0, has_shadow=True, shadow_color=None, shadow_offset=(3,3)):
        draw_text(self.window, text, font, position, scale, alpha, color, centered, icon, icon_at_end, icon_color, icon_rotation, has_shadow, shadow_color, shadow_offset)

    def draw(self):
        self.window.fill((0, 0, 0))
        self.background.draw()

        self.click_area.draw()

        draw_trail(self.window, pygame.math.Vector2(self.mouse_pos), self.mouse_trail, self.mouse_trail_color)
        pygame.display.update()