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
calendar = [os.path.join(path, 'Calendar.png'), os.path.join( path, 'Calendar1.png'), os.path.join(path, 'Calendar2.png'), os.path.join(path, 'Calendar3.png'),
        os.path.join(path, 'Calendar4.png'), os.path.join(path, 'Calendar5.png'), os.path.join(path, 'Calendar6.png'), os.path.join(path, 'Calendar7.png'),
        os.path.join(path, 'Calendar8.png'), os.path.join(path, 'Calendar9.png'), os.path.join(path, 'Calendar10.png'), os.path.join(path, 'Calendar11.png'),
        os.path.join(path, 'Calendar12.png'), os.path.join(path, 'Calendar13.png'), os.path.join(path, 'Calendar14.png'), os.path.join(path, 'Calendar15.png'),
        os.path.join(path, 'Calendar16.png'), os.path.join(path, 'Calendar17.png'), os.path.join(path, 'Calendar18.png')]
test = [os.path.join('Animation Test', '000.png'), os.path.join('Animation Test', '001.png'), os.path.join('Animation Test', '002.png'),
        os.path.join('Animation Test', '003.png'), os.path.join('Animation Test', '004.png'), os.path.join('Animation Test', '005.png'),
        os.path.join('Animation Test', '006.png'), os.path.join('Animation Test', '007.png'), os.path.join('Animation Test', '008.png'),
        os.path.join('Animation Test', '009.png'), os.path.join('Animation Test', '010.png'), os.path.join('Animation Test', '011.png'),
        os.path.join('Animation Test', '012.png'), os.path.join('Animation Test', '013.png'), os.path.join('Animation Test', '014.png')]
# add a gif, clock, that moves and inherit inanimate_object class. (or just modify inanimate_object class itself). Make the function that, when
# clicked, the clock (and calendar) displays another gif of closeups (replace message())
image_list = [calendar, test]
for u in image_list:
    for i in range (len(u)):
        u[i] = pygame.image.load(u[i])
currentframe = 0
animationframe = 5
class animation(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.done = False
    def animate(self, animation_pictures, size, location, run_once):
        global currentframe
        if self.done == True:
            pass
        else:
            currentframe+= 1
            if currentframe >= animationframe:
                currentframe = 0
                if run_once == True and self.index >= (len(animation_pictures)-1):
                    self.done = True
                self.index =(self.index + 1)% len(animation_pictures)        
            image = animation_pictures[self.index]
            image = pygame.transform.scale(image, size)
            DISPLAY.blit(image, location)
obj_calendar = animation()
obj_test = animation()

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

        if event.type == pygame.MOUSEBUTTONDOWN:


    DISPLAY.fill((0,0,0))
    if obj_test.done == True:
        obj_calendar.animate(calendar, (50, 50), (80, 80), False)
    obj_test.animate(test, (DISPLAY_X, DISPLAY_Y), (0, 0), True)

    pygame.display.update()
    fpsClock.tick(FPS)
