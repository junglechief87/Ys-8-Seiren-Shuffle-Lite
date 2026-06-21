import os.path
import csv
import sys
import random
import shared.config as config
from shared.functions import *

def updateINI(progress_callback=None):
    playerSettings = config.executable_directory + "/settings.ini"
    
    # Check if file exists
    if not os.path.exists(playerSettings):
        # Create new file with Settings section and DisplayLanguage
        with open(playerSettings, 'w', encoding='utf-8') as file:
            file.write("[Settings]\n")
            file.write("DisplayLanguage=EN\n")
    else:
        # File exists, read and modify
        with open(playerSettings, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        languageSet = False
        settingsExist = False
        
        # Find if DisplayLanguage exists or where [Settings] is
        for i, line in enumerate(lines):
            if line.startswith("DisplayLanguage="):
                lines[i] = "DisplayLanguage=EN\n"
                languageSet = True
                break
            if line.startswith("[Settings]"):
                settingsExist = True
        
        # If DisplayLanguage not found
        if not languageSet:
            if settingsExist:
                lines.append("DisplayLanguage=EN\n")
            else:
                # No [Settings] section, add both
                lines.append("[Settings]\n")
                lines.append("DisplayLanguage=EN\n")
        
        # Write back
        with open(playerSettings, 'w', encoding='utf-8') as file:
            file.writelines(lines)

    if progress_callback:
        progress_callback(f"Patched: settings.ini")
    

#right now this is only to get rid of some logically problematic beehives but could do more later
def miscFixes(progress_callback=None):
    deleteHives = ['mons47','mons48','mons49']
    locFile = getLocFile('mp1302t2','map')
    monsIDOffset = 26
    monsFlagsOffset = 68
    monsScriptOffset = 92
    
    fileBytes = readFileIntoBuffer(locFile)

    for hive in deleteHives:
        hiveLoc = fileBytes.find(hive.encode('utf-8'))
        fileBytes = bytearray(fileBytes)
        fileBytes = writeStringToBytes(fileBytes,hiveLoc + monsIDOffset,'M0225')
        fileBytes = writeStringToBytes(fileBytes,hiveLoc + monsFlagsOffset,'---------P-------')
        fileBytes = writeStringToBytes(fileBytes,hiveLoc + monsScriptOffset,'m0225:m0225')
    
    writeBufferIntoFile(locFile,fileBytes)
    if progress_callback:
        progress_callback(f"Fixed: {os.path.basename(locFile)}")

    #remove talk script from thanatos near palace
    nearPalaceLocFile = getLocFile('mp6204', 'map')
    fileBytes = readFileIntoBuffer(nearPalaceLocFile)
    thanatosLoc = fileBytes.find('talk:Talk_Thanatos'.encode('utf-8'))
    fileBytes = writeStringToBytes(fileBytes, thanatosLoc, '------------------') #removes the script name so it won't be able to call it, effectively removing the talk option for thanatos near the palace
    writeBufferIntoFile(nearPalaceLocFile,fileBytes)

    if progress_callback:
        progress_callback(f"Patched: {os.path.basename(nearPalaceLocFile)}")

    #setup paro script
    calmInletLocFile = getLocFile('mp1201', 'map')
    fileBytes = readFileIntoBuffer(calmInletLocFile)
    paroLoc = fileBytes.find('talk:Talk_Paro'.encode('utf-8'))
    fileBytes = writeStringToBytes(fileBytes, paroLoc, 'rng:Paro_Party') #changes script name to use custom paro script
    writeBufferIntoFile(calmInletLocFile,fileBytes)

    if progress_callback:
        progress_callback(f"Patched: {os.path.basename(calmInletLocFile)}")

    ys8EXE = config.executable_path
    exeBytes = readFileIntoBuffer(ys8EXE)
    exeBytes[0x29B1BA:0x29B1C3] = [0xF3,0x44,0x0F,0x59, 0x15, 0x21, 0xCF, 0x30, 0x00] 
    # Changes ys8.exe+29BDBA - F3 44 0F59 15 D5653100  - mulss xmm10,[ys8.exe+5B2398] { (0.10) }
    # to ys8.exe+29BDBA - F3 44 0F59 15 21CF3000  - mulss xmm10,[ys8.exe+5A8CE4] { (4.00) }
    # makes raids and intercepts more rewarding
    exeBytes[0x29B2A0:0x29B2A1] = [0xEB] 
    # Changes ys8.exe+29B2A0 - 74 12 - je ys8.exe+29B2AD
    # to ys8.exe+29B2A0 - EB 12 - jmp ys8.exe+29B2AD
    # skips check on party leader that prevents Dana forms from getting exp
    writeBufferIntoFile(ys8EXE, exeBytes)

    if progress_callback:
        progress_callback(f"Patched: Ys8.exe")

    # speeds up respawn time of exploding plants to reduce downtime in Oceanus fight
    explosivePlant = os.path.join(config.executable_directory, "chr/enemy/m0660/m0660.mtb")
    plantRespawn = readFileIntoBuffer(explosivePlant)
    plantRespawn[0xE05:0xE07] = [0x3C,0x00] #Sets respawn timer on explosive plants in Archeozic Chasme to 1 second instead of 8

    writeBufferIntoFile(explosivePlant,plantRespawn)
    if progress_callback:
        progress_callback(f"Patched: m0660.mtb")

def randomizeOctoBosses(settings):
    random.seed(settings['seed'])
    octus1 = getLocFile('mp6301','map')
    octus2 = getLocFile('mp6302','map')
    octus3 = getLocFile('mp6303','map')
    octus4 = getLocFile('mp6304','map')

    octoMonData = {
        'M0881':{'script':'m0881:m0881', 'data':'m0881/m0881'},
        'M0882':{'script':'m0882:m0882', 'data':'m0882/m0882'},
        'M0883':{'script':'m0883:m0883', 'data':'m0883/m0883'},
        'M0884':{'script':'m0884:m0884', 'data':'m0884/m0884'},
        'M0885':{'script':'m0885:m0885', 'data':'m0885/m0885'},
        'M0886':{'script':'m0886:m0886', 'data':'m0886/m0886'},
        'M0887':{'script':'m0887:m0887', 'data':'m0887/m0887'},
        'M0888':{'script':'m0888:m0888', 'data':'m0888/m0888'},
        'M0889':{'script':'m0889:m0889', 'data':'m0889/m0889'},
        'M0890':{'script':'m0890:m0890', 'data':'m0890/m0890'},
        }
    
    monsIDOffset = 29
    monsScriptOffset = 91

    #values specific to octus1 map
    dataOffsets = [837,869]
    eventOffsets = [5484,5647]
    octus1bytes = readFileIntoBuffer(octus1)
    octus1Mons = ['ev_mons09','ev_mons10']
    for index,octoMon in enumerate(octus1Mons):
        octoMonLoc = octus1bytes.find(octoMon.encode('utf-8'))
        if settings['options']['octus_paths_opened'] == 1:
            selectedOctoMon = random.choice(list(octoMonData.items()))
        else:
            #this is to restore the original values
            selectedOctoMon = tuple(octoMonData.items())[index+8]
        octus1bytes = writeStringToBytes(octus1bytes, dataOffsets[index], selectedOctoMon[1]['data'])
        octus1bytes = writeStringToBytes(octus1bytes, octoMonLoc + monsIDOffset, selectedOctoMon[0])
        octus1bytes = writeStringToBytes(octus1bytes, octoMonLoc + monsScriptOffset, selectedOctoMon[1]['script'])
        octus1bytes = writeStringToBytes(octus1bytes, eventOffsets[index], selectedOctoMon[1]['script'])

    writeBufferIntoFile(octus1,octus1bytes)

    #values specific to octus2 map
    dataOffsets = [837,869,901]
    eventOffsets = [7426,7589,7752]
    octus2bytes = readFileIntoBuffer(octus2)
    octus2Mons = ['ev_mons01','ev_mons02','ev_mons03']
    for index,octoMon in enumerate(octus2Mons):
        octoMonLoc = octus2bytes.find(octoMon.encode('utf-8'))
        if settings['options']['octus_paths_opened'] == 1:
            selectedOctoMon = random.choice(list(octoMonData.items()))
        else:
            #this is to restore the original values
            selectedOctoMon = tuple(octoMonData.items())[index]
        octus2bytes = writeStringToBytes(octus2bytes, dataOffsets[index], selectedOctoMon[1]['data'])
        octus2bytes = writeStringToBytes(octus2bytes, octoMonLoc + monsIDOffset, selectedOctoMon[0])
        octus2bytes = writeStringToBytes(octus2bytes, octoMonLoc + monsScriptOffset, selectedOctoMon[1]['script'])
        octus2bytes = writeStringToBytes(octus2bytes, eventOffsets[index], selectedOctoMon[1]['script'])
    
    writeBufferIntoFile(octus2,octus2bytes)

    #values specific to octus3 map
    dataOffsets = [837,869,901]
    eventOffsets = [9460,9623,9786]
    octus3bytes = readFileIntoBuffer(octus3)
    octus3Mons = ['ev_mons04','ev_mons05','ev_mons06']
    for index,octoMon in enumerate(octus3Mons):
        octoMonLoc = octus3bytes.find(octoMon.encode('utf-8'))
        if settings['options']['octus_paths_opened'] == 1:
            selectedOctoMon = random.choice(list(octoMonData.items()))
        else:
            #this is to restore the original values
            selectedOctoMon = tuple(octoMonData.items())[index+3]
        octus3bytes = writeStringToBytes(octus3bytes, dataOffsets[index], selectedOctoMon[1]['data'])
        octus3bytes = writeStringToBytes(octus3bytes, octoMonLoc + monsIDOffset, selectedOctoMon[0])
        octus3bytes = writeStringToBytes(octus3bytes, octoMonLoc + monsScriptOffset, selectedOctoMon[1]['script'])
        octus3bytes = writeStringToBytes(octus3bytes, eventOffsets[index], selectedOctoMon[1]['script'])
    
    writeBufferIntoFile(octus3,octus3bytes)

    #values specific to octus4 map
    dataOffsets = [837,869]
    eventOffsets = [6037,6200]
    octus4bytes = readFileIntoBuffer(octus4)
    octus4Mons = ['ev_mons07','ev_mons08']
    for index,octoMon in enumerate(octus4Mons):
        octoMonLoc = octus4bytes.find(octoMon.encode('utf-8'))
        if settings['options']['octus_paths_opened'] == 1:
            selectedOctoMon = random.choice(list(octoMonData.items()))
        else:
            #this is to restore the original values
            selectedOctoMon = tuple(octoMonData.items())[index+6]
        octus4bytes = writeStringToBytes(octus4bytes, dataOffsets[index], selectedOctoMon[1]['data'])
        octus4bytes = writeStringToBytes(octus4bytes, octoMonLoc + monsIDOffset,selectedOctoMon[0])
        octus4bytes = writeStringToBytes(octus4bytes, octoMonLoc + monsScriptOffset, selectedOctoMon[1]['script'])
        octus4bytes = writeStringToBytes(octus4bytes, eventOffsets[index], selectedOctoMon[1]['script'])
    
    writeBufferIntoFile(octus4,octus4bytes)

def pastDanaFixes(enable):
    bullfrodon = os.path.join(config.executable_directory, "chr/enemy/m2102/m2102.mtb")
    lonbrius = os.path.join(config.executable_directory, "chr/enemy/b101/b101b.mtb")
    deanafrog = os.path.join(config.executable_directory, "chr/enemy/m0884/m0884.mtb")
    melaiduma = os.path.join(config.executable_directory, "chr/enemy/b170/b170.mtb")
    originOfLife = os.path.join(config.executable_directory, "chr/enemy/b010/b010.mtb")
    theos = os.path.join(config.executable_directory, "chr/enemy/b021/b021.mtb")

    # Remove Bullfrodon swallow if Past Dana Mode on or restore script names if not ######
    disableSwallow = readFileIntoBuffer(bullfrodon)

    if enable:
        disableSwallow[0xCA6:0xCAA] = [0x5F,0x4F,0x46,0x46] #Spells _OFF so it's easy to find in the file, changes the function name so it won't be able to call it from the enemy script
    else:
        disableSwallow[0xCA6:0xCAA] = [0x00,0x00,0x00,0x00] #Restores original script name

    writeBufferIntoFile(bullfrodon,disableSwallow)

    # Remove Lonbrius bites if Past Dana Mode on or restore script names if not ######
    disableBites = readFileIntoBuffer(lonbrius)

    if enable:
        disableBites[0x3753:0x3757] = [0x5F,0x4F,0x46,0x46] #Spells _OFF so it's easy to find in the file, changes the function name so it won't be able to call it from the enemy script
        disableBites[0x3BFE:0x3C02] = [0x5F,0x4F,0x46,0x46]
        disableBites[0x4222:0x4226] = [0x5F,0x4F,0x46,0x46]
    else:
        disableBites[0x3753:0x3757] = [0x00,0x00,0x00,0x00] #Restores original script name
        disableBites[0x3BFE:0x3C02] = [0x00,0x00,0x00,0x00] 
        disableBites[0x4222:0x4226] = [0x00,0x00,0x00,0x00] 

    writeBufferIntoFile(lonbrius,disableBites)

    # Remove Deanafrog swallow if Past Dana Mode on or restore script names if not ######
    disableSwallow2 = readFileIntoBuffer(deanafrog)

    if enable:
        disableSwallow2[0xCA7:0xCAB] = [0x5F,0x4F,0x46,0x46] #Spells _OFF so it's easy to find in the file, changes the function name so it won't be able to call it from the enemy script
    else:
        disableSwallow2[0xCA7:0xCAB] = [0x00,0x00,0x00,0x00] #Restores original script name

    writeBufferIntoFile(deanafrog,disableSwallow2)

    # Remove Origin of Life vanish if Past Dana Mode on or restore script names if not ######
    disableVanish = readFileIntoBuffer(originOfLife)

    if enable:
        disableVanish[0xD739:0xD73D] = [0x5F,0x4F,0x46,0x46] #Spells _OFF so it's easy to find in the file, changes the function name so it won't be able to call it from the enemy script
    else:
        disableVanish[0xD739:0xD73D] = [0x00,0x00,0x00,0x00] #Restores original script name

    writeBufferIntoFile(originOfLife,disableVanish)

    # Remove Melaiduma vanish slash if Past Dana Mode on or restore script names if not ######
    disableVanishSlash = readFileIntoBuffer(melaiduma)

    if enable:
        disableVanishSlash[0x75E9:0x75ED] = [0x5F,0x4F,0x46,0x46] #Spells _OFF so it's easy to find in the file, changes the function name so it won't be able to call it from the enemy script
    else:
        disableVanishSlash[0x75E9:0x75ED] = [0x00,0x00,0x00,0x00] #Restores original script name

    writeBufferIntoFile(melaiduma,disableVanishSlash)

    # Remove Theos bind attack if Past Dana Mode on or restore script names if not ######
    disableBind = readFileIntoBuffer(theos)

    if enable:
        disableBind[0x4A78:0x4A7C] = [0x5F,0x4F,0x46,0x46] #Spells _OFF so it's easy to find in the file, changes the function name so it won't be able to call it from the enemy script
        disableBind[0x4CF2:0x4CF6] = [0x5F,0x4F,0x46,0x46]
    else:
        disableBind[0x4A78:0x4A7C] = [0x00,0x00,0x00,0x00] #Restores original script name
        disableBind[0x4CF2:0x4CF6] = [0x00,0x00,0x00,0x00]

    writeBufferIntoFile(theos, disableBind)

def makeResourceDropsGuaranteed(progress_callback=None):
    resourcePointDropTable = os.path.join(config.executable_directory, "text/itempt.tbb")
    makeDropsGuaranteed = readFileIntoBuffer(resourcePointDropTable)
    resourceStrings = ['ICON3D_MT_N1_STONE','ICON3D_MT_N1_WOOD','ICON3D_MT_N1_FLOWER', 'ICON3D_US_MANGO','ICON3D_US_BERRY','ICON3D_US_DRAGONFRUIT']
    viableRewards = {'ICON3D_MT_N1_STONE':['ICON3D_MT_N2_STONE','ICON3D_MT_N3_STONE','ICON3D_MT_N4_STONE','ICON3D_MT_R2_STONE','ICON3D_MT_R4_STONE'],
                     'ICON3D_MT_N1_WOOD': ['ICON3D_MT_N2_WOOD','ICON3D_MT_N3_WOOD','ICON3D_MT_N4_WOOD','ICON3D_MT_R2_WOOD','ICON3D_MT_R4_WOOD'],
                     'ICON3D_MT_N1_FLOWER': ['ICON3D_MT_N2_FLOWER','ICON3D_MT_N3_FLOWER','ICON3D_MT_N4_FLOWER','ICON3D_MT_R1_FLOWER','ICON3D_MT_R3_FLOWER','ICON3D_MT_R5_FLOWER'],
                     'ICON3D_US_MANGO': ['ICON3D_US_MANGO_S'],
                     'ICON3D_US_BERRY': ['ICON3D_US_BERRY_S'],
                     'ICON3D_US_DRAGONFRUIT': ['ICON3D_US_DRAGONFRUIT_S']}
    
    for resourceString in resourceStrings:
        currentPos = 1263
        while makeDropsGuaranteed.find(resourceString.encode('utf-8'), currentPos) != -1:
            bottomTierResourceIndex = makeDropsGuaranteed.find(resourceString.encode('utf-8'), currentPos)

            stringSize = len(resourceString)
            currentPos = currentPos + stringSize
            
            # process higher tier rewards values
            higherTierResourceOffset = makeDropsGuaranteed[bottomTierResourceIndex+stringSize:].find('ICON3D_'.encode('utf-8')) + stringSize
            higherTierResourceIndex = higherTierResourceOffset + bottomTierResourceIndex

            if resourceString in ['ICON3D_US_MANGO','ICON3D_US_BERRY','ICON3D_US_DRAGONFRUIT']:
                higherTierResourceValue = makeDropsGuaranteed[higherTierResourceIndex:higherTierResourceIndex+stringSize+2]
            else:
                higherTierResourceValue = makeDropsGuaranteed[higherTierResourceIndex:higherTierResourceIndex+stringSize]

            # process rare rewards values
            rareResourceOffset = makeDropsGuaranteed[higherTierResourceIndex+stringSize:].find('ICON3D_'.encode('utf-8')) + stringSize
            rareResourceIndex = rareResourceOffset + higherTierResourceIndex
            rareResourceValue = makeDropsGuaranteed[rareResourceIndex:rareResourceIndex+stringSize]
            
            # write new values and make adjustments for special cases
            if higherTierResourceValue.decode('utf-8') in viableRewards[resourceString]:
                if resourceString in ['ICON3D_US_MANGO','ICON3D_US_BERRY','ICON3D_US_DRAGONFRUIT']:
                    makeDropsGuaranteed[higherTierResourceIndex+stringSize+2:higherTierResourceIndex+stringSize+5] = [0x00,0x39,0x39] # maximize odds since we can't change file size
                else:
                    makeDropsGuaranteed[bottomTierResourceIndex:bottomTierResourceIndex+stringSize] = higherTierResourceValue
                
            if rareResourceValue.decode('utf-8') in viableRewards[resourceString]:
                makeDropsGuaranteed[higherTierResourceIndex:higherTierResourceIndex+stringSize] = rareResourceValue
                
    writeBufferIntoFile(resourcePointDropTable,makeDropsGuaranteed)
    if progress_callback:
        progress_callback(f"Updated: {os.path.basename(resourcePointDropTable)}")

STATUS_DEFAULTS = {
    'ADOL': {'EXPMIN': 100, 'EXPMAX': 500000, '属性1': 'ZOKU_WATER', '属性1値': 100},
    'LAXIA': {'EXPMIN': 95, 'EXPMAX': 450000, '属性1': 'ZOKU_LIGHT', '属性1値': 100},
    'SAHAD': {'EXPMIN': 105, 'EXPMAX': 550000, '属性1': 'ZOKU_EARTH', '属性1値': 100},
    'HUMMEL': {'EXPMIN': 90, 'EXPMAX': 420000, '属性1': 'ZOKU_LIGHT', '属性1値': 100},
    'RICOTTA': {'EXPMIN': 97, 'EXPMAX': 480000, '属性1': 'ZOKU_EARTH', '属性1値': 100},
    'DANA': {'EXPMIN': 102, 'EXPMAX': 520000, '属性1': 'ZOKU_WATER', '属性1値': 100},
    'DANA2': {'EXPMIN': 102, 'EXPMAX': 520000, '属性1': 'ZOKU_EARTH', '属性1値': 100},
    'DANA3': {'EXPMIN': 102, 'EXPMAX': 520000, '属性1': 'ZOKU_LIGHT', '属性1値': 100},
}

STATUS_ASSOCIATIONS = {
    'Slash': 'ZOKU_WATER',
    'Strike': 'ZOKU_EARTH',
    'Pierce': 'ZOKU_LIGHT',
}

def setElementalAssociations(damageMapping, charID):
    if charID == 'DANA2':
        charID = 'GRATIKA'
    elif charID == 'DANA3':
        charID = 'LUMINOUS'
    for damageType, character in damageMapping.items():
        if charID in [character.upper() for character in character]:
            return STATUS_ASSOCIATIONS[damageType]

def updateStatusCSV(settings):
    options = settings['options']
    exp_multiplier = options['experience_multiplier']
    statusFileLoc = os.path.join(config.executable_directory, "text/en/status.csv")
    statusEdits = {}
    
    for character in STATUS_DEFAULTS:
        statusEdits[character] = {
            'EXPMIN': int(STATUS_DEFAULTS[character]['EXPMIN'] / exp_multiplier),
            'EXPMAX': int(STATUS_DEFAULTS[character]['EXPMAX'] / exp_multiplier),
            '属性1': STATUS_DEFAULTS[character]['属性1'] if options['shuffle_damage_types'] != 1 else setElementalAssociations(settings['damage_mapping'], character),
            '属性1値': STATUS_DEFAULTS[character]['属性1値']
        }

    edit_csv(statusFileLoc, statusEdits)

RAID_STAGE_DEFAULTS = {
    "INTERCEPT_STAGE01": {"ウェイブファイル１": "text/stage/st_01_p.csv", "メニュー表示用ウェーブ数": 3, "ランクＢ:判定スコア": 30000, "ランクＡ:判定スコア": 55000, "ランクＳ:判定スコア": 80000,
                          "ランクＣ：判定スコア": 1000, "ランクＢ：判定スコア": 10000, "ランクＡ：判定スコア": 20000, "ランクＳ：判定スコア": 30000},
    "INTERCEPT_STAGE02": {"ウェイブファイル１": "text/stage/st_02_p.csv", "メニュー表示用ウェーブ数": 4, "ランクＢ:判定スコア": 35000, "ランクＡ:判定スコア": 60000, "ランクＳ:判定スコア": 85000,
                          "ランクＣ：判定スコア": 1000, "ランクＢ：判定スコア": 10000, "ランクＡ：判定スコア": 25000, "ランクＳ：判定スコア": 45000},
    "INTERCEPT_STAGE03": {"ウェイブファイル１": "text/stage/st_03_p.csv", "メニュー表示用ウェーブ数": 3, "ランクＢ:判定スコア": 20000, "ランクＡ:判定スコア": 45000, "ランクＳ:判定スコア": 65000,
                          "ランクＣ：判定スコア": 5000, "ランクＢ：判定スコア": 15000, "ランクＡ：判定スコア": 30000, "ランクＳ：判定スコア": 55000},
    "INTERCEPT_STAGE04": {"ウェイブファイル１": "text/stage/st_04_p.csv", "メニュー表示用ウェーブ数": 4, "ランクＢ:判定スコア": 20000, "ランクＡ:判定スコア": 45000, "ランクＳ:判定スコア": 65000,
                          "ランクＣ：判定スコア": 5000, "ランクＢ：判定スコア": 20000, "ランクＡ：判定スコア": 40000, "ランクＳ：判定スコア": 65000},
    "INTERCEPT_STAGE05": {"ウェイブファイル１": "text/stage/st_05_p.csv", "メニュー表示用ウェーブ数": 3, "ランクＢ:判定スコア": 30000, "ランクＡ:判定スコア": 50000, "ランクＳ:判定スコア": 70000,
                          "ランクＣ：判定スコア": 10000, "ランクＢ：判定スコア": 30000, "ランクＡ：判定スコア": 50000, "ランクＳ：判定スコア": 80000},
    "INTERCEPT_STAGE06": {"ウェイブファイル１": "text/stage/st_06_p.csv", "メニュー表示用ウェーブ数": 5, "ランクＢ:判定スコア": 40000, "ランクＡ:判定スコア": 80000, "ランクＳ:判定スコア": 120000,
                          "ランクＣ：判定スコア": 10000, "ランクＢ：判定スコア": 35000, "ランクＡ：判定スコア": 65000, "ランクＳ：判定スコア": 100000},
    "INTERCEPT_STAGE07": {"ウェイブファイル１": "text/stage/st_07_p.csv", "メニュー表示用ウェーブ数": 4, "ランクＢ:判定スコア": 35000, "ランクＡ:判定スコア": 65000, "ランクＳ:判定スコア": 90000,
                          "ランクＣ：判定スコア": 10000, "ランクＢ：判定スコア": 35000, "ランクＡ：判定スコア": 70000, "ランクＳ：判定スコア": 130000},
    "INTERCEPT_STAGE08": {"ウェイブファイル１": "text/stage/st_08_p.csv", "メニュー表示用ウェーブ数": 3, "ランクＢ:判定スコア": 60000, "ランクＡ:判定スコア": 100000, "ランクＳ:判定スコア": 135000,
                          "ランクＣ：判定スコア": 30000, "ランクＢ：判定スコア": 70000, "ランクＡ：判定スコア": 120000, "ランクＳ：判定スコア": 180000},
    "INTERCEPT_STAGE09": {"ウェイブファイル１": "text/stage/st_09_p.csv", "メニュー表示用ウェーブ数": 4, "ランクＢ:判定スコア": 40000, "ランクＡ:判定スコア": 65000, "ランクＳ:判定スコア": 90000,
                          "ランクＣ：判定スコア": 10000, "ランクＢ：判定スコア": 40000, "ランクＡ：判定スコア": 80000, "ランクＳ：判定スコア": 130000},
    "INTERCEPT_STAGE11": {"ウェイブファイル１": "text/stage/st_11_p.csv", "メニュー表示用ウェーブ数": 3, "ランクＢ:判定スコア": 40000, "ランクＡ:判定スコア": 80000, "ランクＳ:判定スコア": 115000,
                          "ランクＣ：判定スコア": 20000, "ランクＢ：判定スコア": 50000, "ランクＡ：判定スコア": 100000, "ランクＳ：判定スコア": 140000},
    "INTERCEPT_STAGE12": {"ウェイブファイル１": "text/stage/st_12_p.csv", "メニュー表示用ウェーブ数": 4, "ランクＢ:判定スコア": 50000, "ランクＡ:判定スコア": 100000, "ランクＳ:判定スコア": 150000,
                          "ランクＣ：判定スコア": 10000, "ランクＢ：判定スコア": 30000, "ランクＡ：判定スコア": 110000, "ランクＳ：判定スコア": 170000},
    "INTERCEPT_STAGE21": {"ウェイブファイル１": "text/stage/st_21_p.csv", "メニュー表示用ウェーブ数": 3, "ランクＢ:判定スコア": 40000, "ランクＡ:判定スコア": 70000, "ランクＳ:判定スコア": 95000,
                          "ランクＣ：判定スコア": 10000, "ランクＢ：判定スコア": 30000, "ランクＡ：判定スコア": 80000, "ランクＳ：判定スコア": 110000},
    "INTERCEPT_STAGE22": {"ウェイブファイル１": "text/stage/st_22_p.csv", "メニュー表示用ウェーブ数": 3, "ランクＢ:判定スコア": 50000, "ランクＡ:判定スコア": 100000, "ランクＳ:判定スコア": 140000,
                          "ランクＣ：判定スコア": 5000, "ランクＢ：判定スコア": 50000, "ランクＡ：判定スコア": 80000, "ランクＳ：判定スコア": 135000},
    "INTERCEPT_STAGE23": {"ウェイブファイル１": "text/stage/st_23_p.csv", "メニュー表示用ウェーブ数": 6, "ランクＢ:判定スコア": 90000, "ランクＡ:判定スコア": 135000, "ランクＳ:判定スコア": 170000,
                          "ランクＣ：判定スコア": 5000, "ランクＢ：判定スコア": 80000, "ランクＡ：判定スコア": 160000, "ランクＳ：判定スコア": 230000},
    "INTERCEPT_STAGE24": {"ウェイブファイル１": "text/stage/st_24_p.csv", "メニュー表示用ウェーブ数": 6, "ランクＢ:判定スコア": 80000, "ランクＡ:判定スコア": 135000, "ランクＳ:判定スコア": 185000,
                          "ランクＣ：判定スコア": 10000, "ランクＢ：判定スコア": 50000, "ランクＡ：判定スコア": 250000, "ランクＳ：判定スコア": 400000},
    "INTERCEPT_STAGE25": {"ウェイブファイル１": "text/stage/st_25_p.csv", "メニュー表示用ウェーブ数": 9, "ランクＢ:判定スコア": 110000, "ランクＡ:判定スコア": 160000, "ランクＳ:判定スコア": 230000,
                          "ランクＣ：判定スコア": 20000, "ランクＢ：判定スコア": 100000, "ランクＡ：判定スコア": 240000, "ランクＳ：判定スコア": 380000},
    "INTERCEPT_STAGE26": {"ウェイブファイル１": "text/stage/st_26_p.csv", "メニュー表示用ウェーブ数": 9, "ランクＢ:判定スコア": 180000, "ランクＡ:判定スコア": 260000, "ランクＳ:判定スコア": 340000,
                          "ランクＣ：判定スコア": 50000, "ランクＢ：判定スコア": 150000, "ランクＡ：判定スコア": 350000, "ランクＳ：判定スコア": 700000},
    "INTERCEPT_STAGE27": {"ウェイブファイル１": "text/stage/st_27_p.csv", "メニュー表示用ウェーブ数": 6, "ランクＢ:判定スコア": 130000, "ランクＡ:判定スコア": 160000, "ランクＳ:判定スコア": 180000,
                          "ランクＣ：判定スコア": 50000, "ランクＢ：判定スコア": 100000, "ランクＡ：判定スコア": 150000, "ランクＳ：判定スコア": 200000},
}

HUNT_STAGE_DEFAULTS = {
    "INTERCEPT_STAGE31": {"ランクＢ:判定スコア": 450000, "ランクＡ:判定スコア": 550000, "ランクＳ:判定スコア": 650000,
                          "ランクＣ：判定スコア": 700000, "ランクＢ：判定スコア": 800000, "ランクＡ：判定スコア": 950000, "ランクＳ：判定スコア": 1100000},
    "INTERCEPT_STAGE32": {"ランクＢ:判定スコア": 450000, "ランクＡ:判定スコア": 550000, "ランクＳ:判定スコア": 650000,
                          "ランクＣ：判定スコア": 700000, "ランクＢ：判定スコア": 800000, "ランクＡ：判定スコア": 950000, "ランクＳ：判定スコア": 1100000},
    "INTERCEPT_STAGE33": {"ランクＢ:判定スコア": 450000, "ランクＡ:判定スコア": 550000, "ランクＳ:判定スコア": 650000,
                          "ランクＣ：判定スコア": 700000, "ランクＢ：判定スコア": 800000, "ランクＡ：判定スコア": 950000, "ランクＳ：判定スコア": 1100000},
    "INTERCEPT_STAGE34": {"ランクＢ:判定スコア": 450000, "ランクＡ:判定スコア": 550000, "ランクＳ:判定スコア": 650000,
                          "ランクＣ：判定スコア": 700000, "ランクＢ：判定スコア": 800000, "ランクＡ：判定スコア": 950000, "ランクＳ：判定スコア": 1100000},
    "INTERCEPT_STAGE35": {"ランクＢ:判定スコア": 450000, "ランクＡ:判定スコア": 550000, "ランクＳ:判定スコア": 650000,
                          "ランクＣ：判定スコア": 700000, "ランクＢ：判定スコア": 800000, "ランクＡ：判定スコア": 950000, "ランクＳ：判定スコア": 1100000},
    "INTERCEPT_STAGE36": {"ランクＢ:判定スコア": 450000, "ランクＡ:判定スコア": 550000, "ランクＳ:判定スコア": 650000,
                          "ランクＣ：判定スコア": 700000, "ランクＢ：判定スコア": 800000, "ランクＡ：判定スコア": 950000, "ランクＳ：判定スコア": 1100000},
    "INTERCEPT_STAGE37": {"ランクＢ:判定スコア": 450000, "ランクＡ:判定スコア": 550000, "ランクＳ:判定スコア": 650000,
                          "ランクＣ：判定スコア": 700000, "ランクＢ：判定スコア": 800000, "ランクＡ：判定スコア": 950000, "ランクＳ：判定スコア": 1100000},
    "INTERCEPT_STAGE38": {"ランクＢ:判定スコア": 450000, "ランクＡ:判定スコア": 550000, "ランクＳ:判定スコア": 650000,
                          "ランクＣ：判定スコア": 700000, "ランクＢ：判定スコア": 800000, "ランクＡ：判定スコア": 950000, "ランクＳ：判定スコア": 1100000},
    "INTERCEPT_STAGE39": {"ランクＢ:判定スコア": 450000, "ランクＡ:判定スコア": 550000, "ランクＳ:判定スコア": 650000,
                          "ランクＣ：判定スコア": 700000, "ランクＢ：判定スコア": 800000, "ランクＡ：判定スコア": 950000, "ランクＳ：判定スコア": 1100000},
}

HUNT_BOSS_SPAWN_WAVE = {
    "st_31_p.tbb": {"Offset": 0x72C, "OriginalValue": 0x35},
    "st_32_p.tbb": {"Offset": 0x728, "OriginalValue": 0x35},
    "st_33_p.tbb": {"Offset": 0x79C, "OriginalValue": 0x39},
    "st_34_p.tbb": {"Offset": 0x762, "OriginalValue": 0x31},
    "st_35_p.tbb": {"Offset": 0x760, "OriginalValue": 0x34},
    "st_36_p.tbb": {"Offset": 0x751, "OriginalValue": 0x32},
    "st_37_p.tbb": {"Offset": 0x742, "OriginalValue": 0x39},
    "st_38_p.tbb": {"Offset": 0x784, "OriginalValue": 0x33},
    "st_39_p.tbb": {"Offset": 0x7D5, "OriginalValue": 0x34},
}

def fastIntercepts(options):
    intFileLoc = os.path.join(config.executable_directory, "text/en/intstage.csv")
    stageEdits = {}

    if options['fast_intercepts'] == 1:
        for huntFileName, data in HUNT_BOSS_SPAWN_WAVE.items():
            huntFileLoc = os.path.join(config.executable_directory, "text/stage", huntFileName)
            huntFileBytes = readFileIntoBuffer(huntFileLoc)
            huntFileBytes[data['Offset']] = 0x31 # changes boss spawn wave to 1
            writeBufferIntoFile(huntFileLoc, huntFileBytes)
        
        for raid, data in RAID_STAGE_DEFAULTS.items():
            data['ウェイブファイル１'] = data['ウェイブファイル１'].replace(".csv", "_short.csv")
            data['メニュー表示用ウェーブ数'] = data['メニュー表示用ウェーブ数'] // 2
            data["ランクＢ:判定スコア"] = int(round(data["ランクＢ:判定スコア"] * 0.55, -3))
            data["ランクＡ:判定スコア"] = int(round(data["ランクＡ:判定スコア"] * 0.55, -3))
            data["ランクＳ:判定スコア"] = int(round(data["ランクＳ:判定スコア"] * 0.55, -3))
            data["ランクＣ：判定スコア"] = int(round(data["ランクＣ：判定スコア"] * 0.55, -3))
            data["ランクＢ：判定スコア"] = int(round(data["ランクＢ：判定スコア"] * 0.55, -3))
            data["ランクＡ：判定スコア"] = int(round(data["ランクＡ：判定スコア"] * 0.55, -3))
            data["ランクＳ：判定スコア"] = int(round(data["ランクＳ：判定スコア"] * 0.55, -3))
            stageEdits[raid] = data
        
        for hunt, data in HUNT_STAGE_DEFAULTS.items():
            data["ランクＢ:判定スコア"] = int(round(data["ランクＢ:判定スコア"] * 0.55, -3))
            data["ランクＡ:判定スコア"] = int(round(data["ランクＡ:判定スコア"] * 0.55, -3))
            data["ランクＳ:判定スコア"] = int(round(data["ランクＳ:判定スコア"] * 0.55, -3))
            data["ランクＣ：判定スコア"] = int(round(data["ランクＣ：判定スコア"] * 0.55, -3))
            data["ランクＢ：判定スコア"] = int(round(data["ランクＢ：判定スコア"] * 0.55, -3))
            data["ランクＡ：判定スコア"] = int(round(data["ランクＡ：判定スコア"] * 0.55, -3))
            data["ランクＳ：判定スコア"] = int(round(data["ランクＳ：判定スコア"] * 0.55, -3))
            stageEdits[hunt] = data

    else: # restore default values if not enabled
        for huntFileName, data in HUNT_BOSS_SPAWN_WAVE.items():
            huntFileLoc = os.path.join(config.executable_directory, "text/stage", huntFileName)
            huntFileBytes = readFileIntoBuffer(huntFileLoc)
            huntFileBytes[data['Offset']] = data['OriginalValue'] # restore original boss spawn wave
            writeBufferIntoFile(huntFileLoc, huntFileBytes)

        for raid, data in RAID_STAGE_DEFAULTS.items():
            stageEdits[raid] = data
        for hunt, data in HUNT_STAGE_DEFAULTS.items():
            stageEdits[hunt] = data

    edit_csv(intFileLoc, stageEdits, header_line=1)

def AddWarpToFSCCrystal(progress_callback=None):
    '''
      if you ever want to undo this byte modifications we can just replace the same byte sequence for 2D (2D = "-") as the length of the sequence was never modified.
    '''
    fscFile = os.path.join(config.executable_directory, 'map', 'mp6511', 'mp6511.arb')

    try:
        with open(fscFile, 'rb') as f:
            data = bytearray(f.read())

        # Find the 'chkpt' sequence (warp crystal object)
        chkpt_pos = findByteSequence(data, 'chkpt')
        #print(f"Found 'chkpt' at position: {chkpt_pos}")
        # modification start position = (after 't' + 77 bytes)
        #This is the byte sequence responsible for the custom function of the crystal
        mod_pos = chkpt_pos + len('chkpt') + 77
        #print(f"Modification starts at position: {mod_pos}")
        # Writing the new bytes (custom function name)
        new_data = 'mp6511:warp'
        new_bytes = new_data.encode('ascii')

        # Check if we have enough space
        if mod_pos + len(new_bytes) > len(data):
            raise ValueError("Not enough space in file for the modification")

        # Modifying the bytes
        #print("\nOriginal bytes to be modified:")
        for i in range(len(new_bytes)):
            byte_pos = mod_pos + i
            #print(f"Position {byte_pos}: 0x{data[byte_pos]:02x} ({chr(data[byte_pos]) if 32 <= data[byte_pos] <= 126 else 'non-printable'})")
            data[byte_pos] = new_bytes[i]

        # Write the modified data back to the file
        with open(fscFile, 'wb') as f:
            f.write(data)
        if progress_callback:
            progress_callback(f"Patched: {os.path.basename(fscFile)}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def readFileIntoBuffer(path):
    with open(path,"rb") as buffer:
        return bytearray(buffer.read())

def writeBufferIntoFile(path,array):
    with open(path,"wb") as buffer:
        buffer.write(array)
        buffer.close()

def findByteSequence(binaryData, sequence):
    """
    Find the position of a word (byte sequence) in binary file
    Returns the starting index of the byte sequence
    """

    sequenceBytes = sequence.encode('ascii')
    index = binaryData.find(sequenceBytes)
    if index == -1:
        raise ValueError(f"Sequence '{sequence}' not found in file")
    return index