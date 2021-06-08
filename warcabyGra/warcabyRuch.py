import pygame
import math
from warcabyGra.warcabyPlansza import CheckersBoard
from warcabyGra.warcabyPionek import Piece, King
from warcabyGra.warcabyZmienne import ROWS, COL, PADDING, HEIGHT, WIDTH

''' Klasa umożliwiająca sterowanie grą '''

class movePiece:
    def __init__(self):
        self._board = CheckersBoard() 
        self._piecesOnBoard = self._board.getPieces() 
        self._selectedPiece = 0 # pionek który przenosimy lub dla którego sprawdzamy możliwe ruchy
        self._possibleMovesNull = [] # lista wykorzystywana do uzyskania informacji o możliwych ruchach na wolne miejsca (bez zbijania pionków)
        self._nulls = [] # lista wykorzystywana do uzyskania informacji w które miejsce należy przenieść pionek (podczas zbijania innych)
        self._piecesToRemove = [] # lista wykorzystywana do uzyskania informacji które pionki zostają zbite
        self._upperPiece = [] # lista wykorzystywana do uzyskania informacji o poprzednikach zbijanego pionka

    def prepareData(self, win, x, y):

        ''' Metoda przyjmująca koordynaty zdarzenia - MOUSEBUTTONDOWN oraz zamieniająca je na odpowiednie wiersze oraz kolumny.
            Następnie sprawdzana jest możliwość ruchu dla danego pionka. '''

        tmpCol = math.ceil((x-PADDING)/(WIDTH/COL)) - 1
        tmpRow = ROWS - math.ceil((y-PADDING)/(HEIGHT/ROWS))
        if tmpRow < ROWS and tmpRow > -1 and tmpCol < COL and tmpCol > -1:
            tmpPiece = self._board.getPieceWithCoord(tmpRow, tmpCol)
            self.moveNormalPiece(win, tmpPiece, tmpRow, tmpCol)

    def moveNormalPiece(self, win, piece, row, col):

        ''' Metoda ta sprawdza czy podany element szachownicy jest jednym z poniższych:
                - pionkiem - w tym przypadku do list dodajemy jego możliwe ruchy
                - typem string o wartości "null" - czyli inaczej pustym na planszy miejscem - jest to ruch pionka bez zbicia innych
                - typem string o wartości "null", którego wiersz i kolumna znajdują się w liście self.nulls. Oznacza to, że aby przenieść pionek należy zbić inne pionki
                - czymś innym niż wspomniane powyżej - wyświetlana jest wtedy informacja o złym ruchu. '''

        # ---------------------------------------------------------------------------- #
        # Element jest instancji Piece - może to być pionek lub król
        # ---------------------------------------------------------------------------- #
        if isinstance(piece, Piece) and self._board.getEndGame() == False:
            # zerowanie list przechowywujących dane
            self._possibleMovesNull = []
            self._nulls = []
            self._piecesToRemove = []
            self._upperPiece = []
            # sprawdzamy czy możemy ruszac pionkiem w danej turze (decyduje o tym kiego kolor)
            if piece.getColor() == self._board.getColorTurn():
                self._selectedPiece = piece
                self._board.choosePiece(win, row, col)
                # dla obiektów instancji King wyszukujemy inaczej możliwe ruchy
                if isinstance(piece, King):
                    self.findPossible(piece, win, row, col, self.checkIfNullKing)
                else:
                    self.findPossible(piece, win, row, col, self.checkIfNull)
                    self.findPossible(piece, win, row, col, self.checkIfOpposite)

        # ---------------------------------------------------------------------------- #
        # Przenoszenie pionka na puste miejsce bez zbijania innych pionków  
        # ---------------------------------------------------------------------------- #
        elif str(row)+" "+str(col) in self._possibleMovesNull and self._board.getEndGame() == False:
            # sprawdzenie, czy pionek nie jest zamieniany na króla
            self._selectedPiece = self.changeToKing(self._selectedPiece, row, col)
            selectedRow = self._selectedPiece.getRow()
            selectedCol = self._selectedPiece.getCol()
            # zamiana pól w tablicy oraz zmienienie wartości pola row oraz col wybranemu pionkowi
            self._board.changePiece(row, col, self._selectedPiece)
            self._board.changePiece(selectedRow, selectedCol, "null")
            self._selectedPiece.changeRowAndCol(row,col)
            # zmiana tury
            self.oppositeColor()

        # ---------------------------------------------------------------------------- #
        # Przenoszenie pionka na nowe miejsce razem ze zbijaniem odpowiednich pionków 
        # ---------------------------------------------------------------------------- #
        elif str(row)+" "+str(col) in self._nulls and self._board.getEndGame() == False:
            # sprawdzenie, czy pionek nie jest zamieniany na króla 
            self._selectedPiece = self.changeToKing(self._selectedPiece, row, col)
            selectedRow = self._selectedPiece.getRow()
            selectedCol = self._selectedPiece.getCol()
            # zamiana pól w tablicy - pola pustego (z eventu) oraz pola na którym znajduje się pionek do przeniesienia
            self._board.changePiece(row, col, self._selectedPiece)
            self._board.changePiece(selectedRow, selectedCol, "null")
            # sprawdzenie które pionki również należy usunąć z planszy ( w przypadku kiedy przeskakujemy więcej niż jeden pionek)
            index = self._nulls.index(str(row)+" "+str(col))
            while 1:
                self._board.changePiece(self._piecesToRemove[index].getRow(), self._piecesToRemove[index].getCol(), "null")
                self._board.removePiece(self._board.getColorTurn(), win)
                # sprawdzamy poprzednika pionka - jeżeli jest to nasz wybrany pionek (selectedPiece) przerywamy pętlę
                tmpPiece = self._upperPiece[index]
                if tmpPiece.getRow() == self._selectedPiece.getRow() and tmpPiece.getCol() == self._selectedPiece.getCol():
                    break
                self._board.changePiece(tmpPiece.getRow(), tmpPiece.getCol(), "null")
                index -= 1
            # zmiana wartości pola row oraz col wybranemu pionkowi oraz zaaktualizowanie pozostałych na planszy pionków
            self._selectedPiece.changeRowAndCol(row,col)
            self._board.drawPiecesAvailable(win, self._board.returnCount())
            # zmiana tury
            self.oppositeColor()

        # ---------------------------------------------------------------------------- #
        # Wydrukowanie na ekranie informacji o złym ruchu
        # ---------------------------------------------------------------------------- #
        else:
            self._board.drawMoveNotPossible(win)
            if(self._board.getEndGame() == True):
                self._board.drawEnd(win)


    def findPossible(self, piece, win, row, col, fun):

        ''' Metoda odpowiedzialna za sprawdzenie odpowiednich pól na planszy dla danego pionka w zależności od jego koloru oraz typu '''
        
        # Sprawdzamy czy sąsiadujące pola spełniają warunek przekazany przez funkcję fun dla białych pionków lub króla 
        # Funkcja przekazywana jako argument fun to self.checkIfNull lub self.checkIfOpposite
        if self._board.getColorTurn() =="white" or isinstance(piece, King):
            if col+1<COL and row+1<ROWS:
                fun(piece, win, row+1, col+1)
            if col-1>-1 and row+1<ROWS: 
                fun(piece, win, row+1, col-1)

        # Sprawdzamy czy sąsiadujące pola spełniają warunek przekazany przez funkcję fun dla czarnych pionków lub króla 
        if self._board.getColorTurn() =="black" or isinstance(piece, King):
            if col+1<COL and row-1>-1:
                fun(piece, win, row-1, col+1)
            if col-1>-1 and row-1>-1:
                fun(piece, win, row-1, col-1)

    def findPossibleOnDiagonal(self, piece, win, row, col, fun):

        ''' Metoda ta odpowiedzalna jest za sprawdzenie czy dane pola spełniają warunek podany w funkcji ale jedynie po przekątnej 
            Funkcja ta jest wykorzystywana do sprawdzenia wszystkich możliwych pól zawierających wartość "null" dla obiektu instancji King '''

        if col+1<COL and row+1<ROWS and piece.getRow()-row<0 and piece.getCol()-col<0:
            fun(piece, win, row+1, col+1)
        if col-1>-1 and row+1<ROWS and piece.getRow()-row<0 and piece.getCol()-col>0: 
            fun(piece, win, row+1, col-1)
        if col+1<COL and row-1>-1 and piece.getRow()-row>0 and piece.getCol()-col<0:
            fun(piece, win, row-1, col+1)
        if col-1>-1 and row-1>-1 and piece.getRow()-row>0 and piece.getCol()-col>0:
            fun(piece, win, row-1, col-1)

    def checkIfNull(self, piece, win, row, col):

        ''' Metoda ta sprawdza czy dane pole zawiera wartość null - jeżeli tak dodawana jest wartość jego wiersza oraz kolumny do tablicy piecesOnBoard jako string 
            oraz na miejscu tego pola na planszy wyświetlana jest kropka - pokazuje to użytkownikowi potencjalny ruch. '''

        if self._board.getPieceWithCoord(row, col) == "null":
            self._possibleMovesNull.append(str(row)+" "+str(col))
            self._board.makeDot(win, row, col)

    def checkIfNullKing(self, piece, win, row, col):

        ''' Metoda ta sprawdza czy dane pole zawiera wartość null dla Króla - obiektu instancji King - jeżeli pole zawiera wartość null sprawdzamy kolejne pole po przekątnej.
            Jeżeli pole to jest pionkiem sprawdzamy czy jest możliwe jego zbicie przy pomocy funkcji self.checkIfOpposite.'''

        if self._board.getPieceWithCoord(row, col) == "null":
            self._possibleMovesNull.append(str(row)+" "+str(col))
            self._board.makeDot(win, row, col)
            self.findPossibleOnDiagonal(piece, win, row, col, self.checkIfNullKing)
        else:
            self.checkIfOpposite(piece, win, row, col)

    def checkIfOpposite(self, piece, win, row, col):

        ''' Metoda ta sprawdza czy możliwe jest zbicie danego pionka '''

        if isinstance(self._board.getPieceWithCoord(row, col), Piece) and self._board.getPieceWithCoord(row, col).getColor() != piece.getColor():
            # Obliczamy współrzędne dla kolejnego sprawdzanego pola - które aby zbić pionek musi zawierać wartość "null". Dzielenie to jest używane aby zapewnić poprawność danych
            # również w przypadku kiedy sprawdzamy pole dla króla - może on przeskakiwać kilka pól o wartości null, aby zbić pionka.
            calculate = lambda z, x: z+int(x/abs(x))
            calculatedRow = calculate(row, row-piece.getRow())
            calculatedCol = calculate(col, col-piece.getCol())
            if  -1 < calculatedRow < ROWS and -1 < calculatedCol < COL :
                if self._board.getPieceWithCoord(calculatedRow, calculatedCol) == "null":
                    # jeżeli wartość wynosi "null" dodajemy dane do odpowiednich tablic oraz wyświetlamy na planszy kropkę w jego miejscu
                    tmpPiece = Piece(piece.getColor(), calculatedRow, calculatedCol)
                    self._nulls.append(str(calculatedRow)+" "+str(calculatedCol))
                    self._piecesToRemove.append(self._board.getPieceWithCoord(row,col))
                    self._upperPiece.append(piece)
                    self._board.makeDot(win, calculatedRow, calculatedCol)
                    # sprawdzenie możliwości kolejnego przeskoku
                    self.findPossible(tmpPiece, win, calculatedRow, calculatedCol, self.checkIfOpposite)      

    def changeToKing(self, piece, row, col):

        ''' Metoda ta zwraca obiekt instancji króla (King) w przypadku, kiedy pionek o odpowiednim kolorze znajduje się na odpowiedniej granicy planszy. '''

        if piece.getColor() == "white" and row == ROWS-1 or piece.getColor() == "black" and row == 0:
            tmpPiece = King(piece.getColor(), piece.getRow(), piece.getCol())
            return tmpPiece
        else:
            return piece

    def oppositeColor(self):

        ''' Metoda zmieniająca turę '''

        if self._board.getColorTurn() == "white":
            self._board.changeType("black")
        else: 
            self._board.changeType("white")

    def drawBoard(self, win):

        ''' Metoda umożliwiająca dostęp do funkcji rysującej planszę '''

        self._board.drawCheckersBoard(win)
    
    def drawFirstPieces(self, win):

        ''' Metoda umożliwiająca dostęp do funkcji rysującej pierwsze rozmieszczenie pionków '''

        self._board.drawFirstPieces(win)
    
    def drawPieces(self, win):

        ''' Metoda umożliwiająca dostęp do funkcji rysującej ponownie pionki'''

        self._board.drawPieces(win)

    def restartGame(self, win):

        ''' Metoda umożliwiająca restart gry'''
        self._board = CheckersBoard()
        self._piecesOnBoard = self._board.getPieces() 
        self.drawBoard(win)
        self.drawFirstPieces(win)

    # Dodatkowe metody dla testów jednostkowych 

    def returnPiecesOnBoard(self):
        return self._piecesOnBoard

    def drawBoardTestFour(self):
        ''' Rysuj dla testu 4 '''
        self._board.drawPiecesTestFour()

    def drawBoardTestFifth(self):
        ''' Rysuj dla testu 5 '''
        self._board.drawPiecesTestFifth()

    def drawBoardTestSixth(self):
        ''' Rysuj dla testu 6 '''
        self._board.drawPiecesTestSixth()

    def returnWin(self):
        return self._board.getEndGame()

    def drawBoardTestSeventh(self):
        ''' Rysuj dla testu 7 '''
        self._board.drawPiecesTestSeventh()

    def returnCount(self):
        return self._board.getCountOfPieces()


