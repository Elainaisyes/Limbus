import pygame
WIDTH, HEIGHT = 1000, 750
FPS = 60
GAME_NAME = "LIMMMBUS CLICKERRRR"

ARROW = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
HOVER = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)


BACKGROUNDS = {
    "clickarea": {
        "default": {
            "bg_image": "assets/images/backgrounds/clickarea.png",
            "bgm_name": "clickarea_default",
            "trail_color": (255, 255, 180),
        },
        "rush": {
            "bg_image": "assets/images/backgrounds/clickarea.png",
            "bgm_name": "clickarea_rush",
            "trail_color": (255, 255, 80),
        },
    },
    "brown_square": {
        "boss": {
            "bg_image": "assets/images/backgrounds/clickarea.png",
            "bgm_name": "brown_square_boss",
            "trail_color": (165, 42, 42),
        },
    },
}