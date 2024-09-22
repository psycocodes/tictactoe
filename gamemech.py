# Making the tic-tac-toe game 2 player
import pygame


class Game:
    def __init__(self, mode, render=pygame.display.get_surface()):
        self.render = render
        self.board = [[[] for j in range(3)] for i in range(3)]
        self.mode = mode
        self.board_dict = {}
        self.init()
        self.turn = 'p1'
        self.mark_dict = {'p1': 'cross', 'p2': 'circle'}
        self.player_dict = dict(zip(self.mark_dict.values(), self.mark_dict.keys()))
        self.player_dict[None] = 'None'
        self.symbol = {'cross': 'X', 'circle': 'O'}
        self.winner = None
        self.game_over = False
        self.winningset = []

    def init(self):
        for row, i in enumerate(self.board):
            for col, j in enumerate(i):
                self.board_dict[row, col] = j

    def _debug(self):
        return self.board_dict, self.board

    def change_mode(self, mode):
        self.mode = mode

    def player_move(self, pos):
        if pos in self.valid_moves():
            self.board_dict[pos] = self.mark_dict[self.turn]
            self.board[pos[0]][pos[1]] = self.mark_dict[self.turn]
            self.winner = self.is_winner()
            self.turn = 'p1' if self.turn == 'p2' else 'p2'
            self.game_over = False if self.winner is None else True

    def valid_moves(self):
        return [pos for pos, ele in self.board_dict.items() if ele == []]

    def is_winner(self):
        if not self.board_full():
            if self._diagonal_check()[0]:
                return self.player_dict[self._diagonal_check()[1]]
            elif self._row_check()[0]:
                return self.player_dict[self._row_check()[1]]
            elif self._col_check()[0]:
                return self.player_dict[self._col_check()[1]]
            else:
                return None
        else:
            return "Draw"

    def empty(self, seqofpos):
        for pos in seqofpos:
            if self.board_dict[pos] == []:
                return False
        else:
            return True

    def _diagonal_check(self):
        if self.empty([(0, 0), (1, 1), (2, 2)]) and (
                self.board_dict[(0, 0)] == self.board_dict[(1, 1)] == self.board_dict[(2, 2)]):
            self.winningset = [(0, 0), (1, 1), (2, 2), 'd']
            return True, self.board_dict[(1, 1)]
        elif self.empty([(2, 0), (1, 1), (0, 2)]) and (
                self.board_dict[(2, 0)] == self.board_dict[(1, 1)] == self.board_dict[(0, 2)]):
            self.winningset = [(2, 0), (1, 1), (0, 2), 'd']
            return True, self.board_dict[(1, 1)]
        return False, None

    def _row_check(self):
        if self.empty([pos for pos in self.board_dict.keys() if pos[0] == 0]) and (
                self.board_dict[(0, 0)] == self.board_dict[(0, 1)] == self.board_dict[(0, 2)]):
            self.winningset = [(0, 0), (0, 1), (0, 2), 'r']
            return True, self.board_dict[(0, 0)]
        elif self.empty([pos for pos in self.board_dict.keys() if pos[0] == 1]) and (
                self.board_dict[(1, 0)] == self.board_dict[(1, 1)] == self.board_dict[(1, 2)]):
            self.winningset = [(1, 0), (1, 1), (1, 2), 'r']
            return True, self.board_dict[(1, 0)]
        elif self.empty([pos for pos in self.board_dict.keys() if pos[0] == 2]) and (
                self.board_dict[(2, 0)] == self.board_dict[(2, 1)] == self.board_dict[(2, 2)]):
            self.winningset = [(2, 0), (2, 1), (2, 2), 'r']
            return True, self.board_dict[(2, 0)]
        return False, None

    def _col_check(self):
        if self.empty([pos for pos in self.board_dict.keys() if pos[1] == 0]) and (
                self.board_dict[(0, 0)] == self.board_dict[(1, 0)] == self.board_dict[(2, 0)]):
            self.winningset = [(0, 0), (1, 0), (2, 0), 'c']
            return True, self.board_dict[(0, 0)]
        elif self.empty([pos for pos in self.board_dict.keys() if pos[1] == 1]) and (
                self.board_dict[(0, 1)] == self.board_dict[(1, 1)] == self.board_dict[(2, 1)]):
            self.winningset = [(0, 1), (1, 1), (2, 1), 'c']
            return True, self.board_dict[(0, 1)]
        elif self.empty([pos for pos in self.board_dict.keys() if pos[1] == 2]) and (
                self.board_dict[(0, 2)] == self.board_dict[(1, 2)] == self.board_dict[(2, 2)]):
            self.winningset = [(0, 2), (1, 2), (2, 2), 'c']
            return True, self.board_dict[(0, 2)]
        return False, None

    def board_full(self):
        if [] not in self.board_dict.values():
            return True
        return False

    def printboard(self):
        for _ in self.board:
            for box in _:
                if box != []:
                    print(self.symbol[box], sep='|', end='   ')
                else:
                    print('[]', sep='|', end='  ')
            print()
            print('----------')

    def debugmain(self, inputvar):
        if inputvar is not None and self.winner is None:
            self.player_move(inputvar)

    def restart(self):
        self.board = [[[] for j in range(3)] for i in range(3)]
        self.board_dict = {}
        self.winningset = []
        self.winner = None
        self.turn = 'p1'
        self.game_over = False
        self.init()
