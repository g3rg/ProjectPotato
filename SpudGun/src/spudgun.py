'''
Created on 10/10/2011

@author: greg
'''

import sys

import pygame
from pygame.locals import NOFRAME

class SpudGun:
    
    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode([200,200], NOFRAME)
        pygame.display.set_caption('SpugGun')
        self.screen_rect = self.screen.get_rect()
        self.update()

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
    pygame.time.wait(2500)
    sg.drawText("TEST")
    sg.update()
    pygame.time.wait(2500)
    sys.exit(1)
    
if __name__ == '__main__':
    main()
