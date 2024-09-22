import pygame
from constants import *
pygame.font.init()
font = pygame.font.SysFont(None, 40)
color = pygame.Color(WHITE)


def debug(*args, **kwargs):
    win = pygame.display.get_surface()
    win.blit(font.render(str([x for x in args]), 1, color, pygame.Color(BLACK)), (0, 0))
    win.blit(font.render(str(**kwargs), 1, color, pygame.Color(BLACK)), (40, 40))

