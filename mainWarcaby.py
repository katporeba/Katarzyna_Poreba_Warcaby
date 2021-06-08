import pygame
from warcabyGra.warcabyZmienne import WIDTH, HEIGHT, PADDING, PADDING, BUTTON_COORD
from warcabyGra.warcabyRuch import movePiece

''' Polecenia służące do sterowania interfejsem oraz odświeżanie odpowiednich danych '''
def main():
    pygame.init()
    pygame.display.set_caption('Projekt - Warcaby')
    screen = pygame.display.set_mode([WIDTH*2-100, HEIGHT+PADDING*2])
    running = True
    movePieces = movePiece()
    movePieces.drawBoard(screen)
    movePieces.drawFirstPieces(screen)
    
    while running:
        for event in pygame.event.get():
            # Wyjście z gry przy pomocy przycisku x
            if event.type == pygame.QUIT:
                running = False
            # Obsługa zdarzenia przyciśnięcia przyciku myszki
            if event.type == pygame.MOUSEBUTTONDOWN:
                movePieces.drawBoard(screen)
                x,y = event.pos
                # Przyciśnięcie przycisku do resetowania gry
                if BUTTON_COORD[0]-150 <= x <= BUTTON_COORD[0]+150 and BUTTON_COORD[1]-30 <= y <= BUTTON_COORD[1]+30:
                    movePieces.restartGame(screen)
                movePieces.prepareData(screen, x, y)

        movePieces.drawPieces(screen)
        pygame.display.update()

    pygame.quit()

main()