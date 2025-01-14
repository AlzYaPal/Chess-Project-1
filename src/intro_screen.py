import pygame, sys
from pygame.locals import *
pygame.init()

class Screens:
    def __init__(self):
        self.screenNo = 0

    def screenNum(self, screen):
        if self.screenNo == 0:
            self.screenNo = self.menu(screen)
        elif self.screenNo == -1:
            sys.exit()
        return 0

    def draw_button(self, colour, posX, posY):
        pygame.draw.rect(self.screen, colour, (posX, posY, 360, 150))

    def menu(self, screen):
        button1Hover = False
        button2Hover = False
        button1Pos = (120, 200)
        button2Pos = (120, 400)
        self.screen = screen
        bgColour = (10, 108, 3)
        knight = pygame.transform.scale(pygame.image.load("assets/pieces/bN.png"), (123, 123))
        title_font = pygame.font.Font("assets/font/font.otf", 120)
        logo_font = title_font.render("Che s", True, (0, 0, 0))
        font1 = pygame.font.Font("assets/font/font.otf", 75)
        font2 = pygame.font.Font("assets/font/font.otf", 40)
        button1_font = font1.render("PLAY", True, (10, 108, 3))
        button2_font = (font2.render("HOW TO", True, (10, 108, 3)), font2.render("PLAY", True, (10, 108, 3)))
        onMenu = True
        while onMenu:
            self.screen.fill(bgColour)
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button1Hover:
                        return 1
                    elif button2Hover:
                        sys.exit()

            self.screen.blit(logo_font, (53, 20))
            self.screen.blit(knight, (345, 37))
            if button1Pos[0] <= pos[0] <= button1Pos[0] + 360 and button1Pos[1] <= pos[1] <= button1Pos[1] + 150:
                self.draw_button((255, 0, 0), button1Pos[0], button1Pos[1])
                self.draw_button((0, 0, 0), button2Pos[0], button2Pos[1])
                button1Hover = True
                button2Hover = False
            elif button2Pos[0] <= pos[0] <= button2Pos[0] + 360 and button2Pos[1] <= pos[1] <= button2Pos[1] + 150:
                self.draw_button((0, 0, 0), button1Pos[0], button1Pos[1])
                self.draw_button((255, 0, 0), button2Pos[0], button2Pos[1])
                button1Hover = False
                button2Hover = True
            else:
                self.draw_button((0, 0, 0), button1Pos[0], button1Pos[1])
                self.draw_button((0, 0, 0), button2Pos[0], button2Pos[1])
                button1Hover = False
                button2Hover = False
            screen.blit(button1_font, (185, 220))
            screen.blit(button2_font[0], (195, 415))
            screen.blit(button2_font[1], (235, 485))
            pygame.display.flip()
