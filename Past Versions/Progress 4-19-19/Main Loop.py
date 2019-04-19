import pygame, sys, time, os
from pygame.locals import *
from Files import Sprite, Var
pygame.init()

FPS=40
fpsClock= pygame.time.Clock()

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
    print(Var.mousePOS)
    
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # placed here instead of earlier so that it only registers as TRUE once (when pressed), not when held down
                Var.keySPACE = True
            else:
                Var.keySPACE = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Var.mouseCLICK = True
        else:
            Var.mouseCLICK = False

    Sprite.DISPLAY.fill((60,70,80))
    Sprite.objPerson.moveto(4, 4, [(50,5), (300, 5), (300, 300), (50, 300)], False)
    Sprite.objPlayerMono.moveto(4, 4, [Var.mousePOS], False)
    #print('player', Sprite.objPlayerMono.posx , Sprite.objPlayerMono.posx, 'is' + Sprite.objPlayerMono.direction, 'was' + Sprite.objPlayerMono.wasdirection,
     #     'index' + str(Sprite.objPlayerMono.index),
      #    'length' + str(len(Sprite.objPlayerMono.images[Sprite.objPlayerMono.direction])))
    Sprite.objList.update()
    Sprite.Player.update()

    pygame.display.update()
    fpsClock.tick(FPS)
