import pygame, sys, time, os
from pygame.locals import *

pygame.init()
pygame.mixer.init()

FPS=30
fpsClock= pygame.time.Clock()

#Display
DISPLAY_X=1024
DISPLAY_Y=768
DISPLAY=pygame.display.set_mode ((DISPLAY_X, DISPLAY_Y))
pygame.display.set_caption('RPG')

background=pygame.image.load('BasicRoom.png')
background=pygame.transform.scale(background, (DISPLAY_X, DISPLAY_Y))

#music from Youtube audio library
#Auto generated music from https://pernyblom.github.io/abundant-music/index.html
ticking=pygame.mixer.Sound('clock_ticking.ogg')
ticking.set_volume(.5)
ticking.play(-1)

#establish variables for player position
player_x=300
player_y=300
distance=5
diagonalDistance=3.2

#variables for player animation
path = 'Walk Cycles\Player Walk Cycle'
frames=[os.path.join(path, 'Side1.png'), os.path.join( path, 'Side2.png'), os.path.join(path, 'Side3.png'), os.path.join(path, 'Side4.png'),
        os.path.join(path, 'Front1.png'), os.path.join(path, 'Front2.png'), os.path.join(path, 'Front3.png'), os.path.join(path, 'Front4.png'),
        os.path.join(path, 'Back1.png'), os.path.join(path, 'Back2.png'), os.path.join(path, 'Back3.png'), os.path.join(path, 'Back4.png'),]
index=0
currentframe=0
animationframe=6
direction='stop'

arrowkey='notpressed'

'''#game borders set limited to DISPLAY; will change later depending on scene
border_left=0
border_right=DISPLAY_X-30
border_up=0
border_down=DISPLAY_Y-30'''

#scene
scene_room=True

#boundary of rooms
BACKGROUND_DISPLAY_RATIO_X=(DISPLAY_X/300)
BACKGROUND_DISPLAY_RATIO_Y=(DISPLAY_Y/225)

def scene_borders(left, right, up, down):
    global border_left, border_right, border_up, border_down
    border_left= left*BACKGROUND_DISPLAY_RATIO_X
    border_right= right*BACKGROUND_DISPLAY_RATIO_X
    border_up= up*BACKGROUND_DISPLAY_RATIO_Y
    border_down= down *BACKGROUND_DISPLAY_RATIO_Y

while True:
    keys = pygame.key.get_pressed()

    if scene_room==True:
        scene_borders(60, 267, 6, 183)
    else:
        pass

    #walking animation
    if keys[pygame.K_LEFT] == True or keys[pygame.K_RIGHT] == True or keys[pygame.K_d] == True or keys[pygame.K_a] == True:
        currentframe+= 1
        if currentframe >= animationframe:
            currentframe=0
            #index=(index+1)%len(frames)
            index=(index+1)%4
    elif keys[pygame.K_UP] or keys[pygame.K_w] == True == True:
        currentframe+= 1
        if index<=8:
            index=8
        if currentframe >= animationframe:
            currentframe=0
            #index=(index+1)%len(frames)
            index=(index+1)%4+8
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        currentframe+= 1
        if index<=4:
            index=4
        if currentframe >= animationframe:
            currentframe=0
            #index=(index+1)%len(frames)
            index=(index+1)%4+4       


    frame=frames[index]
    player=pygame.image.load (frame)

    #walking sounds
    if arrowkey=='pressed':
        if pygame.mixer.music.get_busy()==True:
            pass
        else:
            pygame.mixer.music.load('Step.ogg')
            pygame.mixer.music.set_volume(0.9)
            pygame.mixer.music.play()
    else:
        pygame.mixer.music.stop()

    #change position with distance
    if direction == 'right':
        player_x += distance
    elif direction == 'down':
        player_y += distance
        #player=pygame.image.load('Down.png')
    elif direction == 'left':
        player_x -= distance
        player=pygame.transform.flip(player, True, False)
    elif direction == 'up':
        player_y -= distance
        #player=pygame.image.load('Up.png')
    #diagonal direction positions
    elif direction == 'downright':
        player_x += diagonalDistance
        player_y += diagonalDistance
    elif direction =='downleft':
        player_x -= diagonalDistance
        player_y += diagonalDistance
        player = pygame.transform.flip(player, True, False)
    elif direction =='upright':
        player_x += diagonalDistance
        player_y -= diagonalDistance
    elif direction =='upleft':
        player_x -= diagonalDistance
        player_y -= diagonalDistance
        player = pygame.transform.flip(player, True, False)
    elif direction == 'stop':
        #player = pygame.image.load('Stand.png')
        index=4
        pass

    #Limit character movement to scene borders
    if player_x < border_left:
        player_x = border_left
    elif player_x > border_right:
        player_x = border_right
    if player_y < border_up:
        player_y = border_up
    elif player_y > border_down:
        player_y = border_down

    #diagonal directions
    #pygame.keys.getpressed() are not in the event loop as they log which keys are pressed on a keyboard at a given time, not by event
    if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT] or (keys[pygame.K_s] and keys[pygame.K_d]):
        direction='downright'
        arrowkey='pressed'
    elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT] or (keys[pygame.K_s] and keys[pygame.K_a]):
        direction='downleft'
        arrowkey='pressed'
    elif keys[pygame.K_UP] and keys[pygame.K_RIGHT] or (keys[pygame.K_w] and keys[pygame.K_d]):
        direction='upright'
        arrowkey='pressed'
    elif keys[pygame.K_UP] and keys[pygame.K_LEFT] or (keys[pygame.K_w] and keys[pygame.K_a]):
        direction='upleft'
        arrowkey='pressed'
                
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            #Set directions
            if event.key == K_LEFT or event.key ==K_a:
                direction='left'
                arrowkey='pressed'
            elif event.key == K_RIGHT or event.key ==K_d:
                direction='right'
                arrowkey='pressed'
            elif event.key==K_UP or event.key ==K_w:
                direction='up'
                arrowkey='pressed'
            elif event.key==K_DOWN or event.key ==K_s:
                direction='down'
                arrowkey='pressed'
            
        else:
                arrowkey='notpressed'
        if event.type==pygame.KEYUP:
            direction='stop'
                
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

    #draw screen    
    player = pygame.transform.scale(player, (int(38*2),int(47*2)))
    DISPLAY.fill((0,0,0))
    DISPLAY.blit(background, (0,0))
    DISPLAY.blit(player, (player_x, player_y))
    
    pygame.display.update()
    fpsClock.tick(FPS)

    
