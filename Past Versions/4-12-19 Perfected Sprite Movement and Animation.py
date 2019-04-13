# Perfected the coordination and movement of BOTH animation and direction; MULTIPLE points can now be called to move to in SUCCESSION
# with just ONE LINE; and this path can be moved over just once or looped forever
# However, the code is still rather BULKY, with too many "if...else" statements, and the initialization of each SPRITE's walk cycle for
# ALL directions is lengthly and at times confusing. I will correct this if I have time.
# Challenges here come from having both list of images and just one image as possible frames for a certain direction of movement, 
# which comes up with
# errors of images not being like lists (being subscriptable) (so I must change that line to not conflict with images)
# Something else that made code more bulky was having to put something like
# imgPersonLeft = imgPerson [4:7] AND THEN placing {'left': imgPersonLeft, ...} INSTEAD OF PLACING THE LIST IN DIRECTLY
# because this conflicts with 
# self.index =(self.index + 1)% len(self.images[self.direction]) in animate(self)
# because the MODULUS of len(self.images[self.direction]) would return a number starting from 0, when
# it should only be possible for the lowest self.index of imgPerson [4:7] to be 4, otherwise the walk sequence is messed up.

# A possible solution is to find a method to add the lowest index of the list after the modulus is taken to self.index
# and to then be able to place the lists back in to the dictionary directly
#####################################################################################################################################
import pygame, sys, time, os
from pygame.locals import *
pygame.init()

FPS=30
fpsClock= pygame.time.Clock()

DISPLAY_X = 1024
DISPLAY_Y = 768
DISPLAY = pygame.display.set_mode ((DISPLAY_X, DISPLAY_Y))
pygame.display.set_caption('Test RPG Animations')


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
image_list = [imgCalendar, imgPerson]
for u in image_list:
    for i in range (len(u)):
        u[i] = pygame.image.load(u[i])

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
             'standing': imgPersonStanding
             }
flip_list = [imgPersonLeft]
for u in flip_list:
    for i in range (len(u)):
        u[i] = pygame.transform.flip(u[i], True, False)

currentframe = 0
animationframe = 5
class Sprite(pygame.sprite.Sprite):
    def __init__(self, images, size, pos, run_once):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.run_once = run_once
        self.done = False
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
                pass
    def update(self):
        self.animate()
        self.changeimage()
        DISPLAY.blit(self.image, (self.posx, self.posy))
            
#objCalendar = Sprite(imgCalendar, (50, 50), (50, 50), 4, 4, False)
objPerson = Sprite(imgPerson, (50, 50), (50, 50), False)

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass


    DISPLAY.fill((60,70,80))
    #objPerson.moveto(4, 4, [(50,5), (300, 5), (300, 300), (50, 300)], False)
    objPerson.moveto(4, 4, [(300, 50), (300, 300)], False)
    objPerson.update()

    pygame.display.update()
    fpsClock.tick(FPS)

