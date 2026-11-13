import pygame

def draw_text(window, text, font, position, scale=1, color=(255, 255, 255), centered=False, icon=None, icon_at_end=False, icon_color=(255,255,255), icon_rotation=0):
    text_surface = font.render(str(text), True, color)
    if scale != 1:
        size = (
            max(1, round(text_surface.get_width() * scale)),
            max(1, round(text_surface.get_height() * scale)),
        )
        text_surface = pygame.transform.smoothscale(text_surface, size)

    icon_surface = None
    gap = round(8 * scale) if icon is not None else 0

    if icon is not None:
        icon_surface = icon.copy()
        if icon_color is not None:
            alpha = 255 if len(icon_color) != 4 else icon_color[3]
            icon_surface.fill((*icon_color[:3], alpha), special_flags=pygame.BLEND_RGBA_MULT)

        icon_height = text_surface.get_height()
        icon_width = round(
            icon_surface.get_width() * icon_height / icon_surface.get_height()
        )
        icon_surface = pygame.transform.smoothscale(
            icon_surface, (icon_width, icon_height)
        )

        if icon_rotation != 0:
            icon_surface = pygame.transform.rotozoom(icon_surface, icon_rotation, 1)

    total_width = text_surface.get_width() + gap
    if icon_surface:
        total_width += icon_surface.get_width()

    total_height = max(text_surface.get_height(), icon_surface.get_height() if icon_surface else 0)

    if centered:
        x = position[0] - total_width // 2
        y = position[1] - total_height // 2
    else:
        x, y = position

    if icon_surface:
        icon_y = y + (total_height - icon_surface.get_height()) // 2
        text_y = y + (total_height - text_surface.get_height()) // 2

        if icon_at_end:
            window.blit(text_surface, (x, text_y))
            icon_x = x + text_surface.get_width() + gap
            window.blit(icon_surface, (icon_x, icon_y))
        else:
            window.blit(icon_surface, (x, icon_y))
            text_x = x + icon_surface.get_width() + gap
            window.blit(text_surface, (text_x, text_y))
    else:
        window.blit(
            text_surface,
            (x, y + (total_height - text_surface.get_height()) // 2),
        )