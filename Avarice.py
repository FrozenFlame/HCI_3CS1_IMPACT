import pygame

from scripts import tools
from scripts.states import Engine #states imported
from scripts.states import MainMenu, MainMenu2
from scripts.Globals import Globals
from scripts.states import Splash
from scripts.states import Tutorial

def main():
    coordinator = tools.Coordinator("Avarice - A Greed-Based Card Game")
    # avarice = Engine.Engine()
    # avarice.main_loop()

    # okay, I'm guessing this is first preload. But eventually, you'll have to push and pop new instances here
    states = {"SPLASH": Splash.Splash(),
              "MAIN_MENU": MainMenu.MainMenu()
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

