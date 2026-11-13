import pygame


class Basic_Image(pygame.sprite.Sprite):
    def __init__(self, image, x, y, window, game, *groups, width=None, height=None, scale=1, rotation=0, alpha=255, color=None):
        super().__init__(*groups)

        self.original_image = image
        self.image = image
        self.pos = pygame.math.Vector2(x, y)

        self.base_width = width
        self.base_height = height
        self.window = window
        self.game = game
        self.scale = scale
        self.rotation = rotation
        self.alpha = alpha
        self.color = color
        self.rect = self.image.get_rect()
        self.visible = True
        self.direction = pygame.math.Vector2(1, 0)

        self.refresh_image()

    def refresh_image(self):
        center = self.rect.center if hasattr(self, "rect") else (0, 0)

        image = self.original_image.copy()
        image = pygame.transform.rotozoom(image, -self.rotation, self.scale)

        if self.base_width is not None or self.base_height is not None:
            target_width = self.base_width if self.base_width is not None else image.get_width()
            target_height = self.base_height if self.base_height is not None else image.get_height()
            image = pygame.transform.smoothscale(
                image,
                (max(1, int(target_width)), max(1, int(target_height)))
            )

        if self.alpha != 255:
            image = image.copy()
            image.set_alpha(self.alpha)

        if self.color is not None:
            tinted = image.copy()
            tinted.fill(self.color, special_flags=pygame.BLEND_RGBA_MULT)
            image = tinted

        self.image = image
        self.rect = self.image.get_rect(center=center)

    def set_scale(self, scale):
        self.scale = scale
        self.refresh_image()

    def set_rotation(self, rotation):
        self.rotation = rotation
        self.refresh_image()

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.refresh_image()

    def set_color(self, color):
        self.color = color
        self.refresh_image()

    def draw(self):
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if self.visible:
            self.window.blit(self.image, self.rect)