import pygame
''' Zmienne używane w projekcie '''
WIDTH, HEIGHT = 800, 800
PADDING = 50
ROWS, COL = 8, 8
SQUARE_SIZE = WIDTH//COL

DARK = (145, 126, 112)
LIGTH = (235, 226, 213)
PADDING_COLOR = (51, 48, 47)
COLOR = (60,120,118)
BACKGROUND = (38, 38, 38)
TEXT_DARK = (92,92,92)
TEXT_LIGHT = (200, 200, 200)

WHITE_IMG = "img/w.png"
BLACK_IMG = "img/b.png"
WHITE_KING_IMG = "img/wk.png"
BLACK_KING_IMG = "img/bk.png"
FRAME = "img/fr.png"

BUTTON_COORD = (WIDTH + PADDING*9, HEIGHT//2+70)

pygame.init()
font = pygame.font.SysFont('Lato', 32)