import pygame
from game import Engine

def main():
    program = Engine.Engine()
    program.main_loop()
    pygame.quit()
    quit()

if __name__ == "__main__": # entry point of program
    main()

