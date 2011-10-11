'''
Created on 10/10/2011

@author: greg
'''

import os
import ConfigParser

import pygame
from pygame.locals import NOFRAME, KEYDOWN, KEYUP, FULLSCREEN, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_LCTRL, K_ESCAPE

APP_NAME = 'SpudGun'

class KeyMap:
    def isExec(self, event):
        return event.type == KEYDOWN and event.key == self.keyExec
    
    def setExec(self, keycode):
        self.keyExec = int(keycode)
    
    def isQuit(self, event):
        return event.type == KEYDOWN and event.key == self.keyQuit
    
    def setQuit(self, keycode):
        self.keyQuit = int(keycode)
             
    def isKeyUp(self, event):
        return event.type == KEYDOWN and event.key == self.keyUp

    def setKeyUp(self, keycode):
        self.keyUp = int(keycode)

    def isKeyDown(self, event):
        return event.type == KEYDOWN and event.key == self.keyDown

    def setKeyDown(self, keycode):
        self.keyDown = int(keycode)

    def isKeyLeft(self, event):
        return event.type == KEYDOWN and event.key == self.keyLeft

    def setKeyLeft(self, keycode):
        self.keyLeft = int(keycode)

    def isKeyRight(self, event):
        return event.type == KEYDOWN and event.key == self.keyRight
    
    def setKeyRight(self, keycode):
        self.keyRight = int(keycode)

class ConfigManager:
    
    def __init__(self, configFile):
        
        self._config = ConfigParser.ConfigParser()
        #config.optionxform = lambda x: x
     
        if os.path.isfile(configFile):
            self._config.read(configFile)

    def save(self, path):
        self._config.write(open(path, "w"))

    def get(self, key, section="APPLICATION", default=""):
        value = None
        if self._config.has_section(section):
            if self._config.has_option(section, key):
                value = self._config.get(section, key)
        
        if value == None:
            value = default
            if not self._config.has_section(section):
                self._config.add_section(section)
            
            self._config.set(section, key, default)
        
        return value

class SpudGun:
    
    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        
        # TODO Read location from cmdline parameter
        self._configFile = "." + os.sep + "spud.conf"
        
        self._config = ConfigManager(self._configFile)
        
        modes = pygame.display.list_modes(0, FULLSCREEN)
        screen_sizex = int(modes[0][0])
        screen_sizey = int(modes[0][1]) 
        
        self.screen = pygame.display.set_mode([screen_sizex,screen_sizey], NOFRAME)
        
        pygame.display.set_caption(APP_NAME)
        self.screen_rect = self.screen.get_rect()
        self.update()
        
        pygame.key.set_repeat(500,30) 
        pygame.time.Clock() 

        # TODO Display intro - Movie?
        pygame.time.wait(2500)
        self.drawText("SpudGun")
        self.update()
        
        self.keyMap = self.configKeyMap()

    def configKeyMap(self):
        km = KeyMap()
        
        km.setKeyUp(self._config.get("KEY_UP", "KEYMAPPING", K_UP))
        km.setKeyDown(self._config.get("KEY_DOWN", "KEYMAPPING", K_DOWN))
        km.setKeyLeft(self._config.get("KEY_LEFT", "KEYMAPPING", K_LEFT))
        km.setKeyRight(self._config.get("KEY_RIGHT", "KEYMAPPING", K_RIGHT))
        km.setExec(self._config.get("KEY_EXEC", "KEYMAPPING", K_LCTRL))
        km.setQuit(self._config.get("KEY_QUIT", "KEYMAPPING", K_ESCAPE))
        
        return km

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

    def saveConfig(self):
        self._config.save(self._configFile)

def main():
    sg = SpudGun()
    sg.mainLoop()
    sg.saveConfig()
    
if __name__ == '__main__':
    main()
