from graphics import GameGraphics
from _debug import debug
from gamemech import Game

def main():
    game = Game('p2p')
    window = GameGraphics(game)
    window.run()

if __name__ == '__main__':
    main()