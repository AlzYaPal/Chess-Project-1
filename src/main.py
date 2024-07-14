import sys, pygame
from chess_engine import *
from vars import *
from colours import *

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
        pygame.display.set_icon(pygame.image.load("assets/icon/icon.png"))
        pygame.display.set_caption("Chess AI")
    
    def main_loop(self):
        colour = 0
        screen = self.screen
        running = True
        while running:
            screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL:
                        colour += 1
                        print(colour)
                        if colour == 12:
                            colour = 0
            self.draw_squares(screen, colours[colour])
            self.draw_pieces()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

    def draw_squares(self, surface, colour):
        for row in range(ROWSIZE):
            for col in range(COLSIZE):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(surface, colour, (row * SQSIZE, col * SQSIZE, SQSIZE, SQSIZE))
    
    def draw_pieces(self):
        for row in range(ROWSIZE):
            for col in range(COLSIZE):
                if self.board[row][col] != "--":
                    self.screen.blit(self.pieces[self.board[row][col]], (col * SQSIZE, row * SQSIZE))
            


main = Main()
main.main_loop()