import sys, pygame

class Main:
    def __init__(self):
        pygame.init()
    
    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        pygame.quit()
        sys.exit()