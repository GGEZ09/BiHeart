import random
import os
import sys

import pygame
from pygame.locals import *
pygame.font.init()
pygame.mixer.init()
import serial
import time
ser=0

def init_serial():
    COMNUM=0
    global ser = serial.Serial(‘/dev/ttyAMA0’, 9600, timeout=1)
    ser.open()
    if ser.isOpen():
        print('Open : '+ser.portstr)

def send_data(COMM,data1,data2):
    msg=[0xA1,0xF1]
    msg.append(int(ord(str(COMM)),16))
    msg.append(int(ord(str(data1)),16))
    msg.append(int(ord(str(data2)),16))
    ser.flushInput()
    ser.write(msg)
    time.sleep(0.3)
    print('I send >> : ',chr(msg[2]),chr(msg[3]),chr(msg[4]))
	
def receive_data_first():
    bytes=ser.readline(3)
    #bytes=bytes[1:]
    ser.flushOutput()
    time.sleep(0.3)
    print('I sent << : '+bytes)
    return bytes

def receive_data():
    bytes=ser.readline()
    #if len(bytes)>3:
    #    bytes=bytes[1:]
    temp=bytes
    ser.flushOutput()
    time.sleep(0.3)
    print('I sent << : '+bytes)
    return bytes

mode="" # main 1,2 / deck 1,2 / pregame / draw / shuffle / att / def / battle

maxlengthdeck=20
screen = pygame.display.set_mode((800, 480))
clock = pygame.time.Clock()
CT=["Card_Attack.png","Card_Snipe.png","Card_Shield.png","Card_Flash.png","Card_Negate.png","Card_Hide.png","Card_Heart.png"]
TT=["Thumb_Attack.png","Thumb_Snipe.png","Thumb_Shield.png","Thumb_Flash.png","Thumb_Negate.png","Thumb_Hide.png","Thumb_Heart.png"]
PT={1:[400], 2:[325,475], 3:[250,400,550], 4:[175,325,475,625], 5:[100,250,400,550,700], 6:[75,205,335,465,595,725], 7:[76,184,292,400,528,616,724], 8:[76,168,261,354,446,539,632,724], 9:[76,157,238,319,400,481,562,643,724]}
beige=(242,234,191)
refb=(255,0,0)
wine=(208,148,130)

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
    
    class cardSprite(pygame.sprite.Sprite):
        """ Sprite that displays a specific card. """
        
        def __init__(self, card, position):
            pygame.sprite.Sprite.__init__(self)
            cardImage = card + ".png"
            self.image, self.rect = imageLoad(cardImage, 1)
            self.position = position
        def update(self):
            self.rect.center = self.position

    class cardAttack(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Card_Attack.png", 1)
            self.position = (75, 120)
            
        def update(self, mX, mY, click, dek2, hsu2, gsu2):
            self.image, self.rect = imageLoad("Card_Attack.png", 1)
            self.position = (75, 120)
            self.rect.center = self.position

            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect = imageLoad("Card_Attack.png", 1)
                self.position = (75, 120)
                self.rect.center = self.position
                hsu2+=1
                gsu2+=1
                
                if CT[0] in dek2:
                    dek2[CT[0]]+=1
                else:
                    dek2[CT[0]]=1
            
            return click, dek2, hsu2, gsu2

    class cardFlash(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Card_Flash.png", 1)
            self.position = (225, 360)
            
        def update(self, mX, mY, click, dek2, hsu2):
            self.image, self.rect =imageLoad("Card_Flash.png", 1)
            self.position = (225, 360)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Card_Flash.png", 1)
                self.position = (225, 360)
                self.rect.center = self.position
                hsu2+=1

                if CT[3] in dek2:
                    dek2[CT[3]]+=1
                else:
                    dek2[CT[3]]=1
            
            return click, dek2, hsu2

    class cardShield(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Card_Shield.png", 1)
            self.position = (375, 120)
            
        def update(self, mX, mY, click, dek2, hsu2):
            self.image, self.rect =imageLoad("Card_Shield.png", 1)
            self.position = (375, 120)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Card_Shield.png", 1)
                self.position = (375, 120)
                self.rect.center = self.position
                hsu2+=1

                if CT[2] in dek2:
                    dek2[CT[2]]+=1
                else:
                    dek2[CT[2]]=1
            
            return click, dek2, hsu2

    class cardNegate(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Card_Negate.png", 1)
            self.position = (75, 360)
            
        def update(self, mX, mY, click, dek2, hsu2):
            self.image, self.rect =imageLoad("Card_Negate.png", 1)
            self.position = (75, 360)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Card_Negate.png", 1)
                self.position = (75, 360)
                self.rect.center = self.position
                hsu2+=1

                if CT[4] in dek2:
                    dek2[CT[4]]+=1
                else:
                    dek2[CT[4]]=1
            
            return click, dek2, hsu2

    class cardSnipe(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Card_Snipe.png", 1)
            self.position = (225, 120)
            
        def update(self, mX, mY, click, dek2, hsu2, gsu2):
            self.image, self.rect =imageLoad("Card_Snipe.png", 1)
            self.position = (225, 120)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Card_Snipe.png", 1)
                self.position = (225, 120)
                self.rect.center = self.position
                hsu2+=1
                gsu2+=1

                if CT[1] in dek2:
                    dek2[CT[1]]+=1
                else:
                    dek2[CT[1]]=1
            
            return click, dek2, hsu2, gsu2
        
    class cardHide(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Card_Hide.png", 1)
            self.position = (375, 360)
            
        def update(self, mX, mY, click, dek2, hsu2):
            self.image, self.rect = imageLoad("Card_Hide.png", 1)
            self.position = (375, 360)
            self.rect.center = self.position

            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect = imageLoad("Card_Hide.png", 1)
                self.position = (375, 360)
                self.rect.center = self.position
                hsu2+=1
                
                if CT[5] in dek2:
                    dek2[CT[5]]+=1
                else:
                    dek2[CT[5]]=1
            
            return click, dek2, hsu2

    class thumbAttack(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Thumb_Attack.png", 1)
            self.position = (665, -40)
            
        def update(self, mX, mY, click, dek2, hsu2, gsu2, tw):
            self.image, self.rect =imageLoad("Thumb_Attack.png", 1)
            self.position = (665, tw)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Thumb_Attack.png", 1)
                self.position = (665, tw)
                self.rect.center = self.position
                hsu2-=1
                gsu2-=1

                if CT[0] in dek2:
                    if dek2[CT[0]]==1:
                        del dek2[CT[0]]
                    else:
                        dek2[CT[0]]-=1
            
            return click, dek2, hsu2, gsu2

    class thumbSnipe(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Thumb_Snipe.png", 1)
            self.position = (665, -40)
            
        def update(self, mX, mY, click, dek2, hsu2, gsu2,tw):
            self.image, self.rect =imageLoad("Thumb_Snipe.png", 1)
            self.position = (665, tw)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Thumb_Snipe.png", 1)
                self.position = (665, tw)
                self.rect.center = self.position
                hsu2-=1
                gsu2-=1

                if CT[1] in dek2:
                    if dek2[CT[1]]==1:
                        del dek2[CT[1]]
                    else:
                        dek2[CT[1]]-=1
            
            return click, dek2, hsu2, gsu2

    class thumbShield(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Thumb_Shield.png", 1)
            self.position = (665, -40)
            
        def update(self, mX, mY, click, dek2, hsu2,tw):
            self.image, self.rect =imageLoad("Thumb_Shield.png", 1)
            self.position = (665, tw)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Thumb_Shield.png", 1)
                self.position = (665, tw)
                self.rect.center = self.position
                hsu2-=1

                if CT[2] in dek2:
                    if dek2[CT[2]]==1:
                        del dek2[CT[2]]
                    else:
                        dek2[CT[2]]-=1
            
            return click, dek2, hsu2

    class thumbFlash(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Thumb_Flash.png", 1)
            self.position = (665, -40)
            
        def update(self, mX, mY, click, dek2, hsu2,tw):
            self.image, self.rect =imageLoad("Thumb_Flash.png", 1)
            self.position = (665, tw)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Thumb_Flash.png", 1)
                self.position = (665, tw)
                self.rect.center = self.position
                hsu2-=1

                if CT[3] in dek2:
                    if dek2[CT[3]]==1:
                        del dek2[CT[3]]
                    else:
                        dek2[CT[3]]-=1
            
            return click, dek2, hsu2

    class thumbNegate(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Thumb_Negate.png", 1)
            self.position = (665, -40)
            
        def update(self, mX, mY, click, dek2, hsu2,tw):
            self.image, self.rect =imageLoad("Thumb_Negate.png", 1)
            self.position = (665, tw)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Thumb_Negate.png", 1)
                self.position = (665, tw)
                self.rect.center = self.position
                hsu2-=1

                if CT[4] in dek2:
                    if dek2[CT[4]]==1:
                        del dek2[CT[4]]
                    else:
                        dek2[CT[4]]-=1
            
            return click, dek2, hsu2

    class thumbHide(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Thumb_Hide.png", 1)
            self.position = (665, -40)
            
        def update(self, mX, mY, click, dek2, hsu2,tw):
            self.image, self.rect =imageLoad("Thumb_Hide.png", 1)
            self.position = (665, tw)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Thumb_Hide.png", 1)
                self.position = (665, tw)
                self.rect.center = self.position
                hsu2-=1

                if CT[5] in dek2:
                    if dek2[CT[5]]==1:
                        del dek2[CT[5]]
                    else:
                        dek2[CT[5]]-=1
            
            return click, dek2, hsu2

    class buttonDeckOk(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Ok.png", 0)
            self.position = (627, 440)
            
        def update(self, mX, mY, click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2):
            self.image, self.rect =imageLoad("Ok.png", 0)
            self.position = (627, 440)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                deck=[]
                for i in dek2:
                    for j in range(dek2[i]):
                        deck.append(i)
                dek=dek2
                hsu=hsu2
                gsu=gsu2
                if hsu<maxlengthdeck:
                    mode="main1"
                else:
                    mode="main2"
                self.image, self.rect =imageLoad("Ok2.png", 0)
                self.position = (627, 440)
                self.rect.center = self.position
                print(gsu2,"/",hsu2)
                print('dek2 : ',dek2)
                print('dek : ',dek)
                print('deck : ', deck)
                
            return click, mode, deck, dek, hsu, gsu

    class buttonDeckCancel(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Cancel.png", 0)
            self.position = (742, 440)
            
        def update(self, mX, mY, click, mode):
            self.image, self.rect =imageLoad("Cancel.png", 0)
            self.position = (742, 440)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                if hsu < maxlengthdeck:
                    mode="main1"
                else:
                    mode="main2"
                click = 0
                self.image, self.rect =imageLoad("Cancel.png", 0)
                self.position = (742, 440)
                self.rect.center = self.position
                print(gsu2,"/",hsu2)
                print('dek2 : ',dek2)
                print('dek : ',dek)
                print('deck : ', deck)
            
            return click, mode
        
    class deckEdit(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("DeckEdit.png", 0)
            self.position = (600, 240)
            
        def update(self, mX, mY, click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2):
            self.image, self.rect = imageLoad("DeckEdit.png", 0)
            self.position = (600, 240)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                mode="deck1"
                click = 0
                self.image, self.rect = imageLoad("DeckEdit.png", 0)
                self.position = (600, 240)
                self.rect.center = self.position
                deck2=deck
                dek2={}
                for i in deck:
                    if i in dek2:
                        dek2[i]+=1
                    else:
                        dek2[i]=1
                hsu2=hsu
                gsu2=gsu
            return click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2
        
    class gameStart(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("GameStart.png", 0)
            self.position = (200, 240)
            
        def update(self, mX, mY, click, mode, deck3, deck, pHands, sun, tuk, que, cnt):
            self.image, self.rect = imageLoad("GameStart.png", 0)
            self.position = (200, 240)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                mode="main3" ## create or join??
                click = 0
                tuk=9
                que=[]
                cnt=2
                
                self.image, self.rect = imageLoad("GameStart.png", 0)
                self.position = (200, 240)
                self.rect.center = self.position
                deck3=shuffleDeck(deck) #shuffle my deck
            
            return click, mode, deck3, deck, pHands, sun, tuk, que, cnt
        
    class gameJoin(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("join.png", 0)
            self.position = (310, 280)
            
        def update(self, mX, mY, click, mode, sun):
            self.image, self.rect = imageLoad("join.png", 0)
            self.position = (310, 280)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                mode="join" ## server decide attack/defend, draw his card, go to "connent"
                click = 0

                sun=random.randint(0,1)
                
                self.image, self.rect = imageLoad("join.png", 0)
                self.position = (310, 280)
                self.rect.center = self.position
            
            return click, mode, sun

    class gameCreate(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("create.png", 0)
            self.position = (500, 280)
            
        def update(self, mX, mY, click, mode):
            self.image, self.rect = imageLoad("create.png", 0)
            self.position = (500, 280)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                mode="create" ## server decide attack/defend, draw his card, go to "connent"
                click = 0
                
                self.image, self.rect = imageLoad("create.png", 0)
                self.position = (500, 280)
                self.rect.center = self.position
            
            return click, mode
        
    class buttonMainTest(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("GameTest.png", 0)
            self.position = (310, 280)
            
        def update(self, mX, mY, click, mode):
            self.image, self.rect = imageLoad("GameTest.png", 0)
            self.position = (310, 280)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                mode="pregame" ## "connect"
                click = 0
                self.image, self.rect = imageLoad("GameTest.png", 0)
                self.position = (310, 280)
                self.rect.center = self.position
            
            return click, mode
        
    class buttonMainCancel(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Cancel2.png", 0)
            self.position = (500, 280)
            
        def update(self, mX, mY, click, mode):
            self.image, self.rect = imageLoad("Cancel2.png", 0)
            self.position = (500, 280)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                mode="main2"
                click = 0
                self.image, self.rect = imageLoad("Cancel2.png", 0)
                self.position = (500, 280)
                self.rect.center = self.position
            
            return click, mode

    class buttonGameSurren(pygame.sprite.Sprite):   # # 
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Surren.png", 0)
            self.position = (745, 40)
            
        def update(self, mX, mY, click, mode):
            self.image, self.rect = imageLoad("Surren.png", 0)
            self.position = (745, 40)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                mode="main2"
                click = 0
                self.image, self.rect = imageLoad("Surren.png", 0)
                self.position = (745, 40)
                self.rect.center = self.position
            
            return click, mode

    class buttonGameOk(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Ok.png", 0)
            self.position = (745, 200)
            
        def update(self, mX, mY, click, mode, sun, pHands, oHands, deck3, cnt):
            self.image, self.rect = imageLoad("Ok.png", 0)
            self.position = (745, 200)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                if mode=="pregame":
                    if sun==0:
                        pHands,deck3,dr=draw(pHands,deck3,2)
                        mode="att"
                    else:
                        mode="def"
                elif mode=="def":
                    mode='defcom'
                elif mode=="att":
                    mode='attcom'
                elif mode=="win"or mode=="los":
                    mode='main2'
                click = 0
                self.image, self.rect = imageLoad("Ok.png", 0)
                self.position = (745, 200)
                self.rect.center = self.position
            
            return click, mode, sun, pHands, oHands, deck3, cnt

    class buttonGameTurnj(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Turnj.png", 0)
            self.position = (745, 120)
            
        def update(self, mX, mY, click, mode, que):
            self.image, self.rect = imageLoad("Turnj.png", 0)
            self.position = (745, 120)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect = imageLoad("Turnj.png", 0)
                self.position = (745, 120)
                self.rect.center = self.position
                que=['T',9,9]
                mode='attcom'
            
            return click, mode, que

    class opponentCard(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("back.png", 1)
            self.position = (-40, 120)
            
        def update(self, mX, mY, click, mode, gtwi, opos, que):
            self.image, self.rect = imageLoad("back.png", 1)
            self.position = (gtwi, 120)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect = imageLoad("back.png", 1)
                self.position = (gtwi, 120)
                self.rect.center = self.position

                if mode=="att" and len(que)==3:
                    if que[0]=="A":
                        que[2]=opos
            
            return click, mode, que

    class playerCard(pygame.sprite.Sprite):   #1
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("back.png", 1)
            self.position = (-40, 360)
            
        def update(self, mX, mY, click, mode, ptwi, tuk, pos, pHands, que):
            self.image, self.rect = imageLoad(pHands[pos], 1)
            if tuk==pos:
                self.position = (ptwi, 330)
            else:
                self.position = (ptwi, 360)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                if mode=="def":
                    que.append(pos)
                    if len(que)==2:
                        pHands[que[0]],pHands[que[1]]=pHands[que[1]],pHands[que[0]]
                        que=[]

                elif mode=="att":
                    pp=pHands[pos]
                    if pp in CT[:2]:
                        if pp == CT[0]:
                            que=["A",pos,9]
                        elif pp == CT[1]:
                            que=["S",pos,9]
                    elif pp == CT[5]:
                        que=["H",pos,9]
                print(pos,que)
                        
            return click, mode, que, pHands

    def shuffleDeck(deck):   #
        l=len(deck)
        for i in range(l-2): #0~17
            t=random.randint(i+1,l-1)
            deck[t],deck[i]=deck[i],deck[t]
        return deck

    def draw(p, d, n):
        if n==1:
            if len(d)==0:
                return p, d, 0
            if len(p)==0:
                return p, d, 0
            elif len(p)<=8:
                p=p+d[:1]
                d=d[1:]
                n=1#succeed draw
            elif len(p)==9:
                d=d[1:]
                n=-1#hand destroy
            return p, d, n
        
        if n==2:
            if len(d)>=2:
                tmp=2
                n=2
            elif len(d)==1:
                tmp=1
                n=1
            elif len(d)==0:
                return p, d, 0
            if len(p)==0:
                return p, d, 0
            elif len(p)<=7:
                p=p+d[:tmp]
                d=d[tmp:]
                n=tmp
            elif len(p)==8:
                p=p+d[:1]
                d=d[tmp:]
                n=1
            elif len(p)==9:
                d=d[tmp:]
                n=-tmp
            return p, d, n

    def upol(o,i):
        o+=i
        if o>9:
            o=9
        elif o<0:
            o=0
        return o
            
    init_serial()
    state=0
    textFont = pygame.font.Font(None,28)
    background, backgroundRect = imageLoad("bjs2.png", 0)        #D09482 / 208 148 130
    oCards = pygame.sprite.Group()
    pCards = pygame.sprite.Group()     #
    dE = deckEdit()                         #
    gS = gameStart()                        #
    gJ = gameJoin()
    gC = gameCreate()
    cA = cardAttack()
    cF = cardFlash()
    cSh = cardShield()
    cN = cardNegate()
    cS = cardSnipe()
    cH = cardHide()
    bDO = buttonDeckOk()
    bDC = buttonDeckCancel()
    tA=thumbAttack()
    tS=thumbSnipe()
    tSh=thumbShield()
    tF=thumbFlash()
    tN=thumbNegate()
    tH=thumbHide()
    bMT=buttonMainTest()
    bMC=buttonMainCancel()
    bGS=buttonGameSurren()
    bGO=buttonGameOk()
    bGT=buttonGameTurnj()
    o1=opponentCard()
    o2=opponentCard()
    o3=opponentCard()
    o4=opponentCard()
    o5=opponentCard()
    o6=opponentCard()
    o7=opponentCard()
    o8=opponentCard()
    o9=opponentCard()
    p1=playerCard()
    p2=playerCard()
    p3=playerCard()
    p4=playerCard()
    p5=playerCard()
    p6=playerCard()
    p7=playerCard()
    p8=playerCard()
    p9=playerCard()
            
    buttons = pygame.sprite.Group(dE, gS)
    deck=[]                 #
    deck2=[]                #
    deck3=[]                #
    que=[]
    to=0                    #timeout
    to2=0
    tuk=9
    n1=0#opponent card show flag
    n2=9#player card show flag(<9)
    acl=0#Location of attackers card
    dcl=0#Location of defenders card
    dr1=0#cards came to my hand at Draw 1
    dr2=0#cards came to my hand at Draw 2
    x1,x2,y1,y2=0.0,0.0,0.0,0.0
    chax1=0.0
    chay1=0.0
    chax2=0.0
    chay2=0.0
    
    dek={}
    dek2={}

    sun=0 #
    cnt=2 #
    pHands, oHands,pPos,oPos= [], [], 0, 0
    buf=0
    pHeart=2
    oHeart=2
	
    ol=6
    mX, mY = 0, 0
    click = 0
    mode="main1"
    modedp=""
    hsu=0
    gsu=0
    hsu2=0
    gsu2=0
    
    while True:
        
        while mode=="main1": #
            state=0
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)             #
            
            titleFont = pygame.font.Font.render(textFont, "Deck is Not Set", 1, (25,25,25), wine)#(208,148,130)
            screen.blit(titleFont, (10, 440))

            gs, backgroundRect = imageLoad("GameStart2.png", 0)   #
            screen.blit(gs, (60,140))                        
            
            title, backgroundRect = imageLoad("title.png", 0)  
            screen.blit(title, (230,30))                        
            buttons = pygame.sprite.Group(dE)
            click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2 = dE.update(mX, mY, click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2)
            buttons.draw(screen)
            
            pygame.display.flip() 
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

        while mode=="main2":
            state=0
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)
            
            title, backgroundRect = imageLoad("title.png", 0)
            screen.blit(title, (230,30))
            buttons = pygame.sprite.Group(dE, gS)
            click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2 = dE.update(mX, mY, click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2)
            click, mode, deck3, deck, pHands ,sun, tuk, que, cnt = gS.update(mX, mY, click, mode, deck3, deck, pHands, sun, tuk, que, cnt)
            buttons.draw(screen)
                
            clock.tick(60)
            pygame.display.flip() 
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

        while mode=="main3": #
            to=0
            state=0
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)
            title, backgroundRect = imageLoad("title.png", 0)   #
            screen.blit(title, (230, 30))
            gsnoti, backgroundRect = imageLoad("GSNOTI.png", 0)   #
            screen.blit(gsnoti, (250, 165))
            buttons=pygame.sprite.Group(gJ, gC)
            buttons.draw(screen)
            click, mode, sun = gJ.update(mX, mY, click, mode, sun)
            click, mode = gC.update(mX, mY, click, mode)

            pygame.display.flip()                           #
        
            for event in pygame.event.get():
                if event.type==QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mX, mY = pygame.mouse.get_pos()
                        click = 1
                elif event.type == MOUSEBUTTONUP:
                    mX, mY = 0, 0
                    click = 0
        
        while mode=="deck1": 
            if hsu2>19:
                mode="deck2"
                break
            textFont2 = pygame.font.Font(None,55)
            background, backgroundRect = imageLoad("bjs.png", 0)    #f2 ea bf / 242 234 191
            screen.blit(background, backgroundRect)
            t=1
            tn=[0,0,0,0,0,0]
            for i in range(5):
                if CT[i] in dek2:
                    tn[i]=dek2[CT[i]]
            twitch=[-33,-33,-33,-33,-33,-33]
            twi=-33
            fs0="";fs1="";fs2="";fs3="";fs4="";fs5="";
            if CT[0] in dek2:
                buttons0=pygame.sprite.Group(tA)
                twi+=66
                twitch[0]=twi
                if dek2[CT[0]] > 1:
                    fs0 = str(dek2[CT[0]])
                buttons0.draw(screen)
            if CT[1] in dek2:
                buttons1=pygame.sprite.Group(tS)
                twi+=66
                twitch[1]=twi
                if dek2[CT[1]] > 1:
                    fs1 = str(dek2[CT[1]])
                buttons1.draw(screen)
            if CT[2] in dek2:
                buttons2=pygame.sprite.Group(tSh)
                twi+=66
                twitch[2]=twi
                if dek2[CT[2]] > 1:
                    fs2 = str(dek2[CT[2]])
                buttons2.draw(screen)
            if CT[3] in dek2:
                buttons3=pygame.sprite.Group(tF)
                twi+=66
                twitch[3]=twi
                if dek2[CT[3]] > 1:
                    fs3 = str(dek2[CT[3]])
                buttons3.draw(screen)
            if CT[4] in dek2:
                buttons4=pygame.sprite.Group(tN)
                twi+=66
                twitch[4]=twi
                if dek2[CT[4]] > 1:
                    fs4 = str(dek2[CT[4]])
                buttons4.draw(screen)
            if CT[5] in dek2:
                buttons5=pygame.sprite.Group(tH)
                twi+=66
                twitch[5]=twi
                if dek2[CT[5]] > 1:
                    fs5 = str(dek2[CT[5]])
                buttons5.draw(screen)

            f0 = pygame.font.Font.render(textFont2, fs0, 1, (255,255,30), (0x8f,0x68,0x68))
            f1 = pygame.font.Font.render(textFont2, fs1, 1, (255,255,30), (0x8f,0x68,0x68))
            f2 = pygame.font.Font.render(textFont2, fs2, 1, (255,255,30), (0x29,0x29,0x29))
            f3 = pygame.font.Font.render(textFont2, fs3, 1, (255,255,30), (0x29,0x29,0x29))
            f4 = pygame.font.Font.render(textFont2, fs4, 1, (255,255,30), (0x29,0x29,0x29))
            f5 = pygame.font.Font.render(textFont2, fs5, 1, (255,255,30), (0x3b,0x6b,0xce))

            screen.blit(f0, (710, twitch[0]-20))
            screen.blit(f1, (710, twitch[1]-20))
            screen.blit(f2, (710, twitch[2]-20))
            screen.blit(f3, (710, twitch[3]-20))
            screen.blit(f4, (710, twitch[4]-20))
            screen.blit(f5, (710, twitch[5]-20))

            buttons=pygame.sprite.Group(cA,cF,cSh,cN,cH,cS,bDO,bDC)
            
            click, dek2, hsu2, gsu2 = cA.update(mX, mY, click, dek2, hsu2, gsu2)          
            click, dek2, hsu2, gsu2 = cS.update(mX, mY, click, dek2, hsu2, gsu2)
            click, dek2, hsu2 = cF.update(mX, mY, click, dek2, hsu2)
            click, dek2, hsu2 = cSh.update(mX, mY, click, dek2, hsu2)
            click, dek2, hsu2 = cN.update(mX, mY, click, dek2, hsu2)
            click, dek2, hsu2 = cH.update(mX, mY, click, dek2, hsu2)
            click, dek2, hsu2, gsu2 = tA.update(mX, mY, click, dek2, hsu2, gsu2, twitch[0])          
            click, dek2, hsu2, gsu2 = tS.update(mX, mY, click, dek2, hsu2, gsu2, twitch[1])
            click, dek2, hsu2 = tSh.update(mX, mY, click, dek2, hsu2, twitch[2])
            click, dek2, hsu2 = tF.update(mX, mY, click, dek2, hsu2, twitch[3])
            click, dek2, hsu2 = tN.update(mX, mY, click, dek2, hsu2, twitch[4])
            click, dek2, hsu2 = tH.update(mX, mY, click, dek2, hsu2, twitch[5])
            click, mode, deck, dek, hsu, gsu = bDO.update(mX, mY, click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2)
            click, mode = bDC.update(mX, mY, click, mode)

            hsuFont = pygame.font.Font.render(textFont, (str(hsu2)+"/20"), 1, (5,5,5), (242,234,191))
            screen.blit(hsuFont, (475, 405))
            gsuFont = pygame.font.Font.render(textFont, (str(gsu2)+"(>9)"), 1, (5,5,5), (242,234,191))
            screen.blit(gsuFont, (475, 455))
            
            buttons.draw(screen)
                
            pygame.display.flip() 
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

        while mode=="deck2": 
            if hsu2<20:
                mode="deck1"
                break
            textFont2 = pygame.font.Font(None,55)
            background, backgroundRect = imageLoad("bjs.png", 0)    #f2 ea bf / 242 234 191
            screen.blit(background, backgroundRect)
            t=1
            tn=[0,0,0,0,0,0]
            for i in range(5):
                if CT[i] in dek2:
                    tn[i]=dek2[CT[i]]
            twitch=[-33,-33,-33,-33,-33,-33]
            twi=-33
            fs0="";fs1="";fs2="";fs3="";fs4="";fs5="";
            if CT[0] in dek2:
                buttons0=pygame.sprite.Group(tA)
                twi+=66
                twitch[0]=twi
                if dek2[CT[0]] > 1:
                    fs0 = str(dek2[CT[0]])
                buttons0.draw(screen)
            if CT[1] in dek2:
                buttons1=pygame.sprite.Group(tS)
                twi+=66
                twitch[1]=twi
                if dek2[CT[1]] > 1:
                    fs1 = str(dek2[CT[1]])
                buttons1.draw(screen)
            if CT[2] in dek2:
                buttons2=pygame.sprite.Group(tSh)
                twi+=66
                twitch[2]=twi
                if dek2[CT[2]] > 1:
                    fs2 = str(dek2[CT[2]])
                buttons2.draw(screen)
            if CT[3] in dek2:
                buttons3=pygame.sprite.Group(tF)
                twi+=66
                twitch[3]=twi
                if dek2[CT[3]] > 1:
                    fs3 = str(dek2[CT[3]])
                buttons3.draw(screen)
            if CT[4] in dek2:
                buttons4=pygame.sprite.Group(tN)
                twi+=66
                twitch[4]=twi
                if dek2[CT[4]] > 1:
                    fs4 = str(dek2[CT[4]])
                buttons4.draw(screen)
            if CT[5] in dek2:
                buttons5=pygame.sprite.Group(tH)
                twi+=66
                twitch[5]=twi
                if dek2[CT[5]] > 1:
                    fs5 = str(dek2[CT[5]])
                buttons5.draw(screen)

            f0 = pygame.font.Font.render(textFont2, fs0, 1, (255,255,30), (0x8f,0x68,0x68))
            f1 = pygame.font.Font.render(textFont2, fs1, 1, (255,255,30), (0x8f,0x68,0x68))
            f2 = pygame.font.Font.render(textFont2, fs2, 1, (255,255,30), (0x29,0x29,0x29))
            f3 = pygame.font.Font.render(textFont2, fs3, 1, (255,255,30), (0x29,0x29,0x29))
            f4 = pygame.font.Font.render(textFont2, fs4, 1, (255,255,30), (0x29,0x29,0x29))
            f5 = pygame.font.Font.render(textFont2, fs5, 1, (255,255,30), (0x3b,0x6b,0xce))

            screen.blit(f0, (710, twitch[0]-20))
            screen.blit(f1, (710, twitch[1]-20))
            screen.blit(f2, (710, twitch[2]-20))
            screen.blit(f3, (710, twitch[3]-20))
            screen.blit(f4, (710, twitch[4]-20))
            screen.blit(f5, (710, twitch[5]-20))

            if gsu2>9:      
                buttons=pygame.sprite.Group(bDO,bDC)
                click, mode, deck, dek, hsu, gsu = bDO.update(mX, mY, click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2)
            else:    
                buttons=pygame.sprite.Group(bDC)
            buttons.draw(screen)
            
            click, dek2, hsu2, gsu2 = tA.update(mX, mY, click, dek2, hsu2, gsu2, twitch[0])          
            click, dek2, hsu2, gsu2 = tS.update(mX, mY, click, dek2, hsu2, gsu2, twitch[1])
            click, dek2, hsu2 = tSh.update(mX, mY, click, dek2, hsu2, twitch[2])
            click, dek2, hsu2 = tF.update(mX, mY, click, dek2, hsu2, twitch[3])
            click, dek2, hsu2 = tN.update(mX, mY, click, dek2, hsu2, twitch[4])
            click, dek2, hsu2 = tH.update(mX, mY, click, dek2, hsu2, twitch[5])
            click, mode = bDC.update(mX, mY, click, mode)

            hsuFont = pygame.font.Font.render(textFont, (str(hsu2)+"/20"), 1, (255,5,5), (242,234,191))
            screen.blit(hsuFont, (475, 405))
            gsuFont = pygame.font.Font.render(textFont, (str(gsu2)+"(>9)"), 1, (255,5,5), (242,234,191))
            screen.blit(gsuFont, (475, 455))
                
            pygame.display.flip() 
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
                

        while mode=="join":#become client
            to+=1
            if to>=15:
                mode="main2"#recieve nothing or strainge data while I send data 5 times, Time Out 
                to=0
            try:
                if state==0:
                    send_data(0,0,0)#send 000 first when opponent recv it, he send 000 to me
                    temp=receive_data()#wait 000 in 5times
                    if temp=='000':
                        to=0
                        state=1
                elif state==1:
                    send_data(1,sun,0)#when recv 000, start communication and server send attack/defend info
                    temp=receive_data()
                    if temp=='1AC':
                        to=0
                        pHands=[CT[6],CT[6]]+deck3[:(sun+3)]
                        deck3=deck3[(sun+3):]
                        ol=sun+6
                        state=2
                elif state==2:
                    send_data(1,sun,0)
                    temp=receive_data()
                    if temp=='1AC':
                        to=0
                        oHeart=2
                        pHeart=2
                        state=0
                        mode="pregame"
            except:
                oo=0;
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)
            title, backgroundRect = imageLoad("title.png", 0)
            screen.blit(title, (230, 30))
            gsnoti, backgroundRect = imageLoad("GSNOTI.png", 0) 
            screen.blit(gsnoti, (250, 165))
            buttons=pygame.sprite.Group(bMT, bMC)
            buttons.draw(screen)
            click, mode = bMT.update(mX, mY, click, mode)
            click, mode = bMC.update(mX, mY, click, mode)
                
            pygame.display.flip() 
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

        while mode=="create":#become server
            to+=1
            if to>=15:
                mode="main2"#recieve nothing or strainge data while I send data 5 times, Time Out 
                to=0
            try:
                if state==0:
                    temp=receive_data_first()#wait in 5times first
                    if temp=='000':
                        to=0
                        state=1
                        
                elif state==1:
                    send_data(0,0,0)
                    temp=receive_data()
                    if temp[0]=='1':
                        to=0
                        state=2
                        sun=(int(temp[1])+1)%2
                        pHands=[CT[6],CT[6]]+deck3[:(sun+3)]
                        deck3=deck3[(sun+3):]
                        ol=sun+6
                        
                elif state==2:
                    send_data(1,'A','C')
                    temp=receive_data()
                    if temp=='999':
                        to=0
                        oHeart=2
                        pHeart=2
                        state=0
                        mode="pregame"
            except:
                oo=0;

            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)
            title, backgroundRect = imageLoad("title.png", 0)   #
            screen.blit(title, (230, 30))
            gsnoti, backgroundRect = imageLoad("GSNOTI.png", 0)   #
            screen.blit(gsnoti, (250, 165))
            buttons=pygame.sprite.Group(bMT, bMC)
            buttons.draw(screen)
            click, mode = bMT.update(mX, mY, click, mode)
            click, mode = bMC.update(mX, mY, click, mode)

            pygame.display.flip()                           #
        
            for event in pygame.event.get():
                if event.type==QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mX, mY = pygame.mouse.get_pos()
                        click = 1
                elif event.type == MOUSEBUTTONUP:
                    mX, mY = 0, 0
                    click = 0
            
        while mode=="pregame":
            try:
                if to<5:
                    send_data(9,9,9)
                    to+=1
            except:
                oo=0;
            cnt=2
            oHeart=2
            pHeart=2
            to2=0
            background, backgroundRect = imageLoad("bjs.png", 0)
            screen.blit(background, backgroundRect)
            if sun==0:#sun=> 0 : attack / 1 : defend
                title, backgroundRect = imageLoad("sun.png", 0)
            else :
                title, backgroundRect = imageLoad("hu.png", 0) 
            screen.blit(title, (100, 10))
            buttons=pygame.sprite.Group(bGS, bGO)
            buttons.draw(screen)
            pPT=PT[len(pHands)]
            j=0
            c=[0]*len(pHands)
            for i in pPT:
                c[j], backgroundRect = imageLoad(pHands[j], 1)
                c[j].set_colorkey(beige)
                screen.blit(c[j], (i-75, 240))
                j+=1
            click, mode = bGS.update(mX, mY, click, mode)
            click, mode, sun, pHands, oHands, deck3, cnt = bGO.update(mX, mY, click, mode, sun, pHands, oHands, deck3, cnt)
                
            pygame.display.flip() 
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
                    
        while mode=="att" or mode=="def":
            try:
                if to2<5:
                    modedp=mode
                    to=0
                    to2+=1
            except:
                oo=0;
            tuk=9
            background, backgroundRect = imageLoad("bjs.png", 0)
            screen.blit(background, backgroundRect)
            if mode=="att":
                buttons=pygame.sprite.Group(bGS, bGT, bGO)
            else :
                buttons=pygame.sprite.Group(bGS, bGO)
            buttons.draw(screen)

            if len(pHands)>9:
                pHands=pHands[:9]
            pPT=PT[len(pHands)]
            j=0
            c=[0]*len(pHands)
            ptwitch=[-40,-40,-40,-40,-40,-40,-40,-40,-40]
            gtwitch=[-40,-40,-40,-40,-40,-40,-40,-40,-40]
            l=len(pHands)
            gtwi=38
            ptwi=38
            for i in range(ol):
                gtwitch[i]=gtwi
                gtwi+=76
            for i in range(l):
                ptwitch[i]=pPT[i]
            buttons1=pygame.sprite.Group(o1,o2,o3,o4,o5,o6,o7,o8,o9)
            buttons1.draw(screen)
            click, mode = bGS.update(mX, mY, click, mode)
            click, mode, sun, pHands, oHands, deck3, cnt = bGO.update(mX, mY, click, mode, sun, pHands, oHands, deck3, cnt)
            click, mode, que = bGT.update(mX, mY, click, mode, que)
            click, mode, que = o1.update(mX, mY, click, mode, gtwitch[0], 0, que)
            click, mode, que = o2.update(mX, mY, click, mode, gtwitch[1], 1, que)
            click, mode, que = o3.update(mX, mY, click, mode, gtwitch[2], 2, que)
            click, mode, que = o4.update(mX, mY, click, mode, gtwitch[3], 3, que)
            click, mode, que = o5.update(mX, mY, click, mode, gtwitch[4], 4, que)
            click, mode, que = o6.update(mX, mY, click, mode, gtwitch[5], 5, que)
            click, mode, que = o7.update(mX, mY, click, mode, gtwitch[6], 6, que)
            click, mode, que = o8.update(mX, mY, click, mode, gtwitch[7], 7, que)
            click, mode, que = o9.update(mX, mY, click, mode, gtwitch[8], 8, que)
            
            if len(que)==3:
                tuk=que[1]
                if que[2]<9:
                    poi, backgroundRect = imageLoad("target.png", 0)
                    poi.set_colorkey((0,0,0))
                    screen.blit(poi, (gtwitch[que[2]]-22, 120))
                    
            pp1=pygame.sprite.Group(p1)
            pp1.draw(screen)
            click, mode, que, pHands = p1.update(mX, mY, click, mode, ptwitch[0],tuk, 0, pHands, que)
            if l>1:
                pp2=pygame.sprite.Group(p2)
                pp2.draw(screen)
                click, mode, que, pHands = p2.update(mX, mY, click, mode, ptwitch[1],tuk, 1, pHands, que)
            if l>2:
                pp3=pygame.sprite.Group(p3)
                pp3.draw(screen)
                click, mode, que, pHands = p3.update(mX, mY, click, mode, ptwitch[2],tuk, 2, pHands, que)
            if l>3:
                pp4=pygame.sprite.Group(p4)
                pp4.draw(screen)
                click, mode, que, pHands = p4.update(mX, mY, click, mode, ptwitch[3],tuk, 3, pHands, que)
            if l>4:
                pp5=pygame.sprite.Group(p5)
                pp5.draw(screen)
                click, mode, que, pHands = p5.update(mX, mY, click, mode, ptwitch[4],tuk, 4, pHands, que)
            if l>5:
                pp6=pygame.sprite.Group(p6)
                pp6.draw(screen)
                click, mode, que, pHands = p6.update(mX, mY, click, mode, ptwitch[5],tuk, 5, pHands, que)
            if l>6:
                pp7=pygame.sprite.Group(p7)
                pp7.draw(screen)
                click, mode, que, pHands = p7.update(mX, mY, click, mode, ptwitch[6],tuk, 6, pHands, que)
            if l>7:
                pp8=pygame.sprite.Group(p8)
                pp8.draw(screen)
                click, mode, que, pHands = p8.update(mX, mY, click, mode, ptwitch[7],tuk, 7, pHands, que)
            if l>8:
                pp9=pygame.sprite.Group(p9)
                pp9.draw(screen)
                click, mode, que, pHands = p9.update(mX, mY, click, mode, ptwitch[8],tuk, 8, pHands, que)
            for i in pPT:
                c[j], backgroundRect = imageLoad(pHands[j], 1)
                c[j].set_colorkey(beige)
                if tuk==j:
                    screen.blit(c[j], (i-75, 210))
                else:
                    screen.blit(c[j], (i-75, 240))
                j+=1
            if len(que)==1:
                swi, backgroundRect = imageLoad("switch.png", 0)
                swi.set_colorkey((255,255,255))
                screen.blit(swi, (pPT[que[0]]-25, 330))
                
            pygame.display.flip() 
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
		    
        while mode=="attcom":
            print(modedp, state)
            to+=1
            if to in [2,5,8,11,14]:
                time.sleep(0.1)
            if to>=20:
                mode=modedp
                to=0
                state=0
                continue
            try:
                if state==0:
                    send_data(0,0,0)
                    temp=receive_data()
                    ol2=ol
                    pHands2=pHands[:]
                    if temp=='000' or temp=='00' or temp[1:]=='00':
                        to=0
                        state=1
                elif state==1:
                    send_data(1,que[0],que[2])# -> ['2','A~T','0~8']
                    temp=receive_data()
                    if temp[0]=='2':#temp -> ['2','0~6','0']
                        n1=1
                        to=0
                        acl=que[1]
                        dcl=que[2]
                        if que[0]!='T':
                            del pHands[que[1]]
                            pHands2=pHands[:]
                        if que[0]=='A':#When I played 'Attack' at -->
                            ac, backgroundRect = imageLoad(CT[0], 1)
                            ac.set_colorkey(beige)
                            n2=1
                            dc, backgroundRect = imageLoad(CT[int(temp[1])], 1)
                            dc.set_colorkey(beige)
                            ol=upol(ol,-1)
                            if temp[1]=='4':#--> Negate : make my turn 1
                                cnt=1
                            elif temp[1]=='3':#--> Flash : opponent draw 2cards
                                ol=upol(ol,2)
                            elif temp[1]=='6':#--> Heart : subtract one of opponent's heart
                                oHeart-=1
                        elif que[0]=='S':#When I played 'Snipe' and -->
                            ac, backgroundRect = imageLoad(CT[1], 1)
                            ac.set_colorkey(beige)
                            if temp[1]=='0':#--> opponent has not secret card : nothing happend
                                oo=0;
                            else:#--> opponent has secret card : delete that card
                                n2=1
                                dc, backgroundRect = imageLoad(CT[int(temp[1])], 1)
                                dc.set_colorkey(beige)
                                ol=upol(ol,-1)
                        elif que[0]=='H':#When I played 'Hide' : draw two cards
                            ac, backgroundRect = imageLoad(CT[5], 1)
                            ac.set_colorkey(beige)
                            pHands,deck3,dr=draw(pHands,deck3,1)
                            dr1=dr
                            pHands,deck3,dr=draw(pHands,deck3,1)
                            dr2=dr
                        elif que[0]=='T':#When I click 'EndTurn' button : end turn
                            ac, backgroundRect = imageLoad("back.png", 1)
                            ac.set_colorkey(beige)
                            acl=0
                            cnt=1
                        
                        to2=0
                        if dcl<9:
                            x2=(dcl+1)*76-78
                        y2=60
                        pPT=PT[len(pHands2)]
                        x1=pPT[acl]-75
                        y1=240
                        chax1=((250-x1)/10)
                        chay1=-12
                        if n2<9:
                            chax2=((475-x2)/10)
                            chay2=6

                        mode="attani"
                        continue

            except:
                oo=0;
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)
            buttons=pygame.sprite.Group(bGS, bGO)
            buttons.draw(screen)
            pPT=PT[len(pHands2)]
            j=0
            c=[0]*len(pHands2)
            for i in pPT:
                c[j], backgroundRect = imageLoad(pHands2[j], 1)
                c[j].set_colorkey(beige)
                screen.blit(c[j], (i-75, 240))
                j+=1
            gtwitch=[-40,-40,-40,-40,-40,-40,-40,-40,-40]
            gtwi=38
            for i in range(ol2):
                gtwitch[i]=gtwi
                gtwi+=76
            buttons1=pygame.sprite.Group(o1,o2,o3,o4,o5,o6,o7,o8,o9)
            buttons1.draw(screen)
                
            pygame.display.flip() 
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

        while mode=="defcom":
            print(modedp, state)
            to+=1
            if to>=20:
                mode=modedp
                to=0
                state=0
                continue
            try:
                if state==0:
                    temp=receive_data()
                    ol2=ol
                    pHands2=pHands[:]
                    if temp=='000' or temp=='00' or temp[1:]=='00':
                        to=0
                        state=1
                elif state==1:
                    send_data(0,0,0)
                    temp=receive_data()
                    if temp[0]=='1':
                        n1=1
                        to=0
                        buf=0
                        t2=int(temp[2])
                        if temp[1]=='A':
                            n2=t2
                            dc, backgroundRect = imageLoad(pHands[t2], 1)
                            ac, backgroundRect = imageLoad(CT[0], 1)
                            ac.set_colorkey(beige)
                            ol=upol(ol,-1)
                            if t2>0: #if shield card locates leftside of opponent aimed card
                                if pHands[t2-1]==CT[2]:
                                    buf=2
                                    dc, backgroundRect = imageLoad(CT[2], 1)
                                    dcl=t2-1
                                    del pHands[t2-1]
                            if buf==0 and t2+1<len(pHands):#if shield card locates rightside of opponent aimed card
                                if pHands[t2+1]==CT[2]:
                                    buf=2
                                    dc, backgroundRect = imageLoad(CT[2], 1)
                                    dcl=t2+1
                                    del pHands[t2+1]
                            if buf==0:
                                buf=CT.index(pHands[t2])
                                if buf==3: #flash
                                    pHands,deck3,dr=draw(pHands,deck3,1)
                                    dr1=dr
                                    pHands,deck3,dr=draw(pHands,deck3,1)
                                    dr2=dr
                                elif buf==4: #Negate
                                    cnt=1
                                elif buf==6: #Heart
                                    buf=6
                                    pHeart-=1
                                #else : attack / snipe / hide
                                dc, backgroundRect = imageLoad(CT[buf], 1)
                                dcl=t2
                                del pHands[t2]
                            dc.set_colorkey(beige)
                        elif temp[1]=='S':
                            ac, backgroundRect = imageLoad(CT[1], 1)
                            ac.set_colorkey(beige)
                            ol=upol(ol,-1)
                            k1=0
                            for i in pHands:
                                if buf!=0:
                                    continue
                                for j in range(2,5):
                                    if i == CT[j]:
                                        buf=j
                                        n2=k1
                                        dc, backgroundRect = imageLoad(pHands[k1], 1)
                                        dc.set_colorkey(beige)
                                        dcl=k1
                                        del pHands[k1]
                                k1+=1
                        elif temp[1]=='H':
                            ac, backgroundRect = imageLoad(CT[5], 1)
                            ac.set_colorkey(beige)
                            ol=upol(ol,1)
                            buf=0
                        elif temp[1]=='T':
                            ac, backgroundRect = imageLoad("back.png", 1)
                            ac.set_colorkey(beige)
                            cnt=1
                        to2=0
                        x1=(acl+1)*76-78
                        y1=60
                        pPT=PT[len(pHands2)]
                        if dcl<9:
                            x2=pPT[dcl]-75
                        y2=240
                        chax1=((250-x1)/10)
                        chay1=6
                        if n2<9:
                            chax2=((475-x2)/10)
                            chay2=-12
                        mode="defani"
                        continue
                
            except:
                oo=0;
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)
            buttons=pygame.sprite.Group(bGS, bGO)
            buttons.draw(screen)
            pPT=PT[len(pHands2)]
            j=0
            c=[0]*len(pHands2)
            for i in pPT:
                c[j], backgroundRect = imageLoad(pHands2[j], 1)
                c[j].set_colorkey(beige)
                screen.blit(c[j], (i-75, 240))
                j+=1
            gtwitch=[-40,-40,-40,-40,-40,-40,-40,-40,-40]
            gtwi=38
            for i in range(ol2):
                gtwitch[i]=gtwi
                gtwi+=76
            buttons1=pygame.sprite.Group(o1,o2,o3,o4,o5,o6,o7,o8,o9)
            buttons1.draw(screen)
                
            pygame.display.flip() 
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


        while mode=="attani":
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)
            buttons=pygame.sprite.Group(bGS, bGO)
            buttons.draw(screen)
            pPT=PT[len(pHands2)]
            j=0
            c=[0]*len(pHands2)
            for i in pPT:
                c[j], backgroundRect = imageLoad(pHands2[j], 1)
                c[j].set_colorkey(beige)
                screen.blit(c[j], (i-75, 240))
                j+=1
            gtwitch=[-40,-40,-40,-40,-40,-40,-40,-40,-40]
            gtwi=38
            for i in range(ol2):
                gtwitch[i]=gtwi
                gtwi+=76
            buttons1=pygame.sprite.Group(o1,o2,o3,o4,o5,o6,o7,o8,o9)
            buttons1.draw(screen)

            if y1>120:
                x1+=chax1
                y1+=chay1
                screen.blit(ac,(x1,y1))
                if n2<9:
                    x2+=chax2
                    y2+=chay2
                    screen.blit(dc,(x2,y2))
                clock.tick(60)
                pygame.display.flip()
            else :
                if dr1==1:
                    if dr2==1:
                        d1, backgroundRect = imageLoad(pHands[-2], 1)
                        d1.set_colorkey(beige)
                        dn=2
                    else:
                        d1, backgroundRect = imageLoad(pHands[-1], 1)
                        d1.set_colorkey(beige)
                        dn=1
                    x3=800.0
                    y3=120.0
                    while x3>650:
                        x3-=(150/60)
                        screen.blit(d1,(x3,y3))
                        
                        clock.tick(60)
                        pygame.display.flip() 
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
                    pHands2.append(pHands[-dn])
                    pPT=PT[len(pHands2)]
                    j=0
                    c=[0]*len(pHands2)
                    for i in pPT:
                        c[j], backgroundRect = imageLoad(pHands2[j], 1)
                        c[j].set_colorkey(beige)
                        screen.blit(c[j], (i-75, 240))
                        j+=1
                    dr1=0
                if dr2==1:
                    d1, backgroundRect = imageLoad(pHands[-1], 1)
                    d1.set_colorkey(beige)
                    x3=800.0
                    y3=120.0
                    while x3>650:
                        x3-=(150/60)
                        screen.blit(d1,(x3,y3))
                        
                        clock.tick(60)
                        pygame.display.flip() 
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
                    pHands2.append(pHands[-1])
                    pPT=PT[len(pHands2)]
                    j=0
                    c=[0]*len(pHands2)
                    for i in pPT:
                        c[j], backgroundRect = imageLoad(pHands2[j], 1)
                        c[j].set_colorkey(beige)
                        screen.blit(c[j], (i-75, 240))
                        j+=1
                    dr2=0
                if dr1==0:
                    to=0
                    state=0
                    to2=0
                    que=[]
                    tuk=9
                    cnt-=1
                    x1,y1,x2,y2=0.0,0.0,0.0,0.0
                    n1=0
                    n2=9
                    t2=0
                    dr1=0
                    dr2=0
                    acl=0
                    dcl=0
                    if oHeart==0:
                        cnt=2
                        mode="win"
                        continue
                    if pHeart==0:
                        cnt=2
                        mode="los"
                        continue
                    if cnt==0:
                        cnt=2
                        ol=upol(ol,2)

                        d1, backgroundRect = imageLoad("switch.png", 0)
                        d1.set_alpha(0)
                        x3=800#My Turn symbol set for 1sec
                        y3=120
                        while x3>650:
                            x3-=(150/60)
                            screen.blit(d1,(x3,y3))
                            d2, backgroundRect = imageLoad("ot.png", 0)
                            d2.set_colorkey(beige)
                            screen.blit(d2,(100,130))
                                
                            clock.tick(60)
                            pygame.display.flip() 
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
                        
                        mode="def"
                        print('cnt :',cnt,'->',mode)
                        continue
                    else:
                        mode="att"
                        if mode=="def":
                            mode="att"
                        print('atttttcnt :',cnt,'->',mode)
            
            pygame.display.flip()
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

        while mode=="defani":
            try:
                while to2<10:
                    modedp="def"
                    to=0
                    send_data(2,buf,0)#send 999 5times to end opponent's 2nd state
                    to2+=1
            except:
                oo=0;
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)
            buttons=pygame.sprite.Group(bGS, bGO)
            buttons.draw(screen)
            pPT=PT[len(pHands2)]
            j=0
            c=[0]*len(pHands2)
            for i in pPT:
                c[j], backgroundRect = imageLoad(pHands2[j], 1)
                c[j].set_colorkey(beige)
                screen.blit(c[j], (i-75, 240))
                j+=1
            gtwitch=[-40,-40,-40,-40,-40,-40,-40,-40,-40]
            gtwi=38
            for i in range(ol2):
                gtwitch[i]=gtwi
                gtwi+=76
            buttons1=pygame.sprite.Group(o1,o2,o3,o4,o5,o6,o7,o8,o9)
            buttons1.draw(screen)

            if y1<120:
                x1+=chax1
                y1+=chay1
                screen.blit(ac,(x1,y1))
                if n2<9:
                    x2+=chax2
                    y2+=chay2
                    screen.blit(dc,(x2,y2))
                clock.tick(60)
                pygame.display.flip()
            else :
                if dr1==1:
                    if dr2==1:
                        d1, backgroundRect = imageLoad(pHands[-2], 1)
                        d1.set_colorkey(beige)
                        dn=2
                    else:
                        d1, backgroundRect = imageLoad(pHands[-1], 1)
                        d1.set_colorkey(beige)
                        dn=1
                    x3=800.0
                    y3=120.0
                    while x3>650:
                        x3-=(150/60)
                        screen.blit(d1,(x3,y3))
                        
                        clock.tick(60)
                        pygame.display.flip() 
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
                    pHands2.append(pHands[-dn])
                    pPT=PT[len(pHands2)]
                    j=0
                    c=[0]*len(pHands2)
                    for i in pPT:
                        c[j], backgroundRect = imageLoad(pHands2[j], 1)
                        c[j].set_colorkey(beige)
                        screen.blit(c[j], (i-75, 240))
                        j+=1
                    dr1=0
                if dr2==1:
                    d1, backgroundRect = imageLoad(pHands[-1], 1)
                    d1.set_colorkey(beige)
                    x3=800.0
                    y3=120.0
                    while x3>650:
                        x3-=(150/60)
                        screen.blit(d1,(x3,y3))
                        
                        clock.tick(60)
                        pygame.display.flip() 
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
                    pHands2.append(pHands[-1])
                    pPT=PT[len(pHands2)]
                    j=0
                    c=[0]*len(pHands2)
                    for i in pPT:
                        c[j], backgroundRect = imageLoad(pHands2[j], 1)
                        c[j].set_colorkey(beige)
                        screen.blit(c[j], (i-75, 240))
                        j+=1
                    dr2=0
                if dr1==0:
                    to=0
                    state=0
                    que=[]
                    tuk=9
                    cnt-=1
                    x1,y1,x2,y2=0.0,0.0,0.0,0.0
                    n1=0
                    n2=9
                    t2=0
                    to2=0
                    dr1=0
                    dr2=0
                    acl=0
                    dcl=0
                    if oHeart==0:
                        cnt=2
                        mode="win"
                        continue
                    if pHeart==0:
                        cnt=2
                        mode="los"
                        continue
                    if cnt==0:
                        cnt=2

                        d1, backgroundRect = imageLoad("switch.png", 0)
                        d1.set_alpha(0)
                        x3=800#My Turn symbol set for 1sec
                        y3=120
                        while x3>650:
                            x3-=(150/60)
                            screen.blit(d1,(x3,y3))
                            d2, backgroundRect = imageLoad("mt.png", 0)
                            d2.set_colorkey(beige)
                            screen.blit(d2,(100,130))
                                
                            clock.tick(60)
                            pygame.display.flip() 
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
                        
                        pHands,deck3,dr=draw(pHands,deck3,1)
                        dr1=dr
                        pHands,deck3,dr=draw(pHands,deck3,1)
                        dr2=dr
                        if dr1==1:
                            if dr2==1:
                                d1, backgroundRect = imageLoad(pHands[-2], 1)
                                d1.set_colorkey(beige)
                                dn=2
                            else:
                                d1, backgroundRect = imageLoad(pHands[-1], 1)
                                d1.set_colorkey(beige)
                                dn=1
                            x3=800.0
                            y3=120.0
                            while x3>650:
                                x3-=(150/60)
                                screen.blit(d1,(x3,y3))
                                
                                clock.tick(60)
                                pygame.display.flip() 
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
                            pHands2.append(pHands[-dn])
                            pPT=PT[len(pHands2)]
                            j=0
                            c=[0]*len(pHands2)
                            for i in pPT:
                                c[j], backgroundRect = imageLoad(pHands2[j], 1)
                                c[j].set_colorkey(beige)
                                screen.blit(c[j], (i-75, 240))
                                j+=1
                            dr1=0
                        if dr2==1:
                            d1, backgroundRect = imageLoad(pHands[-1], 1)
                            d1.set_colorkey(beige)
                            x3=800.0
                            y3=120.0
                            while x3>650:
                                x3-=(150/60)
                                screen.blit(d1,(x3,y3))
                                
                                clock.tick(60)
                                pygame.display.flip() 
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
                            pHands2.append(pHands[-1])
                            pPT=PT[len(pHands2)]
                            j=0
                            c=[0]*len(pHands2)
                            for i in pPT:
                                c[j], backgroundRect = imageLoad(pHands2[j], 1)
                                c[j].set_colorkey(beige)
                                screen.blit(c[j], (i-75, 240))
                                j+=1
                            dr2=0

                        dr1,dr2=0,0
                        mode="att"
                        print('cnt :',cnt,'->',mode)
                        continue
                    else:
                        mode="def"
                        print('cnt :',cnt,'->',mode)
                        continue
                    
            pygame.display.flip()
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

        while mode=="win": #
            try:
                if to2<5:
                    to=0
                    send_data(5,5,5)
                    to2+=1
            except:
                oo=0;
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)
            
            title, backgroundRect = imageLoad("title.png", 0)
            screen.blit(title, (230,30))
            buttons=pygame.sprite.Group(bGO)
            buttons.draw(screen)
            click, mode, sun, pHands, oHands, deck3, cnt = bGO.update(mX, mY, click, mode, sun, pHands, oHands, deck3, cnt)

            pygame.display.flip()                           #
        
            for event in pygame.event.get():
                if event.type==QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mX, mY = pygame.mouse.get_pos()
                        click = 1
                elif event.type == MOUSEBUTTONUP:
                    mX, mY = 0, 0
                    click = 0
                    
        while mode=="los": #
            try:
                if to2<5:
                    to=0
                    send_data(4,4,4)
                    to2+=1
            except:
                oo=0;
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)
            
            title, backgroundRect = imageLoad("title.png", 0)
            screen.blit(title, (230,30))
            buttons=pygame.sprite.Group(bGO)
            buttons.draw(screen)
            click, mode, sun, pHands, oHands, deck3, cnt = bGO.update(mX, mY, click, mode, sun, pHands, oHands, deck3, cnt)

            pygame.display.flip()                           #
        
            for event in pygame.event.get():
                if event.type==QUIT:
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
