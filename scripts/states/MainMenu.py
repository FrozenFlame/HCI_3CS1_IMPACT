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
        self.play_button = PlayButton(Globals.RESOLUTION_X*0.5, Globals.RESOLUTION_Y + 100)
        self.play_button.posX -= self.play_button.width *0.5
        self.play_button.posY -= self.play_button.height *0.5
        self.play_button.dspeed = 5

        ''' (ascii font Ogre)
           __             _          ___             _                      
          / /  ___   __ _(_) ___    / __\ ___   ___ | | ___  __ _ _ __  ___ 
         / /  / _ \ / _` | |/ __|  /__\/// _ \ / _ \| |/ _ \/ _` | '_ \/ __|
        / /__| (_) | (_| | | (__  / \/  \ (_) | (_) | |  __/ (_| | | | \__ \ 
        \____/\___/ \__, |_|\___| \_____/\___/ \___/|_|\___|\__,_|_| |_|___/
                    |___/                                                   
        '''

        self.player2_picking = False
        self.heroPrime = False  # hero has been held down

        '''
         _____                _                 
        /__   \_ __ __ _  ___| | _____ _ __ ___ 
          / /\/ '__/ _` |/ __| |/ / _ \ '__/ __|
         / /  | | | (_| | (__|   <  __/ |  \__ \
         \/   |_|  \__,_|\___|_|\_\___|_|  |___/
                                        
        '''
        self.hero_hover = None  # name of hero being hovered
        self.hero_selected = None  # name of hero that has been clicked
        self.player_hero = None
        self.player2_hero = None
        self.phase = Phase.START_SCREEN


        '''
            ___          _                     _     _           _       
           /   \___  ___(_) __ _ _ __     ___ | |__ (_) ___  ___| |_ ___ 
          / /\ / _ \/ __| |/ _` | '_ \   / _ \| '_ \| |/ _ \/ __| __/ __|
         / /_//  __/\__ \ | (_| | | | | | (_) | |_) | |  __/ (__| |_\__ \ 
        /___,' \___||___/_|\__, |_| |_|  \___/|_.__// |\___|\___|\__|___/
                           |___/                  |__/                   
        '''

        pygame.mixer.music.load("assets\\music\\game\\hero_select.ogg")
        pygame.mixer.music.set_volume(0.12)
        self.navigating = pygame.mixer.Sound("assets\\sounds\\navigating again.ogg")

        # logo
        self.logo = pygame.image.load("assets/logo/Avarice-Logo-final.png").convert_alpha()
        self.logo_pos = Globals.RESOLUTION_X/2, Globals.RESOLUTION_Y/2

        # background
        self.backdrop = pygame.image.load("assets/logo/backdrop.jpg").convert_alpha()
        self.backdropMovable = Movable(self.logo,1000,5,"distance", self.logo_pos)
        self.font = FontObj.factory("Team IMPACT", Globals.RESOLUTION_X/2,Globals.RESOLUTION_Y/2,'POORICH.ttf',115,silver)
        self.font.is_visible = False

        # background Cs
        self.backCs = self.generate_c(True)
        self.frontCs = self.generate_c(False)
        self.y_termination = 800
        self.c_may_move = False

        # HERO SELECT HEADER #
        self.select_text = FontObj.factory("Select a Hero", Globals.RESOLUTION_X *0.35 +1000, Globals.RESOLUTION_Y *0.10, 'big_noodle_titling_oblique.ttf', 150, lightgrey)
        self.select_text_pos2 = Globals.RESOLUTION_X *0.65, Globals.RESOLUTION_Y *0.10
        self.player_text = FontObj.factory(Globals.user1name, Globals.RESOLUTION_X *0.15 +1200, Globals.RESOLUTION_Y *0.14, 'big_noodle_titling_oblique.ttf', 80, white)
        self.player2_text = FontObj.factory(Globals.user2name, Globals.RESOLUTION_X *0.15 +1300, Globals.RESOLUTION_Y *0.14, 'big_noodle_titling_oblique.ttf', 80, white)
        self.vs_text = FontObj.factory("VS", Globals.RESOLUTION_X *0.5, 1300, "big_noodle_titling_oblique.ttf", 120, white)

        # HERO SELECT PANEL ASSETS #

        self.resizer = 1.35
        self.billy_img = pygame.image.load("assets/heroes/hero_billy.png").convert_alpha()
        self.billy_img = pygame.transform.smoothscale(self.billy_img, (round(self.billy_img.get_rect().width * self.resizer), round(self.billy_img.get_rect().height * self.resizer)))
        self.king_img = pygame.image.load("assets/heroes/hero_king.png").convert_alpha()
        self.king_img = pygame.transform.smoothscale(self.king_img, (round(self.king_img.get_rect().width * self.resizer), round(self.king_img.get_rect().height * self.resizer)))
        self.victoria_img = pygame.image.load("assets/heroes/hero_victoria.png").convert_alpha()
        self.victoria_img = pygame.transform.smoothscale(self.victoria_img, (round(self.victoria_img.get_rect().width * self.resizer), round(self.victoria_img.get_rect().height * self.resizer)))

        # HERO SELECT PANEL #
        self.hero_panel_pos = Globals.RESOLUTION_X * 0.5, Globals.RESOLUTION_Y * 0.5
        self.billy = Movable(self.billy_img,1000,5,"distance", self.hero_panel_pos)
        self.billy.set_absolute((self.hero_panel_pos[0]-self.billy.rect.width -15, self.hero_panel_pos[1]))
        self.king = Movable(self.king_img,1000,5,"distance", self.hero_panel_pos)
        self.victoria = Movable(self.victoria_img,1000,5,"distance", self.hero_panel_pos)
        self.victoria.set_absolute((self.hero_panel_pos[0]+self.victoria.rect.width +15, self.hero_panel_pos[1]))
        self.billy.current_pos_as_default()
        self.king.current_pos_as_default()
        self.victoria.current_pos_as_default()
        self.billy_font = FontObj.factory("Uncle Billy", self.billy.rect.center[0], self.billy.rect.center[1]+120,"ONYX.TTF",100, white)
        self.king_font = FontObj.factory("King of Beggars", self.king.rect.center[0], self.king.rect.center[1]+120, "POORICH.TTF", 50, white)
        self.victoria_font = FontObj.factory("Victoria", self.victoria.rect.center[0], self.victoria.rect.center[1]+120, "Chalk-hand-lettering-shaded_demo.ttf", 100, white)
        self.billy_font.distancespeed = 4.5
        self.king_font.distancespeed = 4.6
        self.victoria_font.distancespeed = 3.8
        self.billy_font.set_absolute((self.billy_font.rect.center[0] +1200, self.billy_font.rect.center[1]))
        self.king_font.set_absolute((self.king_font.rect.center[0]+950, self.king_font.rect.center[1]))
        self.victoria_font.set_absolute((self.victoria_font.rect.center[0]+950, self.victoria_font.rect.center[1]))

        # timings
        self.phase_start_time = None
        self.delay_to_hero = 800
        self.isHovering = False

        # READY SCREEN OBJECTS - forced to default for now*
        self.player_img = self.victoria_img
        self.player2_img = self.king_img
        self.player_imgmov =  Movable(self.player_img, 1000, 4, "distance", (Globals.RESOLUTION_X * 0.5 - 1000, Globals.RESOLUTION_Y * 0.5))
        self.player2_imgmov = Movable(self.player2_img, 1000, 5, "distance", (Globals.RESOLUTION_X * 0.5 + 1000, Globals.RESOLUTION_Y * 0.5))

        self.hero_pick_name = None
        self.hero2_pick_name = None

        # for persist #
        self.usera = None
        self.userb = None
        self.heroa = None
        self.herob = None
        self.playera = None
        self.playerb = None
        # end for persists #

        # faders
        self.screen = pygame.display.set_mode((1280, 720))
        self.fadeScreen = pygame.Surface((1280, 720))
        self.fadeScreen.fill((0, 0, 0))  # black
        self.faded = False
        self.buttons.set_image(self.buttons.startButtonNormal)
        self.has_faded_out = False
        self.playing_sound = False

        ###Sound Clips######
        self.fadeInSound = pygame.mixer.Sound("assets\\sounds\\waterdrop_short.ogg")
        self.fadeInSound.set_volume(0.10)
        self.pickedHero = pygame.mixer.Sound("assets\\sounds\\Clicking sound.ogg")
        self.readyToPlay = pygame.mixer.Sound("assets\\sounds\\showHero.ogg")
        self.readyToPlay.set_volume(0.30)
        self.hoverSound = pygame.mixer.Sound("assets\\sounds\\hovering.ogg")
        self.cancelSound = pygame.mixer.Sound("assets\\sounds\\cancel.ogg")
    def fadeIn(self):
        alpha = 0
        while alpha <= 255:
            self.fadeScreen.set_alpha(alpha)
            self.draw(self.screen)
            self.screen.blit(self.fadeScreen, (0, 0))
            pygame.display.update()
            pygame.time.delay(1)
            alpha += 5


        self.faded = True

    def fadeOut(self):
        self.fadeInSound.play()
        alpha = 250
        while alpha >= 0:


            self.fadeScreen.set_alpha(alpha)
            self.draw(self.screen)
            self.screen.blit(self.fadeScreen, (0, 0))
            pygame.display.update()
            pygame.time.delay(1)
            alpha -= 5
        self.faded = False

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
                # self.hoverSound.play()



            elif self.king.is_pointed(*mouse):
                # print("King moused over")
                # self.hoverSound.play()

                self.hero_hover = "King"
            elif self.victoria.is_pointed(*mouse):

                # if self.hovered:
                #
                #     self.hoverSound.play()
                #     self.hovered = False
                # print("Victoria moused over")
                self.hero_hover = "Victoria"
            else:  # no one is moused over
                # print("Nobody moused over")
                self.hero_hover = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if click[0] == 1 and self.billy.is_pointed(*mouse):
                    self.hero_selected = "Billy"
                    self.heroPrime = True
                elif click[0] == 1 and self.king.is_pointed(*mouse):
                    self.hero_selected = "King"
                    self.heroPrime = True
                elif click[0] == 1 and self.victoria.is_pointed(*mouse):
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
                        self.pickedHero.play()
                        self.player2_picking = True
                    else:

                        print("Player 2 has chosen ", self.hero_selected)
                        self.player2_hero = self.hero_selected
                        self.pickedHero.play()
                        self.readyToPlay.play()
                        self.select_text.set_destination(self.player2_text.posX, self.select_text.posY - 1000)
                        self.player2_text.set_destination(self.player2_text.posX , self.player2_text.posY - 1000)
                        self.billy.set_destination(self.billy.posX,self.billy.posY - 1000)
                        self.king.set_destination(self.king.posX,self.king.posY - 1000)
                        self.victoria.set_destination(self.victoria.posX,self.victoria.posY - 1000)
                        self.billy_font.set_destination(self.billy.posX, self.billy.posY - 1000)
                        self.king_font.set_destination(self.king.posX, self.king.posY - 1000)
                        self.victoria_font.set_destination(self.victoria.posX, self.victoria.posY - 1000)


                        if self.player_hero == "Billy":
                            self.player_img = self.billy_img
                        elif self.player_hero == "King":
                            self.player_img = self.king_img
                        else:
                            self.player_img = self.victoria_img

                        if self.player2_hero == "Billy":
                            self.player2_img = self.billy_img
                        elif self.player2_hero == "King":
                            self.player2_img = self.king_img
                        else:
                            self.player2_img = self.victoria_img

                        self.player_imgmov = Movable(self.player_img,1000, 4,"distance",(Globals.RESOLUTION_X*0.5-1000, Globals.RESOLUTION_Y *0.5))
                        self.player2_imgmov = Movable(self.player2_img,1000, 5,"distance",(Globals.RESOLUTION_X*0.5+1000, Globals.RESOLUTION_Y *0.5))

                        self.phase_start_time = pygame.time.get_ticks()
                        self.play_button.set_image(self.play_button.startButtonNormal)
                        self.player_imgmov.set_destination(Globals.RESOLUTION_X*0.5-300, Globals.RESOLUTION_Y*0.5-100)
                        self.player2_imgmov.set_destination(Globals.RESOLUTION_X * 0.5+300, Globals.RESOLUTION_Y * 0.5-100)
                        self.play_button.set_destination(Globals.RESOLUTION_X*0.50-(self.play_button.width/2), Globals.RESOLUTION_Y *0.90-(self.play_button.height/2))
                        self.phase = Phase.TO_READY


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.getevt_heroselect_esc()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if click[2] == 1:
                    self.getevt_heroselect_esc()

        elif self.phase == Phase.START_SCREEN:
            self.buttons.get_evt(click, event, mouse)

            if self.buttons.has_message:  # start button
                self.buttons.has_message = False
                message = self.buttons.get_message()
                if message["phase"] == "TO_HERO":
                    self.c_may_move = True
                    self.phase = Phase.TO_HERO
                    # play hero select music

                    pygame.mixer.music.play(-1)
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

                    self.heroes_to_default()

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
                self.fadeIn()
                self.phase = Phase.TO_GAME
                self.delay_to_hero = pygame.time.get_ticks()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    self.getevt_readyup_esc()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if click[2] == 1:

                    self.getevt_readyup_esc()

    def update(self, screen, keys, currentTime, dt):
        if self.c_may_move:
            for c in self.backCs:
                c.update(dt)
                if c.exact_position[1] >= self.y_termination:
                    scale = random.randrange(100, 170)
                    cimg = pygame.transform.smoothscale(pygame.image.load("assets\\logo\\Avarice C asset - light.png"), (scale, scale)).convert_alpha()
                    c.surface = cimg
                    c.set_absolute((random.randrange(-10,1250),-random.randrange(80,500)))
                    c.set_destination(c.exact_position[0], 1200)

            for c2 in self.frontCs:
                c2.update(dt)
                if c2.exact_position[1] >= self.y_termination:
                    scale = random.randrange(100, 300)
                    cimg = pygame.transform.smoothscale(pygame.image.load("assets\\logo\\Avarice C asset - dark.png"), (scale, scale)).convert_alpha()
                    c2.surface = cimg
                    c2.set_absolute((random.randrange(-10,1250),-random.randrange(80,500)))
                    c2.set_destination(c2.exact_position[0], 1200)


        self.font.update(dt)
        if self.phase == Phase.START_SCREEN:
            if not self.has_faded_out:
                self.has_faded_out = True
                self.fadeOut()


        elif self.phase == Phase.TO_HERO:
            self.backdropMovable.update(dt)
            self.buttons.update(dt)
            self.vs_text.update(dt)

            # player texts
            self.update_select_text(dt)
            # heroes animation
            self.update_heroes(dt)

            self.player_imgmov.update(dt)
            self.player2_imgmov.update(dt)
            # buttons animation
            # hero fonts
            self.play_button.update(dt)
            if currentTime - self.phase_start_time >= self.delay_to_hero:
                print("Changing Phase to HERO_SELECT")
                self.phase = Phase.HERO_SELECT
        elif self.phase == Phase.HERO_SELECT:  # backdrop and buttons no longer updated
            # player texts
            self.update_select_text(dt)
            # heroes animation
            self.update_heroes(dt)
            # buttons animation
            # hero fonts
        elif self.phase == Phase.TO_START:
            self.backdropMovable.update(dt)
            self.buttons.update(dt)
            self.update_select_text(dt)
            self.update_heroes(dt)

            if currentTime - self.phase_start_time >= self.delay_to_hero:
                print("Changing Phase to START_SCREEN")
                self.phase = Phase.START_SCREEN
        elif self.phase == Phase.READY_UP:

            self.update_select_text(dt)
            self.vs_text.update(dt)
            self.play_button.update(dt)

            self.update_heroes(dt)

            self.player_imgmov.update(dt)
            self.player2_imgmov.update(dt)


        elif self.phase == Phase.TO_READY:
            # self.backdropMovable.update(dt)
            # self.buttons.update(dt)
            self.play_button.update(dt)
            self.vs_text.update(dt)

            self.update_select_text(dt)
            self.update_heroes(dt)

            self.player_imgmov.update(dt)
            self.player2_imgmov.update(dt)
            if currentTime - self.phase_start_time >= 500:
                print("Changing Phase READY UP")
                print("Player 1 has selected ", self.player_hero)
                print("Player 2 has selected ", self.player2_hero)

                self.player_text.set_absolute((Globals.RESOLUTION_X * 0.5 - 1000, Globals.RESOLUTION_Y * 0.6 + 150))
                self.player_text.set_destination(Globals.RESOLUTION_X * 0.5 - 300, Globals.RESOLUTION_Y * 0.5 + 150)
                self.player2_text.set_absolute((Globals.RESOLUTION_X * 0.5 + 1000, Globals.RESOLUTION_Y * 0.6 + 150))
                self.player2_text.set_destination(Globals.RESOLUTION_X * 0.5 + 300, Globals.RESOLUTION_Y * 0.5 + 150)

                self.vs_text.set_destination(Globals.RESOLUTION_X * 0.5, Globals.RESOLUTION_Y * 0.5)

                # if self.player_hero == "Billy":
                # elif self.player_hero == "King":
                # elif self.player_hero == "Victoria":

                # self.billy.set_absolute()
                self.phase = Phase.READY_UP

        elif self.phase == Phase.TO_GAME:
            self.play_button.update(dt)

            self.update_select_text(dt)

            self.update_heroes(dt)
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.music.stop()

            if currentTime - self.phase_start_time >= 300:
                self.setup_players(Globals.user1name, Globals.user2name)
                self.phase = Phase.GAME

        elif self.phase == Phase.GAME:
            print("POPPING THE SPEAR")
            self.next = "AVARICE"

            self.finished = True


        self.draw(screen)

    def setup_players(self,p,p2):
        self.usera = User(p, 99, 0)
        if self.player_hero == "Billy":
            self.heroa = Hero(self.player_hero, self.billy_img)
        elif self.player_hero == "King":
            self.heroa = Hero(self.player_hero, self.king_img)
        else:
            self.heroa = Hero(self.player_hero, self.victoria_img)
        self.playera = Player(self.usera, self.heroa, DeckBuilder.build_deck(self.player_hero))  # NOTE set hero name deck here

        self.userb = User(p2, 99, 0)
        if self.player2_hero == "Billy":
            self.herob = Hero(self.player2_hero, self.billy_img)
        elif self.player2_hero == "King":
            self.herob = Hero(self.player2_hero, self.king_img)
        else:
            self.herob = Hero(self.player2_hero, self.victoria_img)
        self.playerb = Player(self.userb, self.herob, DeckBuilder.build_deck(self.player2_hero))  # NOTE set hero name deck here

    def draw(self, screen):
        pygame.draw.rect(screen, gold, (000,000,1280,720))  # background
        for c in self.backCs:
            c.draw(screen)
        for c2 in self.frontCs:
            c2.draw(screen)

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

            self.draw_select_text(screen)
            self.vs_text.draw(screen)
            self.draw_heroes(screen)
            self.player_imgmov.draw(screen)
            self.player2_imgmov.draw(screen)
            self.play_button.draw(screen)

        elif self.phase == Phase.HERO_SELECT:
            # draw back and next buttons
            # draw heroes
            # draw heroes text
            self.draw_select_text(screen)

            self.draw_heroes(screen)

        elif self.phase == Phase.READY_UP:
            self.vs_text.draw(screen)
            self.play_button.draw(screen)

            self.player_imgmov.draw(screen)
            self.player2_imgmov.draw(screen)
            self.draw_select_text(screen)

        elif self.phase == Phase.TO_READY:
            self.vs_text.draw(screen)
            self.select_text.draw(screen)
            self.player2_text.draw(screen)
            self.play_button.draw(screen)

            self.draw_heroes(screen)

            self.player_imgmov.draw(screen)
            self.player2_imgmov.draw(screen)
            self.draw_select_text(screen)

        elif self.phase == Phase.TO_GAME:
            self.player_imgmov.draw(screen)
            self.player2_imgmov.draw(screen)
        elif self.phase == Phase.GAME:
            # self.draw(self.screen)
            screen.fill((0,0,0))
    '''
    #    ___           _           _ _                                          _                  _                      _                               _           _                 _        _       _
    #   / __\ __ _ ___(_) ___ __ _| | |_   _   ___  ___  _ __ ___   ___   _ __ | | __ _  ___ ___  | |_ ___    _ __  _   _| |_   _ __ ___ _ __   ___  __ _| |_ ___  __| |   ___ ___   __| | ___  | | ___ | |
    #  /__\/// _` / __| |/ __/ _` | | | | | | / __|/ _ \| '_ ` _ \ / _ \ | '_ \| |/ _` |/ __/ _ \ | __/ _ \  | '_ \| | | | __| | '__/ _ \ '_ \ / _ \/ _` | __/ _ \/ _` |  / __/ _ \ / _` |/ _ \ | |/ _ \| |
    # / \/  \ (_| \__ \ | (_| (_| | | | |_| | \__ \ (_) | | | | | |  __/ | |_) | | (_| | (_|  __/ | || (_) | | |_) | |_| | |_  | | |  __/ |_) |  __/ (_| | ||  __/ (_| | | (_| (_) | (_| |  __/ | | (_) | |
    # \_____/\__,_|___/_|\___\__,_|_|_|\__, | |___/\___/|_| |_| |_|\___| | .__/|_|\__,_|\___\___|  \__\___/  | .__/ \__,_|\__| |_|  \___| .__/ \___|\__,_|\__\___|\__,_|  \___\___/ \__,_|\___| |_|\___/|_|
    #                                  |___/                             |_|                                 |_|                        |_|
    '''
    # get_event
    def getevt_heroselect_esc(self):
        self.cancelSound.play()
        if not self.player2_picking:
            pygame.mixer.music.fadeout(600)
            self.c_may_move = False
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

            self.billy.set_destination(self.hero_panel_pos[0] + 900, self.hero_panel_pos[1])
            self.king.set_destination(self.hero_panel_pos[0] + 900, self.hero_panel_pos[1])
            self.victoria.set_destination(self.hero_panel_pos[0] + 900, self.hero_panel_pos[1])
            self.billy_font.set_destination(self.billy_font.rect.center[0] + 1250, self.billy_font.rect.center[1])
            self.king_font.set_destination(self.king_font.rect.center[0] + 950, self.king_font.rect.center[1])
            self.victoria_font.set_destination(self.victoria_font.rect.center[0] + 950, self.victoria_font.rect.center[1])
        else:
            # animations
            self.player2_picking = False
            self.select_text.back_to_default()
            self.player_text.back_to_default()
            self.player2_text.set_destination(self.player2_text.rect.center[0] + 400, Globals.RESOLUTION_Y * 0.14)
    def getevt_readyup_esc(self):
        self.cancelSound.play()
        self.heroes_to_default()
        self.vs_text.back_to_default()
        self.player_text.set_absolute((-900, 100))
        self.player_text.destination = None
        self.player2_text.set_absolute((Globals.RESOLUTION_X *0.8, -900))
        self.select_text.set_destination(*self.select_text_pos2)
        self.player2_text.back_to_default()

        self.player_imgmov.set_destination(Globals.RESOLUTION_X * 0.5 - 1000, Globals.RESOLUTION_Y * 0.5 + 100)
        self.player2_imgmov.set_destination(Globals.RESOLUTION_X * 0.5 + 1000, Globals.RESOLUTION_Y * 0.5 + 100)

        self.play_button.back_to_default()
        self.phase = Phase.TO_HERO
        self.phase_start_time = pygame.time.get_ticks()

    # update
    def update_heroes(self, dt):
        self.billy.update(dt)
        self.king.update(dt)
        self.victoria.update(dt)
        self.billy_font.update(dt)
        self.king_font.update(dt)
        self.victoria_font.update(dt)
    def update_select_text(self, dt):
        self.select_text.update(dt)
        self.player_text.update(dt)
        self.player2_text.update(dt)
    # draw
    def draw_heroes(self, screen):
        self.billy.draw(screen)
        self.king.draw(screen)
        self.victoria.draw(screen)

        self.billy_font.draw(screen)
        self.king_font.draw(screen)
        self.victoria_font.draw(screen)

    def draw_select_text(self, screen):
        self.select_text.draw(screen)
        self.player_text.draw(screen)
        self.player2_text.draw(screen)

    # generic
    def heroes_to_default(self):
        self.billy.back_to_default()
        self.king.back_to_default()
        self.victoria.back_to_default()
        self.billy_font.back_to_default()
        self.king_font.back_to_default()
        self.victoria_font.back_to_default()

    def generate_c(self, is_background=True):
        if is_background:
            c = []
            for x in range(0, 30):
                scale = random.randrange(100, 170)
                cimg = pygame.transform.smoothscale(pygame.image.load("assets\\logo\\Avarice C asset - light.png"),(scale,scale)).convert_alpha()
                c.append(Movable(cimg, random.randrange(200,500), 4, "constant", (random.randrange(0, 1250), random.randrange(0, 680))))
                c[x].set_destination(c[x].exact_position[0], 820)
            return c
        else:
            c = []
            for x in range(0, 20):
                scale = random.randrange(100, 300)
                cimg = pygame.transform.smoothscale(pygame.image.load("assets\\logo\\Avarice C asset - dark.png"),(scale,scale)).convert_alpha()
                c.append(Movable(cimg, random.randrange(300, 900), 4, "constant", (random.randrange(0, 1250), random.randrange(0, 680))))
                c[x].set_destination(c[x].exact_position[0], 820)
            return c

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
        self.phase = Phase.START_SCREEN
        self.buttons.set_image(self.buttons.startButtonNormal)
        pygame.mixer.music.load("assets\\music\\game\\hero_select.ogg")
        pygame.mixer.music.set_volume(0.12)
    def cleanup(self):  # state is finished
        self.done = False

        '''
            TEST ONLY STATIC PERSIST
        '''

        if not Globals.gameStart:
            self.persist['playerA'] = self.playera
            self.persist['playerB'] = self.playerb
            self.persist['portraitA'] = self.player_imgmov
            self.persist['portraitB'] = self.player2_imgmov
            self.persist['fontA'] = self.player_text
            self.persist['fontB'] = self.player2_text
            self.persist['STARTED'] = False  # this is a flag that Engine will use to determine it to set down the pieces in place.
            Globals.gameStart = True
            self.usera = None
            self.userb = None
            self.heroa = None
            self.herob = None
            self.playera = None
            self.playerb = None

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



'''
archived code

'''
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
