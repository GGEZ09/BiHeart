import random
import os
import sys

import pygame
from pygame.locals import *
pygame.font.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800,480),0,32)
clock=pygame.time.Clock()

def imageLoad(name, card):              #
    if card == 1:
        fullname = os.path.join("images/cards/", name)
    else: fullname = os.path.join('images', name)
    
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', name)
        raise SystemExit
    image = image.convert()
    
    return image, image.get_rect()

def display(font, sentence):
    displayFont = pygame.font.Font.render(font, sentence, 1, (255,255,255), (0,0,0)) 
    return displayFont

def mainGame():
    pic=pygame.image.load("images/cards/Card_Heart.png")
    
    x,y=0,150
    movex,movey=2,2

    while True:
        x+=movex
        y+=movey
        if x<=0 or x>=800:
            movex=-movex
        if y<=0 or y>=480:
            movey=-movey
        background, backgroundRect = imageLoad("bjs2.png", 0)
        screen.blit(background, backgroundRect)
        screen.blit(pic,(x,y))
        pygame.display.flip()
        clock.tick(20)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mX, mY = pygame.mouse.get_pos()
                    click = 1
            elif event.type == MOUSEBUTTONUP:
                mX, mY = 0, 0
                click = 0

if __name__ == "__main__":
    mainGame()
