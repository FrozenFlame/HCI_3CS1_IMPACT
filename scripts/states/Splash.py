import pygame, math, time, random
from enum import Enum, auto
from .. import tools

from ..Globals import Globals

class Splash(object):
    def __init__(self):
        tools.State.__init__(self)

        self.splash = pygame.image.load("assets\\splash\\splash.png").convert_alpha()
        self.next = "MAIN_MENU"
        self.screen = pygame.display.set_mode((1280, 720))
        self.fadeScreen = pygame.Surface((1280, 720))
        self.fadeScreen.fill((0, 0, 0))  # black
        self.faded = True
        self.logotime = False
        self.timeout = 5000
        self.alpha_step = 2
        self.pause = False

    def fadeOut(self):
        alpha = 255
        while alpha >= 0:
            self.fadeScreen.set_alpha(alpha)
            self.draw(self.screen)
            self.screen.blit(self.fadeScreen, (0, 0))
            pygame.display.update()
            pygame.time.delay(1)
            alpha -= self.alpha_step
        self.faded = False
        self.logotime = True
        self.pause = False

    def fadeIn(self):
        alpha = 0
        while alpha <= 255:
            self.fadeScreen.set_alpha(alpha)
            self.draw(self.screen)
            self.screen.blit(self.fadeScreen, (0, 0))
            pygame.display.update()
            pygame.time.delay(1)
            alpha += self.alpha_step
        self.faded = True
        self.pause = True

    def get_evt(self, event):
        if event.type == pygame.QUIT:
            self.done = True

        if event.type == pygame.KEYUP:
            self.finished = True

    def update(self, screen, keys, currentTime, deltaTime):
        if self.faded and not self.pause:
            self.fadeOut()
        elif self.logotime and not self.pause:
            currentTick = currentTime
            if currentTick >= self.timeout:
                self.logotime = False
        elif not self.pause:
            self.fadeIn()

        currentTick = currentTime
        if currentTick >= self.timeout+2000:
            self.finished = True


    def draw(self, screen):
        screen.blit(self.splash, (0,0))
        if self.faded:
            self.screen.blit(self.fadeScreen, (0, 0))

    def startup(self, currentTime, persistent):
        self.persist = persistent
        pass

    def cleanup(self):
        self.done = False
        Globals.state = "AVARICE"
        return self.persist