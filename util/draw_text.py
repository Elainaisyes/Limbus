import pygame

def render_wrapped_text(font, text, color, scale, max_width):
    lines = []

    for paragraph in str(text).split('\n'):
        line = ""

        for word in paragraph.split():
            candidate = f"{line} {word}".strip()

            if line and font.size(candidate)[0] * scale > max_width:
                lines.append(line)
                line = word
            else: 
                line = candidate

        lines.append(line)

    line_height = font.get_linesize()
    surface_width = max(1, max(font.size(line)[0] for line in lines))
    surface = pygame.Surface((surface_width, line_height * len(lines)), pygame.SRCALPHA)

    for index, line in enumerate(lines):
        surface.blit(font.render(line, True, color), (0, index * line_height))

    return surface

def draw_text(window, text, font, position, scale=1, alpha=255, color=(255,255,255), centered=False, align="left", icon=None, icon_at_end=False, icon_color=(255,255,255), icon_rotation=0, has_shadow=True, shadow_color=None, shadow_offset=(2,2), rotation=0, max_width=None):
    text = str(text)
    wrap_width = max_width / scale if max_width is not None else None

    if wrap_width is None:
        text_surface = font.render(text, True, color)
    else:
        text_surface = render_wrapped_text(font, text, color, wrap_width)

    if shadow_color is None:
        shadow_color = tuple(max(0, value - 100) for value in color[:3])

    shadow_surface = None
    if has_shadow:
        if wrap_width is None:
            shadow_surface = font.render(text, True, shadow_color)
        else:
            shadow_surface = render_wrapped_text(
                font, text, shadow_color, wrap_width
            )

    if scale != 1:
        size = (
            max(1, round(text_surface.get_width() * scale)),
            max(1, round(text_surface.get_height() * scale)),
        )
        text_surface = pygame.transform.smoothscale(text_surface, size)

        if shadow_surface is not None:
            shadow_surface = pygame.transform.smoothscale(shadow_surface, size)

    if rotation != 0:
        text_surface = pygame.transform.rotate(text_surface, -rotation)
        if shadow_surface is not None:
            shadow_surface = pygame.transform.rotate(shadow_surface, -rotation)

        rotated_offset = pygame.Vector2(shadow_offset).rotate(rotation)
        shadow_offset = (round(rotated_offset.x), round(rotated_offset.y))

    if alpha < 255:
        text_surface.set_alpha(alpha)
        if shadow_surface is not None:
            shadow_surface.set_alpha(alpha)

    icon_surface = None
    gap = round(8 * scale) if icon is not None else 0

    if icon is not None:
        icon_surface = icon.copy()

        if icon_color is not None:
            icon_alpha = icon_color[3] if len(icon_color) == 4 else 255
            combined_alpha = round(alpha * icon_alpha / 255)
            icon_surface.fill(
                (*icon_color[:3], combined_alpha),
                special_flags=pygame.BLEND_RGBA_MULT,
            )

        icon_height = text_surface.get_height()
        icon_width = round(
            icon_surface.get_width() * icon_height / icon_surface.get_height()
        )
        icon_surface = pygame.transform.smoothscale(
            icon_surface, (icon_width, icon_height)
        )

        if icon_rotation != 0:
            icon_surface = pygame.transform.rotozoom(
                icon_surface, icon_rotation, 1
            )

    total_width = text_surface.get_width() + gap
    if icon_surface is not None:
        total_width += icon_surface.get_width()

    total_height = max(
        text_surface.get_height(),
        icon_surface.get_height() if icon_surface is not None else 0,
    )

    if centered or align == "center":
        x = position[0] - total_width // 2
        y = position[1] - total_height // 2 if centered else position[1]
    elif align == "right":
        x = position[0] - total_width
        y = position[1]
    else:
        x, y = position

    text_y = y + (total_height - text_surface.get_height()) // 2

    if icon_surface is not None:
        icon_y = y + (total_height - icon_surface.get_height()) // 2

        if icon_at_end:
            if shadow_surface is not None:
                window.blit(
                    shadow_surface,
                    (x + shadow_offset[0], text_y + shadow_offset[1]),
                )
            window.blit(text_surface, (x, text_y))
            icon_x = x + text_surface.get_width() + gap
            window.blit(icon_surface, (icon_x, icon_y))
        else:
            window.blit(icon_surface, (x, icon_y))
            text_x = x + icon_surface.get_width() + gap
            if shadow_surface is not None:
                window.blit(
                    shadow_surface,
                    (text_x + shadow_offset[0], text_y + shadow_offset[1]),
                )
            window.blit(text_surface, (text_x, text_y))
    else:
        if shadow_surface is not None:
            window.blit(
                shadow_surface,
                (x + shadow_offset[0], text_y + shadow_offset[1]),
            )
        window.blit(text_surface, (x, text_y))