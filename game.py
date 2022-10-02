__license__ = "https://unlicense.org/"
__version__ = "0.0.0"
__author__ = "Justin Witt"

import board, logging

class Game:
    #Default board size
    ROWS = 18
    COLS = 70

    def __init__(self) -> None:
        self.board = board.Board(self.ROWS, self.COLS)
        self.password = self.board.newBoard()
        self.attempts = 4

    def newGame(self) -> None:
        self.password = self.board.newBoard()
        self.attempts = 4

    def select(self) -> tuple:
        choice = self.board.cursor.select()
        common = -1
        if choice == "r":
            self.attempts = 4
        elif choice == "w" or choice == "l":
            pass
        else:
            common = self.__wordCheck(choice)
        return choice, common

    def __wordCheck(self, word:str) -> int:
        """returns the number of chars that share indexs in two strings

            Args:
                word:str - word to compare against password
        """

        r = 0
        for i in range(len(word)):
            try:
                if self.password[i]==word[i]: r+= 1
            except IndexError:
                break  
        return r

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info(f" LICENSE: {__license__} AUTHOR: {__author__} VERSION: {__version__}")
