import pygame
from warcabyGra.warcabyRuch import movePiece 
from warcabyGra.warcabyPionek import King, Piece 
from warcabyGra.warcabyZmienne import WIDTH, HEIGHT, PADDING, PADDING
pygame.init()
win = pygame.display.set_mode([WIDTH*2-100, HEIGHT+PADDING*2])

#klasa do rzucania własnych wyjątków
class Error(Exception):
    pass

class WrongMove(Error):
    '''Raised when move is not possible '''
    pass

def firstTest():
    #przygotowanie planszy
    try:
        movePieces = movePiece()
        movePieces.drawBoard(win)
        movePieces.drawFirstPieces(win)
        pieces = movePieces.returnPiecesOnBoard()

        #wybranie białego pionka oraz pola na które chcemy go przenieść
        tmpPiece1 = pieces[2][2]
        tmpDestination1 = pieces[3][3]
        movePieces.moveNormalPiece(win, tmpPiece1, 2, 2)
        movePieces.moveNormalPiece(win, tmpDestination1, 3, 3)

        #wybranie czarnego pionka oraz pola na które chcemy go przenieść
        tmpPiece2 = pieces[5][7]
        tmpDestination2 = pieces[4][6]

        #zamienianie ich miejscem
        movePieces.moveNormalPiece(win, tmpPiece2, 5, 7)
        movePieces.moveNormalPiece(win, tmpDestination2, 4, 6)

        #sprawdzenie czy pionki zamieniły swoje miejsce
        if(pieces[2][2] == tmpDestination1 and pieces[3][3] == tmpPiece1 and pieces[5][7] == tmpDestination2 and pieces[4][6] == tmpPiece2):
            print("Correct values - first test\n")
        else:
            raise WrongMove

    except WrongMove:
        print("First test failed")


def secondTest():
    try:
        #przygotowanie planszy
        movePieces = movePiece()
        movePieces.drawBoard(win)
        movePieces.drawFirstPieces(win)
        pieces = movePieces.returnPiecesOnBoard()

        #wybranie białego pionka
        tmpPiece1 = pieces[2][2]
        #wybranie zajętego przez inny pionek pola
        tmpDestination1 = pieces[1][1]
        #zamienianie ich miejscem
        movePieces.moveNormalPiece(win, tmpPiece1, 2, 2)
        movePieces.moveNormalPiece(win, tmpDestination1, 1, 1)

        #sprawdzenie czy pionki poprawnie nie zamieniły miejsc
        if(pieces[2][2] == tmpDestination1 and pieces[3][3] == tmpPiece1):
            raise WrongMove
        else:
            print("Correct values - Second test\n")

    except WrongMove:
        print("Second test failed")

def thirdTest():
    try:
        #przygotowanie planszy
        movePieces = movePiece()
        movePieces.drawBoard(win)
        movePieces.drawFirstPieces(win)
        pieces = movePieces.returnPiecesOnBoard()

        #zmiana miejsca białego pionka
        tmpPiece1 = pieces[2][2]
        tmpDestination1 = pieces[3][3]
        movePieces.moveNormalPiece(win, tmpPiece1, 2, 2)
        movePieces.moveNormalPiece(win, tmpDestination1, 3, 3)

        #zmiana miejsca czarnego pionka
        tmpPiece2 = pieces[5][5]
        tmpDestination2 = pieces[4][4]
        movePieces.moveNormalPiece(win, tmpPiece2, 5, 5)
        movePieces.moveNormalPiece(win, tmpDestination2, 4, 4)

        #zbicie pionka czarnego przez białego
        tmpPiece1 = pieces[3][3]
        tmpDestination1 = pieces[5][5]
        movePieces.moveNormalPiece(win, tmpPiece1, 3, 3)
        movePieces.moveNormalPiece(win, tmpDestination1, 5, 5)

        #sprawdzenie czy pionek czarny, króty znajdował się w komórce 4,4 został zamieniony na pustą wartość oraz czy na miejscu 5,5 znajduje się pionek biały
        if(pieces[4][4] == "null" and pieces[5][5] == tmpPiece1):
            print("Correct values - Third test\n")
        else:
            raise WrongMove 

    except WrongMove:
        print("Third test failed")

def fourthTest():
    try:
        #przygotowanie planszy
        movePieces = movePiece()
        movePieces.drawBoard(win)
        movePieces.drawBoardTestFour()
        pieces = movePieces.returnPiecesOnBoard()

        #zbicie przez pionka białego dwóch pionków czarnych, znajdują się one na pozycji 1,1 oraz 3,3
        tmpPiece1 = pieces[0][0]
        tmpDestination1 = pieces[4][4]
        movePieces.moveNormalPiece(win, tmpPiece1, 0, 0)
        movePieces.moveNormalPiece(win, tmpDestination1, 4, 4)

        #sprawdzenie czy pionki zostały zbite oraz pionek biały zmienił miejsce
        if(pieces[1][1] == "null" and pieces[3][3] == "null" and pieces[4][4] == tmpPiece1):
            print("Correct values - Fourth test\n")
        else:
            raise WrongMove 

    except WrongMove:
        print("Fourth test failed")

def fifthTest():
    try:
        #przygotowanie planszy
        movePieces = movePiece()
        movePieces.drawBoard(win)
        movePieces.drawBoardTestFifth()
        pieces = movePieces.returnPiecesOnBoard()

        #przejscie białego pionka na pole 7,7 i sprawdzenie czy pionek ten stał się damką
        tmpPiece1 = pieces[6][6]
        tmpDestination1 = pieces[7][7]
        movePieces.moveNormalPiece(win, tmpPiece1, 6, 6)
        movePieces.moveNormalPiece(win, tmpDestination1, 7, 7)

        #sprawdzenie czy pionek jest damką
        if isinstance(pieces[7][7], King):
            print("Correct values - Fifth test\n")
        else:
            raise WrongMove 

    except WrongMove:
        print("Fifth test failed")

def sixthTest():
    try:
        #przygotowanie planszy
        movePieces = movePiece()
        movePieces.drawBoard(win)
        movePieces.drawBoardTestSixth()
        pieces = movePieces.returnPiecesOnBoard()

        #przejscie białego pionka na pole 7,7 (zamiana na damkę)
        tmpPiece1 = pieces[6][6]
        tmpDestination1 = pieces[7][7]
        movePieces.moveNormalPiece(win, tmpPiece1, 6, 6)
        movePieces.moveNormalPiece(win, tmpDestination1, 7, 7)

        # ustawiamy drugi raz turę dla pionka białego
        movePieces.oppositeColor()

        tmpPiece1 = pieces[7][7]
        tmpDestination1 = pieces[1][1]
        movePieces.moveNormalPiece(win, tmpPiece1, 7, 7)
        movePieces.moveNormalPiece(win, tmpDestination1, 1, 1)

        #sprawdzenie czy czarny pionek znajdujący się na polu 2,2 został zbity
        if pieces[2][2] == "null" and pieces[1][1] == tmpPiece1:
            print("Correct values - Sixth test\n")
        else:
            raise WrongMove 

    except WrongMove:
        print("Sixth test failed")

def seventhTest():
    try:
        #przygotowanie planszy
        movePieces = movePiece()
        movePieces.drawBoard(win)
        movePieces.drawBoardTestSeventh()
        pieces = movePieces.returnPiecesOnBoard()

        movePieces.oppositeColor()

        #zbicie pionka białego przez pionka czarnego
        tmpPiece1 = pieces[3][3]
        tmpDestination1 = pieces[1][1]
        movePieces.moveNormalPiece(win, tmpPiece1, 3, 3)
        movePieces.moveNormalPiece(win, tmpDestination1, 1, 1)

        #sprawdzenie czy gra się zakończyła
        if movePieces.returnWin() == True:
            print("Correct values - Seventh test\n")
        else:
            raise WrongMove 

    except WrongMove:
        print("Seventh test failed")

def eighthTest():
    try:
        #przygotowanie planszy
        movePieces = movePiece()
        movePieces.drawBoard(win)
        movePieces.drawBoardTestSeventh()
        pieces = movePieces.returnPiecesOnBoard()

        movePieces.oppositeColor()

        #zbicie pionka białego przez pionka czarnego
        tmpPiece1 = pieces[3][3]
        tmpDestination1 = pieces[1][1]
        movePieces.moveNormalPiece(win, tmpPiece1, 3, 3)
        movePieces.moveNormalPiece(win, tmpDestination1, 1, 1)

        #rozpoczęcie gry od nowa i pobranie ilości białych i czarnych pionków
        movePieces.restartGame(win)
        whitePieces, balckPieces = movePieces.returnCount()

        #sprawdzenie czy gra rozpoczęła się od nowa
        if whitePieces == 12 and balckPieces == 12:
            print("Correct values - Eighth test\n")
        else:
            raise WrongMove 

    except WrongMove:
        print("Eighth test failed")

firstTest()
secondTest()
thirdTest()
fourthTest()
fifthTest()
sixthTest()
seventhTest()
eighthTest()