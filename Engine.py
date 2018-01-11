import pygame
'''
This class is responsible for holding the main loop, graphics rendering, and scene/event handling.
'''
class Engine(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Avarice - A Greed-Based Card Game")
        self.screen = pygame.display.set_mode((1280,720))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.done = False

    # handles events which happen in the program
    def eventLoop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

    # orders individual elements to update themselves (your coordinates, sprite change, etc)
    def update(self, deltaTime):
        pass

    # orders individual elements to draw themselves in the correct order (your blits)
    def draw(self):
        self.screen.fill((100,100,100))
        pygame.draw.rect(self.screen, (0, 0, 0), [100, 100, 100, 100]) # this is just to put something in
        pass

    def main_loop(self):
        while not self.done:
            # dt is multiplied to the vector values here in order to simulate the movements over time.
            # without it, it would cause the graphic to teleport to the location instantaneously
            deltaTime = self.clock.tick(self.fps)/1000 # delta time (for framerate independence)

            self.eventLoop()
            self.update(deltaTime)
            self.draw()
            pygame.display.update()


