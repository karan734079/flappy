import random #for generate random number
import sys
import pygame
from pygame.locals import *

#global variables for the game
FPS=32
SCREENWIDTH=289
SCREENHEIGHT=511
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY=SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER='gamedata/sprites/bird.png'
BACKGROUND='gamedata/sprites/background.png'
PIPE='gamedata/sprites/pipe.png'

def welcomescreen():
    #shows welcome images on the screen
    playerx=int(SCREENWIDTH/5)
    playery=int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    messagex=int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
    messagey=int(SCREENHEIGHT*0.13)
    basex=0

    while True:
        for event in pygame.event.get():
            #if user clicks on X button
            if event.type== QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
                # IF USER PRESSES THE SPACE OR UP KEY ,START THE GAME
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
           
def mainGame():
    score=0
    playerx=int(SCREENWIDTH/5)                
    playery=int(SCREENWIDTH/2)
    basex=0
    #create 2 pipes for blitting on the screen
    newpipe1=getRandomPipe()
    newpipe2=getRandomPipe()
    #my list of upper pipes
    upperpipes=[
        {'x':SCREENWIDTH+200,'y':newpipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newpipe2[0]['y']}
    ]
    #my list of lower pipes
    lowerpipes=[
        {'x':SCREENWIDTH+200,'y':newpipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newpipe2[1]['y']}
    ]
    pipevlx=-4

    playerVlY=-9
    playerMaxVlY=10
    playerMinvlY=-8
    playerAccY=1

    playerFlapVl= -8 #velocity while flapping
    playerFlapped= False #it is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type== QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery > 0:
                    playerVlY=playerFlapVl
                    playerFlapped=True
                    GAME_SOUNDS['wing'].play()

        crashtest=isCollide(playerx,playery,upperpipes,lowerpipes) #this function will return true if player is crashed
        if crashtest:
            return 

        #check for scroe
        playerMidPos=playerx+GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidPos=pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<=playerMidPos<pipeMidPos+4:
                score=score+1
                print(f"Your Score Is {score}")    
                GAME_SOUNDS['point'].play()    

        if playerVlY<playerMaxVlY and not playerFlapped:
            playerVlY+=playerAccY

        if playerFlapped:
            playerFlapped=False 

        playerheight=GAME_SPRITES['player'].get_height()
        playery=playery+min(playerVlY,GROUNDY-playery-playerheight)
        
        #moves pipes to the left
        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
            upperpipe['x']+=pipevlx
            lowerpipe['x']+=pipevlx

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperpipes[0]['x']<5:
            newpipe=getRandomPipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])
             
        #if pipe is out of the screen, remove it
        if upperpipes[0]['x']<-GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        #lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperpipe['x'],upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerpipe['x'],lowerpipe['y']))
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery)) 
        mydigits=[int(x) for x in list(str(score))]
        width=0
        for digits in mydigits:
            width+=GAME_SPRITES['numbers'][digits].get_width()
        xoffset=(SCREENWIDTH-width)/2

        for digits in mydigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digits],(xoffset,SCREENHEIGHT*0.12))
            xoffset+=GAME_SPRITES['numbers'][digits].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
def isCollide(playerx,playery,upperpipes,lowerpipes):
    if playery>GROUNDY-25 or playerx<0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperpipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerpipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False

def getRandomPipe():
    #generate positions of 2 pipes(one bottom  straight and one top rotated pipe) for blitting on the screen
    pipeheight=GAME_SPRITES['pipe'][0].get_height()    
    offset=SCREENHEIGHT/3
    y2=offset+random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()-1.2*offset))
    pipex=SCREENWIDTH+10
    y1=pipeheight-y2+offset
    pipe=[
        {'x':pipex,'y':-y1},#upper pipe
        {'x':pipex,'y':y2}#lower pipe
    ]       
    return pipe

if __name__ == "__main__":
    #main function from where game will start
    pygame.init()#all pygame modules
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird by Karan")
    #game sprites
    GAME_SPRITES['numbers']=(
        pygame.image.load('gamedata/sprites/0.png').convert_alpha(),
        pygame.image.load('gamedata/sprites/1.png').convert_alpha(),
        pygame.image.load('gamedata/sprites/2.png').convert_alpha(),
        pygame.image.load('gamedata/sprites/3.png').convert_alpha(),
        pygame.image.load('gamedata/sprites/4.png').convert_alpha(),
        pygame.image.load('gamedata/sprites/5.png').convert_alpha(),
        pygame.image.load('gamedata/sprites/6.png').convert_alpha(),
        pygame.image.load('gamedata/sprites/7.png').convert_alpha(),
        pygame.image.load('gamedata/sprites/8.png').convert_alpha(),
        pygame.image.load('gamedata/sprites/9.png').convert_alpha(),
    )
    GAME_SPRITES['message']=pygame.image.load('gamedata/sprites/image.jpg').convert_alpha()
    GAME_SPRITES['base']=pygame.image.load('gamedata/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe']=(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha() ,180),
    pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()
    #game sounds
    GAME_SOUNDS['die']=pygame.mixer.Sound('gamedata/audio/die.wav')
    GAME_SOUNDS['hit']=pygame.mixer.Sound('gamedata/audio/hit.wav')
    GAME_SOUNDS['point']=pygame.mixer.Sound('gamedata/audio/point.wav')
    GAME_SOUNDS['swoosh']=pygame.mixer.Sound('gamedata/audio/swoosh.wav')
    GAME_SOUNDS['wing']=pygame.mixer.Sound('gamedata/audio/wing.wav')

    while True:
        welcomescreen()#shows welcome screen to the user untill it presses the button
        mainGame()# main function 