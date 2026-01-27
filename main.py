import pygame
import sys
import maze

#pygame.init()

MAIN_WID, MAIN_HEI = 800, 800
SCREEN = pygame.display.set_mode((MAIN_WID, MAIN_HEI))

COL1 = (255, 255, 255)

cellWidths = 40
cellHeights = 30

run = False
while run:
    
    SCREEN.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

    pygame.display.flip()