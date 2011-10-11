'''
Created on 10/10/2011

@author: greg
'''

import pygame
from pygame.locals import NOFRAME, KEYDOWN, KEYUP, FULLSCREEN

APP_NAME = 'SpudGun'

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
        
    def intro(self):
        pygame.time.wait(2500)
        self.drawText("SpudGun")
        self.update()
        pygame.time.wait(2500)

    def mainLoop(self):
        lastEventTicks = pygame.time.get_ticks()
        notQuitting = True
        while notQuitting:
            #Poll for events
            for event in pygame.event.get():
                
                if event.type == KEYDOWN or event.type == KEYUP:
                    lastEventTicks = pygame.time.get_ticks()
                    
                if event.type == KEYDOWN:
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
    sg.intro()
    sg.mainLoop()
    
if __name__ == '__main__':
    main()
