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
# importing all Sprite image files here
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
class Sprite(pygame.sprite.Sprite):
    def __init__(self, images, size, pos, run_once):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.run_once = run_once
        self.done = False
        #images is a DICTIONARY of list of images lined up to a direction the object is in
        self.images = images
        self.image = None
        self.size = size
        self.dx = 0
        self.dy = 0
        self.posx = pos[0]
        self.posy = pos[1]
        self.nextpoint = 1
        self.pointcount = 0
        self.direction = 'standing'
        self.wasdirection = 'left'
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
            '''print (self.direction)
            print (str(len(self.images[self.direction])) + ' but trying to access ' + str(frame))'''
            # sometimes, frame is still previous direction's frame, so the frame is OUT of listindex of current direction
            # this if statement resets index if that is the case
            if self.index > (len(self.images[self.direction]) - 1):
                self.index = 0
                frame = self.index
            self.image = self.images[self.direction][frame]
        else:
            self.image = self.images[self.direction]
        self.image = pygame.transform.scale(self.image, self.size)
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
            pass
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
        DISPLAY.blit(self.image, (self.posx, self.posy))

######################################################################################################################################################
# setting up player class
class Player(Sprite):
    def __init__(self, images, size, pos, run_once):
        Sprite.__init__(self, images, size, pos, run_once)
    def move(self):
        if Var.keyDOWN:
            self.direction = 'down'
            self.wasdirection = 'down'
            self.posy += abs(self.dy)
        elif Var.keyUP:
            self.direction = 'up'
            self.wasdirection = 'up'
            self.posy -= abs(self.dy)
        if Var.keyLEFT:
            self.direction = 'left'
            self.wasdirection = 'left'
            self.posx -= abs(self.dx)
        elif Var.keyRIGHT:
            self.direction = 'right'
            self.wasdirection = 'right'
            self.posx += abs(self.dx)
        elif not (Var.keyDOWN or Var.keyUP):
            self.direction = 'standing'
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
        #print('is' + self.direction, 'was' + self.wasdirection, str(frame))
        if isinstance(self.images[self.direction], list):
            if self.index > (len(self.images[self.direction]) - 1):
                self.index = 0
                frame = self.index
            self.image = self.images[self.direction][frame]
        else:
            self.image = self.images[self.direction]
        self.image = pygame.transform.scale(self.image, self.size)
    def update(self):
        self.move()
        self.animate()
        self.playerimage()
        DISPLAY.blit(self.image, (self.posx, self.posy))        

#######################################################################################################################################################
# initializing all Sprites
objList = pygame.sprite.Group()
objPerson = Sprite(imgPerson, (38, 47), (50, 50), False)
objPlayerMono = Sprite(imgPlayerMono, (int(260/2), int(365/2)), (100, 100), False)
objList.add(objPerson, objPlayerMono)

Player = Player(imgPlayerMono, (int(260/2), int(365/2)), (100, 100), False)
Player.dx = 4
Player.dy = 4

