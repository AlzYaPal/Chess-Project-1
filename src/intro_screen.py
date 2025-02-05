import pygame, sys, webbrowser
from pygame.locals import *
pygame.init()

class Screens:
    def __init__(self):
        self.screenNo = 0

    def screenNum(self, screen): #Works out which screen is required next (Menu, Instructions, Game)
        if self.screenNo == 0:
            self.screenNo = self.menu(screen) #Runs the menu screen
            self.screenNum(screen)
        elif self.screenNo == 2:
            self.screenNo = self.instructions(screen) #Runs the instructions screen
            self.screenNum(screen)
        else:
            print(3)
            return 0 #Returns to main.py and the game starts

    def draw_button(self, colour, posX, posY):
        pygame.draw.rect(self.screen, colour, (posX, posY, 360, 150)) #Draws the 'Play' and 'How to Play' buttons on the screen in the menu

    #Function for the Main Menu
    def menu(self, screen):
        pygame.display.set_caption("Chess")
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
                        return 2

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

    #Function for the Instruction Screen
    def instructions(self, screen):
        pygame.display.set_caption("Chess Instructions - Press [ESC] to exit")
        onInstructions = True
        linkFont = pygame.font.Font("assets/font/dahliaregictik.ttf", 45)
        linkText = linkFont.render("Click to learn to play chess", True, (255, 255, 255), (0, 0, 0))
        linkTextHover = linkFont.render("Click to learn to play chess", True, (255, 255, 255), (255, 0, 0))
        fontSize = 25
        usingTheEngine = [pygame.font.Font("assets/font/dahliaregictik.ttf", 70).render("Using the Engine", True, (0, 0, 0)), pygame.font.Font("assets/font/dahliaregictik.ttf", fontSize).render("The caption at the top always states whose", True, (0, 0, 0)), pygame.font.Font("assets/font/dahliaregictik.ttf", fontSize).render("turn it is", True, (0, 0, 0)), pygame.font.Font("assets/font/dahliaregictik.ttf", fontSize).render("Select a piece to move it", True, (0, 0, 0)), pygame.font.Font("assets/font/dahliaregictik.ttf", fontSize).render("Spots to move to are highlighted", True, (0, 0, 0)), pygame.font.Font("assets/font/dahliaregictik.ttf", fontSize).render("Select the square to move to", True, (0, 0, 0)), pygame.font.Font("assets/font/dahliaregictik.ttf", fontSize).render("Click a non-highlighted space to cancel", True, (0, 0, 0))]
        fontCoords = [(10, 150), (10, 250), (10, 280), (10, 330), (10, 380), (10, 430), (10, 480)]
        while onInstructions:
            screen.fill((10, 108, 3))
            pos = pygame.mouse.get_pos()
            if 10 <= pos[0] <= 590 and 40 <= pos[1] <= 90:
                screen.blit(linkTextHover, (10, 40))
            else:
                screen.blit(linkText, (10, 40))
            for i in range(len(usingTheEngine)):
                screen.blit(usingTheEngine[i], (fontCoords[i]))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        return 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 10 <= pos[0] <= 590 and 40 <= pos[1] <= 90:
                        webbrowser.open("https://www.instructables.com/Playing-Chess/")
            pygame.display.flip()