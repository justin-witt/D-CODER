__license__ = "https://unlicense.org/"
__version__ = "0.0.0"
__author__ = "Justin Witt"

import random, gamewords, logging
from finder import Pairs

class Board:
    #Chars used to generate the board
    FILLERS = ["/","\\","{","}","[","]","<",">","(",")",".",",","`","~",";","@","$","%","^","&","*","+","-","#","!","?"]
    DIFFICULTIES = {"easy":gamewords.FIVE}

    def __init__(self, rows:int, cols:int) -> None:
        self.ROWS = rows
        self.COLS = cols
        #Add difficulty settings later using this area of board maybe try and figure out better workaround
        self.difficulty = self.DIFFICULTIES["easy"]
        self.board = []
        self.lemons = {}
        self.cursor = Cursor(self)

    def newBoard(self) -> str:
        """generates new game board, resets required vars and returns the "password"
        """
        self.__clearBoard()
        password = self.__genBoard().upper()
        self.cursor.loc = 0
        self.cursor.stop = len(self.board)
        return password

    def __genBoard(self) -> str:        
        #populate the board with "clutter"
        for _ in range(self.ROWS*self.COLS):
            choice=random.choice(self.FILLERS)
            self.board.append(Pawn(choice, 1, 0))
        
        password = self.__addWords()
        #find and set length of each valid pair of openers and closers
        finder = Pairs()
        pairs = []
        prev = 0

        for i in range(self.COLS, (self.ROWS*self.COLS)+self.COLS, self.COLS):
            temp = finder.getPairs("".join(n.val for n in self.board[prev:i]))
            temp = [[x+prev, y+prev] for x, y in temp]
            pairs = pairs + temp
            prev = i

        for i in pairs:
            self.board[i[0]].length = i[1] - i[0]
        
        return password

    def __addWords(self) -> str:

        def placeWords(n:int, row:int) -> None:
            ROW_START = row*self.COLS
            WORD_LENGTH = len(words[0])
            STEP = round(self.COLS / n)

            start = ROW_START
            stop = start + STEP

            for _ in range(1,n+1):
                word_placement = random.randint(start, stop - WORD_LENGTH)
                word = words.pop()
                added.append([word, word_placement])
                
                for i in range(WORD_LENGTH):
                    self.board[word_placement+i] = Pawn(word[i].upper(), WORD_LENGTH, i)
                    self.board[word_placement+i].isWord = True
                start+=STEP
                stop+=STEP

        # LOW/HIGH sets min/max words to place per row
        LOW = 1
        HIGH = 3

        #This area will need some work to be able to add difficulty levels
        words = gamewords.FIVE.copy()
        random.shuffle(words)
        added = []

        for i in range(self.ROWS):
            placeWords(random.randint(LOW,HIGH), i)

        password=added.pop(random.randrange(len(added)))[0]
        self.lemons = {i[0]:i[1] for i in added}
        return password

    def __clearBoard(self) -> None:
        self.board = []

    def toString(self) -> str:
        """returns a string version of the gameboard"""
        return "".join(pawn.val for pawn in self.board)

    def readableBoard(self) -> None:
        """prints a readable version of a game board
        """
        string_board = self.toString()
        start = 0
        stop = self.COLS
        for _ in range(self.ROWS):
            print(string_board[start:stop])
            start=stop
            stop+=self.COLS

class Cursor:
    def __init__(self, board:Board) -> None:
        self.__board = board
        self.stop = len(self.__board.board)
        self.loc = 0

    def select(self) -> str:
        start = self.__board.board[self.loc]
        
        if start.isWord or start.length == 1:
            return self.__selectWord()
        else:
            return self.__selectAdv()

    def __selectWord(self) -> str:
        """gets the selected word or char from board and returns it as a string
        """
        output = ""

        for i in range(self.__board.board[self.loc].length):
            output += self.__board.board[self.loc + i].val
        
        return output

    def __removeSelected(self, index) -> None:
        r = self.__board.board[index]
        if r.isWord:
            for i in range(r.length):
                self.__board.board[index+i].val = "."
                self.__board.board[index+i].index = 0
                self.__board.board[index+i].length = 1
        else:
            self.__board.board[index+r.length-1].val = "."
            r.val = "."
            r.length = 1

    def __selectAdv(self) -> str:
        self.__removeSelected(self.loc)
        roll = random.random()
        if roll < .1:
            return "r"
        elif roll < .5:
            return self.__lemonAdv()
        else:
            return "l"

    def __lemonAdv(self) -> str:
        c = random.choice([i for i in self.__board.lemons])
        self.__removeSelected(self.__board.lemons[c])
        del(self.__board.lemons[c])
        return "w"

    def up(self) -> None:
        move = self.loc-self.__board.COLS
        self.loc = move if self.validMove(move) else self.loc
        self.loc -= self.__board.board[self.loc].index

    def down(self) -> None:
        move = self.loc+self.__board.COLS
        self.loc = move if self.validMove(move) else self.loc
        self.loc -= self.__board.board[self.loc].index

    def left(self) -> None:
        move=self.loc-1
        self.loc = move if self.validMove(move) else self.loc
        self.loc -= self.__board.board[self.loc].index

    def right(self) -> None:
        jump = 1 if not self.__board.board[self.loc].isWord else self.__board.board[self.loc].length
        move=self.loc+jump
        self.loc = move if self.validMove(move) else self.loc
        self.loc -= self.__board.board[self.loc].index

    def validMove(self, pos) -> bool:
        return not (pos < 0 or pos >= self.stop)

class Pawn:
    def __init__(self, val: int, length: int, index: int) -> None:
        self.val = val
        self.length = length
        self.index = index
        self.isWord = False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info(f" LICENSE: {__license__} AUTHOR: {__author__} VERSION: {__version__}")
