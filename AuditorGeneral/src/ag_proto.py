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

def getRomZipFileInfo(game):
    roms = {}
    fileList = []
    fileList.append(MAME_ROM_DIR_PATH + os.sep + game['name'] + '.zip')
    
    if game.has_key('cloneof') and os.path.isfile(MAME_ROM_DIR_PATH + os.sep + game['cloneof'] + ".zip"):
        fileList.append(MAME_ROM_DIR_PATH + os.sep + game['cloneof'] + '.zip')
        
    if game.has_key('romof') and os.path.isfile(MAME_ROM_DIR_PATH + os.sep + game['romof'] + ".zip"):
        fileList.append(MAME_ROM_DIR_PATH + os.sep + game['romof'] + '.zip')
    
    for file in fileList:   
        zip = zipfile.ZipFile(file, "r")
        infoList = zip.infolist()
        for info in infoList:
            roms[info.filename] = info
    
    return roms

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
                            if foundRoms[rom['name']].CRC != crc:
                                missing = True
                                if VERBOSE:
                                    print "CRC For " + game['name'] + " - " +  rom['name']
                                    print "Incorrect crc for " + rom['name'] + " should be " + str(crc) + " but is " + str(foundRoms[rom['name']].CRC)
                    else:
                        # TODO work out if missing from parent, or child
                        missing = True
                        if VERBOSE:
                            print "Missing rom " + rom['name']
                
            elif os.path.isdir(dirPath):
                None
            else:
                missing = True
                
            if missing:
                print "Missing " + game['name']
                missingZipCount = missingZipCount + 1

    
    else:
        print "Mame info file and / or Mame rom dir not found"

if __name__ == '__main__':
    doMain()