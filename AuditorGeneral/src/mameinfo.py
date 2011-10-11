'''
Created on 11/10/2011

@author: greg
'''

from BeautifulSoup import BeautifulSoup

class MameInfo:
    def __init__(self):
        self.build_name = ""
        self.games = {}

    def loadMameInfoFromPath(self, path):
        infoFile = open(path, 'r')
        soup = BeautifulSoup(infoFile.read())
        
        self.build_name = soup.find('mame')['build']
        
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
            self.description = getNoneSafeAttr(game, 'description', "")
            
            self.samples = []
            samples = game.findAll('sample')
            for sample in samples:
                self.samples.append(getNoneSafeAttr(sample, 'name'))

            self.roms = {}
            roms = game.findAll('rom')
            for rom in roms:
                rInfo = RomInfo(rom)
                self.roms[rInfo.name] = rInfo
            
            driver = game.find('driver')

            if driver == None:
                self.driverStatus = ""
                self.driverEmulationStatus = ""
                self.driverColorStatus = ""
                self.driverSoundStatus = ""
                self.driverGraphicStatus = ""
            else:
                self.driverStatus = getNoneSafeAttr(driver, 'status')
                self.driverEmulationStatus = getNoneSafeAttr(driver, 'emulation')
                self.driverColorStatus = getNoneSafeAttr(driver, 'color')
                self.driverSoundStatus = getNoneSafeAttr(driver, 'sound')
                self.driverGraphicStatus = getNoneSafeAttr(driver, 'graphic')


class RomInfo:
    def __init__(self, rom = None):
        if rom == None:
            self.name = ""
            self.size = 0
            self.crc = ""
            self.status = None
        else:
            self.name = getNoneSafeAttr(rom, 'name')
            self.size = getNoneSafeAttr(rom, 'size')
            self.crc = getNoneSafeAttr(rom, 'crc')
            self.status = getNoneSafeAttr(rom, 'status')

class DiskInfo:
    def __init__(self):
        self.name = ""
        self.md5 = ""
        self.sha1 = ""
        self.status = ""
        self.optional = False
 
 
def getNoneSafeAttr(tag, key, default=None):
    if tag.has_key(key):
        return tag[key]
    else:
        return default
