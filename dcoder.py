__license__ = "https://unlicense.org/"
__version__ = "0.0.0"
__author__ = "Justin Witt"

import curses, ui, game
from curses import wrapper

class DCODER:

    def __init__(self, u, g) -> None:
        self.u = u
        self.g = g
        
        self.g.newGame()
        
        self.MOVES = {
        450:self.up, 
        119:self.up,
        119-32:self.up,
        259:self.up,
        456:self.down, 
        115:self.down, 
        115-32:self.down,
        258:self.down,
        452:self.left,
        97:self.left,
        97-32:self.left,
        260:self.left, 
        454:self.right, 
        100:self.right,
        100-32:self.right,
        261:self.right,
        10:self.select,
        32:self.select,
        459:self.select
        }

    def gameLoop(self, stdscrn):
        move = 0
        while move != 3:
            curses.curs_set(0)
            limits = stdscrn.getmaxyx()
            middle = [round(i / 2) for i in limits]
            self.u.updateAll(stdscrn, middle)
            stdscrn.refresh()
            move = stdscrn.getch()
            stdscrn.clear()
            output = None
            try:
                output = self.MOVES[move](middle)
            except Exception:
                pass
            if output:
                #ADVANTAGE HANDLER
                if output[1] == -1:
                    if output[0] == "r":
                        self.g.attempts = 4
                        self.u.notiFeed("Attempts reset")
                    elif output[0] == "w":
                        self.u.notiFeed("Lemon removed")
                    elif output[0] == "l":
                        self.u.notiFeed("Unlucky Lemon")
                #WON HANDLER
                elif output[1] == len(self.g.password):
                    self.u.gameOver(stdscrn, middle, True)
                    self.g.newGame()
                    move = stdscrn.getch()
                #EVERYTHING ELSE
                elif output[1] == -2:
                    pass
                else:
                    self.u.notiFeed(f"{output[0]}: {output[1]}/{len(self.g.password)}")
                    self.g.attempts -= 1
                #LOST HANDLER
                if self.g.attempts == 0:
                    self.u.gameOver(stdscrn, middle, False)
                    self.g.newGame()
                    move = stdscrn.getch()

    def up(self, middle):
        self.g.board.cursor.up()
        return [None, -2]
    
    def down(self, middle):
        self.g.board.cursor.down()
        return [None, -2]
    
    def left(self, middle):
        self.g.board.cursor.left()
        return [None, -2]
    
    def right(self, middle):
        self.g.board.cursor.right()
        return [None, -2]

    def select(self, middle):
        output = self.g.select()
        return output

def main(stdscrn):
    g = game.Game()
    u = ui.UI(g)
    d = DCODER(u, g)
    d.gameLoop(stdscrn)

if __name__ == '__main__':
    wrapper(main)
