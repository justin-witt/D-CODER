__license__ = "https://unlicense.org/"
__version__ = "0.0.0"
__author__ = "Justin Witt"

import logging
from curses import A_REVERSE

class UI:
    def __init__(self, game) -> None:
        self.game = game 
        self.feed = []
    
    def updateAll(self, stdscrn, middle):
        self.updateBoard(stdscrn, middle)
        self.highlight(stdscrn, middle)
        self.updateFeed(stdscrn, middle)
        self.updateAttempts(stdscrn, middle)

    def updateBoard(self, stdscrn, middle):
        y = middle[0] - (round(self.game.ROWS / 2))
        x = middle[1] - (round(self.game.COLS / 2))
        start = 0
        stop = self.game.COLS
        for i in range(self.game.ROWS):
            stdscrn.addstr(y + i, x, self.game.board.toString()[start:stop])
            start=stop
            stop += self.game.COLS
        
    def highlight(self, stdscrn, middle):
        ystart, xstart = middle
        xstart -= round(self.game.COLS / 2)
        ystart -= round(self.game.ROWS / 2)
        y, x = divmod(self.game.board.cursor.loc, self.game.COLS)
        board = self.game.board.board
        cloc = self.game.board.cursor.loc
        stdscrn.addstr(ystart+y, xstart+x, "".join(i.val for i in board[cloc:cloc+board[cloc].length]), A_REVERSE)

    def updateFeed(self, stdscrn, middle):
        y, x = middle
        y += round(self.game.ROWS / 2) - 3
        x += round(self.game.COLS / 2) + 1
        #THIS IS JUST THE CONCEPT NEED TO DO MORE WORK
        for i in self.feed[::-1]:
            stdscrn.addstr(y, x, i)
            y -= 1

    def updateAttempts(self, stdscrn, middle):
        y, x = middle
        y += round(self.game.ROWS / 2) - 1
        x += round(self.game.COLS / 2) + 1
        stdscrn.addstr(y, x, f"Attempts: {self.game.attempts}")

    def notiFeed(self, notif):
        self.feed.append(notif)
        if len(self.feed) == 6:
            self.feed.pop(0)

    def gameOver(self, stdscrn, middle, result:bool):
        y, x = middle
        over = "GAME OVER"
        self.feed = []
        prompt = "WINNER" if result else "LOSER"
        stdscrn.addstr(y, x - round(len(over) / 2), over)
        stdscrn.addstr(y + 1, x - round(len(prompt) / 2), prompt)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info(f" LICENSE: {__license__} AUTHOR: {__author__} VERSION: {__version__}")
