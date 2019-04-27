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

    Sprite.objPerson.moveto(1, 1, [(100, 100), (500, 50), (50, 500)], True)

    Sprite.DISPLAY.fill((60,70,80))
    Sprite.objList.update()
    Sprite.Player.update()

    # print( pygame.sprite.collide_rect(Sprite.Player, Sprite.objPerson))
    
    pygame.display.update()
    fpsClock.tick(FPS)
