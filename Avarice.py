import pygame

from scripts import tools
from scripts.states import Engine #states imported
from scripts.states import MainMenu, MainMenu2
from scripts.Globals import Globals

def main():
    coordinator = tools.Coordinator("Avarice - A Greed-Based Card Game")
    # avarice = Engine.Engine()
    # avarice.main_loop()
    states = {"MAIN_MENU": MainMenu.MainMenu(),
              "MAIN_MENU2": MainMenu2.MainMenu(),
              "AVARICE": Engine.Engine()
              #"OPTIONS": theoretical.Options()
              #"HERO_SELECT": theoretical.HeroSelect()
              #"GAME_SUMMARY": theoretical.GameSummary()
             }
    coordinator.prepstates(states, Globals.state)
    coordinator.main_loop()
    pygame.quit()
    quit()

if __name__ == "__main__": # entry point of program
    main()

