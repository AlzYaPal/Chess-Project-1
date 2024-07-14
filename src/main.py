import sys, pygame
from chess_engine import *
from vars import *

class Main:
    def __init__(self):
        pygame.init()
        self.engine = Engine()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board = self.engine.get_board()
        self.pieces = {"wR": pygame.transform.scale(pygame.image.load("assets/wR.png"), (SQSIZE, SQSIZE)),
                  "wN": pygame.transform.scale(pygame.image.load("assets/wN.png"), (SQSIZE, SQSIZE)),
                  "wB": pygame.transform.scale(pygame.image.load("assets/wB.png"), (SQSIZE, SQSIZE)),
                  "wQ": pygame.transform.scale(pygame.image.load("assets/wQ.png"), (SQSIZE, SQSIZE)),
                  "wK": pygame.transform.scale(pygame.image.load("assets/wK.png"), (SQSIZE, SQSIZE)),
                  "wp": pygame.transform.scale(pygame.image.load("assets/wp.png"), (SQSIZE, SQSIZE)),
                  "bR": pygame.transform.scale(pygame.image.load("assets/bR.png"), (SQSIZE, SQSIZE)),
                  "bN": pygame.transform.scale(pygame.image.load("assets/bN.png"), (SQSIZE, SQSIZE)),
                  "bB": pygame.transform.scale(pygame.image.load("assets/bB.png"), (SQSIZE, SQSIZE)),
                  "bQ": pygame.transform.scale(pygame.image.load("assets/bQ.png"), (SQSIZE, SQSIZE)),
                  "bK": pygame.transform.scale(pygame.image.load("assets/bK.png"), (SQSIZE, SQSIZE)),
                  "bp": pygame.transform.scale(pygame.image.load("assets/bp.png"), (SQSIZE, SQSIZE)),
                  }
        self.keys = ("wR", "wN", "wB", "wQ", "wK", "wp", "bR", "bN", "bB", "bQ", "bK", "bp")
    
    def main_loop(self):
        screen = self.screen
        running = True
        while running:
            screen.fill((255, 255, 255))
            colour = (0, 255, 0)
            self.draw_square(screen, colour)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

    def draw_square(self, surface, colour):
         for row in range(ROWSIZE):
                for col in range(COLSIZE):
                    if (row + col) % 2 == 1:
                        pygame.draw.rect(surface, colour, (row * SQSIZE, col * SQSIZE, SQSIZE, SQSIZE))


main = Main()
main.main_loop()