import pygame, sys, time, os
from pygame.locals import *
from Files import Sprite, Var, Images
pygame.init()

FPS=40
fpsClock= pygame.time.Clock()

# LATER, to optimize performance time, use: https://www.pygame.org/docs/tut/newbieguide.html


def variables():
    keys = pygame.key.get_pressed()
    keyLEFT = keys[pygame.K_LEFT] or keys[pygame.K_a]
    keyRIGHT = keys[pygame.K_RIGHT] or keys[pygame.K_d]
    keyDOWN = keys[pygame.K_DOWN] or keys[pygame.K_s]
    keyUP = keys[pygame.K_UP] or keys[pygame.K_w]

    if keyDOWN:
        Var.keyDOWN = True
    elif keyUP:
        Var.keyUP = True
    if keyLEFT:
        Var.keyLEFT = True
    elif keyRIGHT:
        Var.keyRIGHT = True

    if not keyDOWN:
        Var.keyDOWN = False
    if not keyUP:
        Var.keyUP = False
    if not keyLEFT:
        Var.keyLEFT = False
    if not keyRIGHT:
        Var.keyRIGHT = False

    if keys[pygame.K_LSHIFT]:
        Var.keyLSHIFT = True

    if not keys[pygame.K_LSHIFT]:
        Var.keyLSHIFT = False
        
while True:
    variables()
    Var.mousePOS = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Var.keySPACE = True
            else:
                Var.keySPACE = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Var.mouseCLICK = True
        else:
            Var.mouseCLICK = False

    Sprite.objPerson.moveto(1, 1, [(500, 500), (300, 500)], False)

    Sprite.DISPLAY.fill((60,70,80))
    Sprite.objList.update()
    Sprite.Player.update()
    
    # Note, please change layers depending on y value: https://www.reddit.com/r/pygame/comments/3de4ng/challenge_drawing_in_the_right_order/
    # Answer: https://github.com/iminurnamez/draw-order-challenge/commit/387da00cf21e63d0cddee61737df3edd91aa59b4
    
    pygame.draw.rect(Sprite.DISPLAY, (200, 10, 15), Sprite.Player.colliderect, 2)
    pygame.draw.rect(Sprite.DISPLAY, (200, 15, 15), Sprite.objPerson.colliderect, 2)
    pygame.draw.rect(Sprite.DISPLAY, (200, 15, 15), Sprite.Calendar.colliderect, 2)
    
    pygame.draw.rect(Sprite.DISPLAY, (40, 200, 45), Sprite.objPerson.interactrect, 2)
    pygame.draw.rect(Sprite.DISPLAY, (40, 200, 15), Sprite.Calendar.interactrect, 2)

    Sprite.drawSprites(Sprite.spritesList)

    
    pygame.display.update()
    fpsClock.tick(FPS)
