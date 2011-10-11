'''
Created on 11/10/2011

@author: greg
'''

from BeautifulSoup import BeautifulSoup

class MameInfo:
    def __init__(self):
        self.buildname = ""
        self.games = {}

    def loadMameInfoFromPath(self, path):
        infoFile = open(path, 'r')
        soup = BeautifulSoup(infoFile.read())
        
        self.buildName = soup.find('mame')['build']
        
        for game in soup.findAll('game'):
            if not self.games.has_key(game['name']):
                gInfo = GameInfo(game)
               
                self.games[gInfo.name] = gInfo
        

class GameInfo:
    def __init__(self, game = None):
        if game == None:
            self.name = ""
            self.cloneof = None
            self.romof = None
            self.sampleof = None
            self.year = 1900
            self.description = ""
            self.roms = {}
            self.samples = []
            self.driverStatus = ""
            self.driverEmulationStatus = ""
            self.driverColorStatus = ""
            self.driverSoundStatus = ""
            self.driverGraphicStatus = ""
        else:
            self.name = game['name']
            self.cloneof = getNoneSafeAttr(game, 'cloneof')
            self.romof = getNoneSafeAttr(game, 'romof')
            self.sampleof = getNoneSafeAttr(game, 'sampleof')
            self.year = getNoneSafeAttr(game, 'year')
            self.description = ""
            self.roms = {}
            self.samples = []
            self.driverStatus = ""
            self.driverEmulationStatus = ""
            self.driverColorStatus = ""
            self.driverSoundStatus = ""
            self.driverGraphicStatus = ""

def getNoneSafeAttr(tag, key, default=None):
    if tag.has_key(key):
        return tag[key]
    else:
        return default

class RomInfo:
    def __init__(self):
        self.name = ""
        self.size = 0
        self.crc = ""
        self.status = None
 
class DiskInfo:
    def __init__(self):
        self.name = ""
        self.md5 = ""
        self.sha1 = ""
        self.status = ""
        self.optional = False
 
 
