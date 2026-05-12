import os.path
import csv
import unicodedata
import codecs
from shared.classr import *
import shared.config as config

encode = "utf-8"

def strip_accents_handler(exception):
    """Custom error handler for Shift-JIS encoding: strips accents, falls back to '?' if unable"""
    if isinstance(exception, UnicodeEncodeError):
        char = exception.object[exception.start:exception.end]
        # Strip accents from character using NFD normalization
        normalized = ''.join(c for c in unicodedata.normalize('NFD', char)
                           if unicodedata.category(c) != 'Mn')
        # Try encoding the stripped version in Shift-JIS
        try:
            normalized.encode('Shift-JIS')
            return (normalized, exception.end)
        except:
            # Fall back to '?' if normalization didn't work
            return ('?', exception.end)
    raise exception

# Register the custom error handler
codecs.register_error('strip_accents', strip_accents_handler)
sourceScript = "rng"
_cache = None  # Global variable for lazy loading
def getLocations():
    with open(os.path.join(config.current_directory, "database/location.csv"), encoding='utf-8-sig') as locDB:
        
        locRows = csv.DictReader(locDB)
        locations = []
        for row in locRows:
            # Strip whitespace from keys in case of BOM or encoding issues
            cleaned_row = {k.strip(): v for k, v in row.items()}
            locID = int(cleaned_row['locID'])
            mapID = cleaned_row['mapID']
            mapCheckID = cleaned_row['mapCheckID']
            item = bool(int(cleaned_row['item']))
     
            locationObject = location(locID,mapID,mapCheckID,item)
            locations.append(locationObject)
            
    locDB.close()
    return locations

#def getItems:

def getIcon(itemID):
    with open(os.path.join(config.current_directory, "database/itemTable.csv"), encoding=encode) as itemDB:
        itemRows = csv.DictReader(itemDB) 
        for itemRow in itemRows:
            if int(itemRow['ID']) == itemID:
                icon = itemRow['3DIcon']
                itemDB.close()
                return icon

def getSkillInfo(itemName):
    with open(os.path.join(config.current_directory, "database/skillTable.csv"), encoding=encode) as skillDB:
        skillRows = csv.DictReader(skillDB) 
        for skillRow in skillRows:
            if skillRow['skillName'] == itemName:
                character = skillRow['character']
                skillID = skillRow['skillID']
                skillDB.close()
                if character == 'PARTY_ADOL':
                    characterName = 'Adol'  
                elif character == 'PARTY_LAXIA':
                    characterName = 'Laxia'  
                elif character == 'PARTY_SAHAD':
                    characterName = 'Sahad'  
                elif character == 'PARTY_HUMMEL':
                    characterName = 'Hummel'  
                elif character == 'PARTY_RICOTTA':
                    characterName = 'Ricotta'  
                elif character == 'PARTY_DANA':
                    characterName = 'Dana'  

                return character,skillID,characterName
            
def getLocFile(mapID, fileType):
    cache = load_cache()  # Loads cache only on first call
    if (mapID, fileType) in cache:
        return cache[(mapID, fileType)]

    #The top versoin of the loop is used for running the randomizer from source, the bottom version of the loop is for the executable compile, comment and uncomment accordingly.
    if fileType == 'script':
        #for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__),os.pardir) + "/script/"):
        for root, dirs, files in os.walk(os.path.join(config.executable_directory, "script")):
            for file in files:
                if file.endswith('.scp') and file.find(mapID) >= 0:
                    return os.path.join(root, file)
                
    elif fileType == 'map':
        #for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__),os.pardir) + "/map/"):
        for root, dirs, files in os.walk(os.path.join(config.executable_directory, "map")):
            for file in files:
                if file.endswith('.arb') and file.find(mapID) >= 0:
                    return os.path.join(root, file)
    else:
        raise Exception('Must specify either script or map for file retrieval or specify correct mapID')

def buildLocScripts(locID, source):

    #only build on set of scripts for river valley long shoreline, chests for dawn version share flags
    if locID == 47:
        locID = 44
    elif locID == 48:
        locID = 45
    elif locID == 49:
        locID = 46
        
    if source:
        scriptCall = sourceScript + ':' + str(locID).zfill(4)
    else:
        scriptCall = str(locID).zfill(4)
    return scriptCall

def writeStringToBytes(byteArray,offset,bytesToWrite):
    bytesToWrite = bytesToWrite.encode('utf-8')
    curOffset = offset
    
    for byte in bytesToWrite:
        byteArray[curOffset] = byte
        curOffset+=1

    return byteArray

def getIntRewards():
    with open(os.path.join(config.current_directory, "database/interceptionRewards.csv"), encoding=encode) as rewardDB:
        
        rewardRows = csv.DictReader(rewardDB)
        intRewards = []

        for row in rewardRows:
            stage = row['stage']

            rewards = []
            for index,col in enumerate(row):
                if row[col] == '' or row[col] == None:
                    break
                elif index == 0:
                    pass
                else: 
                    rewards.append(row[col])

            stageReward = interceptReward(stage,rewards)
            intRewards.append(stageReward)
            
    rewardDB.close()
    return intRewards

def getCharacterJoinLv(character):
    lvScript = ''
    for lv in range(1,100):
        if lv == 1:
            lvScript = lvScript + "\tif(LEADER.CHRWORK[CWK_LV] ==" + str(lv) + "){SetLevel(" + character + "," + str(lv) + ")} \n"
        elif lv == 99:
            lvScript = lvScript + "\telse{SetLevel(" + character + "," + str(lv) + ")} \n"
        else:
            lvScript = lvScript + "\telse if(LEADER.CHRWORK[CWK_LV] ==" + str(lv) + "){SetLevel(" + character + "," + str(lv) + ")} \n"

    return lvScript


def load_cache():
    """
    Reads cache.txt and converts it into a dictionary.
    This is used to improve time efficiency of findLocFile
    """
    global _cache
    if _cache is None:  # Load only if it's not already loaded
        _cache = {}  # Initialize empty dictionary
        path = './shared/database/locFileCache.txt'
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.split(",")
                    map_id = parts[0].strip()
                    file_type = parts[1].strip()
                    file_path = parts[2].strip()
                    _cache[(map_id, file_type)] = file_path  # Convert "(mapID, fileType)" back to tuple
    return _cache

def getCharacterJoinLv(character):
    lvScript = ''
    for lv in range(1,100):
        if lv == 1:
            lvScript = lvScript + "\tif(FLAG[GF_TBOX_DUMMY121] == " + str(lv) + "){SetLevel(" + character + "," + str(lv) + ")} \n"
        elif lv == 99:
            lvScript = lvScript + "\telse{SetLevel(" + character + "," + str(lv) + ")} \n"
        else:
            lvScript = lvScript + "\telse if(FLAG[GF_TBOX_DUMMY121] == " + str(lv) + "){SetLevel(" + character + "," + str(lv) + ")} \n"

    return lvScript