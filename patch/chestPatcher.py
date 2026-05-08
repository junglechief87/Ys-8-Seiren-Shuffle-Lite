import os.path
import csv
from shared.classr import *
from shared.functions import *

# Cache for locations to avoid rebuilding on every fillChest call
_locations_cache = None

def set_locations_cache(locations_by_id):
    """Set the locations cache to avoid repeated CSV parsing."""
    global _locations_cache
    _locations_cache = locations_by_id

#Every chest in Ys can take a script parameter that it calls on open, if there is something in it.
#We write a series of scripts onto that chest paremeter based on the randos locID, we want the scripts to be exactly 8 character lengths as this is the game's min script length for the chests. 
#This guarantees we don't overwrite important bytes.
#All other random locations are handled in the game's script .scp files. By reworking the chests like this we can handle all randomization via calls to our own .scp file.
#This allows for greater flexibility as it lets us use whatever we want from the games myriad of prebuilt functions and scripting tools on our chests themselves.
#we only want to patch chest here, obviously, so we look for the string that's tied to all chests and that the type is item.
def cleanChests(locations_by_id=None, progress_callback=None):
    global _locations_cache
    itemIDOffset = 9
    quatityOffset = 15
    scriptOffset = 107
    
    # Use provided dict, global cache, or build fresh
    if locations_by_id is not None:
        loc_dict = locations_by_id
    elif _locations_cache is not None:
        loc_dict = _locations_cache
    else:
        locations = getLocations()
        loc_dict = {loc.locID: loc for loc in locations}
    
    for location in loc_dict.values():
        #we only want to patch chest here, obviously, so we look for the string that's tied to all chests and that the type is item.
        if location.item and location.mapCheckID.find('TBOX') != -1:
            locFile = getLocFile(location.mapID,'map')
            #print("patching .arb file containing chests: " + locFile)
            with open(locFile,"rb") as buffer:
                while (curByte := buffer.read()):
                    fileBytes = curByte

                #we have a special rule here because both chests in the ruins of eternia central district have the same ID for some reason,
                #in the locations list I gave them different IDs so logic and players could tell them apart
                #but for this function that means we need to make a special case
                #switching to a right find should do it since there's only two chests in the file
                #ran into a similar issue for rainbow falls night, I'll need to do something special for it as it has 3 chests
                if location.mapID == 'mp6201' and location.mapCheckID == 'TBOX02':
                    startOfChestArgs = fileBytes.rfind('TBOX01'.encode('utf-8'))
                elif location.mapID == 'mp1304t2':
                    if location.mapCheckID == 'TBOX02':
                        startOfChestArgs = fileBytes.find('TBOX01'.encode('utf-8'),fileBytes.find('TBOX01'.encode('utf-8'))+1)
                    elif location.mapCheckID == 'TBOX03':
                        startOfChestArgs = fileBytes.rfind('TBOX01'.encode('utf-8'))
                    else:
                        startOfChestArgs = fileBytes.find(location.mapCheckID.encode('utf-8'))
                else:
                    startOfChestArgs = fileBytes.find(location.mapCheckID.encode('utf-8'))
                    
                fileBytes = bytearray(fileBytes)
                fileBytes = clearBytes(fileBytes,startOfChestArgs + itemIDOffset,"itemID")    
                fileBytes = clearBytes(fileBytes,startOfChestArgs + quatityOffset,"quantity")
                fileBytes = clearBytes(fileBytes,startOfChestArgs + scriptOffset,"")
                    
                chestScript = buildLocScripts(location.locID, True)
                fileBytes = writeStringToBytes(fileBytes,startOfChestArgs + scriptOffset,chestScript)

                buffer.close()

            with open(locFile,"wb") as buffer:
                buffer.write(fileBytes)
                buffer.close()

            if progress_callback:
                progress_callback(f"Patched {location.mapCheckID} in {location.mapID}")
                    
#clears out existing chest contents and scripts, this is to help error proof our overwritting of the chest data.
def clearBytes(byteArray,startOffset,clearType):
    endOffset = startOffset
    makeChestsClosed = startOffset
    
    while byteArray[endOffset] != 0:
        endOffset+=1
        
    while startOffset <= endOffset:
        byteArray[startOffset] = 00
        startOffset+=1

    if clearType == "quantity":
        byteArray[makeChestsClosed] = 1
    elif clearType == "itemID":
        byteArray[makeChestsClosed] = 139
        byteArray[makeChestsClosed+1] = 00 #I thought I had an issue fixed with some chests with two bytes for their item ID still spawning an item but it cropped up again, so this is an extra failsafe
    
    return byteArray


#places item in the chest
def fillChest(location_id, itemID, quantity, locations_by_id=None):
    global _locations_cache
    itemIDOffset = 9
    quantityOffset = 15
    jingleOffset = 27
    
    # Use provided dict, global cache, or build fresh
    if locations_by_id is not None:
        loc_dict = locations_by_id
    elif _locations_cache is not None:
        loc_dict = _locations_cache
    else:
        locations = getLocations()
        loc_dict = {loc.locID: loc for loc in locations}
    
    location = loc_dict.get(int(location_id))
    
    #find the chest in the file
    if location.mapCheckID.find('TBOX') != -1:
        locFile = getLocFile(location.mapID,'map')
        #print("patching .arb file containing chests: " + locFile)
        with open(locFile,"rb") as buffer:
            while (curByte := buffer.read()):
                fileBytes = curByte

            if location.mapID == 'mp6201' and location.mapCheckID == 'TBOX02':
                startOfChestArgs = fileBytes.rfind('TBOX01'.encode('utf-8'))
            elif location.mapID == 'mp1304t2':
                if location.mapCheckID == 'TBOX02':
                    startOfChestArgs = fileBytes.find('TBOX01'.encode('utf-8'),fileBytes.find('TBOX01'.encode('utf-8'))+1)
                elif location.mapCheckID == 'TBOX03':
                    startOfChestArgs = fileBytes.rfind('TBOX01'.encode('utf-8'))
                else:
                    startOfChestArgs = fileBytes.find(location.mapCheckID.encode('utf-8'))
            else:
                startOfChestArgs = fileBytes.find(location.mapCheckID.encode('utf-8'))

            fileBytes = bytearray(fileBytes)

            #set Quantity
            fileBytes[startOfChestArgs + quantityOffset] = quantity

            #set Jingle sound effect
            fileBytes[startOfChestArgs + jingleOffset] = 0
   
            #place item as 2-byte little-endian int
            fileBytes[startOfChestArgs + itemIDOffset] = itemID & 0xFF
            fileBytes[startOfChestArgs + itemIDOffset + 1] = (itemID >> 8) & 0xFF
            buffer.close()

        #patch file
        with open(locFile,"wb") as buffer:
            buffer.write(fileBytes)
            buffer.close()
    
