import pygame
from math import cos, sin, radians

class Particle (pygame.sprite.Sprite):
    def __init__(self, x, y, radius, angle_direction, speed, decay_rate, color, alpha, *groups):
        super().__init__(*groups)
        self.pos = pygame.math.Vector2(x, y)
        self.current_radius = radius
        # negative so it follows the unit circle
        self.angle_direction = -angle_direction
        self.speed = speed
        self.decay_rate = decay_rate
        self.color = color
        self.alpha = alpha
        angle = radians(self.angle_direction)
        self.direction = pygame.math.Vector2(cos(angle), sin(angle))
        self.image_size = None
        self.build_image()

    def build_image(self):
        diameter = max(1, int(self.current_radius * 2))
        draw_radius = max(1, int(self.current_radius))
        size = (diameter, draw_radius)

        if size != self.image_size:
            self.image = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
            self.image.set_alpha(self.alpha)
            pygame.draw.circle(
                self.image,
                self.color,
                (diameter // 2, diameter // 2),
                draw_radius,
            )
            self._image_size = size

        self.rect = self.image.get_rect(
            center=(self.pos)
        )

    def loop(self):
        self.pos += self.direction * self.speed
        self.current_radius -= 0.01 * self.decay_rate

        if self.current_radius <= 0.5:
            self.kill()
            return

        self.build_image()
        self.rect.center = (self.pos)