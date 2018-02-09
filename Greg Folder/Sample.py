#! /usr/bin/python

import pygame
from pygame import *

pygame.font.init()

WIN_WIDTH = 800 #Obvious definition ma friend "Window Width"
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)#this one is for the camera !!!!
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT) #display the window, using the size of height and width
DEPTH = 32 #use to display the windows
FLAGS = 0
CAMERA_SLACK = 30 #the idea that was never implemented

spritesheet = pygame.image.load("D:/Avarice/HCI_3CS1_IMPACT/mario_003.png")

character = Surface((14,28),pygame.SRCALPHA)
character.blit(spritesheet,(-46,-100))
character = pygame.transform.scale(character, (14*3,28*3))
marioWalk1 = character

character = Surface((16,29),pygame.SRCALPHA)
character.blit(spritesheet,(-80,-100))
character = pygame.transform.scale(character, (16*3,29*3))
marioWalk2 = character

character = Surface((16,29),pygame.SRCALPHA)
character.blit(spritesheet,(-115,-100))
character = pygame.transform.scale(character, (16*3,29*3))
marioWalk3 = character

character = Surface((16,29),pygame.SRCALPHA)
character.blit(spritesheet,(-150,-100))
character = pygame.transform.scale(character, (16*3,29*3))
marioWalk4 = character

platformBlock = pygame.image.load("D:\Avarice\HCI_3CS1_IMPACT\Greg Folder\Capture.PNG")
platformBlock = pygame.transform.scale(platformBlock, (32,32))


def main():
    global cameraX, cameraY #does'nt even exist, so no need to worry about it
    pygame.init() #this one is for initialization of pygame features at once.
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH) #this one will display the screen. easier to initialize and call if we put it together
    pygame.display.set_caption("Use arrows to move!") #caption at the top of the screen
    timer = pygame.time.Clock() #for the framerate my bruddah

    up = down = left = right = running = False # it uses this boolean, for the movements my bruddah
    bg = Surface((32,32))#Surface is an object that represent an image
    bg.convert() #convert bg, for grace performance
    bg.fill(Color("#000000")) #hex code for the black, search for other hexcode you lazy ass !
    entities = pygame.sprite.Group() #Group, is a combination of sprites, and a sprite is for the graphic object
    player = Player(32, 32) #player is of time entity, and an entity is a sprite, well therefore, player is an entity
    platforms = [] #platforms hold the sprites



    x = y = 0
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                                      P",
        "P                                 PPPPPP               P",
        "P                                           EEEE       P",
        "P                    PPPPPPPPPPP                       P",
        "P                                                      P",
        "P                                                      P",
        "P                                                      P",
        "P    PPPPPPPP                                          P",
        "P                                                      P",
        "P                          PPPPPPP                     P",
        "P                 PPPPPP                               P",
        "P                                                      P",
        "P         PPPPPPP                                      P",
        "P                                                      P",
        "P                     PPPPPP                           P",
        "P                                                      P",
        "P   PPPPPPPPPPP                                        P",
        "P                                                      P",
        "P                 PPPPPPPPPPP                          P",
        "P                                                      P",
        "P                                                      P",
        "P                                                      P",
        "P                                                      P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    # build the level
    ''' This ine is for 
    the converting of the 
    level array into a Platform, 
    a platform is an entity, 
    entity is a sprite'''
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)

            x += 32 #this one is for the top , when it completes the first line, proceed to next line
        y += 32
        x = 0
    ''' This one is for the camera'''
    total_level_width  = len(level[0])*32  #for the horizontal line at the top
    total_level_height = len(level)*32 #this for how tall
    #then this one is for passing all the instantiation in one variable.
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)#adding the player for the entity sprite group

    while 1: #while 1 is always true
        timer.tick(60) #this is for setting the time, for the fps, necessary step
        ''' input handling, getting all the inputs on your keyboard then use 
        it to make the character move.'''
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.QUIT
                quit()
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                running = True

                '''
             This one is for releasing the input, making it false once release
                '''
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        # draw background

        for y in range(32): #
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))
                '''
                0,0 then( 0*32 then y*32) for the postition
                we will be copyting screen, copying black square, for the display
                '''

        camera.update(player) #update the camera, with regards to the position of the player

        # update player, draw everything else
        player.update(up,left,right,platforms)  #position of the player that makees the object move
        for e in entities:
            ''' entity is a sprite, so it 
             will read every sprite, then blit it to render the 
             sprite in the screen'''
            screen.blit(e.image, camera.apply(e))

        pygame.display.update() #draws surface on the screen


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
        #current position of the camer, complex camera, for the camera function, then the target, player
def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect  #l,t for the player position
    _, _, w, h = camera #w, h for the camera width and height
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h #top and left

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)
    '''return rectangle that half a distance away from the player'''

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0 #velocity
        self.yvel = 0
        self.faceRight = True;
        self.onGround = False #determine it is the player is in the ground
        self.image = marioWalk1
        self.counter = 0;
        self.image.convert() #convert it
        self.rect = Rect(x, y, 14*3,28*3) #x = 32, y =32, this is for the position and the second one it is for the characteristics
                        #surface and the characteristics should be the same because that is how the system knows it

    def update(self, up,left,right,platforms):
        if up:
            if self.onGround:# only accelerate with gravity if in the air
                self.yvel -= 10 #if y velocity is positive, then it will be going down. #speed for going down
        if not self.onGround:  # only accelerate with gravity if in the air
            self.yvel += 1  # if y velocity is positive, then it will be going down. #speed for going down
        if right:
            self.xvel = 5
            self.faceRight = True
            self.walkloop()
        if left:
            self.xvel = -5
            self.faceRight = False
            self.walkloop()
        if self.yvel > 100:
            self.yvel = 100 #it will keep moving down if positive, so limit it
        if not(left or right):
            self.xvel = 0
            self.updatecharacter(marioWalk1)    #this if for making the player stays on the position

        # increment in x direction
        self.rect.left += self.xvel #it increases depending on the velocity
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms) #go to collide
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:  #loop every platforms
            '''for every platforms, cheking if it collides or intersect, 
            it will read the rect property 
            of the player and also the platform if it collides then proceed to inner
            if '''
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock): #if there is an exit block
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    '''if it collides with the platform, 
                    the player is moving to the right, depending on
                    the wall, so it will no pass'''
                    self.xvel = 0
                    self.xvel = -abs(xvel)
                    print ("Collide Right")
                    self.rect.right = p.rect.left

                if xvel < 0:
                    '''same thing but the
                     player is moving to the left'''
                    print ("collide left")
                    self.rect.left = p.rect.right
                    self.xvel = abs(xvel)
                    self.faceRight = True
                    '''either of this statement will return true
                    if it is not jumping or colliding with the
                    upper platform or lower'''

                if yvel > 0:
                    '''so it will land in the platform 
                then make the onground true'''
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0: #if the player collide with the top
                    p.rect.top = 0

    def animate(self):
        if self.xvel > 0 or self.xvel < 0:
            self.updatecharacter(marioWalk2)
            self.walkloop()
    def walkloop(self):
        if self.counter == 10:
            self.updatecharacter(marioWalk3)
        if self.counter == 15:
            self.updatecharacter(marioWalk4)
            self.counter = 0
        self.counter = self.counter + 1
    def updatecharacter(self,ansurf):
        if not self.faceRight:
            ansurf = pygame.transform.flip(ansurf,True,False)
        self.image = ansurf


class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = platformBlock
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)

if __name__ == "__main__":
    main()