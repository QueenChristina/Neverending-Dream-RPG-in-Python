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
        self.rect.topleft = (self.posx, self.posy)
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
    def ifcollide(self):
        global collideList
        # it's possible collideList is unnecessary as .collide_mask() works by checking .rect collision first, and then .mask
        if self in collideList:            
            if pygame.sprite.collide_mask(self, Player):
                # pygame.sprite.collide_mask() returns the first POINT the collision occurs at
                # Note, POINT is point on MASK, not position in coordinate plane
                self.collisionpoint = (pygame.sprite.collide_mask(self, Player)[0] + self.rect.left, pygame.sprite.collide_mask(self, Player)[1] + + self.rect.top)
                self.collided = True           
            else:
                self.collided = False
    def obstacle(self):
        if self.collided:
            # fix this mess
            '''if self.dx > 0 and (Player.diffx <= 0 or Player.direction == 'standing'):
                self.posx -= self.dx
            elif self.dx < 0 and (Player.diffx >= 0  or Player.direction == 'standing'):
                self.posx += self.dx
            if self.dy > 0 and (Player.diffy <= 0  or Player.direction == 'standing'):
                self.posy -= self.dy
            elif self.dy < 0 and (Player.diffy >= 0  or Player.direction == 'standing'):
                self.posy += self.dy
                
            if Player.diffx > 0:
                Player.posx -= Player.dx
            elif Player.diffx < 0:
                Player.posx += Player.dx
            if Player.diffy > 0:
                Player.posy -= Player.dy
            elif Player.diffy < 0:
                Player.posy += Player.dy'''
            
            print('colliding at' , self.collisionpoint)
            # If using masks, do NOT compare to Player.rect, compare Player MASK's left/right most point
            '''if self.collisionpoint[0] < Player.rect.left:
                print('success')
                overlap = Player.rect.left - self.collisionpoint[0]
                Player.posx -= overlap
                self.dx = 0
            if self.collisionpoint[0] > Player.rect.right:
                print('success')
                overlap = self.collisionpoint[0] - Player.rect.right
                Player.posx += overlap
                self.dx = 0
            if self.collisionpoint[1] > Player.rect.bottom:
                print('success')
                overlap = self.collisionpoint[1] - Player.rect.bottom
                Player.posy -= overlap
                self.dy = 0
            if self.collisionpoint[1] < Player.rect.top:
                print('success')
                overlap = Player.rect.top - self.collisionpoint[1]
                Player.posy += overlap
                self.dy = 0'''
            if Player.diffx > 0:
                Player.posx -= Player.dx
            elif Player.diffx < 0:
                Player.posx += Player.dx
            if Player.diffy > 0:
                Player.posy -= Player.dy
            elif Player.diffy < 0:
                Player.posy += Player.dy               
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
objPerson = Object(imgPerson, 1, (200, 200), False)
objList.add(objPerson)

Player = Player(imgPlayerMono, 2, (500, 500), False)
Player.dx = 4
Player.dy = 4

