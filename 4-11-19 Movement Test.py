
#Next, OPTIONAL sprite collision detection with player and blocking


##########################################################################
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

#run things only once: 
'''def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

@run_once
def my_function(foo, bar):
    return foo+bar
'''

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
        #self.dx and self.dy is the rate at which object moves
        self.dx = dx
        self.dy = dy
        self.posx = pos[0]
        self.posy = pos[1]
        #is object finished moving to (x, y)?
        self.donex = False
        self.doney = True
        self.movecounter = 0
    def moveto(self, newlocations, order):
        # new locations is a the coordinates as tuple; if you want to move to multiple coordinates in successtion
        # just use self.moveto(coord) in succession?
        # rectify the two coord moveto() working at the SAME TIME; add a sort of if done previous...then do this now
        #also get rid of the list, just make is a single point
        if self.movecounter == order or self.movecounter == (order + 0.5):
            print ('moving')
            if (self.posx + self.x) >= (newlocations[0] - abs(self.dx)) and (self.posx + self.x) <= (newlocations[0] + abs(self.dx)):
                if self.donex == False:
                    self.movecounter += 0.5
                    self.donex = True
            elif (self.posx + self.x) <= newlocations[0]:
                self.x += self.dx
                self.donex = False
                if self.dx < 0:
                    self.dx *= -1
            elif (self.posx + self.x) >= newlocations[0]:
                self.x += self.dx
                self.donex = False
                if self.dx > 0:
                    self.dx *= -1
            if (self.posy + self.y) >= (newlocations[1] - abs(self.dy)) and (self.posy + self.y) <= (newlocations[1] + abs(self.dy)):
                if self.doney == False:
                    self.movecounter += 0.5
                    self.doney = True
            elif (self.posy + self.y) <= newlocations[1]:
                self.y += self.dy
                self.doney = False
                if self.dy < 0:
                    self.dy *= -1
            elif (self.posy + self.y) >= newlocations[1]:
                self.y += self.dy
                self.doney = False
                if self.dy > 0:
                    self.dy *= -1
            return self.x, self.y
        else:
            pass
#help: https://web.archive.org/web/20121126060528/http://eli.thegreenplace.net/2008/12/13/writing-a-game-in-python-with-pygame-part-i/
    def backforth(self, lowlimx, highlimx, lowlimy, highlimy):
        print (objCalendar.x)
        if self.dx < 0 and self.x < lowlimx:
                self.dx *= -1
                print( 'too low')
        elif self.dx > 0 and self.x > highlimx:
                self.x = highlimx
                self.dx *= -1
                print('too high')
        if self.dy < 0 and self.y < lowlimy:
                self.dy *= -1
                print( 'too low')
        elif self.dy > 0 and self.y > highlimy:
                self.y = highlimy
                self.dy *= -1
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
    #objCalendar.update(objCalendar.backforth(-10, 100, -10, 100))
    objCalendar.moveto((500, 300), 0)
    objCalendar.moveto((300, 80), 1)
    print (objCalendar.movecounter)
    objCalendar.update()
    #objTest.animate(imgTest, (DISPLAY_X, DISPLAY_Y), 0, 0, True)

    pygame.display.update()
    fpsClock.tick(FPS)
