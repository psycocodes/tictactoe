import pygame
import pygame.gfxdraw
from constants import *
import sys
from _debug import debug
from button import Button


class GameGraphics:
    def __init__(self, board):
        self.board = board
        self.board_dict = board.board_dict
        pygame.init()
        self.RES = self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.FPS = 60
        self.win_center = self.M_WIDTH, self.M_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.win = pygame.display.set_mode(self.RES)
        pygame.display.set_caption('Tictactoe')
        self.running = True
        self.bg_color = pygame.Color('darkslategray')
        self.clock = pygame.time.Clock()
        self.boardscale = 3
        self.selected = None

        self.restart_button = Button(self.win, (675, 380, 160, 50), state=1,
                                  color=WHITEW, corner_radius=10, hover_color=GREENW, disabled_color=GRAY,
                                  font=font_render('f_2', 30), font_values=("RESTART", 30, BLACK))

    def create_gui(self):
        self.win.blit(font_render('f_2').render('TIC TAC TOE', 1, pygame.Color('white')), (260,20))
        self.win.blit(font_render('f_1').render('WINNER: ', 1, pygame.Color("#d78f49")), (590,150))
        self.win.blit(font_render('f_1').render('TURN: ', 1, pygame.Color("#d78f49")), (70,150))
        self.win.blit(font_render('f_2').render(f"{f'Player1 {self.board.symbol[self.board.mark_dict[self.board.turn]]}' if self.board.turn == 'p1' else f'Player2 {self.board.symbol[self.board.mark_dict[self.board.turn]]}'}",
                                                1, pygame.Color("#ffe1e1")), (10, 200))
        _ = {'p1': 'Player 1', 'p2': 'Player 2', None: 'None', 'Draw': 'Draw'}
        self.win.blit(font_render('f_2').render(f'{_[self.board.winner]}', 1, pygame.Color("#ffe1e1")), (590,200))
        self.restart_button.draw()

    def draw(self):
        self.win.fill(self.bg_color)
        self.create_gui()
        self.drawboard()
        self.drawselected()
        self.renderboard(self.board_dict)
        self.drawwinningline()

    def run(self):
        while self.running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                self.running = False
            self.draw()
            self.board.debugmain(self.selected)
            self.selected = None
            # debug(self.board_dict)
            self.restartf()
            self.update()

    def update(self):
        pygame.display.update()

    def toscreenres(self, x, y):
        return x + self.M_WIDTH, y + self.M_HEIGHT

    def drawboard(self):
        self.outline = pygame.Rect(0, 0, 100 * self.boardscale, 100 * self.boardscale)
        self.outline.center = self.toscreenres(0, 0)
        self.boardsq = pygame.Rect(0, 0, self.outline.width // 3, self.outline.height // 3)
        pygame.draw.rect(self.win, pygame.Color('white'), self.outline, 2)
        for i in range(3):
            for j in range(3):
                self.boardsq.x, self.boardsq.y = self.outline.x + self.boardsq.width * i, self.outline.y + self.boardsq.height * j
                pygame.draw.rect(self.win, pygame.Color('white'), self.boardsq, 1)

    def draw_cross(self, row, col):
        scale = -50
        crossrect = self.boardsq.copy()
        crossrect.x, crossrect.y = self.outline.x + crossrect.width * row, self.outline.y + crossrect.height * col
        crossrect = crossrect.inflate(scale, scale)

        coords = ((crossrect.topleft, crossrect.bottomright),
                  (crossrect.topright, crossrect.bottomleft))
        pygame.draw.aaline(self.win, pygame.Color('white'), *coords[0], 1)
        pygame.draw.aaline(self.win, pygame.Color('white'), *coords[1], 1)

    def draw_circle(self, row, col):
        scale = -50
        circlerect = self.boardsq.copy()
        circlerect.x, circlerect.y = self.outline.x + circlerect.width * row, self.outline.y + circlerect.height * col
        circlerect = circlerect.inflate(scale, scale)
        pygame.gfxdraw.aacircle(self.win, *circlerect.center, circlerect.width // 2, pygame.Color('white'))

    def get_mouse_pos(self):
        mx, my = pygame.mouse.get_pos()
        row, col = (mx - self.outline.x) // self.boardsq.width, (my - self.outline.y) // self.boardsq.width
        return (mx, my, row, col) if 2 >= row >= 0 and 2 >= col >= 0 else (mx, my, None, None)

    def drawselected(self):
        row, col = self.get_mouse_pos()[2:]
        self.hover_rect = pygame.Rect(0, 0, self.boardsq.width, self.boardsq.height)
        if row is not None and col is not None:
            self.hover_rect.x, self.hover_rect.y = self.outline.x + self.hover_rect.width * row, self.outline.y + self.hover_rect.height * col
            if pygame.mouse.get_pressed()[0] and self.selected is None:
                self.selected = (row, col)
                pygame.draw.rect(self.win, pygame.Color('green'), self.hover_rect, 3)
            else:
                pygame.draw.rect(self.win, pygame.Color('yellow'), self.hover_rect, 3)

    def renderboard(self, board_dict):
        for pos, ele in board_dict.items():
            if ele == 'cross':
                self.draw_cross(*pos)
            elif ele == 'circle':
                self.draw_circle(*pos)

    def get_boardsqrect_dict(self):
        d = {}
        boardsq = pygame.Rect(0, 0, self.outline.width // 3, self.outline.height // 3)
        for i in range(3):
            for j in range(3):
                _boardsq = pygame.Rect(self.outline.x + boardsq.width * i, self.outline.y + boardsq.height * j,
                                       self.outline.width // 3, self.outline.height // 3)
                d[i, j] = _boardsq
        return d

    def drawwinningline(self):
        d = self.get_boardsqrect_dict()
        if self.board.winningset:
            coords = d[self.board.winningset[0]].center, d[self.board.winningset[2]].center
            pygame.draw.line(self.win, pygame.Color('red'), *coords, 5)

    def restartf(self):
        if self.restart_button.get_action():
            self.board.restart()
            self.board_dict = self.board.board_dict
