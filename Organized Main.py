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
ticking=pygame.mixer.Sound('clock_ticking.ogg')
ticking.set_volume(.5)
ticking.play(-1)

#establish variables for player position
player_x=500
player_y=300
distance=5
diagonalDistance=3.2
direction='stop'
arrowkey='notpressed'

#variables for player animation
path = 'Walk Cycles\Player Walk Cycle'
frames=[os.path.join(path, 'Side1.png'), os.path.join( path, 'Side2.png'), os.path.join(path, 'Side3.png'), os.path.join(path, 'Side4.png'),
        os.path.join(path, 'Front1.png'), os.path.join(path, 'Front2.png'), os.path.join(path, 'Front3.png'), os.path.join(path, 'Front4.png'),
        os.path.join(path, 'Back1.png'), os.path.join(path, 'Back2.png'), os.path.join(path, 'Back3.png'), os.path.join(path, 'Back4.png'),]
index=0
currentframe=0
animationframe=6

#boundary of scene rooms
def scene_borders(width, height, left, right, up, down):
    global border_left, border_right, border_up, border_down
    BACKGROUND_DISPLAY_RATIO_X=(DISPLAY_X/width)
    BACKGROUND_DISPLAY_RATIO_Y=(DISPLAY_Y/height)
    border_left= left*BACKGROUND_DISPLAY_RATIO_X
    border_right= right*BACKGROUND_DISPLAY_RATIO_X
    border_up= up*BACKGROUND_DISPLAY_RATIO_Y
    border_down= down *BACKGROUND_DISPLAY_RATIO_Y

def PointinBox(player_x, player_y, player_rect, obj_x, obj_y, obj_rect, scale):
    leeway = 10
    #Beware account for scaling. Only bottom and right of obj always wrong. Key OF OBJ: 1=right, 2=left, 3=bottom, 4=top
    if (player_x < obj_x + (obj_rect.width * scale ) - leeway) \
    and (player_x + (player_rect.width) > obj_x  + leeway) \
    and (player_y < obj_y + (obj_rect.height * scale ) - (leeway - 5)) \
    and (player_y + (player_rect.height) > obj_y + leeway) \
    :
        return True
    else:
        return False

#set objects in scenes. May make into class later to be interactable
def draw_object(path, file, scale, obj_x, obj_y):
    global player_y, player_x
    obj = pygame.image.load (os.path.join (path, file))
    obj_rect = obj.get_rect()
    obj = pygame.transform.scale (obj, (obj_rect.width*scale , obj_rect.height*scale))
    DISPLAY.blit(obj, (obj_x,obj_y))
    #collision detection and adjustment
    player_rect = player.get_rect()
    #use and learn sprite class later
    '''class object(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.x = 0
            self.y = 0
            self.image = pygame.image.load('object.png')
            self.rect = pygame.Rect(self.x,self.y,32,32) #The rect for collision detection.'''
    #if player_rect.colliderect(obj_rect):
    if PointinBox(player_x, player_y, player_rect, obj_x, obj_y, obj_rect, scale):
        if direction == 'down':
            player_y -= distance
        elif direction == 'up':
            player_y += distance
        elif direction == 'left':
            player_x += distance
        elif direction == 'right':
            player_x -= distance
        elif direction == 'downright':
            player_x -= diagonalDistance
            player_y -= diagonalDistance
        elif direction =='downleft':
            player_x += diagonalDistance
            player_y -= diagonalDistance
        elif direction =='upright':
            player_x -= diagonalDistance
            player_y += diagonalDistance
        elif direction =='upleft':
            player_x += diagonalDistance
            player_y += diagonalDistance          
            
    else:
        pass
        
#walk cycle of sprites and players
def walk_cycle(frame, length_frames):
    global currentframe, index
    currentframe+= 1
    if index<=frame:
        index=frame
    if currentframe >= animationframe:
        currentframe=0
        index=(index+1)%length_frames+frame

#scene
scene_room=True
        
while True:
    keys = pygame.key.get_pressed()

    #set directions
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
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        direction='left'
        arrowkey='pressed'
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direction='right'
        arrowkey='pressed'
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        direction='up'
        arrowkey='pressed'
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        direction='down'
        arrowkey='pressed'
    else:
        direction='stop'
        arrowkey='notpressed'

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

    #walking animation.
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_a]:
        walk_cycle(0, 4)
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        walk_cycle(8, 4)
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        walk_cycle(4, 4)   

    frame=frames[index]
    player=pygame.image.load (frame)
    player = pygame.transform.scale(player, (int(38*2),int(47*2)))
    
    #change position with distance
    if direction == 'right':
        player_x += distance
    elif direction == 'down':
        player_y += distance
    elif direction == 'left':
        player_x -= distance
        player=pygame.transform.flip(player, True, False)
    elif direction == 'up':
        player_y -= distance
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
        index=4
        pass

    #draw screen    
    DISPLAY.fill((0,0,0))
    DISPLAY.blit(background, (0,0))
    DISPLAY.blit(player, (player_x, player_y))

    #Draw scene objects and boundary
    if scene_room==True:
        scene_borders(300, 225, 60, 267, 6, 183)
        draw_object ('Room', 'Bed.png', 3, 250, 80)
        draw_object ('Room', 'Calendar.png', 3, 700, 80)
        draw_object ('Room', 'Fridge.png', 3, 800, 80)
        draw_object ('Room', 'Cat Bowls.png', 3, 250, 500)        
    else:
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
                
    for event in pygame.event.get():        
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

    
    pygame.display.update()
    fpsClock.tick(FPS)

    
