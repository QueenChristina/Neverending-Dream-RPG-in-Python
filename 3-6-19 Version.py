#This version created a class for objects, and text descriptions unique to each object (interactable boxes)
#The limit of the text box now is that it can only write up to 4 lines, and the lines are split by letter count regardless of words
#Next, I will be fixing this by splitting by words, making consecutive text boxes or different text for multiple clicks, interactable
#text box options, and optimizing code so that there is less of a mess of "if....else..." statements, perhaps by replacing text parameter
#in inanimate_objects with a function that considers the progress of the game (ex. number of clicks, the stages passes, etc.) and outputs different
#different text depending on such conditions (or even outputs a random text out of a list to choose from)
#___________________________________________________________________________________________________________________________________
import pygame, sys, time, os
from pygame.locals import *
pygame.init()
pygame.mixer.init()
pygame.font.init()

FPS=30
fpsClock= pygame.time.Clock()


#Display
DISPLAY_X=1024
DISPLAY_Y=768
DISPLAY=pygame.display.set_mode ((DISPLAY_X, DISPLAY_Y))
pygame.display.set_caption('Test RPG')

background = pygame.image.load('BasicRoom.png')
background = pygame.transform.scale(background, (DISPLAY_X, DISPLAY_Y))

#music from Youtube audio library
ticking=pygame.mixer.Sound('clock_ticking.ogg')
ticking.set_volume(.5)
ticking.play(-1)

#establish variables for player position
player_x=500
player_y=300
distance=5
diagonalDistance=3.5
direction='stop'
arrowkey='notpressed'
wasdirection = 'none'

#variables for player animation
path = 'Walk Cycles\Player Walk Cycle'
frames=[os.path.join(path, 'Side1.png'), os.path.join( path, 'Side2.png'), os.path.join(path, 'Side3.png'), os.path.join(path, 'Side4.png'),
        os.path.join(path, 'Front1.png'), os.path.join(path, 'Front2.png'), os.path.join(path, 'Front3.png'), os.path.join(path, 'Front4.png'),
        os.path.join(path, 'Back1.png'), os.path.join(path, 'Back2.png'), os.path.join(path, 'Back3.png'), os.path.join(path, 'Back4.png'),]
index = 0
currentframe = 0
animationframe = 6
    
#Font and text:
text_Toggle = False
text_finished = False
text_frame = 0
text_index = 0
text_fps = 4
line_width = 49
line_height = 45
def message(text):
    global text_finished, text_frame, text_index
    small_font = pygame.font.Font("PixelFont.ttf", 35)
    text_surface = small_font.render(text, False, (255, 255, 255))
    text_box = pygame.image.load('Text Box.png')
    text_box = pygame.transform.scale(text_box, (DISPLAY_X-10, int(DISPLAY_Y/3)))
    DISPLAY.blit(text_box, (0, int(2*DISPLAY_Y/3)))
    text_rect = text_box.get_rect()
    text_surface = small_font.render(text, False, (255, 255, 255))
    if text_index == len(text):
        text_index = len(text)
    else:
        text_frame += 1
        if text_frame >= text_fps:
            currentframe=0
            text_index += 1
    #optimize this mess of 'if ...elses' later. can do a function concerning n lines
    if text_index < line_width:
        DISPLAY.blit(small_font.render(text[0 : text_index], False, (255, 255, 255)), (int(DISPLAY_X/18), int(2.2*DISPLAY_Y/3)))
    elif text_index >= line_width and text_index < 2*line_width:
        DISPLAY.blit(small_font.render(text[0 : line_width], False, (255, 255, 255)), (int(DISPLAY_X/18), int(2.2*DISPLAY_Y/3)))
        DISPLAY.blit(small_font.render(text[line_width : text_index], False, (255, 255, 255)), (int(DISPLAY_X/18), int(2.2*DISPLAY_Y/3) + line_height))
    elif text_index >= 2*line_width and text_index < 3*line_width:
        DISPLAY.blit(small_font.render(text[0 : line_width], False, (255, 255, 255)), (int(DISPLAY_X/18), int(2.2*DISPLAY_Y/3)))
        DISPLAY.blit(small_font.render(text[line_width : 2*line_width], False, (255, 255, 255)), (int(DISPLAY_X/18), int(2.2*DISPLAY_Y/3) + line_height))
        DISPLAY.blit(small_font.render(text[2*line_width : text_index], False, (255, 255, 255)), (int(DISPLAY_X/18), int(2.2*DISPLAY_Y/3) + 2*line_height))
    elif text_index >= 3*line_width:
        DISPLAY.blit(small_font.render(text[0 : line_width], False, (255, 255, 255)), (int(DISPLAY_X/18), int(2.2*DISPLAY_Y/3)))
        DISPLAY.blit(small_font.render(text[line_width : 2*line_width], False, (255, 255, 255)), (int(DISPLAY_X/18), int(2.2*DISPLAY_Y/3) + line_height))
        DISPLAY.blit(small_font.render(text[2*line_width : 3*line_width], False, (255, 255, 255)), (int(DISPLAY_X/18), int(2.2*DISPLAY_Y/3) + 2*line_height))
        DISPLAY.blit(small_font.render(text[3*line_width : text_index], False, (255, 255, 255)), (int(DISPLAY_X/18), int(2.2*DISPLAY_Y/3) + 3*line_height))  
            
        
#boundary of scene rooms
def scene_borders(width, height, left, right, up, down):
    global border_left, border_right, border_up, border_down
    BACKGROUND_DISPLAY_RATIO_X=(DISPLAY_X/width)
    BACKGROUND_DISPLAY_RATIO_Y=(DISPLAY_Y/height)
    border_left= left*BACKGROUND_DISPLAY_RATIO_X
    border_right= right*BACKGROUND_DISPLAY_RATIO_X
    border_up= up*BACKGROUND_DISPLAY_RATIO_Y
    border_down= down *BACKGROUND_DISPLAY_RATIO_Y

def PointinBox(self):
    global player_x, player_y
    player_rect = player.get_rect()
    leeway = 8
    if (player_x < self.x + (self.rect.width * self.scale ) - leeway) \
    and (player_x + (player_rect.width) > self.x  + leeway) \
    and (player_y < self.y + (self.rect.height * self.scale ) - (leeway - 5)) \
    and (player_y + (player_rect.height) > self.y + leeway) \
    :
        return True
    else:
        return False
    
#set objects in scenes. May make into class later to be interactable
class inanimate_object(pygame.sprite.Sprite):
    def __init__(self, path, file, scale, x, y, text):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load (os.path.join (path, file))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale (self.image, (self.rect.width*scale , self.rect.height*scale))
        self.x = x
        self.y = y
        self.path = path
        self.file = file
        self.scale = scale
        self.text = text
    def collision_prevention(self):
        global player_x, player_y
        if PointinBox(self):
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
    def player_near_object(self):
        #delete duplicate
        global player_x, player_y
        player_rect = player.get_rect()
        leeway = -20
        if (player_x < self.x + (self.rect.width * self.scale ) - leeway) \
        and (player_x + (player_rect.width) > self.x  + leeway) \
        and (player_y < self.y + (self.rect.height * self.scale ) - (leeway - 5)) \
        and (player_y + (player_rect.height) > self.y + leeway) \
        :
            return True
        else:
            return False
    def show_text(self):
        if text_Toggle == True and self.player_near_object():
            message(self.text)
    def show(self):
        DISPLAY.blit(self.image, (self.x, self.y))
    def update(self):
        self.show()
        self.collision_prevention()
        
inanimate_objects_list = pygame.sprite.Group()
Bed = inanimate_object('Room', 'Bed.png', 3, 250, 80, "This is the bed, where you can see how awesome the text animation is.")
Calendar = inanimate_object ('Room', 'Calendar.png', 3, 700, 80, "This is a calendar. Text is unique to each object.")
Fridge = inanimate_object ('Room', 'Fridge.png', 3, 800, 80, "This is a fridge, where icebox and cookies go well together and milk. Take a cup of moo juice please, I  insist this stuff is delicious! Unfortunately, this is the limit of the text box.")
Cat_Bowls = inanimate_object ('Room', 'Cat Bowls.png', 3, 250, 500, "These are the cat's bowls. Did you notice the text can be super long now? Look at me go!!! Well, I should just stop now haha.")
inanimate_objects_list.add(Bed, Calendar, Fridge, Cat_Bowls)
        
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
        wasdirection = 'right'
    elif direction == 'down':
        player_y += distance
        wasdirection = 'down'
    elif direction == 'left':
        player_x -= distance
        player=pygame.transform.flip(player, True, False)
        wasdirection = 'left'
    elif direction == 'up':
        player_y -= distance
        wasdirection = 'up'
    elif direction == 'downright':
        player_x += diagonalDistance
        player_y += diagonalDistance
        wasdirection = 'downright'
    elif direction =='downleft':
        player_x -= diagonalDistance
        player_y += diagonalDistance
        player = pygame.transform.flip(player, True, False)
        wasdirection = 'downleft'
    elif direction =='upright':
        player_x += diagonalDistance
        player_y -= diagonalDistance
        wasdirection = 'upright'
    elif direction =='upleft':
        player_x -= diagonalDistance
        player_y -= diagonalDistance
        player = pygame.transform.flip(player, True, False)
        wasdirection = 'upleft'
    elif direction == 'stop':
        if wasdirection == 'none':
            index=4
        elif wasdirection == 'right':
            index=0
        elif wasdirection == 'down':
            index=4            
        elif wasdirection == 'left':
            index=0
            player = pygame.transform.flip(player, True, False)
        elif wasdirection == 'up':
            index=8
        elif wasdirection == 'downright':
            index=0
        elif wasdirection == 'downleft':
            index=0
            player = pygame.transform.flip(player, True, False)
        elif wasdirection == 'upright':
            index=0
        elif wasdirection == 'upleft':
            index=0
            player = pygame.transform.flip(player, True, False)
            
    #draw screen    
    DISPLAY.fill((0,0,0))
    DISPLAY.blit(background, (0,0))
    DISPLAY.blit(player, (player_x, player_y))

    #Draw scene objects and boundary
    if scene_room==True:
        scene_borders(300, 225, 60, 267, 6, 183)
        inanimate_objects_list.update()  
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
        #space or mouse key for text box
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                text_Toggle = not text_Toggle
                text_index = 0
                text_frame = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            text_Toggle = not text_Toggle
            text_index = 0
            text_frame = 0
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
            
    #loop checks if text box should show depending on if player is near object, change later as makes game very slow
    not_near = True
    for thing in inanimate_objects_list:
        #consider iteratable order in list, loops never loop at the same time
        if thing.player_near_object():
            not_near = False
            break
        else:
            not_near = True
    if not_near == True:
        text_Toggle = False
        
    #to blit text last and on top
    for thing in inanimate_objects_list:
        thing.show_text()
        
    pygame.display.update()
    fpsClock.tick(FPS)
