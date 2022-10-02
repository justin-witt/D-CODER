__license__ = "https://unlicense.org/"
__version__ = "0.0.0"
__author__ = "Justin Witt"

import logging

class Pairs:
    """Retrieves pairs of "opener" and "closers" such as parentheses, brackets, etc.
    """
    
    __PAIRS = {
        "{":"}",
        "[":"]",
        "<":">",
        "(":")"
        }
    __check=None
    
    def getPairs(self, phrase:str) -> list:
        """returns a list of all bracket like opening and closing indexes grouped into pairs
        
            Args:
                phrase:str - string to check for pairs
        """

        self.__check = phrase
        results=[]
        for i in range(len(self.__check)-1):
            if self.validOpener(i):
                closer = self.getCloser(i)
                if not (closer == -1):
                    results.append([i,closer])
        return results
    
    def validOpener(self, index:int) -> bool:
        return self.__check[index] in self.__PAIRS
    
    def getCloser(self, index:int) -> int:
        """return the index of the closer for a pair
        
            Args:
                index:int - index of opener
        """

        new = 0
        for i in range(index+1, len(self.__check)):
            if self.__check[i] == self.__check[index]:
                new+=1
            elif self.__check[i] == self.__PAIRS[self.__check[index]]:
                if not new: return i + 1
                else: new-=1
        return -1

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info(f" LICENSE: {__license__} AUTHOR: {__author__} VERSION: {__version__}")
