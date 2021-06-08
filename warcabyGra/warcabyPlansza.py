import pygame
from warcabyGra.warcabyZmienne import ROWS, COL, TEXT_DARK, TEXT_LIGHT, WIDTH, HEIGHT, SQUARE_SIZE, DARK, LIGTH, PADDING, font, COLOR, FRAME, BACKGROUND, BUTTON_COORD
from warcabyGra.warcabyPionek import King, Piece

''' Klasa planszy - umożliwiająca jej tworzenie oraz rysowanie '''

class CheckersBoard:
    def __init__(self):
        self._piecesOnBoard = [] 
        self._whitePieces = 0
        self._blackPieces = 0
        self._colorTurn = "white"
        self._endGame = False
        
    def drawCheckersBoard(self, win):

        ''' Metoda ta rysuje planszę - jej obramówkę (zdjęcie FRAME) oraz kratkę '''

        myImage = pygame.image.load(FRAME)
        win.fill(BACKGROUND)
        pygame.draw.rect(win, BACKGROUND, (0, 0, WIDTH+(PADDING*2), HEIGHT+(PADDING*2)))
        win.blit(myImage, (PADDING/2, PADDING/2))
        pygame.draw.rect(win, DARK, (PADDING, PADDING, WIDTH, HEIGHT))
        for row in range(ROWS):
            for col in range(row % 2, COL, 2):
                pygame.draw.rect(win, LIGTH, (row*SQUARE_SIZE+PADDING, col *SQUARE_SIZE+PADDING, SQUARE_SIZE, SQUARE_SIZE))

    def drawFirstPieces(self, win):

        ''' Metoda przygotowująca pierwsze rozstawienie pionków na planszy. Jest to standardowy wariat opisany w linku dołączonym do dokumentacji. '''
        self._whitePieces = 0
        self._blackPieces = 0
        for i in range(ROWS):
            self._piecesOnBoard.append([])
            for j in range(COL):
                if (j+i)%2 == 0:
                    if i < 3:
                        # tworzenie białych obiektów klasy Piece oraz zapisywanie ich tablicy self.piecesOnBoard, która jest modyfikowana z każdym ruchem
                        tmpPiece = Piece("white", i, j)
                        self._piecesOnBoard[i].append(tmpPiece)
                        self._whitePieces += 1
                        tmpX, tmpY = self.piecePlace(i, j)
                        tmpPiece.drawPiece(win, tmpX, tmpY)
                    elif i > 4:
                        # tworzenie czarnych obiektów klasy Piece oraz zapisywanie ich tablicy self.piecesOnBoard
                        tmpPiece = Piece("black",  i, j)
                        self._piecesOnBoard[i].append(tmpPiece)
                        self._blackPieces +=1
                        tmpX, tmpY = self.piecePlace(i, j)
                        tmpPiece.drawPiece(win, tmpX, tmpY)
                    else: 
                        # resztę planszy wypełniamy wartościamy string "null"
                        self._piecesOnBoard[i].append("null")
                else: 
                    self._piecesOnBoard[i].append("null")

    def drawPieces(self, win):

        ''' Metoda ta wykorzystywana jest do ponownego rysowania pionków na planszy po każdej zmianie.
            Nie są one tu inicjalizowane.  '''

        for i in range(ROWS):
            for j in range(COL):
                if isinstance(self._piecesOnBoard[i][j], Piece):
                    tmpX, tmpY = self.piecePlace(i, j)
                    self._piecesOnBoard[i][j].drawPiece(win, tmpX, tmpY)
        self.drawTurn(win, self._colorTurn)
        self.drawPiecesAvailable(win, self.returnCount())
        self.drawTitleAndButton(win)


    def drawTurn(self, win, color):

        ''' Metoda ta wykorzystywana jest do wyświetlania tur zawodników - aktualna tura wyświetlana jest za pomocą jaśniejszego koloru  '''

        # przygotowujemy tekst dla tury koloru białego
        if color=="white":
            text2 = font.render("Tura zawodnika nr 1", True, TEXT_LIGHT)
            text = font.render("Tura zawodnika nr 2", True, TEXT_DARK)
        # przygotowujemy tekst dla tury koloru czarnego
        else:
            text2 = font.render("Tura zawodnika nr 1", True, TEXT_DARK)
            text = font.render("Tura zawodnika nr 2", True, TEXT_LIGHT)
        # wyświetlamy tekst na ekranie
        textRect = text.get_rect()
        textRect.center = (WIDTH + PADDING*8, PADDING*2)
        textRect2 = text.get_rect()
        textRect2.center = (WIDTH + PADDING*8, HEIGHT)
        win.blit(text, textRect)
        win.blit(text2, textRect2)

    def drawMoveNotPossible(self, win):

        ''' Metoda ta wykorzystywana jest do wyświetlania informacji o niedozwolonym ruchu  '''

        font2 = pygame.font.SysFont('Lato', 20)
        text = font2.render("Ruch niedozwolony", True, COLOR)
        textRect = text.get_rect()
        textRect.center = (WIDTH + PADDING*8, HEIGHT+35)
        win.blit(text, textRect)

    def drawTitleAndButton(self, win):

        ''' Metoda ta wykorzystywana jest do wyświetlania informacji - dodatkowego tytułu oraz przycisku do resetu gry  '''

        font1 = pygame.font.SysFont('PalatinoLinotype', 80)
        font2 = pygame.font.SysFont('PalatinoLinotype', 50)
        font3 = pygame.font.SysFont('Lato', 30)
        text3 = font1.render("Projekt", True, DARK)
        text = font2.render("WARCABY", True, LIGTH)
        text2 = font3.render("Restart gry", True, LIGTH)
        textRect3 = text.get_rect()
        textRect = text.get_rect()
        textRect2 = text.get_rect()
        textRect.center = (WIDTH + PADDING*8, HEIGHT//2)
        textRect2.center = BUTTON_COORD
        textRect3.center = (WIDTH + PADDING*8, HEIGHT//2-70)

        pygame.draw.rect(win, DARK, pygame.Rect(BUTTON_COORD[0]-150, BUTTON_COORD[1]-30, 200, 50), 25, 3)

        win.blit(text3, textRect3)
        win.blit(text, textRect)
        win.blit(text2, textRect2)


    def drawPiecesAvailable(self, win, count):

        ''' Metoda ta wykorzystywana jest do wyświetlania informacji o ilości dostępnych pionków dla poszczególnych kolorów  '''

        black, white = count
        endComment = lambda color : f'Pionki {color}'
        font2 = pygame.font.SysFont('Lato', 15)
        font3 = pygame.font.SysFont('Lato', 70)
        text = font2.render(endComment('czarne'), True, COLOR)
        text4 = font3.render(str(white), True, COLOR)
        text2 = font2.render(endComment('białe'), True, COLOR)
        text3 = font3.render(str(black), True, COLOR)
        textRect = text.get_rect()
        textRect2 = text2.get_rect()
        textRect3 = text3.get_rect()
        textRect4 = text4.get_rect()
        textRect.center = (WIDTH + PADDING*8, PADDING*2+35)
        textRect2.center = (WIDTH + PADDING*8, HEIGHT-35)
        textRect3.center = (WIDTH + PADDING*8, PADDING*2+85)
        textRect4.center = (WIDTH + PADDING*8, HEIGHT-85)
        win.blit(text, textRect)
        win.blit(text2, textRect2)
        win.blit(text3, textRect3)
        win.blit(text4, textRect4)

    def choosePiece(self, win, row, col):

        ''' Metoda zaznaczająca kwadrat na szachownicy na inny kolor '''

        tmpX, tmpY = self.piecePlace(row, col)
        pygame.draw.rect(win, COLOR, (tmpX, tmpY, SQUARE_SIZE, SQUARE_SIZE))

    def makeDot(self, win, row, col):

        ''' Metoda tworząca kolorową kropkę na danym polu '''

        tmpX, tmpY = self.piecePlace(row, col)
        pygame.draw.circle(win, COLOR, (tmpX+SQUARE_SIZE/2, tmpY+SQUARE_SIZE/2), 20)

    def piecePlace(self, row, col):

        ''' Metoda obliczająca koordynaty x oraz y '''

        tmpX = col*SQUARE_SIZE+PADDING
        tmpY = (ROWS - row - 1)*SQUARE_SIZE+PADDING
        return tmpX, tmpY

    def drawEnd(self, win):

        ''' Metoda wyświetlająca informacje o wygranej'''
        endComment = lambda color: f'Wygrał gracz {color}'
        font = pygame.font.SysFont('Lato', 30)
        if self._whitePieces == 0:
            text = font.render(endComment(1), True, COLOR)
        else:
            text = font.render(endComment(2), True, COLOR)
        textRect = text.get_rect()
        textRect.center = (WIDTH + PADDING*8, HEIGHT-200)
        win.blit(text, textRect)


    # Metody pozwalające na działanie na prywatnych własnościach obiektu
    
    def removePiece(self, color, win):
        if color=="white":
            self._whitePieces -= 1
        else:
            self._blackPieces -= 1
        if self._whitePieces == 0 or self._blackPieces == 0:
            self._endGame = True
            self.drawEnd(win)

    def getPieces(self):
        return self._piecesOnBoard

    def getPieceWithCoord(self, row, col):
        return self._piecesOnBoard[row][col]

    def changePiece(self, row, col, piece):
        self._piecesOnBoard[row][col] = piece

    def getColorTurn(self):
        return self._colorTurn

    def getCountOfPieces(self):
        return self._whitePieces, self._blackPieces
    
    def getEndGame(self):
        return self._endGame

    def returnCount(self):
        return self._whitePieces, self._blackPieces
    
    def changeType(self, type):
        self._colorTurn = type
    
    # Dodatkowe metody dla testów jednostkowych 
    
    def nulls(self):
        self._whitePieces = 0
        self._blackPieces = 0
        for i in range(ROWS):
            self._piecesOnBoard.append([])
            for j in range(COL):
                self._piecesOnBoard[i].append("null")

    def drawPiecesTestFour(self):
        ''' Metoda przygotowująca pierwsze rozstawienie pionków na planszy dla testu jednostkowego nr 4'''
        self.nulls()

        tmpPiece = Piece("white", 0, 0)
        self._piecesOnBoard[0][0] = tmpPiece
        self._whitePieces += 1

        tmpPiece = Piece("black", 1, 1)
        self._piecesOnBoard[1][1] = tmpPiece
        self._blackPieces += 1

        tmpPiece = Piece("black", 3, 3)
        self._piecesOnBoard[3][3] = tmpPiece
        self._blackPieces += 1

    def drawPiecesTestFifth(self):
        ''' Metoda przygotowująca pierwsze rozstawienie pionków na planszy dla testu jednostkowego nr 5'''
        self.nulls()

        tmpPiece = Piece("white", 6, 6)
        self._piecesOnBoard[6][6] = tmpPiece
        self._whitePieces += 1

    def drawPiecesTestSixth(self):
        ''' Metoda przygotowująca pierwsze rozstawienie pionków na planszy dla testu jednostkowego nr 6'''
        self.nulls()
       
        tmpPiece = Piece("white", 6, 6)
        self._piecesOnBoard[6][6] = tmpPiece
        self._whitePieces += 1

        tmpPiece = Piece("black", 2, 2)
        self._piecesOnBoard[2][2] = tmpPiece
        self._blackPieces += 1

    def drawPiecesTestSeventh(self):
        ''' Metoda przygotowująca pierwsze rozstawienie pionków na planszy dla testu jednostkowego nr 7'''
        self.nulls()
       
        tmpPiece = Piece("white", 2, 2)
        self._piecesOnBoard[2][2] = tmpPiece
        self._whitePieces += 1

        tmpPiece = Piece("black", 3, 3)
        self._piecesOnBoard[3][3] = tmpPiece
        self._blackPieces += 1

