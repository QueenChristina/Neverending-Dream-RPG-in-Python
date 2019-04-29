# perfected sprite collision detection and prevention of overlap, as well as sprite (other than player) respose to player as obstacle

import pygame, sys, time, os
from pygame.locals import *
from Files import Var
pygame.init()

########################################################################################################################################################
# Setting up DISPLAY and title screen
DISPLAY_X = 1024
DISPLAY_Y = 768
DISPLAY = pygame.display.set_mode ((DISPLAY_X, DISPLAY_Y))
pygame.display.set_caption('Test RPG Animations')


#########################################################################################################################################################
# importing all Sprite image files here. The rest are put into another file.
path = 'Room'
imgCalendar = [os.path.join(path, 'Calendar.png'), os.path.join( path, 'Calendar1.png'), os.path.join(path, 'Calendar2.png'), os.path.join(path, 'Calendar3.png'),
        os.path.join(path, 'Calendar4.png'), os.path.join(path, 'Calendar5.png'), os.path.join(path, 'Calendar6.png'), os.path.join(path, 'Calendar7.png'),
        os.path.join(path, 'Calendar8.png'), os.path.join(path, 'Calendar9.png'), os.path.join(path, 'Calendar10.png'), os.path.join(path, 'Calendar11.png'),
        os.path.join(path, 'Calendar12.png'), os.path.join(path, 'Calendar13.png'), os.path.join(path, 'Calendar14.png'), os.path.join(path, 'Calendar15.png'),
        os.path.join(path, 'Calendar16.png'), os.path.join(path, 'Calendar17.png'), os.path.join(path, 'Calendar18.png')]

path = 'Walk Cycles\Player Walk Cycle'
imgPerson =[os.path.join(path, 'Side1.png'), os.path.join( path, 'Side2.png'), os.path.join(path, 'Side3.png'), os.path.join(path, 'Side4.png'),
        os.path.join(path, 'Front1.png'), os.path.join(path, 'Front2.png'), os.path.join(path, 'Front3.png'), os.path.join(path, 'Front4.png'),
        os.path.join(path, 'Back1.png'), os.path.join(path, 'Back2.png'), os.path.join(path, 'Back3.png'), os.path.join(path, 'Back4.png'),]

path = 'Walk Cycles\MonoPlayer'
imgPlayerMono =[os.path.join(path, '000.png'), os.path.join( path, '001.png'), os.path.join(path, '002.png'), os.path.join(path, '003.png'),
        os.path.join(path, '004.png'), os.path.join(path, '005.png'), os.path.join(path, '006.png'), os.path.join(path, '007.png'),
        os.path.join(path, '008.png'), os.path.join(path, '009.png'), os.path.join(path, '010.png'), os.path.join(path, '011.png'),
        os.path.join(path, '012.png'), os.path.join(path, '013.png'), os.path.join(path, '014.png'), os.path.join(path, '015.png'),
        os.path.join(path, '016.png')]

image_list = [imgCalendar, imgPerson, imgPlayerMono]
for u in image_list:
    for i in range (len(u)):
        u[i] = pygame.image.load(u[i])


#For a list's start to end, add an extra one to the end, as the end is NOT INCLUDED in list[start:end]
        
imgPersonLeft = imgPerson [0:4]
imgPersonRight = imgPerson [0:4]
imgPersonUp = imgPerson [8:12]
imgPersonDown = imgPerson [4:8]
#for standing (still) images, in this order place: [left, right, up, down]
imgPersonStanding = [pygame.transform.flip(imgPerson [0], True, False), imgPerson [0], imgPerson [8], imgPerson [4]]
imgPerson = {'left': imgPersonLeft,
             'right': imgPersonRight,
             'up': imgPersonUp,
             'down': imgPersonDown,
             'standing': imgPersonStanding }

imgPlayerLeft = imgPlayerMono [1:7]
imgPlayerRight = imgPlayerMono [1:7]
imgPlayerUp = imgPlayerMono [8:12]
imgPlayerDown = imgPlayerMono [13:17]
#for standing (still) images, in this order place: [left, right, up, down]
imgPlayerStanding = [imgPlayerMono[0], pygame.transform.flip(imgPlayerMono[0], True, False), imgPlayerMono[7], imgPlayerMono[12]]
imgPlayerMono = {'left': imgPlayerLeft,
             'right': imgPlayerRight,
             'up': imgPlayerUp,
             'down': imgPlayerDown,
             'standing': imgPlayerStanding }

flip_list = [imgPersonLeft, imgPlayerRight]
for u in flip_list:
    for i in range (len(u)):
        u[i] = pygame.transform.flip(u[i], True, False)


#######################################################################################################################################################
# setting up Sprite class        
currentframe = 0
# changing animationframe causes animation to stop working at times
# I believe this is because the computer iteration rate changes, thus changing the your homemade frame rate to fluctuate
# correct this be using FPS instead
# or I could be wrong ... changing FPS itself changes how many frames pass per second, or how fast your animations run
animationframe = 5
collideList = []
class Sprite(pygame.sprite.Sprite):
    def __init__(self, images, imagescale, pos, run_once):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.run_once = run_once
        self.done = False
        #images is a DICTIONARY of list of images lined up to a direction the object is in
        self.images = images
        self.image = None
        self.rect = None
        # Use colliderect to prevent sprite overlap, reserve rect for the true rect of the sprite
        self.colliderect = None
        self.imagescale = imagescale
        self.dx = 0
        self.dy = 0
        self.posx = pos[0]
        self.posy = pos[1]
        self.nextpoint = 1
        self.pointcount = 0
        self.direction = 'standing'
        self.wasdirection = 'left'
        # by self.collided, I mean collided with PLAYER only
        self.collided = False
    def changeimage(self):
        frame = self.index
        if self.dx < 0:
            self.direction = 'left'
            self.wasdirection = 'left'
        elif self.dx > 0:
            self.direction = 'right'
            self.wasdirection = 'right'
        elif self.dy < 0:
            self.direction = 'up'
            self.wasdirection = 'up'
        elif self.dy > 0:
            self.direction = 'down'
            self.wasdirection = 'down'
        else:
            if self.wasdirection == 'left':
                frame = 0
            elif self.wasdirection == 'right':
                frame = 1
            elif self.wasdirection == 'up':
                frame = 2
            elif self.wasdirection == 'down':
                frame = 3
            self.direction = 'standing'
        if isinstance(self.images[self.direction], list):
            if self.index > (len(self.images[self.direction]) - 1):
                self.index = 0
                frame = self.index
            self.image = self.images[self.direction][frame]
        else:
            self.image = self.images[self.direction]
    def imagerect(self):
        self.image = pygame.transform.scale(self.image, (int(self.image.get_size()[0] / self.imagescale ), int(self.image.get_size()[1] / self.imagescale )))
        self.rect = self.image.get_rect()
        # feel free to change size of hitbox later, or even make it a parameter
        self.colliderect = pygame.Rect(self.rect.top, self.rect.left, 3*self.rect.width/4, self.rect.height/3)
        self.rect.topleft = (self.posx, self.posy)
        self.colliderect.midbottom = self.rect.midbottom
    def moveto(self, dx, dy, points, loop):
        self.dx = dx
        self.dy = dy
        if self.posx >= (list(points)[self.pointcount][0] - abs(self.dx)) and self.posx <= (list(points)[self.pointcount][0] + abs(self.dx)):
            self.dx = 0
            if self.posy >= (list(points)[self.pointcount][1] - abs(self.dy)) and self.posy <= (list(points)[self.pointcount][1] + abs(self.dy)):
                if self.pointcount < len(list(points)) :
                    self.pointcount += self.nextpoint
                    if (self.pointcount + 1) > len(list(points)) or self.pointcount < 0:
                        if loop == True:
                            self.nextpoint *= -1
                            self.pointcount += 2*self.nextpoint
                        else:
                            self.pointcount -= self.nextpoint
        elif self.posx <= list(points)[self.pointcount][0]:
            if self.dx < 0:
                self.dx *= -1
        elif self.posx >= list(points)[self.pointcount][0]:
            if self.dx > 0:
                self.dx *= -1
        if self.posy >= (list(points)[self.pointcount][1] - abs(self.dy)) and self.posy <= (list(points)[self.pointcount][1] + abs(self.dy)):
            self.dy = 0
        elif self.posy <= list(points)[self.pointcount][1]:
            if self.dy < 0:
                self.dy *= -1
        elif self.posy >= list(points)[self.pointcount][1]:
            if self.dy > 0:
                self.dy *= -1
        self.posx += self.dx
        self.posy += self.dy
    def animate(self):
        global currentframe
        if self.done == True:
            # I haven't tested this out yet, so beware that this could prove problematic later...make sure you test this! Could be better to remove
            # self.run_once altogether...becareful!
            self.kill()
        else:
            if self.direction == 'standing':
                pass
            elif isinstance(self.images[self.direction], list):
                currentframe+= 1
                if currentframe >= animationframe:
                    currentframe = 0
                    if self.run_once == True and self.index >= (len(self.images[self.direction])-1):
                        self.done = True
                    self.index =(self.index + 1)% len(self.images[self.direction])
            else:
                print(str(self.images[self.direction]), 'is not a list that can be animated')
    def update(self):
        self.animate()
        self.changeimage()
        self.imagerect()
        DISPLAY.blit(self.image, (self.posx, self.posy))

#####################################################################################################################################################
# setting up special Sprite classes that need more than just being animated
# Class Object may be interactible, and are physical obstacles that cannot be walked over
class Object(Sprite):
    def __init__(self, images, imagescale, pos, run_once):
        Sprite.__init__(self, images, imagescale, pos, run_once)
        self.collisionpoint = None
        self.collision = [False] * 8
    def ifcollide(self):
        global collideList
        # it's possible collideList is unnecessary as .collide_mask() works by checking .rect collision first, and then .mask
        if self in collideList:
            # Note, for now I am not using masks for pixel perfect collisions to simplify things, but later I may.
            # if pygame.sprite.collide_mask(self, Player):
                # pygame.sprite.collide_mask() returns the first POINT the collision occurs at
                # Note, POINT is point on MASK, not position in coordinate plane
                # self.collisionpoint = (pygame.sprite.collide_mask(self, Player)[0] + self.rect.left, pygame.sprite.collide_mask(self, Player)[1] + + self.rect.top)
            if self.colliderect.colliderect(Player.colliderect):
                self.collided = True
            else:
                self.collided = False
        else:
            self.collided = False
    def obstacle(self):
        if self.collided:
            # fix this mess
            
            # print('colliding at' , self.collisionpoint)
            # If using masks, do NOT compare to Player.rect, compare Player MASK's left/right most point
            '''if Player.diffx > 0:
                Player.posx -= Player.diffx
                # if self.dx < 0:
                #    self.posx += self.dx
            elif Player.diffx < 0:
                Player.posx -= Player.diffx
                #if self.dx > 0:
                 #   self.posx -= self.dx
            if Player.diffy > 0:
                Player.posy -= Player.diffy
                #if self.dy < 0:
                 #   self.posy += self.dy
            elif Player.diffy < 0:
                Player.posy -= Player.diffy
                #if self.dy > 0:
                 #   self.posy -+ self.dy
            '''

            # using points to which SIDE is colliding with Player rect; BEWARE this may fail at times if one object is much larger than another
            # thanks to https://stackoverflow.com/questions/20180594/pygame-collision-by-sides-of-sprite
            # which side of Player collides with self?
            collision = [False] * 8
            collision[0] = self.colliderect.collidepoint(Player.colliderect.topleft)
            collision[1] = self.colliderect.collidepoint(Player.colliderect.topright)
            collision[2] = self.colliderect.collidepoint(Player.colliderect.bottomleft)
            collision[3] = self.colliderect.collidepoint(Player.colliderect.bottomright)

            collision[4] = self.colliderect.collidepoint(Player.colliderect.midleft)
            collision[5] = self.colliderect.collidepoint(Player.colliderect.midright)
            collision[6] = self.colliderect.collidepoint(Player.colliderect.midtop)
            collision[7] = self.colliderect.collidepoint(Player.colliderect.midbottom)

            side = "no"
            if (collision[0] or self.collision[2] or self.collision[4]) and Player.diffx > 0:
                # LEFT side of Player touching self
                side = "left"
                Player.posx -= Player.diffx
            if (self.collision[1] or self.collision[3] or self.collision[5]) and Player.diffx < 0:
                # RIGHT side of Player touching self
                side = "right"
                Player.posx -= Player.diffx
            if (self.collision[0] or self.collision[1] or self.collision[6]) and Player.diffy > 0:
                # TOP side of Player touching self
                side = "top"
                Player.posy -= Player.diffy
            if (self.collision[2] or self.collision[3] or self.collision[7]) and Player.diffy < 0:
                # BOTTOM side of Player touching self
                side = "bottom"
                Player.posy -= Player.diffy
            print( "colliding at", side , "side of player")
            

            # Is point on self colliding with Player rect // which side of self collides with player?
            # making corner coordinates slightly more inward to prevent corners being "sticky"
            topleft = (self.colliderect.topleft[0] + 1, self.colliderect.topleft[1] -1)
            topright = (self.colliderect.topright[0] - 1, self.colliderect.topright[1] -1)
            bottomleft = (self.colliderect.bottomleft[0] + 1, self.colliderect.bottomleft[1] +1)
            bottomright = (self.colliderect.bottomright[0] - 1, self.colliderect.bottomright[1] +1)
            self.collision[0] = Player.colliderect.collidepoint(topleft)
            self.collision[1] = Player.colliderect.collidepoint(topright)
            self.collision[2] = Player.colliderect.collidepoint(bottomleft)
            self.collision[3] = Player.colliderect.collidepoint(bottomright)

            self.collision[4] = Player.colliderect.collidepoint(self.colliderect.midleft)
            self.collision[5] = Player.colliderect.collidepoint(self.colliderect.midright)
            self.collision[6] = Player.colliderect.collidepoint(self.colliderect.midtop)
            self.collision[7] = Player.colliderect.collidepoint(self.colliderect.midbottom)

            sideself = "no"
            if (self.collision[0] or self.collision[2] or self.collision[4]) and self.dx < 0:
                # LEFT of self touching player
                sideself = "left"
                self.posx += self.dx
            if (self.collision[1] or self.collision[3] or self.collision[5]) and self.dx > 0:
                # RIGHT of self touching player
                sideself = "right"
                self.posx -= self.dx
            if (self.collision[0] or self.collision[1] or self.collision[6]) and self.dy < 0:
                # TOP of self touching player
                sideself = "top"
                self.posy -= self.dy
            if (self.collision[2] or self.collision[3] or self.collision[7]) and self.dy > 0:
                # BOTTOM of self colliding with any of player
                sideself = "bottom"
                self.posy -= self.dy
            print( "colliding at", sideself , "side of self")

        else:
            print('not collided')
            
    def update(self):
        self.animate()
        self.changeimage()
        self.imagerect()
        self.ifcollide()
        self.obstacle()
        DISPLAY.blit(self.image, (self.posx, self.posy))
######################################################################################################################################################
# setting up player class
class Player(Sprite):
    def __init__(self, images, imagescale, pos, run_once):
        Sprite.__init__(self, images, imagescale, pos, run_once)
        self.diffx = 0
        self.diffy = 0
    def move(self):
        # made this look uglier to make prevention of overlaping sprites easier. originally had no self.diff; directly added or substracted self.dx from
        # self.posx 
        if Var.keyDOWN:
            self.direction = 'down'
            self.wasdirection = 'down'
            self.diffy = self.dy
        elif Var.keyUP:
            self.direction = 'up'
            self.wasdirection = 'up'
            self.diffy = -self.dy
        else:
            self.diffy = 0
        if Var.keyLEFT:
            self.direction = 'left'
            self.wasdirection = 'left'
            self.diffx = -self.dx
        elif Var.keyRIGHT:
            self.direction = 'right'
            self.wasdirection = 'right'
            self.diffx = self.dx
        elif not (Var.keyDOWN or Var.keyUP):
            self.direction = 'standing'
            self.diffx = 0
        else:
            self.diffx = 0
        self.posx += self.diffx
        self.posy += self.diffy
    def playerimage(self):
        frame = self.index
        if self.direction == 'standing':
            if self.wasdirection == 'left':
                frame = 0
            elif self.wasdirection == 'right':
                frame = 1
            elif self.wasdirection == 'up':
                frame = 2
            elif self.wasdirection == 'down':
                frame = 3
        if isinstance(self.images[self.direction], list):
            if self.index > (len(self.images[self.direction]) - 1):
                self.index = 0
                frame = self.index
            self.image = self.images[self.direction][frame]
        else:
            self.image = self.images[self.direction]
    def iscollide(self, group):
        global collideList        
        collideList = pygame.sprite.spritecollide(self, group, False)
    def update(self):
        self.move()
        self.animate()
        self.playerimage()
        self.imagerect()
        self.iscollide(objList)
        DISPLAY.blit(self.image, (self.posx, self.posy))        

#######################################################################################################################################################
# initializing all Sprites
objList = pygame.sprite.Group()
objPerson = Object(imgPerson, 1,(200, 200), False)
objList.add(objPerson)

Player = Player(imgPlayerMono, 2, (500, 500), False)
Player.dx = 4
Player.dy = 4

