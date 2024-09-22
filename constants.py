import pygame, os


scale = (16,9)
base = 50
boardbase = 20
WIDTH, HEIGHT = scale[0]*base, scale[1]*base
BOARDW, BOARDH = scale[0]*boardbase, scale[1]*boardbase
BLACK = '#000000'
WHITE = "#fefefe"
GRAY = (139, 139, 139)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITEW = (215, 218, 221)
GREENW = (31, 174, 81)
REDW = (215, 37, 3)
GREENWW = (70, 194, 99)
REDWW = (227, 52, 55)


pygame.font.init()

fonts = {"f_1": "RETRO_SPACE.ttf", "f_2": "RETRO_SPACE_INV.ttf"}


def texture_resize(texture, factor):
    ratio = texture.get_width(), texture.get_height()
    size = int(factor*ratio[0]), int(factor*ratio[1])
    return pygame.transform.scale(texture, size)


def font_render(file_code, size=40):
    return pygame.font.Font(os.path.join('Assets', fonts[file_code]), size)
