import pygame, sys, time, random
from pygame.locals import *
import pyganim, dMapModule

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up the colors
BLACK = (0, 0, 0)
RED = (20, 180, 0)
WHITE = (255, 255, 255)

# set up the window
SPRITEWIDTH = 24
SPRITEHEIGHT = 32
SPRITEDELAY = 0.1
NBSPRITX = 300
NBSPRITY = 200
NBSPRITX_DISP = 30
NBSPRITY_DISP = 20

NB_MONSTER_MAX = 35

gameSurface = pygame.display.set_mode((NBSPRITX_DISP*SPRITEWIDTH, NBSPRITY_DISP*SPRITEHEIGHT), 0, 32)
pygame.display.set_caption('Sprites and Sound')
entireWindowSurface = pygame.Surface((NBSPRITX*SPRITEWIDTH, NBSPRITY*SPRITEHEIGHT))

spriteImage = pygame.image.load('resources/images/player.png')
spriteImage_monstre = pygame.image.load('resources/images/monster.png')

animObj_UP = pyganim.PygAnimation([(spriteImage.subsurface(pygame.Rect(0,0,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage.subsurface(pygame.Rect(SPRITEWIDTH,0,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage.subsurface(pygame.Rect(SPRITEWIDTH*2,0,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY)])
animObj_RIGHT = pyganim.PygAnimation([(spriteImage.subsurface(pygame.Rect(0,SPRITEHEIGHT,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage.subsurface(pygame.Rect(SPRITEWIDTH,SPRITEHEIGHT,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage.subsurface(pygame.Rect(SPRITEWIDTH*2,SPRITEHEIGHT,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY)])
animObj_DOWN = pyganim.PygAnimation([(spriteImage.subsurface(pygame.Rect(0,SPRITEHEIGHT*2,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage.subsurface(pygame.Rect(SPRITEWIDTH,SPRITEHEIGHT*2,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage.subsurface(pygame.Rect(SPRITEWIDTH*2,SPRITEHEIGHT*2,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY)])
animObj_LEFT = pyganim.PygAnimation([(spriteImage.subsurface(pygame.Rect(0,SPRITEHEIGHT*3,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage.subsurface(pygame.Rect(SPRITEWIDTH,SPRITEHEIGHT*3,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage.subsurface(pygame.Rect(SPRITEWIDTH*2,SPRITEHEIGHT*3,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY)])
playerRect = Rect(0,0,SPRITEWIDTH-2,SPRITEHEIGHT-2)
treasure = Rect(0,0,SPRITEWIDTH-2,SPRITEHEIGHT-2)

animObj_m_UP = pyganim.PygAnimation([(spriteImage_monstre.subsurface(pygame.Rect(0,0,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage_monstre.subsurface(pygame.Rect(SPRITEWIDTH,0,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage_monstre.subsurface(pygame.Rect(SPRITEWIDTH*2,0,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY)])
animObj_m_RIGHT = pyganim.PygAnimation([(spriteImage_monstre.subsurface(pygame.Rect(0,SPRITEHEIGHT,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage_monstre.subsurface(pygame.Rect(SPRITEWIDTH,SPRITEHEIGHT,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage_monstre.subsurface(pygame.Rect(SPRITEWIDTH*2,SPRITEHEIGHT,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY)])
animObj_m_DOWN = pyganim.PygAnimation([(spriteImage_monstre.subsurface(pygame.Rect(0,SPRITEHEIGHT*2,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage_monstre.subsurface(pygame.Rect(SPRITEWIDTH,SPRITEHEIGHT*2,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage_monstre.subsurface(pygame.Rect(SPRITEWIDTH*2,SPRITEHEIGHT*2,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY)])
animObj_m_LEFT = pyganim.PygAnimation([(spriteImage_monstre.subsurface(pygame.Rect(0,SPRITEHEIGHT*3,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage_monstre.subsurface(pygame.Rect(SPRITEWIDTH,SPRITEHEIGHT*3,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY),
                           (spriteImage_monstre.subsurface(pygame.Rect(SPRITEWIDTH*2,SPRITEHEIGHT*3,SPRITEWIDTH,SPRITEHEIGHT)), SPRITEDELAY)])

conductor_player = pyganim.PygConductor([animObj_UP, animObj_RIGHT, animObj_DOWN, animObj_LEFT])
conductor_player.play() # starts all three animations at the same time.

monsters = []
for i in range(NB_MONSTER_MAX):

    thespritemonster_up = animObj_m_UP.getCopy()
    thespritemonster_down = animObj_m_DOWN.getCopy()
    thespritemonster_right = animObj_m_RIGHT.getCopy()
    thespritemonster_left = animObj_m_LEFT.getCopy()
    thespritemonster_up.play()
    thespritemonster_right.play()
    thespritemonster_left.play()
    thespritemonster_down.play()

    a_monster = ({'rect':pygame.Rect(0,0,SPRITEWIDTH-2,SPRITEHEIGHT-2),
                  'sprite_up':thespritemonster_up,
                  'sprite_down':thespritemonster_down,
                  'sprite_right':thespritemonster_right,
                  'sprite_left':thespritemonster_left,
                  'speedx':random.randint(-3,3),
                  'speedy':random.randint(-3,3)})
    monsters.append(a_monster)

#CONSTRUCTION DU TERRAIN

tiles = []
possibleBeginPlace=[]
somename= dMapModule.dMap()
somename.makeMap(NBSPRITX,NBSPRITY,30,0,80)
for y in range(NBSPRITY):
        for x in range(NBSPRITX):
                if somename.mapArr[y][x]==0:
                        possibleBeginPlace.append((x,y))
#                if somename.mapArr[y][x]==1:
#                        line += " "
                if somename.mapArr[y][x]==2:
                        tiles.append(Rect(x*SPRITEWIDTH, y*SPRITEHEIGHT, SPRITEWIDTH-1, SPRITEHEIGHT-1))
#                if somename.mapArr[y][x]==3 or somename.mapArr[y][x]==4 or somename.mapArr[y][x]==5:



#print(somename)
random.shuffle(possibleBeginPlace)

playerRect.left = possibleBeginPlace[0][0]*SPRITEWIDTH
playerRect.top = possibleBeginPlace[0][1]*SPRITEHEIGHT
treasure.left = possibleBeginPlace[1][0]*SPRITEWIDTH
treasure.top = possibleBeginPlace[1][1]*SPRITEHEIGHT

nbmonster = NB_MONSTER_MAX
#for monster in monsters[:]:
#        if monster['rect'].collidelist(tiles) != -1:
#            monsters.remove(monster)
#            nbmonster -= 1

listIndex = 2
for monster in monsters:
    monster['rect'].left = possibleBeginPlace[listIndex][0]*SPRITEWIDTH
    monster['rect'].top = possibleBeginPlace[listIndex][1]*SPRITEHEIGHT
    listIndex += 1


anim = animObj_RIGHT
kill = 0
shoots = []
moveUp = moveDown = moveRight = moveLeft = False
shootLaunch = False

# run the game loop
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                moveUp = True
                moveDown = False
            if event.key == K_DOWN:
                moveUp = False
                moveDown = True
            if event.key == K_LEFT:
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT:
                moveRight = True
                moveLeft = False
            if event.key == K_SPACE:
                shootLaunch = True
        if event.type == KEYUP:
            if event.key == K_UP:
                moveUp = False
            if event.key == K_DOWN:
                moveDown = False
            if event.key == K_LEFT:
                moveLeft = False
            if event.key == K_RIGHT:
                moveRight = False
            if shootLaunch and event.key == K_SPACE:
                shootLaunch = False
                speedx = 0
                speedy = 0
                if anim == animObj_UP:
                    speedy -= random.randint(2,5)
                if anim == animObj_DOWN:
                    speedy += random.randint(2,5)
                if anim == animObj_LEFT:
                    speedx -= random.randint(2,5)
                if anim == animObj_RIGHT:
                    speedx += random.randint(2,5)
                shoots.append({'posx':playerRect.centerx, 'posy':playerRect.centery, 'speedx': speedx, 'speedy': speedy, 'radius': random.randint(2,5)})
    if moveDown:
        playerRect.top += 3
        if playerRect.collidelist(tiles) != -1:
            playerRect.top -= 3
        anim = animObj_DOWN
    if moveUp:
        playerRect.top -= 3
        if playerRect.collidelist(tiles) != -1:
            playerRect.top += 3
        anim = animObj_UP
    if moveLeft:
        playerRect.left -= 3
        if playerRect.collidelist(tiles) != -1:
            playerRect.left += 3
        anim = animObj_LEFT
    if moveRight:
        playerRect.left += 3
        if playerRect.collidelist(tiles) != -1:
            playerRect.left -= 3
        anim = animObj_RIGHT

    # TEST COLLISION monster/player
    for monster in monsters[:]:
        if monster['rect'].colliderect(playerRect):
            monsters.remove(monster)
            kill += 1
            pygame.display.set_caption('Sprites and Sound - Kill:' +str(kill) +' remain: '+str(nbmonster-kill))
    # draw the black background onto the (playable) surface
    playableleft = playabletop = playableright = playablebottom = 0
    playableleft = max(playerRect.left - (NBSPRITX_DISP*SPRITEWIDTH)/2,0)
    playabletop = max(playerRect.top - (NBSPRITY_DISP*SPRITEHEIGHT)/2,0)
    if playerRect.top + (NBSPRITY_DISP*SPRITEHEIGHT)/2 > NBSPRITY*SPRITEHEIGHT:
        playabletop = NBSPRITY*SPRITEHEIGHT - NBSPRITY_DISP*SPRITEHEIGHT
    if playerRect.left + (NBSPRITX_DISP*SPRITEWIDTH)/2 > NBSPRITX*SPRITEWIDTH:
        playableleft = NBSPRITX*SPRITEWIDTH - NBSPRITX_DISP*SPRITEWIDTH
    playableRect = pygame.Rect(playableleft,playabletop,NBSPRITX_DISP*SPRITEWIDTH,NBSPRITY_DISP*SPRITEHEIGHT)
    playableSurface = entireWindowSurface.subsurface(playableRect)
    playableSurface.fill(BLACK)

    #player anim
    anim.blit(entireWindowSurface, playerRect)


    # MONSTER ANIM
    for monster in monsters:
        if monster['rect'].collidelist(tiles) != -1:
            monster['speedx'] *= -1
            monster['speedy'] *= -1
            monster['rect'].left += monster['speedx']
            monster['rect'].top += monster['speedy']
        else:
            recttest = monster['rect'].inflate(5,5)

            speedx = min(max(-4,monster['speedx'] + random.randint(-1,1)), 4)
            speedy = min(max(-4,monster['speedy'] + random.randint(-1,1)), 4)
            recttest.left += speedx
            recttest.top += speedy
            if recttest.collidelist(tiles) == -1:
                monster['rect'] = recttest.inflate(-5,-5)
                monster['speedx'] = speedx
                monster['speedy'] = speedy
            else:
                monster['rect'].left += monster['speedx']
                monster['rect'].top += monster['speedy']

        if monster['rect'].colliderect(playableRect):
            # affichage
            if monster['speedx'] > monster['speedy']:
                if monster['speedx']>0:
                    monster['sprite_right'].blit(entireWindowSurface, monster['rect'])
                else:
                    monster['sprite_left'].blit(entireWindowSurface, monster['rect'])
            else:
                if monster['speedy']>0:
                    monster['sprite_down'].blit(entireWindowSurface, monster['rect'])
                else:
                    monster['sprite_up'].blit(entireWindowSurface, monster['rect'])

    #shoot anim
    for shoot in shoots[:]:
        shootRec = pygame.Rect(shoot['posx']+shoot['speedx'], shoot['posy']+shoot['speedy'], shoot['radius'], shoot['radius'])
        goOn = True
        for monster in monsters[:]:
            if monster['rect'].colliderect(shootRec):
                monsters.remove(monster)
                shoots.remove(shoot)
                goOn = False
                kill += 1
                pygame.display.set_caption('Sprites and Sound - Kill:' +str(kill) +' remain: '+str(nbmonster-kill))
        if goOn:
            for wall in tiles:
                if wall.colliderect(shootRec):
                    shoots.remove(shoot)
                    goOn = False
        if goOn:
            shoot['posx'] = shoot['speedx'] + shoot['posx']
            shoot['posy'] = shoot['speedy'] + shoot['posy']
            if shootRec.colliderect(playableRect):
                pygame.draw.circle(entireWindowSurface, WHITE, (shoot['posx'], shoot['posy']), shoot['radius'])


    # PAINT WALL
    for wall in tiles:
        if wall.colliderect(playableRect):
            entireWindowSurface.fill(WHITE, wall)

    if treasure.colliderect(playableRect):
        entireWindowSurface.fill(RED, treasure)

    #SET THE GAME
    gameSurface.blit(playableSurface, pygame.Rect(0,0,NBSPRITX_DISP*SPRITEWIDTH, NBSPRITY_DISP*SPRITEHEIGHT))
    if kill == nbmonster or treasure.colliderect(playerRect):
        pygame.quit()
        sys.exit()


    pygame.display.update()
    mainClock.tick(40)
