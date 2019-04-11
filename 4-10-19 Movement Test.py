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
imgTest = [os.path.join('Animation Test', '000.png'), os.path.join('Animation Test', '001.png'), os.path.join('Animation Test', '002.png'),
        os.path.join('Animation Test', '003.png'), os.path.join('Animation Test', '004.png'), os.path.join('Animation Test', '005.png'),
        os.path.join('Animation Test', '006.png'), os.path.join('Animation Test', '007.png'), os.path.join('Animation Test', '008.png'),
        os.path.join('Animation Test', '009.png'), os.path.join('Animation Test', '010.png'), os.path.join('Animation Test', '011.png'),
        os.path.join('Animation Test', '012.png'), os.path.join('Animation Test', '013.png'), os.path.join('Animation Test', '014.png')]
# add a gif, clock, that moves and inherit inanimate_object class. (or just modify inanimate_object class itself). Make the function that, when
# clicked, the clock (and calendar) displays another gif of closeups (replace message())
image_list = [imgCalendar, imgTest]
for u in image_list:
    for i in range (len(u)):
        u[i] = pygame.image.load(u[i])
        
currentframe = 0
animationframe = 5
class Sprite(pygame.sprite.Sprite):
    def __init__(self, images, size, pos, dx, dy, run_once):
        #you can put init(self, velocity) and then velocity.x and velocity.y if velocity inputted is a coordinate
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.run_once = run_once
        self.done = False
        self.images = images
        self.size = size
        #self.x and self.y is to be added to self.posx and self.posy for a final coordinate
        self.x = 0
        self.y = 0
        self.dx = dx
        self.dy = dy
        self.posx = pos[0]
        self.posy = pos[1]
#help: https://web.archive.org/web/20121126060528/http://eli.thegreenplace.net/2008/12/13/writing-a-game-in-python-with-pygame-part-i/
    def backforth(self, lowlimx, highlimx, lowlimy, highlimy):
        print (objCalendar.x)
        if self.dx < 0 and self.x < lowlimx:
                self.dx = -self.dx
                print( 'too low')
        elif self.dx > 0 and self.x > highlimx:
                self.x = highlimx
                self.dx = -self.dx
                print('too high')
        if self.dy < 0 and self.y < lowlimy:
                self.dy = -self.dy
                print( 'too low')
        elif self.dy > 0 and self.y > highlimy:
                self.y = highlimy
                self.dy = -self.dy
                print('too high')
        self.move()
    def move(self):
        self.x += self.dx
        self.y += self.dy
        return self.x, self.y
    def animate(self):
        global currentframe
        if self.done == True:
            pass
        else:
            currentframe+= 1
            if currentframe >= animationframe:
                currentframe = 0
                if self.run_once == True and self.index >= (len(self.images)-1):
                    self.done = True
                self.index =(self.index + 1)% len(self.images)
    def update(self, *movefunction):
        self.animate()
        image = self.images[self.index]
        image = pygame.transform.scale(image, self.size)
        movefunction
        DISPLAY.blit(image, (self.posx + self.x, self.posy + self.y))
            
objCalendar = Sprite(imgCalendar, (50, 50), (50, 50), 4, 4, False)
#you can change self.dx or self.dy later in the while loop by just calling self.dx = #; ex, obkCalendar.dx = 10
#if the dx and dy are different while limx and limy same, the movement will be diamond like instead of linear
#objTest = Sprite(0, 0)

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
    #if objTest.done == True:
    objCalendar.update(objCalendar.backforth(-10, 100, -10, 100))
    #objTest.animate(imgTest, (DISPLAY_X, DISPLAY_Y), 0, 0, True)

    pygame.display.update()
    fpsClock.tick(FPS)
