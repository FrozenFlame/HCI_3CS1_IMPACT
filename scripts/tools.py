import pygame
from scripts.Globals import Globals
#this class dictates which state the program is in
print("[tools.py]Coordinator loaded")
class Coordinator(object):
    def __init__(self, title):
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.currentTime = 0.0
        self.fps = Globals.fps
        self.keys = pygame.key.get_pressed()
        self.state_dictionary = None
        self.state_name = None
        self.state = None
        self.done = False # end of program flag


    def prepstates(self, states, initstate):
        self.state_dictionary = states
        self.state_name = initstate
        self.state = self.state_dictionary[self.state_name]
        print("[tools.py] Current state: {0}".format(self.state))

    def update(self,dt):
        #general update passer to state
        self.currentTime = pygame.time.get_ticks()
        if self.state.quit:
            self.done = True
        elif self.state.finished:
            self.flip_state()
        self.state.update(self.screen, self.keys, self.currentTime, dt)

    def flip_state(self):
        # changes the state you are in
        self.state.finished = False # this will prevent the state from instantly ending if you've ended that state previously
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dictionary[self.state_name]
        tempState = self.state_dictionary[previous]
        item = {previous, tempState}
        print("[tools] Current state found in globals: {0}".format(Globals.state))
        print("[tools] STATE FLIPPING! Previous State: {0}, Next state: {1}".format(previous,self.state.next))
        # self.state_dictionary.pop()
        # self.state_dictionary.append(item)
        # self.state.startup(self.currentTime, persist)
        # self.state.previous = previous

    def evt_loop(self):
        # general event loop, mostly keystrokes etc. finer tuning in per-State's respective event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                self.keys = pygame.key.get_pressed()
            elif event.type == pygame.KEYUP:
                self.keys = pygame.key.get_pressed()
            self.state.get_evt(event)  #the passing of events into a state

    def main_loop(self):
        # the main loop of the whole program
        while not self.done:
            delta_time = self.clock.tick(self.fps)/1000.0
            self.evt_loop()
            self.update(delta_time)
            pygame.display.update()
            # FPS
            pygame.display.set_caption("Avarice - A Greed-Based Card Game - FPS: {0:.2f}".format(self.clock.get_fps()))


class State(object):

    def __init__(self):
        self.startTime = 0.0  # time when the state started
        self.currentTime = 0.0  # time of the state currently
        self.finished = False  # end of this state, cue state flip
        self.quit = False  # quitting the game from this state
        self.next = None  # the next state to be loaded
        self.previous = None  # the state loaded before this one
        self.persist = {}  # resultant of cleanup

    def get_evt(self):
        '''
        Overwrite @ children classes
        '''
        pass

    def startup(self, currentTime, persistent):
        '''
        Add variables passed in persistent to the proper attributes and
        set the start time of the State to the current time.
        @ Overwritten portion
        '''
        self.persist = persistent
        self.startTime = currentTime

    def cleanup(self):
        '''
        Add variables that should persist to the self.persist dictionary.
        Then reset State.done to False.
        @ Overwritten portion
        :return: persist
        '''
        self.done = False
        return self.persist

    def update(self, surface, keys, current_time):
        '''
        Overwrite @ children classes
        '''
