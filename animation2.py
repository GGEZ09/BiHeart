import pygame
import os
import random
import sys

pygame.init()
screen = pygame.display.set_mode((800,480),0,32)
clock = pygame.time.Clock()  # A clock to limit the frame rate.
pygame.display.set_caption("this game")

def imageLoad(name, card):              #
    if card == 1:
        fullname = os.path.join("images/cards/", name)
    else: fullname = os.path.join('images/', name)
    
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

class Background:
    picture, backgroundRect = imageLoad("bjs2.png", 0)

    def __init__(self, x, y):
        self.xpos = x
        self.ypos = y

    def draw(self):
        screen.blit(self.picture, (self.xpos, self.ypos))


class player_1:
    name="dah.gif"
    fullname = os.path.join('images/', name)
    picture = pygame.image.load(fullname)

    def __init__(self, x, y):
        self.ypos = y
        self.xpos = x
        self.speed_x = 0
        self.speed_y = 0
        self.rect = self.picture.get_rect()


    def update(self):
        self.xpos =+ self.speed_x
        self.ypos =+ self.speed_y

    def draw(self):      #left right
        #screen.blit(pygame.transform.flip(self.picture, True, False), self.rect)
        screen.blit(self.picture, (self.xpos, self.ypos))



#player_two_bullet_list = pygame.sprite.Group()
player_one = player_1(0, 0)
#player_two = player_2(0, 720)
cliff = Background(0, 0)

while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player_one.speed_y = -5

                elif event.key == pygame.K_s:
                    player_one.speed_y = 5

                #elif event.key == pygame.K_UP:
                    #player_two.speed_y = -5

                #elif event.key == pygame.K_DOWN:
                    #player_two.speed_y = 5


                #elif event.key == pygame.K_KP0:
                    #bullet_player_two = Bullet_player_2

                    #bullet_player_two.ypos = player_two.ypos
                    #bullet_player_two.xpos = player_two.xpos

                    #bullet_player_two.speed_x = 14

                    #player_two_bullet_list.add(bullet_player_two)


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d and player_one.speed_x > 0:
                    player_one.speed_x = 0
                elif event.key == pygame.K_a and player_one.speed_x < 0:
                    player_one.speed_x = 0


                #elif event.key == pygame.K_UP and player_two.speed_x > 0:
                    #player_two.speed_x = 0
                #elif event.key == pygame.K_DOWN and player_two.speed_x < 0:
                    #player_two.speed_x = 0


    player_one.update()
    #player_two.update()
    player_one.draw()
    #player_two.draw()

    #player_two_bullet_list.update()


    #for bullet_player_two in player_two_bullet_list:
            #bullet_player_two.draw()


    pygame.display.flip()
    clock.tick(60)
