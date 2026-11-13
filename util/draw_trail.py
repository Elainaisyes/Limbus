import pygame
from constants import WIDTH, HEIGHT

def draw_trail(window, start, trail_list, color):
    points = [start, *[point.pos for point in reversed(list(trail_list))]]

    if len(points) < 2:
        return

    max_distance = max((point - start).length() for point in points)
    if max_distance == 0:
        return

    trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    segment_count = len(points) - 1
    base_alpha = color[3] if len(color) == 4 else 255

    for index, (start, end) in enumerate(zip(points, points[1:])):
        fade = 1 - index / max(1, segment_count - 1)
        alpha = round(base_alpha * fade)
        width = max(1, round(8 * fade))
        pygame.draw.line(trail_surface, (*color[:3], alpha), start, end, width)

    window.blit(trail_surface, (0, 0))