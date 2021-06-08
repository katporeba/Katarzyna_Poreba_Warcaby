import pygame
from warcabyGra.warcabyZmienne import WHITE_IMG, BLACK_IMG, WHITE_KING_IMG, BLACK_KING_IMG

''' Klasa pionka - umożliwiająca jego tworzenie oraz rysowanie '''

class Piece:
    def __init__(self, color, row, col):
        self._color = color 
        self._row = row
        self._col = col
        # określenie zdjęcia wyświetlanego na planszy
        if color == "black":
            self._imageAdress = BLACK_IMG
        elif color == "white":
            self._imageAdress = WHITE_IMG
        self._myImage = pygame.image.load(self._imageAdress)

    # Metody pozwalające na działanie na prywatnych własnościach obiektu
    def drawPiece(self, win, xCoord, yCoord):
        win.blit(self._myImage, (xCoord+5, yCoord+5))
    
    def getRow(self):
        return self._row

    def getCol(self):
        return self._col
    
    def getColor(self):
        return self._color
    
    def changeRowAndCol(self, row, col):
        self._row = row
        self._col = col

    def __repr__(self) -> str:
        return self.getColor()

''' Klasa króla dziedzicząca po klasie pionek - umożliwiająca jego tworzenie '''

class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        if color == "black":
            self._imageAdress = BLACK_KING_IMG
        elif color == "white":
            self._imageAdress = WHITE_KING_IMG
        self._myImage = pygame.image.load(self._imageAdress)

