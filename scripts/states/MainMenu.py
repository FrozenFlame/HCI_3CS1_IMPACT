import pygame, math, time, random
from enum import Enum, auto

from scripts import tools
from .classes.Buttons import Buttons
from .classes.ButtonCol.PlayButton import PlayButton
from .classes.Player import Player
from .classes.Hero import Hero
from .classes.User import User
from .classes.DeckBuilder import DeckBuilder
from .classes.FontObj import FontObj
from .classes.Movable import Movable

from ..Globals import Globals

brown = (122, 104, 58)
bronze = (161, 116, 25)
silver = (183, 183, 183)
lightgrey = (150, 150, 150)
gold = (213, 165, 0)
parachute_raid = (255,252,194)
pistachio003 = (242,239,170)
white = (255,255,255)

class MainMenu(object):
    def __init__(self):
        tools.State.__init__(self)
        self.next = None
        self.buttons = Buttons(Globals.RESOLUTION_X*0.50, Globals.RESOLUTION_Y *0.80)
        self.buttons.posX -= self.buttons.width *0.5
        self.buttons.posY -= self.buttons.height *0.5
        self.buttons.dspeed = 5
        self.finished = False
        self.play_button = PlayButton(Globals.RESOLUTION_X*0.50, Globals.RESOLUTION_Y *0.90)
        self.play_button.posX -= self.play_button.width *0.5
        self.play_button.posY -= self.play_button.height *0.5
        self.play_button.dspeed = 5

        self.heroPrime = False  # hero has been held down
        self.hero_hover = None  # name of hero being hovered
        self.hero_selected = None  # name of hero that has been clicked
        self.player_hero = None
        self.player2_hero = None

        self.globals = Globals()

        self.player2_picking = False

        # logo
        self.logo = pygame.image.load("assets/logo/Avarice-Logo-final.png").convert_alpha()
        self.logo_pos = Globals.RESOLUTION_X/2, Globals.RESOLUTION_Y/2

        # background
        self.backdrop = pygame.image.load("assets/logo/backdrop.jpg").convert_alpha()
        self.backdropMovable = Movable(self.logo,1000,5,"distance", self.logo_pos)

        self.phase = Phase.START_SCREEN

        self.font = FontObj.factory("Team IMPACT", Globals.RESOLUTION_X/2,Globals.RESOLUTION_Y/2,'POORICH.ttf',115,silver)
        self.font.is_visible = False

        # hero images and fonts and header
        self.select_text = FontObj.factory("Select a Hero",Globals.RESOLUTION_X *0.35 +1000, Globals.RESOLUTION_Y *0.10, 'big_noodle_titling_oblique.ttf', 150, lightgrey)
        self.select_text_pos2 = Globals.RESOLUTION_X *0.65, Globals.RESOLUTION_Y *0.10
        self.player_text = FontObj.factory("Player 1",Globals.RESOLUTION_X *0.15 +1000, Globals.RESOLUTION_Y *0.14, 'big_noodle_titling_oblique.ttf', 80, white)
        self.player2_text = FontObj.factory("Player 2",Globals.RESOLUTION_X *0.15 +1200, Globals.RESOLUTION_Y *0.14, 'big_noodle_titling_oblique.ttf', 80, white)

        self.resizer = 1.35
        self.billy_img = pygame.image.load("assets/heroes/hero_billy.png").convert_alpha()
        self.billy_img = pygame.transform.smoothscale(self.billy_img, (round(self.billy_img.get_rect().width * self.resizer), round(self.billy_img.get_rect().height * self.resizer)))
        self.king_img = pygame.image.load("assets/heroes/hero_king.png").convert_alpha()
        self.king_img = pygame.transform.smoothscale(self.king_img, (round(self.king_img.get_rect().width * self.resizer), round(self.king_img.get_rect().height * self.resizer)))
        self.victoria_img = pygame.image.load("assets/heroes/hero_victoria.png").convert_alpha()
        self.victoria_img = pygame.transform.smoothscale(self.victoria_img, (round(self.victoria_img.get_rect().width * self.resizer), round(self.victoria_img.get_rect().height * self.resizer)))

        self.hero_panel_pos = Globals.RESOLUTION_X * 0.5, Globals.RESOLUTION_Y * 0.5
        
        self.billy = Movable(self.billy_img,1000,5,"distance", self.hero_panel_pos)
        self.billy.set_absolute((self.hero_panel_pos[0]-self.billy.rect.width -15, self.hero_panel_pos[1]))
        self.king = Movable(self.king_img,1000,5,"distance", self.hero_panel_pos)
        self.victoria = Movable(self.victoria_img,1000,5,"distance", self.hero_panel_pos)
        self.victoria.set_absolute((self.hero_panel_pos[0]+self.victoria.rect.width +15, self.hero_panel_pos[1]))

        self.billy.current_pos_as_default()
        self.king.current_pos_as_default()
        self.victoria.current_pos_as_default()

        self.player_hero_movable = None
        self.player2_hero_movable = None

        # timings
        self.phase_start_time = None
        self.delay_to_hero = 800

        # for persist #
        self.usera = None
        self.userb = None
        self.heroa = None
        self.herob = None
        self.playera = None
        self.playerb = None
        # end for persists #



    def get_evt(self,event):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if event.type == pygame.QUIT:
            self.done = True
        #animation for the button
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                print ("[MainMenu(STATE)] O button pressed")
                # self.font.posX += 5
                # self.font.rect.center = self.font.rect.center[0]+5, self.font.rect.center[1]
                self.font.set_destination(0,0)
                # self.backdropMovable.set_destination(self.backdropMovable.rect.center[0]-1100, self.backdropMovable.rect.center[1])
                # self.buttons.set_destination(self.buttons.rect[0] -1100, self.buttons.rect[1])
                # self.backdropMovable.rect = 0,0
            elif event.key == pygame.K_p:
                self.font.back_to_default()
                # self.backdropMovable.back_to_default()
                # self.buttons.back_to_default()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.font.set_destination(*mouse)

        if self.phase == Phase.HERO_SELECT:
            # button clicks for hero selection, Next, and back.

            if self.billy.is_pointed(*mouse):
                # print("Billy moused over")
                self.hero_hover = "Billy"
            elif self.king.is_pointed(*mouse):
                # print("King moused over")
                self.hero_hover = "King"
            elif self.victoria.is_pointed(*mouse):
                # print("Victoria moused over")
                self.hero_hover = "Victoria"
            else:  # no one is moused over
                # print("Nobody moused over")
                self.hero_hover = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if click[0] == 1 and self.billy.is_pointed(*mouse):
                    print(1)
                    self.hero_selected = "Billy"
                    self.heroPrime = True
                elif click[0] == 1 and self.king.is_pointed(*mouse):
                    print(2)
                    self.hero_selected = "King"
                    self.heroPrime = True
                elif click[0] == 1 and self.victoria.is_pointed(*mouse):
                    print(3)
                    self.hero_selected = "Victoria"
                    self.heroPrime = True

            if event.type == pygame.MOUSEBUTTONUP:

                if click[0] == 0 and self.heroPrime and (self.hero_selected == self.hero_hover):
                    if not self.player2_picking:
                        print("Player 1 has chosen ", self.hero_selected)
                        self.player_hero = self.hero_selected
                        # set flag to go
                        self.player_text.set_destination(self.player_text.posX - 350, self.player_text.posY)
                        self.player2_text.back_to_default()
                        self.select_text.set_destination(*self.select_text_pos2)

                        self.player2_picking = True
                    else:
                        print("Player 2 has chosen ", self.hero_selected)
                        self.player2_hero = self.hero_selected
                        self.select_text.set_destination(self.player2_text.posX - 1400, self.select_text.posY)
                        self.player2_text.set_destination(self.player2_text.posX - 1280, self.player2_text.posY)
                        self.billy.set_destination(self.billy.posX -1280,self.billy.posY)
                        self.king.set_destination(self.king.posX -1280,self.billy.posY)
                        self.victoria.set_destination(self.victoria.posX -1280,self.billy.posY)

                        self.phase_start_time = pygame.time.get_ticks()
                        self.play_button.set_image(self.play_button.startButtonNormal)
                        self.phase = Phase.TO_READY


            if event.type == pygame.KEYDOWN:
                if not self.player2_picking:
                    if event.key == pygame.K_ESCAPE:
                        self.phase = Phase.TO_START
                        self.phase_start_time = pygame.time.get_ticks()
                        print("[MainMenu(STATE)] Going back to StartScreen")

                        self.font.set_destination(0, 0)
                        self.backdropMovable.back_to_default()
                        self.buttons.back_to_default()
                        self.buttons.set_image(self.buttons.startButtonNormal)
                        self.select_text.distancespeed = 7
                        self.player_text.distancespeed = 8
                        self.player2_text.distancespeed = 4

                        self.select_text.set_destination(self.select_text.rect.center[0] + 1200, Globals.RESOLUTION_Y * 0.10)
                        self.player_text.set_destination(self.player_text.rect.center[0] + 1450, Globals.RESOLUTION_Y * 0.14)
                        # self.player2_text.set_destination(self.player2_text.rect.center[0] + 1200, Globals.RESOLUTION_Y * 0.15)

                        self.billy.set_destination(self.hero_panel_pos[0] +900, self.hero_panel_pos[1])
                        self.king.set_destination(self.hero_panel_pos[0] +900, self.hero_panel_pos[1])
                        self.victoria.set_destination(self.hero_panel_pos[0] +900, self.hero_panel_pos[1])
                else:
                    if event.key == pygame.K_ESCAPE:
                        # animations
                        self.player2_picking = False
                        self.select_text.back_to_default()
                        self.player_text.back_to_default()
                        self.player2_text.set_destination(self.player2_text.rect.center[0] + 400, Globals.RESOLUTION_Y * 0.14)

        elif self.phase == Phase.START_SCREEN:
            self.buttons.get_evt(click, event, mouse)
            # if self.buttons.has_message: # backup of old start button (goes straight into game
            #     self.buttons.has_message = False
            #     self.finished = True
            #     self.next = "AVARICE"
            #     if not Globals.gameStart:  # game is the selected next state
            #         usera = User("Champion", 99, 0)
            #         userb = User("Challenger", 0, 0)
            #         heroa = Hero("Victoria", "this is supposed to be a surface, not a string")
            #         herob = Hero("King of Beggars", "this is supposed to be a surface, not a string")
            #         playera = Player(usera, heroa, DeckBuilder.build_deck(""))
            #         playerb = Player(userb, herob, DeckBuilder.build_deck(""))
            #         self.persist['playerA'] = playera
            #         self.persist['playerB'] = playerb
            #         self.persist['STARTED'] = False  # this is a flag that Engine will use to determine it to set down the pieces in place.
            #         Globals.gameStart = True

            if self.buttons.has_message:  # start button
                self.buttons.has_message = False
                message = self.buttons.get_message()
                if message["phase"] == "TO_HERO":
                    self.phase = Phase.TO_HERO
                    # play hero select music
                    # send MAIN elements flying to left (set destination x by -1100)
                    self.backdropMovable.set_destination(self.backdropMovable.rect.center[0]-1200, self.backdropMovable.rect.center[1])
                    self.buttons.set_destination(self.buttons.rect[0] -1200, self.buttons.rect[1])
                    self.phase_start_time = pygame.time.get_ticks()

                    # bring in Character select
                    self.select_text.defaultPos = Globals.RESOLUTION_X * 0.35, Globals.RESOLUTION_Y * 0.10
                    self.player_text.defaultPos = Globals.RESOLUTION_X * 0.15, Globals.RESOLUTION_Y * 0.14
                    self.player2_text.defaultPos = Globals.RESOLUTION_X * 0.85, Globals.RESOLUTION_Y * 0.14
                    self.select_text.distancespeed = 7
                    self.player_text.distancespeed = 4
                    self.player2_text.distancespeed = 4
                    self.select_text.back_to_default()
                    self.player_text.back_to_default()
                    # self.player2_text.back_to_default()

                    self.billy.set_absolute((self.hero_panel_pos[0] +900, self.hero_panel_pos[1]))
                    self.king.set_absolute((self.hero_panel_pos[0] +900, self.hero_panel_pos[1]))
                    self.victoria.set_absolute((self.hero_panel_pos[0] +900, self.hero_panel_pos[1]))
                    self.billy.back_to_default()
                    self.king.back_to_default()
                    self.victoria.back_to_default()

                    # allow coins to get moving
                    # reset wait timer
        elif self.phase == Phase.READY_UP:
            self.play_button.get_evt(click,event,mouse)
            if self.play_button.has_message:
                self.play_button.has_message = False

                # usera = User("Player", 99, 0)
                # userb = User("Challenger", 0, 0)
                #
                #
                # heroa = Hero(self.player_hero, "img")
                # herob = Hero(self.player2_hero, "img")
                # playera = Player(usera, heroa, DeckBuilder.build_deck(""))
                # playerb = Player(userb, herob, DeckBuilder.build_deck(""))
                # self.persist['playerA'] = playera
                # self.persist['playerB'] = playerb
                # self.persist['STARTED'] = False  # this is a flag that Engine will use to determine it to set down the pieces in place.
                # Globals.gameStart = True
                self.phase = Phase.TO_GAME
                self.delay_to_hero = pygame.time.get_ticks()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.billy.back_to_default()
                    self.king.back_to_default()
                    self.victoria.back_to_default()
                    self.select_text.set_destination(*self.select_text_pos2)
                    self.player2_text.back_to_default()
                    self.phase_start_time = pygame.time.get_ticks()
                    self.phase = Phase.TO_HERO



    def update(self, screen, keys, currentTime, dt):

        self.font.update(dt)
        if self.phase == Phase.START_SCREEN:

            pass
        elif self.phase == Phase.TO_HERO:
            self.backdropMovable.update(dt)
            self.buttons.update(dt)

            # player texts
            self.select_text.update(dt)
            self.player_text.update(dt)
            self.player2_text.update(dt)
            # heroes animation
            self.billy.update(dt)
            self.king.update(dt)
            self.victoria.update(dt)
            # buttons animation
            # hero fonts
            if currentTime - self.phase_start_time >= self.delay_to_hero:
                print("Changing Phase to HERO_SELECT")
                self.phase = Phase.HERO_SELECT
        elif self.phase == Phase.HERO_SELECT:  # backdrop and buttons no longer updated
            # player texts
            self.select_text.update(dt)
            self.player_text.update(dt)
            self.player2_text.update(dt)
            # heroes animation
            # self.billy.update(dt)
            # self.king.update(dt)
            # self.victoria.update(dt)

            # buttons animation
            # hero fonts
        elif self.phase == Phase.TO_START:
            self.backdropMovable.update(dt)
            self.buttons.update(dt)
            self.select_text.update(dt)
            self.player_text.update(dt)
            self.player2_text.update(dt)

            self.billy.update(dt)
            self.king.update(dt)
            self.victoria.update(dt)

            if currentTime - self.phase_start_time >= self.delay_to_hero:
                print("Changing Phase to START_SCREEN")
                self.phase = Phase.START_SCREEN
        elif self.phase == Phase.READY_UP:

            self.select_text.update(dt)
            self.player2_text.update(dt)

            self.play_button.update(dt)

            self.billy.update(dt)
            self.king.update(dt)
            self.victoria.update(dt)


        elif self.phase == Phase.TO_READY:
            # self.backdropMovable.update(dt)
            # self.buttons.update(dt)
            self.play_button.update(dt)

            self.select_text.update(dt)
            self.player_text.update(dt)
            self.player2_text.update(dt)

            self.billy.update(dt)
            self.king.update(dt)
            self.victoria.update(dt)
            if currentTime - self.phase_start_time >= 500:
                print("Changing Phase to START_SCREEN")
                print("Player 1 has selected ", self.player_hero)
                print("Player 2 has selected ", self.player2_hero)

                # if self.player_hero == "Billy":
                # elif self.player_hero == "King":
                # elif self.player_hero == "Victoria":

                # self.billy.set_absolute()
                self.phase = Phase.READY_UP

        elif self.phase == Phase.TO_GAME:
            self.play_button.update(dt)

            self.select_text.update(dt)
            self.player_text.update(dt)
            self.player2_text.update(dt)

            self.billy.update(dt)
            self.king.update(dt)
            self.victoria.update(dt)
            if currentTime - self.phase_start_time >= self.delay_to_hero:
                self.phase = Phase.GAME

        elif self.phase == Phase.GAME:
            self.setup_players("Vex", "Slasher399")
            self.next = "AVARICE"
            self.finished = True



        self.draw(screen)

    def setup_players(self,p,p2):
        self.usera = User(p, 99, 0)
        if self.player_hero == "Billy":
            self.heroa = Hero(self.player_hero, self.billy_img)
        elif self.hero_selected == "King":
            self.heroa = Hero(self.player_hero, self.king_img)
        else:
            self.heroa = Hero(self.player_hero, self.victoria_img)
        self.playera = Player(self.usera, self.heroa, DeckBuilder.build_deck(""))  # NOTE set hero name deck here

        self.userb = User(p2, 99, 0)
        if self.player2_hero == "Billy":
            self.herob = Hero(self.player2_hero, self.billy_img)
        elif self.player2_hero == "King":
            self.herob = Hero(self.player2_hero, self.king_img)
        else:
            self.herob = Hero(self.player2_hero, self.victoria_img)
        self.playerb= Player(self.userb, self.herob, DeckBuilder.build_deck(""))  # NOTE set hero name deck here



    def draw(self, screen):
        pygame.draw.rect(screen, gold, (000,000,1280,720))  # background
        # screen.blit(self.backdrop, (0,0))
        self.font.draw(screen)

        if self.phase == Phase.START_SCREEN:
            self.buttons.draw(screen)
            # screen.blit(self.logo, self.logo_pos)
            # self.play_button.draw(screen)
            self.backdropMovable.draw(screen)

        elif self.phase == Phase.TO_HERO or self.phase == Phase.TO_START:
            self.buttons.draw(screen)
            self.backdropMovable.draw(screen)

            self.select_text.draw(screen)
            self.player_text.draw(screen)
            self.player2_text.draw(screen)

            self.billy.draw(screen)
            self.king.draw(screen)
            self.victoria.draw(screen)
        elif self.phase == Phase.HERO_SELECT:
            # draw back and next buttons
            # draw heroes
            # draw heroes text
            self.select_text.draw(screen)
            self.player_text.draw(screen)
            self.player2_text.draw(screen)

            self.billy.draw(screen)
            self.king.draw(screen)
            self.victoria.draw(screen)
        elif self.phase == Phase.READY_UP:
            self.select_text.draw(screen)
            self.player_text.draw(screen)
            self.player2_text.draw(screen)

            self.play_button.draw(screen)

            self.billy.draw(screen)
            self.king.draw(screen)
            self.victoria.draw(screen)
        elif self.phase == Phase.TO_READY:
            self.select_text.draw(screen)
            self.player2_text.draw(screen)
            self.play_button.draw(screen)
            self.billy.draw(screen)
            self.king.draw(screen)
            self.victoria.draw(screen)
        elif self.phase == Phase.TO_GAME:
            self.select_text.draw(screen)
            self.player2_text.draw(screen)
            self.play_button.draw(screen)
            self.billy.draw(screen)
            self.king.draw(screen)
            self.victoria.draw(screen)


    def startup(self, currentTime, persistent):
        '''
        Add variables passed in persistent to the proper attributes and
        set the start time of the State to the current time.
        @ Overwritten portion
        '''
        self.persist = persistent
        self.startTime = currentTime
        # for persist #
        self.usera = None
        self.userb = None
        self.heroa = None
        self.herob = None
        self.playera = None
        self.playerb = None
        # end for persists #
        self.finished = False
        self.phase = Phase.START_SCREEN
        self.buttons.set_image(self.buttons.startButtonNormal)

    def cleanup(self):  # state is finished
        self.done = False

        '''
            TEST ONLY STATIC PERSIST
        '''

        if not Globals.gameStart:
            self.persist['playerA'] = self.playera
            self.persist['playerB'] = self.playerb
            self.persist['STARTED'] = False  # this is a flag that Engine will use to determine it to set down the pieces in place.
            Globals.gameStart = True
            self.finished = True

        return self.persist

class Phase(Enum):

    START_SCREEN = auto()
    TO_START = auto()    # transition animation
    TO_HERO = auto()    # transition animation
    HERO_SELECT = auto()
    TO_READY = auto()
    READY_UP = auto()
    TO_GAME = auto()
    GAME = auto()