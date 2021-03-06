#APPLE level editor, v.1
#Controls:
#m: Move selected object
#Delete: Delete object

import pygame, sys, os
from pygame import *
pygame.init()

knownMonsters = ['NuiJagaP', 'CCGPunk']
knownBlocks = ['Block', 'WallRunBlock', 'BreakBlock']

def imgLoad(imgFile, mode):
    if mode == 'i':
        folder = 'ItemImgs'
    elif mode == 's':
        folder = 'SceneImgs'
    elif mode == 'n':
        folder = 'NPC_Imgs'
    elif mode == 'ic':
        folder = 'Icons'
    elif mode == 'a':
        folder = 'APPLEimgs'
    elif mode == 'al':
        folder = 'APPLElvls'
    else:
        folder = None
    if folder != None:
        filePath = os.path.join('..', 'Resources', folder, imgFile)
        returnFile = pygame.image.load(filePath)
        return returnFile

def txtLoad(txtFile, mode):
    if mode == 'n':
        folder = 'NPC_Text'
    elif mode == 'c':
        folder = 'Chapters'
    elif mode == 's':
        folder = 'SaveGames'
    elif mode == 'a':
        folder = 'APPLElvls'
    if folder != None:
        filePath = os.path.join('..', 'Resources', folder, txtFile)
        return filePath



class Level:
    def __init__(self, imgSource, txtSource):
        
        self.origin = [0,0]
        self.imgName = imgSource
        self.txtName = txtSource
        self.imgSource = imgLoad(imgSource, 'al')
        self.txtSource = txtLoad(txtSource, 'a')
        self.lvlX = self.imgSource.get_width()*10
        self.lvlY = self.imgSource.get_height()*10
        print(self.lvlX)
        print(self.lvlY)
        self.blocks = []
        self.monsters = []
        self.healths = []
        self.spikes = []
        self.voices = []
        self.start = Start((0,0))
        self.exit = Exit((0,0))
        for x in range(self.imgSource.get_width()):
            for y in range(self.imgSource.get_height()):
                if self.imgSource.get_at((x, y)) == (0,0,0):
                    self.blocks.append(Block('Block', pygame.Rect(x*10, y*10, 10, 10)))
                if self.imgSource.get_at((x, y)) == (0,255,0):
                    self.start = Start((x*10, y*10))#Spawn point is the green pixel
                if self.imgSource.get_at((x, y)) == (0,0,255):#Exit is the blue pixel
                    self.exit = Exit((x*10, y*10))
                if self.imgSource.get_at((x, y)) == (255,0,0):#Red pixels are wall-running surfaces
                    self.blocks.append(Block('WallRunBlock', pygame.Rect(x*10, y*10, 10, 10)))
                if self.imgSource.get_at((x, y)) == (100,0,0):#Dark red pixels are breakable
                    self.blocks.append(Block('BreakBlock', pygame.Rect(x*10, y*10, 10, 10)))

                if self.imgSource.get_at((x, y)) == (25,0,0):#Red: Up-spike
                    self.spikes.append(Spike(8, (x*10, y*10)))
                if self.imgSource.get_at((x, y)) == (0,25,0):#Green: Left-spike
                    self.spikes.append(Spike(6, (x*10, y*10)))
                if self.imgSource.get_at((x, y)) == (0,0,25):#Blue: Down-spike
                    self.spikes.append(Spike(2, (x*10, y*10)))
                if self.imgSource.get_at((x, y)) == (25,25,25):#Grey: Right-spike
                    self.spikes.append(Spike(4, (x*10, y*10)))
                if self.imgSource.get_at((x, y)) == (0,100,0):
                    self.healths.append(Health((x*10, y*10)))
        self.loadTxtFile()
        self.objects = self.blocks + self.monsters + self.spikes + self.healths
        self.objects.append(self.start)
        self.objects.append(self.exit)

    def save(self):
        print('Saving...')
        newImage = pygame.Surface((self.lvlX // 10, self.lvlY // 10))
        newImage.fill((255,255,255))
        newFile = open(txtLoad(self.txtName, 'a'), 'w')
        newFile.close()
        newFile = open(txtLoad(self.txtName, 'a'), 'a')
        for i in self.objects:
            if i.name == 'Player':
                print('Start point')
                newImage.set_at((i.rect.left // 10, i.rect.top // 10), (0,255,0))
            if i.name == 'Exit':
                print('End point')
                newImage.set_at((i.rect.left // 10, i.rect.top // 10), (0,0,255))
            if i.name == 'Block' and i.rect.width == 10 and i.rect.height == 10:
                newImage.set_at((i.rect.left // 10, i.rect.top // 10), (0,0,0))
            if (i.name in knownBlocks) and (i.rect.width > 10 or i.rect.height > 10):
                print('Saving block')
                newFile.write('+block'+'|'+i.name+'|'+str(i.rect.left)+'|'+str(i.rect.top)+'|'+str(i.rect.width)+'|'+str(+i.rect.height)+'\n')
            if i.name == 'WallRunBlock':
                newImage.set_at((i.rect.left // 10, i.rect.top // 10), (255,0,0))
            if i.name == 'BreakBlock':
                newImage.set_at((i.rect.left // 10, i.rect.top // 10), (100,0,0))
            if i.name == 'Spike-8':
                newImage.set_at((i.rect.left // 10, (i.rect.top // 10) + 1), (25,0,0))
            if i.name == 'Spike-4':
                newImage.set_at(((i.rect.left // 10), i.rect.top // 10), (25,25,25))
            if i.name == 'Spike-2':
                newImage.set_at((i.rect.left // 10, i.rect.top // 10), (0,0,25))
            if i.name == 'Spike-6':
                newImage.set_at(((i.rect.left // 10) + 1, i.rect.top // 10), (0,25,0))
            if i.name == 'Health':
                newImage.set_at((i.rect.left // 10, i.rect.top // 10), (0,100,0))
            if i.name in knownMonsters:
                print('Saving monster')
                newFile.write('+monster|'+i.name+'|'+str(i.rect.left)+'|'+str(i.rect.top)+'|'+str(i.direction)+'|'+str(i.mood)+'\n')

        for i in self.voices:
            newFile.write('+voice|'+str(i.rect.left)+'|'+str(i.rect.top)+'|'+str(i.rect.width)+'|'+str(i.rect.height)+'|'+i.string+'|'+str(i.delRect.left)+'|'+str(i.delRect.top)+'|'+str(i.delRect.width)+'|'+str(i.delRect.height)+'\n')
        
            

        filePath = os.path.join('..', 'Resources', 'APPLElvls', self.imgName)
        pygame.image.save(newImage, filePath)
        newFile.close()

    def loadTxtFile(self):
        for line in open(self.txtSource, 'r'):
            line = line.strip()
            cmdList = line.split('|')
            if cmdList[0] == '+block':
                print('Adding block')
                self.blocks.append(Block(cmdList[1], pygame.Rect(int(cmdList[2]), int(cmdList[3]), int(cmdList[4]), int(cmdList[5]))))
            elif cmdList[0] == '+monster':
                print('Adding monster')
                self.monsters.append(Monster(cmdList[1], (int(cmdList[2]), int(cmdList[3])), int(cmdList[4]), int(cmdList[5])))
            elif cmdList[0] == '+voice':
                self.voices.append(Voice(pygame.Rect(int(cmdList[1]), int(cmdList[2]), int(cmdList[3]), int(cmdList[4])), cmdList[5], pygame.Rect(int(cmdList[6]), int(cmdList[7]), int(cmdList[8]), int(cmdList[9]))))

    def getViewSurf(self, coord):
        viewRect = pygame.Rect(0,0,600,400)
        if (self.lvlX < coord[0] + 600):
            viewRect.left = self.lvlX - 600
        elif not (self.lvlX < coord[0] + 600):
            viewRect.left = coord[0]

        if (self.lvlY < coord[1] + 400):
            viewRect.top = self.lvlY - 400
        elif not (self.lvlY < coord[1] + 400):
            viewRect.top = coord[1]

        viewSurf = self.lvlSurf.subsurface(viewRect)
        return viewSurf
        
    def moveOrigin(self, deltaX, deltaY):
        #self.origin determines what part of the level you're looking at
        if (self.origin[0] + deltaX + 600 < self.lvlX) and (self.origin[0] + deltaX > 0):
            self.origin[0] += deltaX
        if (self.origin[1] + deltaY + 400 < self.lvlY) and (self.origin[1] + deltaY > 0):
            self.origin[1] += deltaY

    def edit(self):
        lastMousePos = pygame.mouse.get_pos()
        mousePos = pygame.mouse.get_pos()
        deltaX = 0
        deltaY = 0
        objects = ['Block("Block", pygame.Rect(roundToTen(self.origin[0]+mousePos[0]),roundToTen(self.origin[1]+mousePos[1]),10,10))',
                   'Voice(pygame.Rect(roundToTen(self.origin[0]+mousePos[0]),roundToTen(self.origin[1]+mousePos[1]),10,10), "", pygame.Rect(roundToTen(self.origin[0]+mousePos[0]+10),roundToTen(self.origin[1]+mousePos[1]+10),10,10))',
                   'Health((roundToTen(self.origin[0]+mousePos[0]), roundToTen(self.origin[1]+mousePos[1])))',
                   'Spike(8, (roundToTen(self.origin[0]+mousePos[0]), roundToTen(self.origin[1]+mousePos[1])))',
                   'Spike(6, (roundToTen(self.origin[0]+mousePos[0]), roundToTen(self.origin[1]+mousePos[1])))',
                   'Spike(4, (roundToTen(self.origin[0]+mousePos[0]), roundToTen(self.origin[1]+mousePos[1])))',
                   'Spike(2, (roundToTen(self.origin[0]+mousePos[0]), roundToTen(self.origin[1]+mousePos[1])))']
        tools = ['select', 'add', 'delete']
        usedTool = 0
        usedObject = 1
        delPress =False
        mPress = False
        selected = None
        leftClicked = False
        releaseLeftClick = True
        rightClicked = False
        releaseRightClick = True
        while True:
            ePress = False
            sPress = False
            delPress = False
            mPress = False
            upPress = False
            downPress = False
            leftPress = False
            rightPress = False
            enterPress = False #Why are you still here?
            mousePos = pygame.mouse.get_pos()
            deltaX = mousePos[0] - lastMousePos[0]
            deltaY = mousePos[1] - lastMousePos[1]
            
            self.lvlSurf = pygame.Surface((self.lvlX, self.lvlY))
            self.lvlSurf.fill((102, 51, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.save()
                    DTQuit()
                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        leftClicked = False
                        releaseLeftClick = True
                    if event.button == 3:
                        rightClicked = False
                        releaseRightClick = True
                    if event.button == 4:
                        upPress = True
                    if event.button == 5:
                        downPress = True
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        leftClicked = True
                    if event.button == 3:
                        rightClicked = True
                if event.type == KEYUP:
                    if event.key == ord('s'):
                        sPress = True
                    if event.key == ord('m'):
                        mPress = True
                    if event.key == ord('e'):
                        ePress = True
                    if event.key == K_UP:
                        upPress = True
                    if event.key == K_DOWN:
                        downPress = True
                    if event.key == K_LEFT:
                        leftPress = True
                    if event.key == K_RIGHT:
                        rightPress = True
                    if event.key == K_DELETE:
                        delPress = True
                        

            for i in self.objects:
                self.lvlSurf.blit(i.sprite, i.rect)
            for v in self.voices:
                self.lvlSurf.blit(v.mainSprite, v.rect)
                self.lvlSurf.blit(v.delSprite, v.delRect)

            
            if rightClicked:
                self.moveOrigin(deltaX, deltaY)
            if leftClicked and releaseLeftClick:
                
                for i in self.objects:
                    dectRect = pygame.Rect(i.rect.left - self.origin[0], i.rect.top - self.origin[1], i.rect.width, i.rect.height)
                    if dectRect.collidepoint(mousePos):
                        if tools[usedTool] == 'select':
                            selected = i
                            releaseLeftClick = False
                        elif tools[usedTool] == 'delete':
                            self.objects.remove(i)
                for i in self.voices:
                    dectRect = pygame.Rect(i.rect.left - self.origin[0], i.rect.top - self.origin[1], i.rect.width, i.rect.height)
                    dectRect2 = pygame.Rect(i.delRect.left - self.origin[0], i.delRect.top - self.origin[1], i.delRect.width, i.delRect.height)
                    if dectRect.collidepoint(mousePos) or dectRect2.collidepoint(mousePos):
                        if tools[usedTool] == 'select':
                            selected = i
                            releaseLeftClick = False
                        elif tools[usedTool] == 'delete':
                            self.voices.remove(i)

                

                if tools[usedTool] == 'add':
                    releaseLeftClick = False
                    if objects[usedObject].startswith('Voice'):
                        self.voices.append(eval(objects[usedObject]))
                    else:
                        self.objects.append(eval(objects[usedObject]))

            window.blit(self.getViewSurf(self.origin), (0,0))
            if selected != None:
                window.blit(txt.render(selected.name + str(selected.rect), True, (255,255,255)), (0,0))
                pygame.draw.rect(window, (0,255,0), pygame.Rect(selected.rect.left - self.origin[0], selected.rect.top - self.origin[1], selected.rect.width, selected.rect.height), 1)
                if mPress:
                    selected.move()
                if sPress:
                    selected.stretch()
                if ePress:
                    selected.edit()
                if delPress:
                    if selected in self.objects:
                        self.objects.remove(selected)
                    elif selected in self.voices:
                        self.voices.remove(selected)
                    selected = None
            
            else:
                window.blit(txt.render('Nothing selected', True, (255,255,255)), (0,0))
            if leftPress:
                if usedObject > 0:
                    usedObject -= 1
                else:
                    usedObject = len(objects)-1
            if rightPress:
                if usedObject < len(objects)-1:
                    usedObject += 1
                else:
                    usedObject = 0
                
            if downPress:
                if usedTool > 0:
                    usedTool -= 1
                else:
                    usedTool = len(tools)-1
            if upPress:
                if usedTool < len(tools)-1:
                    usedTool += 1
                else:
                    usedTool = 0
            window.blit(txt.render(str((self.origin[0] + mousePos[0], self.origin[1] + mousePos[1])), True, (255,255,255)), (0, 20))
            window.blit(txt.render(tools[usedTool], True, (255,255,255)), (0, 40))
            window.blit(txt.render(objects[usedObject], True, (255,255,255)), (0, 60))
            lastMousePos = mousePos
            
            pygame.display.update()

class Block:
    def __init__(self, kind, rect):
        self.name = kind
        self.rect = rect
        if self.name == 'Block':
            self.sprite = imgLoad('BlockSprite.bmp', 'a')
        elif self.name == 'WallRunBlock':
            self.sprite = imgLoad('WallRunBlock.bmp', 'a')
        elif self.name == 'BreakBlock':
            self.sprite = imgLoad('HitBlock.bmp', 'a')
        else:
            self.sprite = pygame.Surface(10,10)
            self.sprite.fill((255,255,255))
        self.sprite = pygame.transform.scale(self.sprite, (self.rect.width, self.rect.height))
            
    def stretch(self):
        print('\nStretch how far in the X direction?')
        deltaX = input()
        if deltaX == '':
            deltaX = 0
        deltaX = int(deltaX)
        print('Stretch how far in the Y direction?')
        deltaY = input()
        if deltaY == '':
            deltaY = 0
        deltaY = int(deltaY)
        self.rect.width += deltaX
        self.rect.height += deltaY

        self.sprite = pygame.transform.scale(self.sprite, (self.rect.width, self.rect.height))

    def move(self):
        print('\nCoords will be rounded to 10.')
        newX = input('Move X how far?')
        newY = input('Move Y how far?')
        if newX != '':
            newX = roundToTen(newX)
            self.rect.left += newX
        if newY != '':
            newY = roundToTen(newY)
            self.rect.top += newY

    def edit(self):
        print('\n 1) Block')
        print(' 2) WallRunBlock')
        print(' 3) BreakBlock')
        newType = input('New block type:')
        if newType == '1':
            self.sprite = imgLoad('BlockSprite.bmp', 'a')
            self.name = 'Block'
        elif newType == '2':
            self.name = 'WallRunBlock'
            self.sprite = imgLoad('WallRunBlock.bmp', 'a')
        elif newType == '3':
            self.sprite = imgLoad('HitBlock.bmp', 'a')
            self.name = 'BreakBlock'
            
        self.sprite = pygame.transform.scale(self.sprite, (self.rect.width, self.rect.height))


class Health:
    def __init__(self, coord):
        self.name = 'Health'
        self.rect = pygame.Rect(coord[0], coord[1], 10, 10)
        self.sprite = imgLoad('Health.bmp', 'a')
        self.sprite.set_colorkey((0,255,0))

    def move(self):
        print('\nCoords will be rounded to 10.')
        newX = input('Move X how far?')
        newY = input('Move Y how far?')
        if newX != '':
            newX = roundToTen(newX)
            self.rect.left += newX
        if newY != '':
            newY = roundToTen(newY)
            self.rect.top += newY

    def stretch(self):
        print('Not stretchable')

    def edit(self):
        print('No special edits')

class Voice:
    def __init__(self, rect, string, delRect):
        '''Text that shows up in an APPLE level when the player walks in the corresponding Rect()'''
        self.name = 'Voice'
        self.string = string
        self.rect = rect
        self.delRect = delRect #delRect is where the voice is deleted.
        self.mainSprite = pygame.Surface((self.rect.width, self.rect.height))
        self.mainSprite.fill((0,255,0))
        self.mainSprite.set_alpha(150)
        self.delSprite = pygame.Surface((self.delRect.width, self.delRect.height))
        self.delSprite.fill((255,0,0))
        self.delSprite.set_alpha(150)

    def move(self):
        print('\nCoords will be rounded to 10.')
        newX = input("Push main rect how far on the X-axis?")
        newY = input("Push main rect how far on the Y-axis?")
        if newX != '':
            newX = roundToTen(newX)
            self.rect.left += newX
        if newY != '':
            newY = roundToTen(newY)
            self.rect.top += newY
        newX = input("\nPush delRect how far on the X-axis?")
        newY = input("Push delRect how far on the Y-axis?")
        if newX != '':
            newX = roundToTen(newX)
            self.delRect.left += newX
        if newY != '':
            newY = roundToTen(newY)
            self.delRect.top += newY

    def stretch(self):
        
        print('\nStretch main rect how far in the X direction?')
        deltaX = input()
        if deltaX == '':
            deltaX = 0
        deltaX = int(deltaX)
        print('Stretch main rect how far in the Y direction?')
        deltaY = input()
        if deltaY == '':
            deltaY = 0
        deltaY = int(deltaY)
        self.rect.width += deltaX
        self.rect.height += deltaY

        print('\nStretch delRect how far in the X direction?')
        deltaX = input()
        if deltaX == '':
            deltaX = 0
        deltaX = int(deltaX)
        print('Stretch delRect how far in the Y direction?')
        deltaY = input()
        if deltaY == '':
            deltaY = 0
        deltaY = int(deltaY)
        self.delRect.width += deltaX
        self.delRect.height += deltaY        

        self.mainSprite = pygame.transform.scale(self.mainSprite, (self.rect.width, self.rect.height))
        self.delSprite = pygame.transform.scale(self.delSprite, (self.delRect.width, self.delRect.height))

    def edit(self):
        print('\nOld string:' + self.string)
        print('Input new string:')
        newString = input()
        if newString != '':
            self.string = newString

class Spike:
    #Don't step on the pointy bits
    #Finished for now...
    def __init__(self, side, position):
        self.name = 'Spike'
        self.sprite = imgLoad('Spike.bmp', 'a').convert()
        self.sprite.set_colorkey((0,255,0))
        if side == 6:
            self.name += '-6'
            self.sprite = pygame.transform.flip(self.sprite, True, False)
            self.rect = pygame.Rect(position[0]-10, position[1], 20, 10)
        elif side == 4:
            self.name += '-4'
            self.rect = pygame.Rect(position[0], position[1], 20, 10)
        elif side == 2:
            self.name += '-2'
            self.sprite = pygame.transform.rotate(self.sprite, 90)
            self.rect = pygame.Rect(position[0], position[1], 10, 20)
        elif side == 8:
            self.name += '-8'
            self.sprite = pygame.transform.rotate(self.sprite, 270)
            self.rect = pygame.Rect(position[0], position[1]-10, 10, 20)

    def move(self):
        print('\nCoords will be rounded to 10.')
        newX = input('Push horizontally:')
        newY = input('Push vertically:')
        if newX != '':
            newX = roundToTen(newX)
            self.rect.left += newX
        if newY != '':
            newY = roundToTen(newY)
            self.rect.top += newY

    def stretch(self):
        print('Not stretchable')

    def edit(self):
        newSide = input('\nSwitch side to:')
        self.sprite = imgLoad('Spike.bmp', 'a').convert()
        if newSide == '6':
            self.name = 'Spike-6'
            self.sprite = pygame.transform.flip(self.sprite, True, False)
            self.rect = pygame.Rect(self.rect.left-10, self.rect.top, 20, 10)
        elif newSide == '4':
            self.name = 'Spike-4'
            self.rect = pygame.Rect(self.rect.left, self.rect.top, 20, 10)
        elif newSide == '2':
            self.name = 'Spike-2'
            self.sprite = pygame.transform.rotate(self.sprite, 90)
            self.rect = pygame.Rect(self.rect.left, self.rect.top, 10, 20)
        elif newSide == '8':
            self.name = 'Spike-8'
            self.sprite = pygame.transform.rotate(self.sprite, 270)
            self.rect = pygame.Rect(self.rect.left, self.rect.top-10, 10, 20)

        
class Monster:
    def __init__(self, name, coord, direction, mood):
        self.name = name
        self.direction = direction
        self.mood = mood
        self.sprite = imgLoad(name+'.bmp', 'a')
        self.sprite.set_colorkey(self.sprite.get_at((0,0)))
        self.rect = pygame.Rect(coord[0], coord[1], self.sprite.get_width(), self.sprite.get_height())

    def move(self):
        print('\nCoords will be rounded to 10.')
        newX = input('New X coord:')
        newY = input('New Y coord:')
        if newX != '':
            newX = roundToTen(newX)
            self.rect.left = newX
        if newY != '':
            newY = roundToTen(newY)
            self.rect.top = newY
            
    def stretch(self):
        print('Not stretchable')

    def edit(self):
        print('\nChange mood?  0 = calm, 1 = angry.  Currently ' + str(self.mood))
        moodSwap = input('Y/N:').lower()
        print('Change direction?  0 = left, 1 = right.  Currently ' + str(self.direction))
        dirSwap = input('Y/N:').lower()
        if moodSwap.startswith('y'):
            print('Changing mood')
            if self.mood == 0:
                self.mood = 1
            elif self.mood == 1:
                self.mood = 0
        if dirSwap.startswith('y'):
            print('Changing direction')
            if self.direction == 0:
                self.direction = 1
            elif self.direction == 1:
                self.direction = 0
    
class Start:
    def __init__(self, coord):
        self.name = 'Player'
        self.rect = pygame.Rect(coord[0], coord[1], 20, 40)
        self.sprite = imgLoad('HuxStand.bmp', 'a')

    def move(self):
        print('\nCoords will be rounded to 10.')
        newX = input('New X coord:')
        newY = input('New Y coord:')
        if newX != '':
            newX = roundToTen(newX)
            self.rect.left = newX
        if newY != '':
            newY = roundToTen(newY)
            self.rect.top = newY
            
    def stretch(self):
        print('Not stretchable')

    def edit(self):
        pass
        
class Exit:
    def __init__(self, coord):
        self.name = 'Exit'
        self.rect = pygame.Rect(coord[0], coord[1], 20, 20)
        self.sprite = imgLoad('ExitBlock.bmp', 'a')

    def move(self):
        print('\nCoords will be rounded to 10.')
        newX = input('New X coord:')
        newY = input('New Y coord:')
        if newX != '':
            newX = roundToTen(newX)
            self.rect.left = newX
        if newY != '':
            newY = roundToTen(newY)
            self.rect.top = newY

    def stretch(self):
        print('Not stretchable')

    def edit(self):
        pass

def DTQuit():
    pygame.quit()
    sys.exit()

def roundToTen(num):
    newNum = int(str(num)[0:-1] + '0')
    return newNum



print(".bmp file name")
bmpFile = 'Level6.bmp'
print(".txt file name")
txtFile = 'Level6.txt'
print('Loading...')

WX = 600
WY = 400
window = pygame.display.set_mode((WX, WY), 0, 32)
txt = pygame.font.Font('cour.ttf', 15)
txt.set_bold(True)

level = Level(bmpFile, txtFile)
level.edit()
