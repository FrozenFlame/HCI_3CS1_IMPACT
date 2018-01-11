import sys
import pygame
from game.scripts.Globals import *

pygame.init()

resX = 900
resY = 600
gameDisplay = pygame.display.set_mode((resX, resY))
clock = pygame.time.Clock()

def main():
    print("hello world")
    print(sys.path)
    running = True
    while running:
        if Globals.scene == "main_menu":
            gameDisplay.fill((255, 255, 255))
            click = pygame.mouse.get_pressed()
            print(click)
            if click[0] == 1:
                Globals.scene = "hero_select"
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                    print("You've quit the game")
        if Globals.scene == "hero_select":
            gameDisplay.fill((155,0,155))
            click = pygame.mouse.get_pressed()
            print(click)
            if click[1] == 1:
                Globals.scene = "options"
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                    print("You've quit the game")

        if Globals.scene == "options":
            gameDisplay.fill((0,200,100))
            click = pygame.mouse.get_pressed()
            print(click)
            if click[2] == 1:
                Globals.scene = "main_menu"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                    print("You've quit the game")



        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()

    pygame.quit()
    quit()
