import pygame, sys, time, os
from pygame.locals import *
from Files import Var, Sprite
pygame.init()


# Recall to initiate a new sprite; Sprite(self, images, imagescale, pos, run_once), Object(...), or Player(...)
# In this document, I upload images for ALL Sprites' parameter: images
# Sprites will be initiated in separate documents and be differentiated by object, background, enemy, etc. LATER when I have time
# Images parameter MUST be a dictionary corresponding to: self.direction - 'standingleft/right/up/down', 'left', 'right', 'up', 'down'; it's standing if not moving
# self.direction CAN have more states too later to change sprite, but those must be explicitly changed

############################################################################################################################################################
# create a list of image sequences composing a Sprite
path = 'Room'
imgCalendar = [os.path.join(path, 'Calendar.png'), os.path.join( path, 'Calendar1.png'), os.path.join(path, 'Calendar2.png'), os.path.join(path, 'Calendar3.png'),
        os.path.join(path, 'Calendar4.png'), os.path.join(path, 'Calendar5.png'), os.path.join(path, 'Calendar6.png'), os.path.join(path, 'Calendar7.png'),
        os.path.join(path, 'Calendar8.png'), os.path.join(path, 'Calendar9.png'), os.path.join(path, 'Calendar10.png'), os.path.join(path, 'Calendar11.png'),
        os.path.join(path, 'Calendar12.png'), os.path.join(path, 'Calendar13.png'), os.path.join(path, 'Calendar14.png'), os.path.join(path, 'Calendar15.png'),
        os.path.join(path, 'Calendar16.png'), os.path.join(path, 'Calendar17.png'), os.path.join(path, 'Calendar18.png')]


# add ALL images to a common list and load it up if not standard name
image_list = [imgCalendar]
for u in image_list:
    for i in range (len(u)):
        u[i] = pygame.image.load(u[i])
        
#########################################################################################################################################################
# Use this to load animations of standard names; totalimages is the NAME of your last image if first image is named 000.png
def listimages(path, totalimages):
    listimages =[os.path.join(path, '000.png'), os.path.join( path, '001.png'), os.path.join(path, '002.png'), os.path.join(path, '003.png'),
        os.path.join(path, '004.png'), os.path.join(path, '005.png'), os.path.join(path, '006.png'), os.path.join(path, '007.png'),
        os.path.join(path, '008.png'), os.path.join(path, '009.png'), os.path.join(path, '010.png'), os.path.join(path, '011.png'),
        os.path.join(path, '012.png'), os.path.join(path, '013.png'), os.path.join(path, '014.png'), os.path.join(path, '015.png'),
        os.path.join(path, '016.png')]
    listimages = listimages[0: totalimages + 1]
    for i in range(len(listimages)):
        i = pygame.image.load(u[i])
    return listimages

#############################################################################################################################################################



#########################################################################################################################################################
# create a dictionary of those images
def dictimages(left, right, up, down, standleft, standright, standup, standdown):
    dictimages = {'left': left,
             'right': right,
             'up': up,
             'down': down,
             'standingleft': standleft,
             'standingright': standright,
             'standingup': standup,
             'standingdown': standdown
        }
    return dictimages

# This simplified function will let you automatically flip lists/images for LEFT, and STANDLEFT
def autodict(right, up, down, standright, standup, standdown):
    dictimages = {'left': flip(right),
             'right': right,
             'up': up,
             'down': down,
             'standingleft': flip(standright),
             'standingright': standright,
             'standingup': standup,
             'standingdown': standdown
        }
    return dictimages


def flip(this):
    if type(this) is list:
        that = []
        for i in range(len(this)):
            i = pygame.transform.flip(this[i], True, False)
            that.append(i)
    else:
        that = pygame.transform.flip(this, True, False)
    return that


########################################################################################################################################################        
# For a list's start to end, add an extra one to the end, as the end is NOT INCLUDED in list[start:end]. If flipping with flip(this), must set equal to var b4        
Calendar = dictimages(None, None, None, None, imgCalendar[3:15], None, None, None)

