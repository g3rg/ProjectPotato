'''
Created on 08/10/2011

@author: Perry
'''

import os
import zipfile

from BeautifulSoup import BeautifulSoup

# TODO Switch to config files / cmdline params
#MAME_XML_INFO_PATH="..\\test\\small_mameinfo.xml"
MAME_XML_INFO_PATH="c:\\temp\\mame\\tools\\fullinfo.xml"
MAME_ROM_DIR_PATH="c:\\temp\\mame\\roms"
VERBOSE = True

def formatMissingRomInfo(rom):
    # Add up all rom.sizes to indicate exploded zip size...
    # output name + rom name + parent info?
    
    print "Nicely Formatted!"
    

def getRomZipFileInfo(game):
    roms = {}
    fileList = []
    fileList.append(MAME_ROM_DIR_PATH + os.sep + game['name'] + '.zip')
    
    if game.has_key('cloneof') and os.path.isfile(MAME_ROM_DIR_PATH + os.sep + game['cloneof'] + ".zip"):
        fileList.append(MAME_ROM_DIR_PATH + os.sep + game['cloneof'] + '.zip')
        
    if game.has_key('romof') and os.path.isfile(MAME_ROM_DIR_PATH + os.sep + game['romof'] + ".zip"):
        fileList.append(MAME_ROM_DIR_PATH + os.sep + game['romof'] + '.zip')
    
    #TODO Check if order of this guaranteed? need to make sure child is processed first
    for file in fileList:   
        zip = zipfile.ZipFile(file, "r")
        infoList = zip.infolist()
        for info in infoList:
            if not roms.has_key(info.filename):
                roms[info.filename] = info
    
    return roms

def missingFromParent(game, rom, soup):
    #TODO make sure its the same ROM, i.e. same name + same CRC!
    missingRomBelongsToParent = False
    
    if game.has_key('cloneof'):
        cloneof = soup.find('game', { 'name' : game['cloneof'] })
        if cloneof != None:
            missingRomBelongsToParent = cloneof.find('rom', { 'name' : rom['name']}) != None
        
    if not missingRomBelongsToParent:
        if game.has_key('romof'):
            romof = soup.find('game', { 'name' : game['romof'] })
            if romof != None:
                missingRomBelongsToParent = romof.find('rom', {'name' : rom['name']}) != None
        
    return missingRomBelongsToParent

def doMain():
    print "Analysing!"
    
    if os.path.isfile(MAME_XML_INFO_PATH) and os.path.isdir(MAME_ROM_DIR_PATH):
        infoFile = open(MAME_XML_INFO_PATH, "r")
        soup = BeautifulSoup(infoFile.read())
        games = soup.findAll("game")
        missingZipCount = 0
        for game in games:
            filePath = MAME_ROM_DIR_PATH + os.sep + game['name'] + ".zip"
            dirPath = MAME_ROM_DIR_PATH + os.sep + game['name']
            missing = False
            if os.path.isfile(filePath):
                foundRoms = getRomZipFileInfo(game)
                roms = game.findAll('rom')
                for rom in roms:
                    if rom['name'] in foundRoms:
                        # TODO Check CRC
                        if not rom.has_key('crc'):
                            if rom.has_key('status'):
                                if rom['status'] != 'nodump': 
                                    print "No CRC - " + game['name'] + " - " + rom['name']
                        else:
                            crc = int(rom['crc'], 16)
                            foundCrc = foundRoms[rom['name']].CRC
                            # TODO why does 18w_b1 in 18w2.zip not add up!
                            if foundCrc != crc:
                                missing = True
                                print "Incorrect crc for " + rom['name'] + " should be " + str(crc) + " but is " + str(foundCrc)
                    else:
                        if rom.has_key('status'):
                            if rom['status'] != 'nodump':
                                missingInParent = missingFromParent(game, rom, soup)
                                if not missingInParent:
                                    missing = True
                                    print "Missing rom " + rom['name']
                
            elif os.path.isdir(dirPath):
                None
            else:
                missing = True
                
            if missing:
                print "Missing set " + game['name']
                missingZipCount = missingZipCount + 1

    
    else:
        print "Mame info file and / or Mame rom dir not found"

if __name__ == '__main__':
    doMain()