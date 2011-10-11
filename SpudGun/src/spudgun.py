'''
Created on 10/10/2011

@author: greg
'''

import pygame
from pygame.locals import NOFRAME, KEYDOWN, KEYUP, FULLSCREEN, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_LCTRL, K_ESCAPE

APP_NAME = 'SpudGun'

class KeyMap:
    keyUp = K_UP
    keyDown = K_DOWN
    keyLeft = K_LEFT
    keyRight = K_RIGHT
    keyExec = K_LCTRL
    keyQuit = K_ESCAPE

    def __init__(self):
        None

    def isQuit(self, event):
        return event.type == KEYDOWN and event.key == self.keyQuit
    
    def setQuit(self, keycode):
        self.keyQuit = keycode
             
    def isKeyUp(self, event):
        return event.type == KEYDOWN and event.key == self.keyUp

    def setKeyUp(self, keycode):
        self.keyUp = keycode

    def isKeyDown(self, event):
        return event.type == KEYDOWN and event.key == self.keyDown

    def setKeyDown(self, keycode):
        self.keyDown = keycode

    def isKeyLeft(self, event):
        return event.type == KEYDOWN and event.key == self.keyLeft

    def setKeyLeft(self, keycode):
        self.keyLeft = keycode

    def isKeyRight(self, event):
        return event.type == KEYDOWN and event.key == self.keyRight
    
    def setKeyRight(self, keycode):
        self.keyRight = keycode
        
class SpudGun:
    
    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        
        modes = pygame.display.list_modes(0, FULLSCREEN)
        screen_sizex = int(modes[0][0])
        screen_sizey = int(modes[0][1]) 
        
        self.screen = pygame.display.set_mode([screen_sizex,screen_sizey], NOFRAME)
        
        pygame.display.set_caption(APP_NAME)
        self.screen_rect = self.screen.get_rect()
        self.update()
        
        pygame.key.set_repeat(500,30) 
        pygame.time.Clock() 

        # Display intro - Movie?
        pygame.time.wait(2500)
        self.drawText("SpudGun")
        self.update()
        
        self.keyMap = KeyMap()

    def mainLoop(self):
        lastEventTicks = pygame.time.get_ticks()
        notQuitting = True
        while notQuitting:
            #Poll for events
            for event in pygame.event.get():
                
                if event.type == KEYDOWN or event.type == KEYUP:
                    lastEventTicks = pygame.time.get_ticks()
                    
                if self.keyMap.isQuit(event):
                    notQuitting = False

    def drawText(self, string):
        font = pygame.font.Font(None, 16)
        text = font.render(string, 1, ([255,255,255]))
        text_rect = text.get_rect()
        self.screen.fill([5,5,5])
        self.screen.blit(text, text_rect)
    
    def update(self):
        pygame.display.flip()

def main():
    sg = SpudGun()
    sg.mainLoop()
    
if __name__ == '__main__':
    main()
