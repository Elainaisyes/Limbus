import pygame, random
from constants import FPS, HEIGHT
from classes.Basic_Image import Basic_Image
from util.lerp import lerp

class ClickButton(Basic_Image):
    def __init__(self, image, x, y, window, game, *groups, width=None, height=None, scale=1, rotation=0, alpha=255, color=None, area=None):
        super().__init__(image, x, y, window, game, *groups, width=width, height=height, scale=scale, rotation=rotation, alpha=alpha, color=color)
        self.area = area
        self.click_amount = 0
        self.time_since_last_click = 0
        self.default_scale = scale
        self.target_rotation = rotation

        self.click_particles = pygame.sprite.Group()

        self.click_sfx = pygame.mixer.Sound('assets/audios/sfx/blip.mp3')
    
    def click(self):
        self.target_rotation = random.randint(-15,15)
        self.set_scale(self.default_scale * 1.15)
        self.time_since_last_click = 0
        self.game.coins += self.game.coins_per_click
        self.click_amount += 1
        particle = Basic_Image(self.original_image, self.game.mouse_pos[0], self.game.mouse_pos[1], self.window, self.game, self.click_particles, scale=random.uniform(0.2,0.4))
        particle.direction.x = random.uniform(-3,3)
        particle.direction.y = -8
        particle.rotation = random.randint(0,360)
        particle.set_rotation(particle.rotation)
        self.game.audio_manager.play_sound(self.click_sfx, 0.35)
        if random.randint(1,10) == 1 and self.game.background_type != "rush":
            self.game.in_rush = True
            self.game.set_background("clickarea", "rush", 3, False)

    def loop(self):
        self.time_since_last_click += 1
        self.set_rotation(lerp(self.rotation, self.target_rotation, 0.2))
        if self.time_since_last_click >= FPS//10:
            self.set_scale(lerp(self.scale, self.default_scale, 0.1))
        if self.time_since_last_click >= FPS//2:
            self.target_rotation = 0

        for particle in self.click_particles:
            particle.direction.y = min(particle.direction.y + 0.5, 15)
            particle.pos += particle.direction
            rotation_step = 1 if particle.direction.x >= 0 else -1
            particle.set_rotation(particle.rotation + rotation_step*5)
            if particle.pos.y >= HEIGHT + 100:
                particle.kill()
            
    def draw(self):
        super().draw()
        for particle in self.click_particles:
            particle.draw()