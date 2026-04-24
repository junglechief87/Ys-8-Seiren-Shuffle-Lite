import csv
import os.path
import shared.classr as classr
import random
import math
from shared.functions import *  
from randomizer.crew import *
from randomizer.shuffle import *
from randomizer.gameStartFunctions import *
from patch.chestPatcher import *
from randomizer.audioShuffle import *
from patch.miscPatches import pastDanaFixes, randomizeOctoBosses, newExpMult
from randomizer.buildEntrances import *

#This is essentially the BnB for how this rando works. This script writes a big .scp file, the game's native scripting files, that we call for all randomized locations (as well as some other important functions for a rando)
#This takes in the game's shuffled list of loctions and then builds the scripts.
#We named our script file rng because we need something short, our script calls from the chests are limited to 8 characters so our standard format for script call is rng:(locID where locID is a 4 digit id).
#Plus rng.scp is a fitting filename for a rando.
patchFile = ''
scpIncludeList = ['#include "inc/mons.h"','#include "inc/def.h"','#include "inc/efx.h"','#include "inc/flag.h"','#include "inc/se.h"',
                  '#include "inc/scr_inc.h"','#include "inc/3dicon.h"','#include "inc/skilldef.h"','#include "inc/vo.h"','#include "inc/temp/rng.h"'] #standard set of header files used in most Ys 8 .scp files
genericMessage = " Obtained."
crewMessage = " joined the Village."
partyMessage = " joined the Party."
skillMessage = " has learned skill #2C"
landmarkMessage = ' discovered.'
treasureScript = {
"372": "mp6561:EvOpenTBox",
"358": "mp6554:EvOpenTBox",
"317": "mp6531m:EvOpenTBox",
"291": "mp6519:EvOpenTBox",
"288": "mp6513:EvOpenTBox",
"239": "mp6345:SubEV_05_Get_Bell_ED",
"19": "mp0408:EV_M05S152_ED",
"18": "mp0405:EV_M05S170_ED",
"13": "mp0404:EV_M05S150_ED",
"9": "mp0403:EV_M05S151_ED"
}

def rngPatcherMain(patch):
    global patchFile
    patchFile = ''
    rngScriptFile = getLocFile('rng','script')

    # if patch_file == 'Past Dana':
    #     global partyMessage 
    #     partyMessage = " joined the Village."
    #     pastDanaFixes(True)  
    # else:
    #     pastDanaFixes(False)

    #if patch_file:
    #    randomize_bgmtbl()
    #else:
    #    restore_original_bgm()

    for inc in scpIncludeList:
        patchFile = patchFile + inc + '\n'
    
    duplicateChests = [47,48,49,179]
    for location in patch.item_map:
        loc_data = patch.item_map[location]
        loc_id = int(location)
        if location not in duplicateChests: #no need to build out functions for the same location twice, these chests share flags with the not dawn version
            #cleanup the placeholders the game had for chests without scripts
            if location in treasureScript.keys():
                script = ('EventCue("' + treasureScript[location] + '")')
            else:
                script = ""
                
            # opening cutscene
            patchFile = patchFile + buildStartParameters(patch) 
            patchFile = patchFile + manageEarlyGameParty(patch)
            patchFile = patchFile + soloStartingCharacterEvent(patch)

            if loc_data.itemID == 139:#progressive shop rank
                patchFile = patchFile + shopUpgrades(loc_id, loc_data, script)
            elif loc_data.item_type == 'Item': 
                patchFile = patchFile + genericItemMessage(loc_id, patch, script)      
            elif loc_data.category == 'Crew':
                patchFile = patchFile + buildCrewLocation(loc_id, patch, script)
            elif 'Skill' in loc_data.category: #skills contain the character name in the category
                patchFile = patchFile + buildSkillLocation(loc_id, patch, script)
            elif loc_data.category == 'Landmark':
                patchFile = patchFile + buildLandmarks(loc_id, patch, script)

    bossScalingScript = bossScaling()
    patchFile = patchFile + bossScalingScript

    if patch.settings.options.final_boss_access == 2:
        patchFile = patchFile + buildPsyches(patch.item_map, patch.settings)
    if patch.settings.options.former_sanctuary_crypt == 1:
        patchFile = patchFile + buildFSCWarp()

    patchFile = patchFile + interceptionHandler(parameters)
    patchFile = patchFile + jewelTrade(shuffledLocations)
    patchFile = patchFile + talkHints(shuffledLocations)
    patchFile = patchFile + octusGoal(parameters)
    if parameters.openOctusPaths:
        patchFile = patchFile + octoBosses(parameters, finalNonGoalBossLevel)
    else:
        #this is to restore the original values
        randomizeOctoBosses(parameters)
    patchFile = patchFile + goal(parameters)
    patchFile = patchFile + endingHandler(parameters,finalNonGoalBossLevel)
    if parameters.entranceShuffle:
        patchFile = patchFile + buildEntrances()
    with open(rngScriptFile, 'w', encoding = 'Shift-JIS') as fileToPatch: #build the entire rng file from one big string
        fileToPatch.write(patchFile)
        fileToPatch.close()

    expMult(parameters)
    
    spoilerLog.flush()
    spoilerLog.close()

# ==========================================================================================================
# Generic Item Function
# ==========================================================================================================
#function used for all non-person item function generation
def genericItemMessage(location_id, patch, vanillaScript):
    options = patch.settings
    loc_data = patch.item_map[location_id]
    itemId = loc_data.item_id
    itemQuantity = loc_data.item_quantity

    itemIcon = getIcon(itemId)
    itemSE = 'ITEMMSG_SE_NORMAL' #Placeholder item jingles in chests
    scriptName = buildLocScripts(location_id,False)
    #'Maiden Journal','Blue Seal of Whirling Water','Green Seal of Roaring Stone','Golden Seal of Piercing Light','Treasure Chest Key','Frozen Flower','Shrine Maiden Amulate'
    danaPastEventsItems = [698,700,701,702,796,699,727]
    script = ""

    #unique item functions that will need additional scripting when the item is recieved
    if itemId == 739: #glow stone
        script = script + makeGlowStoneUseful()
    elif itemId in danaPastEventsItems:
        script = script + danaPastEvents(itemId)
    elif itemId == 9: #mistilteinn
        script = script + sopEvent(options)
        #this solution for unique message on the progressive weapons is a little heavy handed but it should resolves all issues I had with them
        if options.progressive_super_weapons == 1:
            if loc_data.location_type == 'event':   
                getItemFunction =  """
function "{0}"
{{
    GetItem(ICON3D_WP_ADOL_009,1) //rusty sword is the best representation of broken weapon I can think of
    GetItemMessageExPlus(-1,1,{1},"#2CBroken Mistilteinn#0C Obtained.",0,0)
    WaitPrompt()
    WaitCloseWindow()
    {2}
}}
"""  
            else:
                fillChest(location_id,146,itemQuantity)

                getItemFunction =  """
function "{0}"
{{
    SetStopFlag(STOPFLAG_TALK)
    {2}
    ResetStopFlag(STOPFLAG_TALK)
}}
""" 
            return getItemFunction.format(scriptName,itemSE,script)
        
    elif itemId == 13: #Spirit Ring Celesdia
        script = script + spiritRingEvent(options)
        if options.progressive_super_weapons == 1:
            if loc_data.location_type == 'event':   
                getItemFunction =  """
function "{0}"
{{
    GetItem(ICON3D_WP_ADOL_009,1) //rusty sword is the best representation of broken weapon I can think of
    GetItemMessageExPlus(-1,1,{1},"#2CBroken Spirit Ring#4C Obtained.",0,0)
    WaitPrompt()
    WaitCloseWindow()
    {2}
}}
"""  
            else:
                fillChest(location_id,147,itemQuantity)

                getItemFunction =  """
function "{0}"
{{
    SetStopFlag(STOPFLAG_TALK)
    {2}
    ResetStopFlag(STOPFLAG_TALK)
}}
""" 
            return getItemFunction.format(scriptName,itemSE,script)
    elif itemId == 149: # AP Item
        if loc_data.location_type == 'event':   
            getItemFunction =  """
function "{0}"
{{
    GetItemMessageExPlus(-1,1,{1},"Sent {3} to {4}.",0,0)
    WaitPrompt()
    WaitCloseWindow()
    {2}
}}
"""  
        else:
            fillChest(location_id,149,itemQuantity)
            getItemFunction =  """
function "{0}"
{{
    SetStopFlag(STOPFLAG_TALK)
    GetItemMessageExPlus(-1,1,{1},"Sent {3} to {4}.",0,0)
    WaitPrompt()
    WaitCloseWindow()
    {2}
    ResetStopFlag(STOPFLAG_TALK)
}}
""" 
        return getItemFunction.format(scriptName,itemSE,script,loc_data.item_name, loc_data.player)
    elif itemId == 770: #logbook from east coast cave
        script = script + pirateShipDocks()
    elif itemId in [760,761,762,763]: #T memos
        script = script + interceptUnlock()
    elif itemId == 629: #fishing rod
        startingBait = """
    GetItem(ICON3D_FISHBAIT_WORM,30)
    """
        script = script + startingBait
    elif itemId == 779: #ship blueprints
        buildBoat = """
    SetFlag(GF_SUBEV_06_1111_LOOK_BOAT,1)
    """
        script = script + buildBoat
    
    # if itemId in [750,751,752,753,754,755,760,761,762,763] and options.memo_hints:
    #     script = script + memoHints(itemId)
        
    message = genericMessage
    script =  script + vanillaScript #append the original chest scripts to the end of the function

    if itemId == 218:
        #Adding the other 2 medals to the slash medal check
        script =  script + """
    GetItem(ICON3D_AC_068,1)
    GetItem(ICON3D_AC_069,1)
            """ 
    if itemId == 206: #Jade pendant
        if options.former_sanctuary_crypt == 1:
            script = script + """
    SetFlag(SF_SYS_CLEARED, 1)
    SetFlag(GF_SUBEV_PAST_07_CLEAR, 1)
                """
    #if the location is not inside an event we want to freeze the player while they receive the item. This prevents some awkwardness, it's strictly for polish.
    #setting the talk flags and then unsetting them during events can break many events though, so we don't want to do it there. Many events already have these flags set at their starts and ends.
    if loc_data.location_type == 'event':   
        getItemFunction =  """
function "{0}"
{{
    GetItem({1},{2})
    GetItemMessageExPlus({1},{2},{3},"{4}",0,0)
    WaitPrompt()
    WaitCloseWindow()
    {5}
}}
"""  
    else:
        fillChest(location_id,itemId,itemQuantity)
        getItemFunction =  """
function "{0}"
{{
    SetStopFlag(STOPFLAG_TALK)
    {5}
    ResetStopFlag(STOPFLAG_TALK)
}}
"""
    if script == "" and location_id not in treasureScript.keys() and loc_data.location_type == 'chest':
        return # if there is not script and the location_id doesn't have a script in vanilla then we can just return nothing, no need to write a function that does nothing
    return getItemFunction.format(scriptName,itemIcon,itemQuantity,itemSE,message,script)

# ==========================================================================================================
# Crew Item Function
# ==========================================================================================================
#function used for all people function generations
def buildCrewLocation(location_id, patch, vanillaScript):
    options = patch.settings
    loc_data = patch.item_map[location_id]
    scriptName = buildLocScripts(location_id,False)
    itemIcon = -1
    itemID = 143
    itemQuantity = 1
    itemSE = 'ITEMMSG_SE_NORMAL' #Placeholder item jingles in chests

    if patch.party_flag:
        message = "#2C" + loc_data.item_name + "#4C" + partyMessage
    else:
        message = "#2C" + loc_data.item_name + "#4C" + crewMessage
        
    crewFlags = getCrewFlags(loc_data.item_name)

     #if the location is not inside an event we want to freeze the player while they receive the item. This prevents some awkwardness, it's strictly for polish.
     #setting the talk flags and then unsetting them during events can break many events though, so we don't want to do it there. Many events already have these flags set at their starts and ends.    
    if loc_data.location_type == 'event':
        getCrewFunction = """
function "{0}"
{{
    GetItem(ICON3D_143,1)  
    GetItemMessageExPlus({1},{2},{3},"{4}",0,0)
    WaitPrompt()
    WaitCloseWindow()
    {5}
    {6}
}}
"""
    else: 
        fillChest(location_id,itemID,1)
        getCrewFunction = """
function "{0}"
{{
    SetStopFlag(STOPFLAG_TALK)
    
    GetItemMessageExPlus({1},{2},{3},"{4}",0,0)
    WaitPrompt()
    WaitCloseWindow()
    {5}
    {6}
    ResetStopFlag(STOPFLAG_TALK)
}}
"""   
    return getCrewFunction.format(scriptName,itemIcon,itemQuantity,itemSE,message,crewFlags,vanillaScript)

# ==========================================================================================================
# Skill Item Function
# ==========================================================================================================
#now skills are in the rando and they need a third special handler for their locations
def buildSkillLocation(location_id, patch, vanillaScript):
    loc_data = patch.item_map[location_id]
    scriptName = buildLocScripts(location_id,False)
    itemIcon = -1
    itemID = 144
    itemQuantity = 1
    itemSE = 'ITEMMSG_SE_NORMAL'
    skillInfo = getSkillInfo(loc_data.item_name) #returns tuple: character,skill ID,character name
    character = skillInfo[0]
    skillID = skillInfo[1]
    characterName = skillInfo[2]
    message = "#4C" + characterName + skillMessage + loc_data.item_name + "#4C."

    if "Starting Skill" in loc_data.location_name: #for starting skills just go ahead and give the skill, don't bombard the player with messages each time they get a character.
        getSkillFunction = """
function "{0}"
{{
    GetSkill({6},{7},1)
}}
"""
    elif loc_data.location_type == 'event':
        getSkillFunction = """
function "{0}"
{{

    GetSkill({6},{7},1)
    GetItemMessageExPlus({1},{2},{3},"{4}",0,0)
    WaitPrompt()
    WaitCloseWindow()
    {5}
}}
"""
    else: 
         fillChest(location_id,itemID,1)
         getSkillFunction = """
function "{0}"
{{
    SetStopFlag(STOPFLAG_TALK)
    
    GetSkill({6},{7},1)
    GetItemMessageExPlus({1},{2},{3},"{4}",0,0)
    WaitPrompt()
    WaitCloseWindow()  
    {5}
    ResetStopFlag(STOPFLAG_TALK)
}}
"""  
    return getSkillFunction.format(scriptName,itemIcon,itemQuantity,itemSE,message,vanillaScript,character,skillID)

# ==========================================================================================================
# Landmark Function
# ==========================================================================================================
def buildLandmarks(location_id, patch, vanillaScript):
    loc_data = patch.item_map[location_id]
    scriptName = buildLocScripts(location_id, False)
    itemIcon = -1
    itemID = 148
    itemQuantity = 1
    itemSE = 'ITEMMSG_SE_NORMAL'
    message = "#2C" + loc_data.location_name + "#4C" + landmarkMessage

    landmarks = {
        'Birdsong Rock':            'GF_LOCATION01',
        'Cobalt Crag':              'GF_LOCATION02',
        'Rainbow Falls':            'GF_LOCATION03',
        'Metavolicalis':            'GF_LOCATION04',
        'Parasequoia':              'GF_LOCATION05',
        'Chimney Rock':             'GF_LOCATION08',
        'Indigo Mineral Vein':      'GF_LOCATION09',
        'Beached Remains':          'GF_LOCATION10',
        'Field of Medicinal Herbs': 'GF_LOCATION11',
        'Airs Cairn':               'GF_LOCATION13',
        'Zephyr Hill':              'GF_LOCATION16',
        'Lapis Mineral Vein':       'GF_LOCATION17',
        'Beehive':                  'GF_LOCATION19',
        'Ship Graveyard':           'GF_LOCATION21',
        'Hidden Pirate Storehouse': 'GF_LOCATION22',
        'Magna Carpa':              'GF_LOCATION23',
        'Prismatic Mineral Vein':   'GF_LOCATION24',
        'Unicalamites':             'GF_LOCATION25',
        'Breath Fountain':          'GF_LOCATION27',
        'Ancient Tree':             'GF_LOCATION28',
        'Sky Garden':               'GF_LOCATION32',
        'Soundless Hall':           'GF_LOCATION33',
        'Graves of Ancient Heroes': 'GF_LOCATION34',
        'Milky White Vein':         'GF_LOCATION18'
        }
    
    if loc_data.location_type == 'event':
        getLandmarkFunction = """
function "{0}"
{{
    
    GetItemMessageExPlus({1},{2},{3},"{4}",0,0)
    WaitPrompt()
    WaitCloseWindow()
    SetFlag({5},1)
    {6}
}}
"""
    else: 
        fillChest(location_id,itemID,1)
        getLandmarkFunction = """
function "{0}"
{{
    SetStopFlag(STOPFLAG_TALK)
    
    GetItemMessageExPlus({1},{2},{3},"{4}",0,0)
    WaitPrompt()
    WaitCloseWindow()
    SetFlag({5},1)
    {6}
    ResetStopFlag(STOPFLAG_TALK)
}}
"""   
    return getLandmarkFunction.format(scriptName,itemIcon,itemQuantity,itemSE,message,landmarks[loc_data.location_name],vanillaScript)

# ==========================================================================================================
# Boss Scaling Function
# ==========================================================================================================
def bossScaling():
    return "function \"bossScaling\"\n{\n\t//placeholder to keep existing build functioning until features are implemented\n}\n"
#     bossLevels = [5,7,13,14,20,23,26,28,29,32,35,40,43,45,48,51,53,58,60,60,80]
#     bossIDs = {'Byfteriza': 'M0111',
#                'Avalodragil': 'B150',
#                'Serpentus': 'B100',
#                'Clareon': 'B000',
#                'Lonbrigius': 'B101B',
#                'Gargantula': 'B001',
#                'Magamandra': 'B102',
#                'Laspisus': 'B002',
#                'Kiergaard Weissman': 'B152',
#                'Avalodragil 2': 'B154',
#                'Giasburn': 'B003',
#                'Brachion': 'B006',
#                'Exmetal': 'B104',
#                'Carveros': 'B004',
#                'Pirate Revenant': 'B103',
#                'Coelacantos': 'B106',
#                'Oceanus': 'B007',
#                'Doxa Griel': 'B105',
#                'Basileus': 'B005',
#                'Mephorash': 'B153',
#                'Silvia': 'B155',}
#     remainingBosses = []
#     finalBossLevels = []
#     bossLevelsDictByRegion = {}
#     HPmod = 0.5
#     firstPostSecondCharacterBoss = ''
#     partySize = 0
#     secondCharacterSphere = 0
#     soloPartyBoss = True
#     secondCharacterFound = False

#     if not parameters.goal == 'Untouchable' and parameters.formerSanctuaryCrypt: # Make sure Melaiduma's level and ID are in the pool if he's not the goal
#         bossLevels.append(99) 
#         bossIDs['Melaiduma'] = 'B170' 

#     if not parameters.goal == 'Release the Psyches': # Make sure the Psyches' levels and IDs are in the pool if they aren't the goal
#         bossLevels.extend([67,70,73,75])
#         bossIDs['Psyche-Hydra'] = 'B112'
#         bossIDs['Psyche-Minos'] = 'B110'
#         bossIDs['Psyche-Nestor'] = 'B111'
#         bossIDs['Psyche-Ura'] = 'B008'

#     for location in playthroughAllProgression.locations:
#         if location.party:
#             partySize += 1
#             if partySize >= 2:
#                 secondCharacterSphere = location.sphere
#                 secondCharacterFound = True
#                 print('Second character joins in sphere: ' + str(secondCharacterSphere))
#                 print(location.itemName)
#                 break

#     for location in playthroughAllProgression.locations:
#         if location.mapCheckID in bossIDs.keys() and location.sphere >= secondCharacterSphere and secondCharacterFound:
#             firstPostSecondCharacterBoss = bossIDs.get(location.mapCheckID)
#             break
                


#     # build out a list of IDs for us to track what bosses aren't in the pool
#     for boss in bossIDs.keys():
#         remainingBosses.append(bossIDs.get(boss))

#     random.seed(parameters.seed)
#     spoilerLog.write(f'\n'
#                      f'Boss Levels:\n')   
#     # process bosses that are accessible before the goal in the seed and assign them levels in ascending order as the playthrough should have them in order
#     for boss in playthroughAllProgression.bosses:
#         if boss.mapCheckID in bossIDs.keys():
#             bossID = bossIDs.get(boss.mapCheckID)
#             bossLevel = bossLevels.pop(0)
#             finalNonGoalBossLevel = random.randrange(bossLevel-2,bossLevel+2)
#             finalBossLevels.append([remainingBosses.pop(remainingBosses.index(bossID)),random.randrange(bossLevel-2,bossLevel+2)])
#             spoilerLog.write(f'\tBoss: {boss.mapCheckID} - Level {finalBossLevels[-1][1]}\n')

#             if boss.mapCheckID in ['Clareon','Gargantula','Laspisus','Giasburn','Brachion','Carveros','Pirate Revenant','Oceanus','Basileus','Mephorash']:  #only bosses with psyches flags 
#                 bossLevelsDictByRegion[boss.locRegion] = finalBossLevels[-1][1] #storing this for use with psyches
#         elif boss.mapCheckID == 'Gilkyra Encounter':
#             finalBossLevels.append(['M0902', max(random.randrange(bossLevel-4,bossLevel+4), 5)])
    
#     # bosses post goal have their levels shuffled from among the remaining levels in the boss level pool
#     random.shuffle(bossLevels)
#     for bossID in remainingBosses:
#         bossLevel = bossLevels.pop(0)
#         finalBossLevels.append([bossID,random.randrange(bossLevel-2,bossLevel+2)])
#         bossName = [name for name, id in bossIDs.items() if id == bossID][0]
#         spoilerLog.write(f'\tBoss: {bossName} - Level {finalBossLevels[-1][1]}\n')

#     fscBosses = ''
#     fscBossesHP = ''
#     script = '\tfunction "bossScaling"\n\t{\n'
#     for boss in finalBossLevels:
#         script = script + '\t\tSetChrWorkGroup(' + boss[0] + ', CWK_LV, ' + str(boss[1]) + ')\n'

#         #balance decision to lower boss HP if there are any bosses before party join, some fights are super tedious in early game if they show up and it's more punishing to lose them than we want for game pacing. 
#         if firstPostSecondCharacterBoss == boss[0]:
#             soloPartyBoss = False

#         if soloPartyBoss and parameters.charMode != 'Past Dana':
#             if boss[0] == 'M0111':
#                 script = script + '\t\tSetChrWork("tu_m0111_01", CWK_MAXHP, (tu_m0111_01.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
#                 script = script + '\t\tSetChrWork("tu_m0111_01", CWK_HP, (tu_m0111_01.CHRWORK[CWK_MAXHP]))\n'
#             elif boss[0] == 'B101B':
#                 script = script + '\t\tSetChrWork("b101a", CWK_MAXHP, (b101a.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
#                 script = script + '\t\tSetChrWork("b101a", CWK_HP, (b101a.CHRWORK[CWK_MAXHP]))\n'
#                 script = script + '\t\tSetChrWork("b101b", CWK_MAXHP, (b101b.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
#                 script = script + '\t\tSetChrWork("b101b", CWK_HP, (b101b.CHRWORK[CWK_MAXHP]))\n'
#                 script = script + '\t\tSetChrWork("b101c", CWK_MAXHP, (b101c.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
#                 script = script + '\t\tSetChrWork("b101c", CWK_HP, (b101c.CHRWORK[CWK_MAXHP]))\n'
#                 script = script + '\t\tSetChrWork("b101d", CWK_MAXHP, (b101d.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
#                 script = script + '\t\tSetChrWork("b101d", CWK_HP, (b101d.CHRWORK[CWK_MAXHP]))\n'
#                 script = script + '\t\tSetChrWork("b101", CWK_MAXHP, (b101.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
#                 script = script + '\t\tSetChrWork("b101", CWK_HP, (b101.CHRWORK[CWK_MAXHP]))\n'
#             elif boss[0] in ['B150','B100']:
#                 script = script + '\t\tSetChrWorkGroup(' + boss[0] + ', CWK_MAXHP, (' + boss[0] + '.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
#                 script = script + '\t\tSetChrWorkGroup(' + boss[0] + ', CWK_HP, (' + boss[0] + '.CHRWORK[CWK_MAXHP]))\n'
#             else:
#                 script = script + '\t\tSetChrWork("' + boss[0].lower() + '", CWK_MAXHP, (' + boss[0].lower() + '.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
#                 script = script + '\t\tSetChrWork("' + boss[0].lower() + '", CWK_HP, (' + boss[0].lower() + '.CHRWORK[CWK_MAXHP]))\n'
                

#             #handling special cases for bosses with forms or minions
#             if boss[0] == 'B005':
#                 script = script + '\t\tSetChrWorkGroup(M0644, CWK_MAXHP, (M0644.CHRWORK[CWK_MAXHP] *' + str(HPmod) + '))\n'
#                 script = script + '\t\tSetChrWorkGroup(M0644, CWK_HP, (M0644.CHRWORK[CWK_MAXHP]))\n'
#                 script = script + '\t\tSetChrWorkGroup(M0643, CWK_MAXHP, (M0643.CHRWORK[CWK_MAXHP] *' + str(HPmod) + '))\n' #if you can beat these enemies you can reach basileus so scale them too; this is the force garmr required to beat to reach basileus
#                 script = script + '\t\tSetChrWorkGroup(M0643, CWK_HP, (M0643.CHRWORK[CWK_MAXHP]))\n'
#             if boss[0] == 'B170': 
#                 fscBossesHP = (
#                             f'\t\tSetChrWorkGroup(B103,	CWK_MAXHP,	(B103.CHRWORK[CWK_MAXHP] * ' + str(HPmod) + '))\n'
#                             f'\t\tSetChrWorkGroup(B103,	CWK_HP,	(B103.CHRWORK[CWK_MAXHP]))\n'
#                             f'\t\tSetChrWorkGroup(B006,	CWK_MAXHP,	(B006.CHRWORK[CWK_MAXHP] * ' + str(HPmod) + '))\n'
#                             f'\t\tSetChrWorkGroup(B006,	CWK_HP,	(B006.CHRWORK[CWK_MAXHP]))\n'
#                             f'\t\tSetChrWorkGroup(B001,	CWK_MAXHP,	(B001.CHRWORK[CWK_MAXHP] * ' + str(HPmod) + '))\n'
#                             f'\t\tSetChrWorkGroup(B001,	CWK_HP,	(B001.CHRWORK[CWK_MAXHP]))\n'
#                             f'\t\tSetChrWorkGroup(B105,	CWK_MAXHP,	(B105.CHRWORK[CWK_MAXHP] * ' + str(HPmod) + '))\n'
#                             f'\t\tSetChrWorkGroup(B105,	CWK_HP,	(B105.CHRWORK[CWK_MAXHP]))\n'
#                             f'\t\tSetChrWorkGroup(B161,	CWK_MAXHP,	(B161.CHRWORK[CWK_MAXHP] * ' + str(HPmod) + '))\n'
#                             f'\t\tSetChrWorkGroup(B161,	CWK_HP,	(B161.CHRWORK[CWK_MAXHP]))\n'
#                             )
    
#         #handling special cases for bosses with forms or minions
#         if boss[0] == 'B005':
#             script = script + '\t\tSetChrWorkGroup(M0644, CWK_LV, ' + str(boss[1]) + ')\n'
#             script = script + '\t\tSetChrWorkGroup(M0643, CWK_LV, ' + str(boss[1]-1) + ')\n' #if you can beat these enemies you can reach basileus so scale them too
#         if boss[0] == 'B101B':
#             script = script + '\t\tSetChrWorkGroup(B101, CWK_LV, ' + str(boss[1]) + ')\n'
#         if boss[0] == 'B170': # set FSC bosses relative to Melaiduma if Melaiduma is scaled
#             fscBosses = (f'\n\tfunction "fscBosses"\n'
#                          f'\t{{\n'
#                          f'\t\tSetChrWorkGroup(B103,	CWK_LV,	' + str(max(1,boss[1]-10)) + ')\n'
#                          f'\t\tSetChrWorkGroup(B006,	CWK_LV,	' + str(max(1,boss[1]-12)) + ')\n'
#                          f'\t\tSetChrWorkGroup(B001,	CWK_LV,	' + str(max(1,boss[1]-14)) + ')\n'
#                          f'\t\tSetChrWorkGroup(B105,	CWK_LV,	' + str(max(1,boss[1]-16)) + ')\n'
#                          f'\t\tSetChrWorkGroup(B161,	CWK_LV,	' + str(max(1,boss[1]-18)) + ')\n'
#                          f'\n' + fscBossesHP + '\n'
#                          f'\t}}\n')
                        
#     script = script + '\t}'

#     return script + fscBosses, finalNonGoalBossLevel, bossLevelsDictByRegion
# def memoHints(itemID):
#     match itemID:
#         case 750:
#             return "\n\t\tSetFlag(GF_SUBEV_GET_MEMO_P_01,1)\n"
#         case 751:
#             return "\n\t\tSetFlag(GF_SUBEV_GET_MEMO_P_02,1)\n"
#         case 752:
#             return "\n\t\tSetFlag(GF_SUBEV_GET_MEMO_P_03,1)\n"
#         case 753:
#             return "\n\t\tSetFlag(GF_SUBEV_GET_MEMO_P_04,1)\n"
#         case 754:
#             return "\n\t\tSetFlag(GF_SUBEV_GET_MEMO_P_05,1)\n"
#         case 755:
#             return "\n\t\tSetFlag(GF_SUBEV_GET_MEMO_P_06,1)\n"
#         case 760:
#             return "\n\t\tSetFlag(GF_SUBEV_GET_MEMO_T_01,1)\n"
#         case 761:
#             return "\n\t\tSetFlag(GF_SUBEV_GET_MEMO_T_02,1)\n"
#         case 762:
#             return "\n\t\tSetFlag(GF_SUBEV_GET_MEMO_T_03,1)\n"
#         case 763:
#             return "\n\t\tSetFlag(GF_SUBEV_GET_MEMO_T_04,1)\n"

# ==========================================================================================================
#  Psyche Checkpoint Function
# ==========================================================================================================
#GF_TBOX_DUMMY112 is our flag for release the psyches so these won't get called outside this game mode.
#New version of this script hacks the checkpoint in Castaway Village and uses the boss flags for activation of the custom shop
#The boss menu is essentially a custom shop, it uses Dina's jewel trade menu as a base, there are two version of it depending on game mode
def buildPsyches(locations, options):
    # region: boss flag for region
    bossFlagDict = {'Silent Tower': 'FLAG[GF_SUBEV_06_6413_KILL_BOSS]',
                    'Octus Overlook': 'FLAG[GF_TBOX_DUMMY161]',
                    'Valley of Kings': 'FLAG[GF_TBOX_DUMMY080]',
                    'Archeozoic Chasm': 'FLAG[GF_TBOX_DUMMY078]',
                    'Pirate Ship Eleftheria': 'FLAG[GF_05MP0405_READ_REED]',
                    'Baja Tower': 'FLAG[GF_05MP6329_KILL_BAHABOSS]',
                    'Temple of the Great Tree': 'FLAG[GF_04MP6410_KILL_GUARDIAN]',
                    'Mont Gendarme': 'FLAG[GF_03MP4341_KILL_ANCIENT]',
                    'Schlamm Jungle': 'FLAG[GF_02MP2308_KILL_HIPPO]',
                    'Eroded Valley': 'FLAG[GF_TBOX_DUMMY074]',
                    'Towering Coral Forest': 'FLAG[GF_02MP1308_KILL_CHAMELEON]',
                    'Former Sanctuary Crypt - Final Floor': 'FLAG[GF_SUBEV_UNTOUCHABLE]'}
    #Boss name: load boss map script, boss event, boss map id, boss character id
    bossCue = {'Hydra': ['LoadArg("map/mp6305b/mp6305b.arg")', 'EventCue("mp6305b:EV_RetryBoss")', 'MN_D_MP6305b', 'B112'],
               'Minos': ['LoadArg("map/mp6306b/mp6306b.arg")', 'EventCue("mp6306b:EV_RetryBoss")', 'MN_D_MP6306b', 'B110'],
               'Nestor': ['LoadArg("map/mp6307b/mp6307b.arg")', 'EventCue("mp6307b:EV_RetryBoss")', 'MN_D_MP6307b', 'B111'],
               'Ura': ['LoadArg("map/mp6308b/mp6308b.arg")', 'EventCue("mp6308b:EV_RetryBoss")', 'MN_D_MP6308b', 'B008'],
               'Le-Erythros': ['LoadArg("map/mp6409b/mp6409b.arg")', 'EventCue("mp6409b:EV_RetryBoss")', 'MN_D_MP6409B', 'B012'],
               'Grazios': ['LoadArg("map/mp6519m/mp6519m.arg")', 'EventCue("mp6519m:EV_RetryBoss")', 'MN_D_MP6519M','B161'],
               'Nebritia': ['LoadArg("map/mp6529m/mp6529m.arg")', 'EventCue("mp6529m:EV_RetryBoss")', 'MN_D_MP6529M','B162'],
               'Argura': ['LoadArg("map/mp6539m/mp6539m.arg")', 'EventCue("mp6539m:EV_RetryBoss")', 'MN_D_MP6539M', 'B163'],
               'Crusos': ['LoadArg("map/mp6549m/mp6549m.arg")', 'EventCue("mp6549m:EV_RetryBoss")', 'MN_D_MP6549M', 'B011'],
               'Blasphima': ['LoadArg("map/mp6559m/mp6559m.arg")', 'EventCue("mp6559m:EV_RetryBoss")', 'MN_D_MP6559M', 'B164'],
               'Le-Kyanos': ['LoadArg("map/mp6204m/mp6204m.arg")', 'EventCue("mp6204m:EV_Boss_Jump")', 'MN_F_MP6204M', 'B165'],
               'Melaiduma': ['LoadArg("map/mp6569/mp6569.arg")', 'EventCue("mp6569:EV_RetryBoss")', 'MN_D_MP6569', 'B170']
        }
    
    # if options.charMode == 'Past Dana':
    #     bossPool = ['Grazios','Nebritia','Argura','Crusos','Blasphima','Le-Kyanos']
    # else:
    #     bossPool = ['Hydra','Minos','Nestor','Ura','Le-Erythros']

    bossPool = ['Hydra','Minos','Nestor','Ura','Le-Erythros']

    if options.former_sanctuary_crypt == 0:
        bossPool.append('Melaiduma')
        
    random.shuffle(bossPool)

    for location in shuffledLocations:
        if location.itemName == 'Psyches of the Sky Era\Braziers Fight(DANA)':
            bossFight1 = bossFlagDict[location.locRegion]
            bossLoc1 = location.locRegion
        if location.itemName == 'Psyches of the Insectoid Era\Stone Fight(DANA)':
            bossFight2 = bossFlagDict[location.locRegion]
            bossLoc2 = location.locRegion
        if location.itemName == 'Psyches of the Frozen Era\Clairvoyance Fight(DANA)':
            bossFight3 = bossFlagDict[location.locRegion]
            bossLoc3 = location.locRegion
        if location.itemName == 'Psyches of the Ocean Era\Frost Fight(DANA)':
            bossFight4 = bossFlagDict[location.locRegion]
            bossLoc4 = location.locRegion
        if location.itemName == 'Empty Psyches\Magma Fight(DANA)':
            bossFight5 = bossFlagDict[location.locRegion]
            bossLoc5 = location.locRegion

    wardenScaling = """
        SetChrWork("b012", CWK_MAXHP, (b012.CHRWORK[CWK_MAXHP] * 3.0f))
        SetChrWork("b012", CWK_HP, (b012.CHRWORK[CWK_MAXHP]))
"""

    danaWardenIncrease = 5
    danaModerateWardenIncrease = 2
    normalWardenIncrease = 10
    moderateWardenIncrease = 5

    if parameters.charMode == 'Past Dana':
        
        try:
            warden1Level = bossLevelsDictByRegion[bossLoc1] + danaWardenIncrease
        except:
            warden1Level = finalNonGoalBossLevel + danaModerateWardenIncrease
        try:
            warden2Level = bossLevelsDictByRegion[bossLoc2] + danaWardenIncrease
        except:
            warden2Level = finalNonGoalBossLevel + danaModerateWardenIncrease
        try:
            warden3Level = bossLevelsDictByRegion[bossLoc3] + danaWardenIncrease
        except:
            warden3Level = finalNonGoalBossLevel + danaModerateWardenIncrease
        try:
            warden4Level = bossLevelsDictByRegion[bossLoc4] + danaWardenIncrease
        except:
            warden4Level = finalNonGoalBossLevel + danaModerateWardenIncrease
        try:
            warden5Level = bossLevelsDictByRegion[bossLoc5] + danaWardenIncrease
        except:
            warden5Level = finalNonGoalBossLevel + danaModerateWardenIncrease
    else:
        

        try:
            warden1Level = bossLevelsDictByRegion[bossLoc1] + normalWardenIncrease
        except:
            warden1Level = finalNonGoalBossLevel + moderateWardenIncrease
        try:
            warden2Level = bossLevelsDictByRegion[bossLoc2] + normalWardenIncrease
        except:
            warden2Level = finalNonGoalBossLevel + moderateWardenIncrease
        try:
            warden3Level = bossLevelsDictByRegion[bossLoc3] + normalWardenIncrease
        except:
            warden3Level = finalNonGoalBossLevel + moderateWardenIncrease
        try:
            warden4Level = bossLevelsDictByRegion[bossLoc4] + normalWardenIncrease
        except:
            warden4Level = finalNonGoalBossLevel + moderateWardenIncrease

    spoilerLog.write('\nPsyches Boss Assignments:\n')
    spoilerLog.write('\tPsyches of the Sky Era\Braziers Fight(DANA) Region: ' + bossLoc1 + " Warden:" + bossPool[0] + " Level:" + str(warden1Level) + '\n')
    spoilerLog.write('\tPsyches of the Insectoid Era\Stone Fight(DANA) Region: ' + bossLoc2 + " Warden:" + bossPool[1] + " Level:" + str(warden2Level) + '\n')
    spoilerLog.write('\tPsyches of the Frozen Era\Clairvoyance Fight(DANA) Region: ' + bossLoc3 + " Warden:" + bossPool[2] + " Level:" + str(warden3Level) + '\n')
    spoilerLog.write('\tPsyches of the Ocean Era\Frost Fight(DANA) Region: ' + bossLoc4 + " Warden:" + bossPool[3] + " Level:" + str(warden4Level) + '\n')
    if parameters.charMode == 'Past Dana':
        spoilerLog.write('\tEmpty Psyches\Magma Fight(DANA) Region: ' + bossLoc5 + " Warden:" + bossPool[4] + " Level:" + str(warden5Level) + '\n')

    wardenScaling = wardenScaling + '\t\tSetChrWorkGroup(' + bossCue[bossPool[0]][3] + ', CWK_LV, ' + str(warden1Level) + ')\n'
    if bossPool[0] == 'Ura': wardenScaling = wardenScaling + '\t\tSetChrWorkGroup(B008BIT, CWK_LV, ' + str(warden1Level) + ')\n'

    wardenScaling = wardenScaling + '\t\tSetChrWorkGroup(' + bossCue[bossPool[1]][3] + ', CWK_LV, ' + str(warden2Level) + ')\n'
    if bossPool[1] == 'Ura': wardenScaling = wardenScaling + '\t\tSetChrWorkGroup(B008BIT, CWK_LV, ' + str(warden2Level) + ')\n'
    
    wardenScaling = wardenScaling + '\t\tSetChrWorkGroup(' + bossCue[bossPool[2]][3] + ', CWK_LV, ' + str(warden3Level) + ')\n'
    if bossPool[2] == 'Ura': wardenScaling = wardenScaling + '\t\tSetChrWorkGroup(B008BIT, CWK_LV, ' + str(warden3Level) + ')\n'

    wardenScaling = wardenScaling + '\t\tSetChrWorkGroup(' + bossCue[bossPool[3]][3] + ', CWK_LV, ' + str(warden4Level) + ')\n'
    if bossPool[3] == 'Ura': wardenScaling = wardenScaling + '\t\tSetChrWorkGroup(B008BIT, CWK_LV, ' + str(warden4Level) + ')\n'

    if parameters.charMode == 'Past Dana':
        wardenScaling = wardenScaling + '\t\tSetChrWorkGroup(' + bossCue[bossPool[4]][3] + ', CWK_LV, ' + str(warden5Level) + ')\n'
        if bossPool[4] == 'Ura': wardenScaling = wardenScaling + '\t\tSetChrWorkGroup(B008BIT, CWK_LV, ' + str(warden5Level) + ')\n'

    ### Past Dana Mode Bosses
    if parameters.charMode == 'Past Dana':
        bossCheckpoint = """
    function "bossCheckpoint"
    {{
        SetStopFlag(STOPFLAG_TALK)
        
        SetFlag(TF_MENU_SELECT2, 0)
        MenuReset()
        MenuType(MENUTYPE_POPUP)
        
        //--------------------------------------------------------------------------------------

        if({0} && !FLAG[GF_SUBEV_PAST_02_BOSS])
        {{
            MenuAdd(10, "#2C{5}: Chamber of Braziers Guardian ({10})")	
        }}
        else if(!{0} || FLAG[GF_SUBEV_PAST_02_BOSS])
        {{
            MenuAdd(11, "{5}: Chamber of Braziers Guardian({10})")	
        }}

        if({1} && !FLAG[GF_SUBEV_PAST_BOSS_B2])	
        {{
            MenuAdd(20, "#2C{6}: Chamber of Stone Guardian({11})")	
        }}
        else if(!{1} || FLAG[GF_SUBEV_PAST_BOSS_B2])
        {{
            MenuAdd(21, "{6}: Chamber of Stone Guardian({11})")	
        }}
        
        if({2} && !FLAG[GF_SUBEV_PAST_BOSS_B3])	
        {{
            MenuAdd(30, "#2C{7}: Chamber of Clairvoyance Guardian({12})")	
        }}
        else if(!{2} || FLAG[GF_SUBEV_PAST_BOSS_B3])
        {{
            MenuAdd(31, "{7}: Chamber of Clairvoyance Guardian({12})")	
        }}

        if({3} && !FLAG[GF_SUBEV_PAST_BOSS_B4])	
        {{
            MenuAdd(40, "#2C{8}: Chamber of Frost Guardian({13})")	
        }}
        else if(!{3} || FLAG[GF_SUBEV_PAST_BOSS_B4])
        {{
            MenuAdd(41, "{8}: Chamber of Frost Guardian({13})")	
        }}		

        if({4} && !FLAG[GF_SUBEV_PAST_BOSS_B5])	
        {{
            MenuAdd(50, "#2C{9}: Chamber of Magma Guardian({14})")	
        }}
        else if(!{4} || FLAG[GF_SUBEV_PAST_BOSS_B5])
        {{
            MenuAdd(51, "{9}: Chamber of Magma Guardian({14})")	
        }}			
        //--------------------------------------------------------------------------------------
        

        MenuEnable( 11, 0)
        MenuEnable( 21, 0)
        MenuEnable( 31, 0)
        MenuEnable( 41, 0)
        MenuEnable( 51, 0)

        MenuOpen( TF_MENU_SELECT2 , 283 , ADOLMENU_PPOSY , -2 , -2 , 10 , 1)
        WaitMenu(0)
        CloseMessage(6,0)
        WaitCloseMessage(6)
        MenuClose(10, 0)
        
        if(FLAG[TF_MENU_SELECT2] == 10)
        {{
            MenuClose(10, 0)
            SetFlag(GF_TBOX_DUMMY127,1)
            GetItem(ICON3D_831,1)
            SetFlag(SF_PAST_MODE, 1)
            {15}
            {16}
            //FadeIn(FADE_BLACK,FADE_NORMAL)
            WaitFade()
        }}
        else if(FLAG[TF_MENU_SELECT2] == 20)
        {{
            MenuClose(10, 0)
            SetFlag(GF_TBOX_DUMMY127,1)
            GetItem(ICON3D_831,1)
            SetFlag(SF_PAST_MODE, 1)
            {17}
            {18}
            //FadeIn(FADE_BLACK,FADE_NORMAL)
            WaitFade()
        }}
        else if(FLAG[TF_MENU_SELECT2] == 30)
        {{
            MenuClose(10, 0)
            SetFlag(GF_TBOX_DUMMY127,1)
            GetItem(ICON3D_831,1)
            SetFlag(SF_PAST_MODE, 1)
            {19}
            {20}
            //FadeIn(FADE_BLACK,FADE_NORMAL)
            WaitFade()
        }}
        else if(FLAG[TF_MENU_SELECT2] == 40)
        {{
            MenuClose(10, 0)
            SetFlag(GF_TBOX_DUMMY127,1)
            GetItem(ICON3D_831,1)
            SetFlag(SF_PAST_MODE, 1)
            {21}
            {22}
            //FadeIn(FADE_BLACK,FADE_NORMAL)
            WaitFade() 
        }}
        else if(FLAG[TF_MENU_SELECT2] == 50)
        {{
            MenuClose(10, 0)
            SetFlag(GF_TBOX_DUMMY127,1)
            GetItem(ICON3D_831,1)
            SetFlag(SF_PAST_MODE, 1)
            {23}
            {24}
            //FadeIn(FADE_BLACK,FADE_NORMAL)
            WaitFade()
        }}
        ResetStopFlag(STOPFLAG_TALK)
    
    }}

    function "wardenScaling"
    {{
        {26} 
    }}
    
    {25}

"""
        bossReturn = """
        function "bossReturn"
        {{
            SetFlag( SF_BOSS_BATTLE, 0 )
            if(WORK[WK_MAPNAMENO] == {0})
            {{
                SetFlag(GF_SUBEV_PAST_02_BOSS,1)
                LoadArg("map/mp1201/mp1201.arg")
		        EventCue("mp1201:EV_M01S080_ED")
            }}
            else if(WORK[WK_MAPNAMENO] == {1})
            {{
                SetFlag(GF_SUBEV_PAST_BOSS_B2,1)
                LoadArg("map/mp1201/mp1201.arg")
		        EventCue("mp1201:EV_M01S080_ED")
            }}
            else if(WORK[WK_MAPNAMENO] == {2})
            {{
                SetFlag(GF_SUBEV_PAST_BOSS_B3,1)
                LoadArg("map/mp1201/mp1201.arg")
		        EventCue("mp1201:EV_M01S080_ED")
            }}
            else if(WORK[WK_MAPNAMENO] == {3})
            {{
                SetFlag(GF_SUBEV_PAST_BOSS_B4,1)
                LoadArg("map/mp1201/mp1201.arg")
		        EventCue("mp1201:EV_M01S080_ED")
            }}
            else if(WORK[WK_MAPNAMENO] == {4})
            {{
                SetFlag(GF_SUBEV_PAST_BOSS_B5,1)
                LoadArg("map/mp1201/mp1201.arg")
		        EventCue("mp1201:EV_M01S080_ED")
            }}  
        }}
"""
        bossReturn = bossReturn.format(bossCue[bossPool[0]][2], bossCue[bossPool[1]][2], bossCue[bossPool[2]][2], bossCue[bossPool[3]][2], bossCue[bossPool[4]][2])

        return bossCheckpoint.format(bossFight1,bossFight2,bossFight3,bossFight4,bossFight5,
                                     bossLoc1,bossLoc2,bossLoc3,bossLoc4,bossLoc5,
                                     bossPool[0],bossPool[1],bossPool[2],bossPool[3],bossPool[4],
                                     bossCue[bossPool[0]][0],bossCue[bossPool[0]][1],bossCue[bossPool[1]][0],bossCue[bossPool[1]][1],
                                     bossCue[bossPool[2]][0],bossCue[bossPool[2]][1],bossCue[bossPool[3]][0],bossCue[bossPool[3]][1],
                                     bossCue[bossPool[4]][0],bossCue[bossPool[4]][1],
                                     bossReturn,wardenScaling)
    
    #### Standard Mode

    bossCheckpoint = """
    function "bossCheckpoint"
    {{
        SetStopFlag(STOPFLAG_TALK)
        
        SetFlag(TF_MENU_SELECT2, 0)
        MenuReset()
        MenuType(MENUTYPE_POPUP)
        
        //--------------------------------------------------------------------------------------

        if({0} && !FLAG[GF_06MP6305_TALK_HYDRA])
        {{
            MenuAdd(10, "#2C{4}: Ocean Warden({9})")	
        }}
        else if(!{0} || FLAG[GF_06MP6305_TALK_HYDRA])
        {{
            MenuAdd(11, "{4}: Ocean Warden({9})")	
        }}

        if({1} && !FLAG[GF_06MP6306_TALK_MINOS])	
        {{
            MenuAdd(20, "#2C{5}: Frost Warden({10})")	
        }}
        else if(!{1} || FLAG[GF_06MP6306_TALK_MINOS])
        {{
            MenuAdd(21, "{5}: Frost Warden({10})")	
        }}
        
        if({2} && !FLAG[GF_06MP6307_TALK_NESTOR])	
        {{
            MenuAdd(30, "#2C{6}: Insect Warden({11})")	
        }}
        else if(!{2} || FLAG[GF_06MP6307_TALK_NESTOR])
        {{
            MenuAdd(31, "{6}: Insect Warden({11})")	
        }}

        if({3} && !FLAG[GF_06MP6308_TALK_SARAI])	
        {{
            MenuAdd(40, "#2C{7}: Sky Warden({12})")	
        }}
        else if(!{3} || FLAG[GF_06MP6308_TALK_SARAI])
        {{
            MenuAdd(41, "{7}: Sky Warden({12})")	
        }}			
        //--------------------------------------------------------------------------------------
        

        MenuEnable( 11, 0)
        MenuEnable( 21, 0)
        MenuEnable( 31, 0)
        MenuEnable( 41, 0)

        MenuOpen( TF_MENU_SELECT2 , 283 , ADOLMENU_PPOSY , -2 , -2 , 10 , 1)
        WaitMenu(0)
        CloseMessage(6,0)
        WaitCloseMessage(6)
        MenuClose(10, 0)
        
        if(FLAG[TF_MENU_SELECT2] == 10)
        {{
            MenuClose(10, 0)
            SetFlag(GF_TBOX_DUMMY127,1)
            GetItem(ICON3D_831,1)
            {13}
            {14}
            //FadeIn(FADE_BLACK,FADE_NORMAL)
            WaitFade()
        }}
        else if(FLAG[TF_MENU_SELECT2] == 20)
        {{
            MenuClose(10, 0)
            SetFlag(GF_TBOX_DUMMY127,1)
            GetItem(ICON3D_831,1)
            {15}
            {16}
            //FadeIn(FADE_BLACK,FADE_NORMAL)
            WaitFade()
        }}
        else if(FLAG[TF_MENU_SELECT2] == 30)
        {{
            MenuClose(10, 0)
            SetFlag(GF_TBOX_DUMMY127,1)
            GetItem(ICON3D_831,1)
            {17}
            {18}
            //FadeIn(FADE_BLACK,FADE_NORMAL)
            WaitFade()  
        }}
        else if(FLAG[TF_MENU_SELECT2] == 40)
        {{
            MenuClose(10, 0)
            SetFlag(GF_TBOX_DUMMY127,1)
            GetItem(ICON3D_831,1)
            {19}
            {20}
            //FadeIn(FADE_BLACK,FADE_NORMAL)
            WaitFade()  
        }}
        ResetStopFlag(STOPFLAG_TALK)
    
    }}
    
    function "wardenScaling"
    {{
        {8} 
    }}

    {21}
"""
    bossReturn = """
        function "bossReturn"
        {{
            SetFlag( SF_BOSS_BATTLE, 0 )
            if(WORK[WK_MAPNAMENO] == {0})
            {{
                SetFlag(GF_06MP6305_TALK_HYDRA,1)
                LoadArg("map/mp1201/mp1201.arg")
		        EventCue("mp1201:EV_M01S080_ED")
            }}
            else if(WORK[WK_MAPNAMENO] == {1})
            {{
                SetFlag(GF_06MP6306_TALK_MINOS,1)
                LoadArg("map/mp1201/mp1201.arg")
		        EventCue("mp1201:EV_M01S080_ED")
            }}
            else if(WORK[WK_MAPNAMENO] == {2})
            {{
                SetFlag(GF_06MP6307_TALK_NESTOR,1)
                LoadArg("map/mp1201/mp1201.arg")
		        EventCue("mp1201:EV_M01S080_ED")
            }}
            else if(WORK[WK_MAPNAMENO] == {3})
            {{
                SetFlag(GF_06MP6308_TALK_SARAI,1)
                LoadArg("map/mp1201/mp1201.arg")
		        EventCue("mp1201:EV_M01S080_ED")
            }}
        }}
"""
    bossReturn = bossReturn.format(bossCue[bossPool[0]][2], bossCue[bossPool[1]][2], bossCue[bossPool[2]][2], bossCue[bossPool[3]][2])

    return bossCheckpoint.format(bossFight1,bossFight2,bossFight3,bossFight4,
                                     bossLoc1,bossLoc2,bossLoc3,bossLoc4,wardenScaling,
                                     bossPool[0],bossPool[1],bossPool[2],bossPool[3],
                                     bossCue[bossPool[0]][0],bossCue[bossPool[0]][1],bossCue[bossPool[1]][0],bossCue[bossPool[1]][1],
                                     bossCue[bossPool[2]][0],bossCue[bossPool[2]][1],bossCue[bossPool[3]][0],bossCue[bossPool[3]][1],
                                     bossReturn)

#The glow stone will now trigger this script from the chest that has it. This unlocks night explorations.
def makeGlowStoneUseful():
    script = """
    // Flag setting/item collection
    SetFlag(GF_OPEN_PANGAIA_T2,1) //Pangaia Great Plains night map released
    //SetFlag( GF_QUEST_613, QUEST_START ) // [QS613]
    //SetDiaryFlag( DF_QS613_START, 1 ) // [QS613]
    // Flag setting/item collection
    SetFlag(GF_OPEN_GENSD_T2,1) //Gendarme night map released
    //SetFlag( GF_QUEST_505, QUEST_START ) // [QS505] Saw the start event for gathering moonlight grass (Drifting Village/Night D)
    //SetDiaryFlag( DF_QS505_START, 1 ) // [QS505]I heard from Licht.
    //Flag setting/item collection
    SetFlag(GF_OPEN_CORAL_T2,1) //Coral Forest night map released
    //SetFlag( GF_QUEST_232, QUEST_START ) // [QS232] Watched the Dark Night Mystery (Drifting Village/Night D) starting event
    //SetDiaryFlag( DF_QS232_START, 1 ) // [QS232]I heard from Dogi.
"""
    return script

#These items will trigger these flags for Dana's past events.
#Dana's past events are pretty linear and don't make for great rando content, there are probably interesting things that could be done with sanctuary crypt but it's massive and pretty linear with vanilla behavior.
#So we're instead taking items from her past, most of them key items, and making them items that will auto complete all specific Dana past events that affect the present. 
#There are 7 Dana past events where she is able to do things that affect the present, so there are 7 key items here.
def danaPastEvents(pastItem):
    if pastItem == 698: #'Maiden Journal'
        script = """
    if(!FLAG[GF_03MP1101_LEAVE_CAMP] ) //primordial passage access
    {
        SetFlag(GF_TBOX_DUMMY131, 1) // activate load zone to pinnacle from temple approach, moved to primordial passage post entrance shuffle
        SetFlag(GF_03MP1101_LEAVE_CAMP,1)
    }
    """
    elif pastItem == 700: #'Blue Seal of Whirling Water'
        script = """
    if(!FLAG[GF_04MP5101_OUT_CAMP]) //ruins of eternia access
    {
        SetFlag( GF_04MP5101_OUT_CAMP, 1 )
        SetFlag(GF_04MP6401M_GO_MP6101M,1)
        SetFlag( GF_04MP6101_MAKE_CAMP, 1 )
        SetFlag( GF_04MP6101_CRYSTAL_FLASH, 1 )
        SetFlag(GF_SUBEV_PAST_01_GIMMICK_A,1) // Past Part I: Achieved [Past Gimmick : Waterway Repair]
        SetFlag(GF_SUBEV_PAST_01_GIMMICK_C,1) // Past episode I: Viewed [Past gimmick: Reflection in modern version]
        SetFlag(GF_SUBEV_PAST_01_LP_1ST,1) // Past Part I: [LP: Bookshelf in Dana's Room] First time
    }
    """
    elif pastItem == 701: #'Green Seal of Roaring Stone'
        script = """
    if(!FLAG[GF_04MP6201_DIS_OBSTACLE]) //temple of the great tree access
    {
        SetFlag(GF_04MP6201_DIS_OBSTACLE,1)
        SetFlag(GF_SUBEV_PAST_02_GIMMICK_A, 1) // Past Part II: Watched the event [Past Gimmick : Listen to the story of the key]
        SetFlag(GF_SUBEV_PAST_02_GIMMICK_B, 1)// Past Part II: [Past Gimmick : Listen to the story about the key] Opened the door
        SetFlag(GF_SUBEV_PAST_02_FIRECNT_A, 1)// Past Part II: [Past Quest E: Examine the light on the statue] Light the three candlesticks
        SetFlag(GF_SUBEV_PAST_02_FIRECNT_B, 1)// Past Part II: [Past Quest E: Examine the light on the statue] Light the three candlesticks
        SetFlag(GF_SUBEV_PAST_02_FIRECNT_C, 1)// Past Part II: [Past Quest E: Examine the light on the statue] Light the three candlesticks
    }
    """
    elif pastItem == 702: #'Golden Seal of Piercing Light'
        script = """
    if(!FLAG[GF_05MP6201M_GOTO_BAHA]) //baja tower access
    {
        SetFlag(GF_05MP6201M_GOTO_BAHA,1)
        SetFlag(GF_SUBEV_PAST_03_GIMMICK_L,1) // Watched Past Edition III: [Past Gimmick : Helping Animals]
        SetFlag(GF_SUBEV_PAST_03_GIMMICK_A, 2) // Past Edition III: Achieved [Past Gimmick: Helping animals] (substitute 2)
        SetFlag(GF_SUBEV_PAST_03_GIMMICK_B, 1) // Viewed past edition III: [Past gimmick : Reflection in modern edition]
        SetFlag(GF_GET_GRATICA,	1)
    }
    """
    elif pastItem == 699: #'Frozen Flower'
        script = """
    if(!FLAG[GF_05MP6204_APPEAR_CASTLE]) //chasm access
    {
        SetFlag(GF_05MP6204_APPEAR_CASTLE,1)
        SetFlag(GF_SUBEV_PAST_04_GIMMICK_L, 1)// Watched Past Chapter IV: [Past Gimmick : Repairing the Great Monastery Door]
        SetFlag(GF_SUBEV_PAST_04_GIMMICK, 2)// Past Part IV: Achieved [Past Gimmick : Repairing the door of the Great Monastery] (substitute 2)
        SetFlag(GF_OPEN_FLOOR_02,1) //I saw a prediction that the second floor would open.
    }
    """
    elif pastItem == 796: #'Treasure Chest Key'
        script = """
    if(!FLAG[GF_05MP6105_GOTO_VALLAY]) //lodinia marsh back half access
    {
        SetFlag(GF_05MP6105_GOTO_VALLAY,1)
        SetFlag(GF_OPEN_FLOOR_03,1) //I saw a prediction that the third floor would open.
        SetFlag(GF_GET_LUMINOUS,1)
    }
    """
    elif pastItem == 727: #'Shrine Maiden Amulate'
        script = """
    if(!FLAG[GF_SUBEV_PAST_06_GIMMICK_A]) //hill of eternity
    {
        SetFlag(GF_SUBEV_PAST_06_GIMMICK_A,1) // Watched Past Edition VI: [Past Gimmick : Discovered Poisonous Swamp]
        SetFlag(GF_SUBEV_PAST_06_GIMMICK_B,1)// Past Chapter VI: Moved the meteor fragment with [Past Gimmick : Purification of Poisonous Swamp]
        SetFlag(GF_SUBEV_PAST_06_GIMMICK_C,1) // Watched past edition VI: [Past gimmick : Reflection in modern edition]
        SetFlag(GF_OPEN_FLOOR_04, 1) //I saw a prediction that the 4th floor would open.
        SetFlag(GF_OPEN_FLOOR_05, 1) //I saw a prediction that the 5th floor would open.
    }  									
    """
    return script

#Sword of Psyches event. Adol gets Mistletein(probably mispelled that)
#we make sure the weapon is equipped here when it is received, if progressive super weapons we just set the flag for haivng received it so Kathleen will know the upgrade can happen at shop rank max 
def sopEvent(options):
    if options.progressive_super_weapons == 1:
        script = """
    SetFlag(GF_TBOX_DUMMY071,1)
    """
    else:
        script = """
	SetFlag(GF_ADOLWEAPON_BACKUP,(ADOL.CHRWORK[CWK_WEAPON]))
	GetItem(ICON3D_WP_ADOL_008,1)
	EquipWeapon(ADOL,ICON3D_WP_ADOL_008)
	SetFlag(GF_TBOX_DUMMY071,1)
	"""
    return script

#dana spirit ring
def spiritRingEvent(options):
    if options.progressive_super_weapons == 1:
        script = """
    SetFlag(GF_TBOX_DUMMY108,1)
    """
    else:
        script = """
	GetItem(ICON3D_WP_DANA_005,1)
	EquipWeapon(DANA,ICON3D_WP_DANA_005)
	SetFlag(GF_TBOX_DUMMY108,1)
	"""
    return script

#This makes shop upgrades progressive and is also what makes the flame stones actually do something.
#In vanilla all they did was act as a signpost for flags that were already set. 
#Kathleen has also been added the the to the shop upgrade chain as the first step. This is to help with combat balancing. 
#The idea being that weapons are the most important factor for combat balancing so making sure that Kathleen is found first before the reforge chains are unlocked will help with the game flow.
#Also to improve character balance in the rando late joining characters now have weapons they get from Kathleen for free we speaking with her at specific shop upgrade ranks.
#AP moves the shop upgrade checks to the init of castaway village, this allows up to simplify this function but we still need this for shop rank overflow.
def shopUpgrades(location_id, loc_data, vanillaScript):
    scriptName = buildLocScripts(location_id,False)

    if loc_data.location_type == 'event':   
        getItemFunction =  """
function "{0}"
{{
    if (ALLITEMWORK[ICON3D_139] >= 8)
    {{
            GetItem(ICON3D_MT_N4_STONE,5)
            GetItemMessageExPlus(ICON3D_MT_N4_STONE,5,ITEMMSG_SE_NORMAL," Obtained.",0,0)
            WaitPrompt()
            WaitCloseWindow()
    }}
    else
    {{
        GetItem(ICON3D_139,1)
        GetItemMessageExPlus(ICON3D_139,1,ITEMMSG_SE_NORMAL," Obtained.",0,0)
        WaitPrompt()
        WaitCloseWindow()
        {1}
    }}
}}
"""  
    else:
        fillChest(location_id,139,1)
        getItemFunction =  """
function "{0}"
{{
    SetStopFlag(STOPFLAG_TALK)
    if (ALLITEMWORK[ICON3D_139] >= 8)
    {{
            GetItem(ICON3D_MT_N4_STONE,5)
            GetItemMessageExPlus(ICON3D_MT_N4_STONE,5,ITEMMSG_SE_NORMAL," Obtained.",0,0)
            WaitPrompt()
            WaitCloseWindow()
    }}
    else
    {{
        {1}
    }}
    ResetStopFlag(STOPFLAG_TALK)
}}
"""   
    return getItemFunction.format(scriptName,vanillaScript)

#setting for when the great tree of origins entrance opens
def octusGoal(parameters):
    if parameters.goal == 'Find Crew':
        octusAccess ="""
function "openTree"
{{
    if(WORK[WK_NPCNUM] >= {0} && !FLAG[GF_06MP6409_OPEN_GATE])
    {{
        SetFlag(GF_06MP6409_OPEN_GATE, 1)
        CallFunc("mp6409:init")
    }}
}}
"""
        return octusAccess.format(str(parameters.numOctus))
    
    elif parameters.goal in ['Seiren Escape','Untouchable']:
        octusAccess ="""
function "openTree"
{
    SetFlag(GF_06MP6409_OPEN_GATE, 1)
    CallFunc("mp6409:init")
}
"""
        return octusAccess
    
    elif parameters.goal == 'Release the Psyches':
        octusAccess ="""
function "openTree"
{{
    if(ALLITEMWORK[ICON3D_831] >= {0} && !FLAG[GF_06MP6409_OPEN_GATE]) //ICON3D_831:junk item used for tracking
    {{
        SetFlag(GF_06MP6409_OPEN_GATE, 1)
        CallFunc("mp6409:init")
    }}
}}
"""
    return octusAccess.format(str(parameters.numOctus))
    
#Our goals for entering the selection sphere
def goal(parameters):
    if parameters.goal == 'Find Crew':
        selectionSphereAccess ="""
function "goal"
{{
    if(WORK[WK_NPCNUM] >= {0})
    {{
        // filler
    }}
    else 
    {{
        SetChrWork("LP_warpin_mp6310b", CWK_CHECKOFF, 1)
        SetChrPos("b020",-100000.00f,0.00f,0.00f)
    }}
}}
"""
        return selectionSphereAccess.format(str(parameters.numGoal))
    
    elif parameters.goal == 'Seiren Escape':
        selectionSphereAccess ="""
function "goal"
{
    if(ALLITEMWORK[ICON3D_SHIP_PLAN] && ALLITEMWORK[ICON3D_SEIREN_CHART] && FLAG[GF_TBOX_DUMMY071])
    {
        // filler
    }
    else 
    {
        SetChrWork("LP_warpin_mp6310b", CWK_CHECKOFF, 1)
        SetChrPos("b020",-100000.00f,0.00f,0.00f)
    }
}
"""
        return selectionSphereAccess
        
    elif parameters.goal == 'Release the Psyches':
        selectionSphereAccess ="""
function "goal"
{{
    if(ALLITEMWORK[ICON3D_831] >= {0}) //ICON3D_831:junk item used for tracking
    {{
        // filler
    }}
    else 
    {{
        SetChrWork("LP_warpin_mp6310b", CWK_CHECKOFF, 1)
        SetChrPos("b020",-100000.00f,0.00f,0.00f)
    }}
}}
"""
    
        return selectionSphereAccess.format(str(parameters.numGoal))

    elif parameters.goal == 'Untouchable':
        selectionSphereAccess ="""
function "goal"
{
    if(FLAG[GF_SUBEV_UNTOUCHABLE])
    {
        // filler
    }
    else 
    {
        SetChrWork("LP_warpin_mp6310b", CWK_CHECKOFF, 1)
        SetChrPos("b020",-100000.00f,0.00f,0.00f)
    }
}
"""
    return selectionSphereAccess

def octoBosses(parameters, finalNonGoalBossLevel):
    random.seed(parameters.seed)
    octoBossAliases = ['"ev_mons01"','"ev_mons02"','"ev_mons03"','"ev_mons04"','"ev_mons05"','"ev_mons06"','"ev_mons07"','"ev_mons08"','"ev_mons09"','"ev_mons10"']
    #octus bosses exp and HP go up based on bosses leading into the end game. This is to help prep for the final boss.
    #the HP mod is just a percentage of a rough approcimation of the highest level the final boss could get to if unlucky.
    HPmod = max(round(finalNonGoalBossLevel/110,2),0.25)
    EXPMod = max(round(math.pow(finalNonGoalBossLevel,2.11)*0.00058,1),1)
    script = '\tfunction "setOctoBossLevels"\n\t{\n'
    for boss in octoBossAliases:
        bossLevel = random.randrange(65,75)
        script = script + '\t\tSetLevel(' + boss + ', ' + str(bossLevel) + ')\n'
        script = script + '\t\tSetChrWork(' + boss + ', CWK_MAXHP, (' + boss.replace('"','') + '.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
        script = script + '\t\tSetChrWork(' + boss + ', CWK_HP, (' + boss.replace('"','') + '.CHRWORK[CWK_MAXHP]))\n'
        script = script + '\t\tSetChrWorkGroup(' + boss + ', CWK_EXPMUL, ' + str(EXPMod) + 'f)\n'
    script = script + '\t}\n'

    randomizeOctoBosses(parameters)

    return script
#This sorts out our final boss settings.
#First we figure out what phases we're doing then we run through our script that's called to start the final boss and what's used to call the ending cutscenes.
#if we're only doing theos then the theos start script calls theos and the ending script calls the ending cutscene.
#if we're doing both then the ending cutscene script instead calls origin.
#if we're only doing origin then the theos start script calls the origin boss fight.
#for Past Dana we only load the Io fight
def endingHandler(parameters, finalNonGoalBossLevel):
    finalBossLevel = finalNonGoalBossLevel + 2

    if parameters.charMode != 'Past Dana':
        finalBossLevel = finalBossLevel + 2
    if parameters.goal == 'Untouchable':
        finalBossLevel = 80
    if parameters.goal == 'release the psyches':
        finalBossLevel = finalBossLevel + 2*parameters.numGoal

    
    if parameters.finalBoss == 'Both':
        spoilerLog.write('\nFinal Boss Level: ' + parameters.finalBoss + ' ' + str(finalBossLevel) + ',' + str(finalBossLevel + 1) + '\n')
    elif parameters.finalBoss == 'Origin of Life':
        spoilerLog.write('\nFinal Boss Level: ' + parameters.finalBoss + ' ' + str(finalBossLevel + 1) + '\n')
    else:
        spoilerLog.write('\nFinal Boss Level: ' + parameters.finalBoss + ' ' + str(finalBossLevel) + '\n')

    finalBossLevelScript = """
    function "finalBossLevel"
    {{
        SetChrWorkGroup(B020, CWK_LV, {0})
        SetChrWorkGroup(B021, CWK_LV, {0})
        SetChrWorkGroup(B021IVY, CWK_LV, {0})
        SetChrWorkGroup(B022, CWK_LV, {0})
        SetChrWorkGroup(B023, CWK_LV, {0})
        SetChrWorkGroup(B024, CWK_LV, {0})
        SetChrWorkGroup(B025, CWK_LV, {0})
        SetChrWorkGroup(B009, CWK_LV, {1})
        SetChrWorkGroup(B010, CWK_LV, {1})
        SetChrWorkGroup(B030, CWK_LV, {0})
    }}
    """
    finalBossLevelScript = finalBossLevelScript.format(str(finalBossLevel), str(finalBossLevel + 1))

    if parameters.charMode == 'Past Dana':
        ioFightLoad = """
    function "finalBoss"
    {
        LoadArg("map/mp6569m/c.arg")
	    EventCue("mp6569m:EV_RetryBoss")
    }
    """
        return ioFightLoad + finalBossLevelScript
    
    if parameters.theosPhase == 'First':
        theosPhase = ''
    elif parameters.theosPhase == 'Second':
        theosPhase = 'SetFlag(GF_MP6310B_ENDROGRAM_STEP,1)'
    elif parameters.theosPhase == 'Final':
        theosPhase = 'SetFlag(GF_MP6310B_ENDROGRAM_STEP,2)'
    
    if parameters.originPhase == 'First':
        originPhase = ''
    elif parameters.originPhase == 'Final':
        originPhase = 'SetFlag(GF_MP8323_2NDBATTLE,1)'

    if parameters.carePackage == 'Generous':
        package = """
        GetItem(ICON3D_US_BERRY_S,9)
        GetItem(ICON3D_US_COCONUT_S,9)
        GetItem(ICON3D_US_MANGO_S,9)
        GetItem(ICON3D_US_DRAGONFRUIT_S,9)
        GetItem(ICON3D_USFD_FOOD15,9)
        GetItem(ICON3D_USFD_FOOD03,9)
        GetItem(ICON3D_US_RESSURECT_02,9)
        GetItem(ICON3D_US_EXTRA_02,2)
        """
    elif parameters.carePackage == 'Lite':
        package = """
        GetItem(ICON3D_US_BERRY_S,5)
        GetItem(ICON3D_US_COCONUT_S,5)
        GetItem(ICON3D_US_MANGO_S,5)
        GetItem(ICON3D_US_DRAGONFRUIT_S,5)
        GetItem(ICON3D_USFD_FOOD15,1)
        GetItem(ICON3D_US_RESSURECT_02,1)
        GetItem(ICON3D_US_EXTRA_02,1)
        """
    elif parameters.carePackage == 'None':
        package = ""
        

    if parameters.finalBoss == 'Theos de Endogram' or parameters.finalBoss == 'Both':
        theosStartScript = """
    function "finalBoss"
    {{
        {0}
        LoadArg("map/mp6310b/mp6310b.arg")
	    EventCue("mp6310b:EV_M06S240")
    }}
    """
        theosStartScript = theosStartScript.format(theosPhase)
    elif parameters.finalBoss == 'Origin of Life':
        theosStartScript = """
    function "finalBoss"
    {{
        {0}
        LoadArg("map/mp8323/mp8323.arg")
		EventCue("mp8323:init")
    }}
    """
        theosStartScript = theosStartScript.format(originPhase)

    if parameters.finalBoss == 'Theos de Endogram' or parameters.finalBoss == 'Origin of Life':
        ending1 = """
    function "ending"
    {
        LoadArg("map/mp0021/mp0021.arg")
        EventCue("mp0021:EV_M07S130")
    }
    
    function "ending2"
    {
        LoadArg("map/mp0021/mp0021.arg")
        EventCue("mp0021:EV_M07S130")
    }
    """
    elif parameters.finalBoss == 'Both':
        ending1 = """
    function "ending"
    {{
        {0}
        {1}
        LoadArg("map/mp8323/mp8323.arg")
		EventCue("mp8323:init")
    }}

    function "ending2"
    {{
        LoadArg("map/mp0021/mp0021.arg")
        EventCue("mp0021:EV_M07S130")
    }}
    """
        ending1 = ending1.format(originPhase,package)

    return theosStartScript + ending1 + finalBossLevelScript

#This flag was original tripped by the chest event from the chest on the Docks of East Coast Cave. Now it has been moved to the note that was originally in that chest.
def pirateShipDocks():
    script = """

    SetFlag(GF_05MP7411_READ_NOTE1, 1)

"""
    return script

#this builds out all our intercept rewards, it's called every time we return from an intercept in castaway village by checking the flags for last stage rank and stage clear
def interceptionHandler(parameters):
    interceptionRewards = getIntRewards()

    script = """
function "newInterceptControl"
{
	SetWork(WK_ITC_BASE_LV, 9)
	SetWork(WK_ITC_DECOY_NUM, 8)
	SetWork(WK_ITC_DECOY_LV, 5)
	SetWork(WK_ITC_DECOY_OPT, 1)
	SetWork(WK_ITC_BARRICADE_NUM, 4)
	SetWork(WK_ITC_BARRICADE_LV, 5)
	SetWork(WK_ITC_BARRICADE_OPT, 1)
	SetWork(WK_ITC_CATAPULT_NUM, 1)
	SetWork(WK_ITC_CATAPULT_LV, 5)
	SetWork(WK_ITC_CATAPULT_OPT, 1)
	SetWork(WK_ITC_GONG_NUM, 1)
	SetWork(WK_ITC_GONG_LV, 3)
	SetWork(WK_ITC_GONG_OPT, 1)

    if (FLAG[GF_INTERCEPT_LASTRESULT] == 1)
    {

"""
    for stage in interceptionRewards:
        stageCheck = """
        if (FLAG[GF_INTERCEPT_LASTSTAGEID] == {0})
        {{
            SetStopFlag(STOPFLAG_TALK)

"""
        script = script + stageCheck.format(stage.stage)

        if parameters.intRewards:
            totalReward = 0
            for index,reward in enumerate(stage.rewards):
                if index % 2 == 0 or index == 0:
                    item = reward
                else:
                    itemNum = reward

                totalReward+=1
                if totalReward == 2:
                    rewardGet = """

                GetItem({0},{1})
                GetItemMessageExPlus({0},{1},ITEMMSG_SE_NORMAL,"{2}",0,0)
                WaitPrompt()
                WaitCloseWindow()

                """
                    script = script + rewardGet.format(item,itemNum,genericMessage)
                    totalReward = 0

        if stage.stage == 'INTERCEPT_STAGE02':
            dogiReward = """
            SetFlag(GF_TBOX_DUMMY089,1)
            """
        elif stage.stage == 'INTERCEPT_STAGE03':
            dogiReward = """
            SetFlag(GF_TBOX_DUMMY090,1)"""
        elif stage.stage == 'INTERCEPT_STAGE05':
            dogiReward = """
            SetFlag(GF_TBOX_DUMMY091,1)
            """
        elif stage.stage == 'INTERCEPT_STAGE07':
            dogiReward = """
            SetFlag(GF_TBOX_DUMMY092,1)
            """
        elif stage.stage == 'INTERCEPT_STAGE09':
            dogiReward = """
            SetFlag(GF_TBOX_DUMMY093,1)
            """
        else:
            dogiReward = ''

        stageFooter = """
            ResetStopFlag(STOPFLAG_TALK)
        }"""  
        
        script = script + dogiReward + stageFooter

    scriptFooter = """
        SetFlag(GF_INTERCEPT_LASTRESULT, 0)
	    SetFlag(GF_INTERCEPT_LASTSTAGEID, INTERCEPT_STAGE_NONE)
	    CallFunc("mp1201:init") 
    }
}  
"""
    script = script + scriptFooter

    return script

def jewelTrade(locations):
    dinasItems = [None] * 10
    for location in locations:
        if location.locName == "Jewel Trade":
            dinasItems[location.locID - 461] = copyLocationToNewLoc(location) #dina's location IDs for the rando start at ID 461 so this gets us the exact array index we need to have them in order inside the array
    
    #we have to do a little extra work for skills because of the divergent way I handled skills in the locaiton file
    for item in dinasItems: 
        if item.skill:
            skillInfo = getSkillInfo(item.itemName)
            item.itemName = skillInfo[2] + " Skill -" + skillInfo[1]
    
    script = """
function "newTradeHandler"
{{
        
    if(ALLITEMWORK[ICON3D_MT_R4_GOLD] > 0 && !FLAG[GF_TBOX_DUMMY095])
    {{
        MenuAdd(10, "#2C Prismatic Jewel x 1 #0C for #2C {0}#0C .")
    }}
    else
    {{
        MenuAdd(11, "Prismatic Jewel x 1 for {0}.")
    }}
    if(ALLITEMWORK[ICON3D_MT_R4_GOLD] > 0 && !FLAG[GF_TBOX_DUMMY096])
	{{
        MenuAdd(20, "#2C Prismatic Jewel x 1 #0C for #2C {1}#0C .")
	}}
	else
	{{
        MenuAdd(21, "Prismatic Jewel x 1 for {1}.")
	}}

	if(ALLITEMWORK[ICON3D_MT_R4_GOLD] >= 2 && !FLAG[GF_TBOX_DUMMY097])
	{{
		MenuAdd(110, "#2C Prismatic Jewel x 2 #0C for #2C {2}#0C .")
	}}
	else
	{{
		MenuAdd(111, "Prismatic Jewel x 2 for {2}.")
	}}
	
	if(ALLITEMWORK[ICON3D_MT_R4_GOLD] >= 10 && !FLAG[GF_TBOX_DUMMY098])
	{{
		MenuAdd(30, "#2C Prismatic Jewel x 10 #0C for #2C {3}#0C .")
	}}
	else
	{{
		MenuAdd(31, "Prismatic Jewel x 10 for {3}.")
	}}
	
	if(ALLITEMWORK[ICON3D_MT_R4_GOLD] >= 25 && !FLAG[GF_TBOX_DUMMY099])
    {{
		MenuAdd(40, "#2C Prismatic Jewel x 25 #0C for #2C {4}#0C .")
	}}
	else
	{{
		MenuAdd(41, "Prismatic Jewel x 25 for {4}.")
	}}

	//--------------------------------------------------------------------------------------

	if(ALLITEMWORK[ICON3D_MT_R4_GOLD] >= 1 && !FLAG[GF_OLDITEM_TRADE_01])	
    {{
		MenuAdd(50, "#2C Prismatic Jewel x 1 #0C for #2C {5}#0C .")
	}}
	else
	{{
		MenuAdd(51, "Prismatic Jewel x 1 for {5}.")
	}}

	if(ALLITEMWORK[ICON3D_MT_R4_GOLD] >= 1 && !FLAG[GF_OLDITEM_TRADE_02])	
    {{
		MenuAdd(60, "#2C Prismatic Jewel x 1 #0C for #2C {6}#0C .")
	}}
	else
	{{
		MenuAdd(61, "Prismatic Jewel x 1 for {6}.")
	}}
	
	if(ALLITEMWORK[ICON3D_MT_R4_GOLD] >= 2 && !FLAG[GF_OLDITEM_TRADE_03])	
    {{
		MenuAdd(70, "#2C Prismatic Jewel x 2 #0C for #2C {7}#0C .")
	}}
	else
	{{
		MenuAdd(71, "Prismatic Jewel x 2 for {7}.")
	}}

	if(ALLITEMWORK[ICON3D_MT_R4_GOLD] >= 2 && !FLAG[GF_OLDITEM_TRADE_04])	
    {{
		MenuAdd(80, "#2C Prismatic Jewel x 2 #0C for #2C {8}#0C .")
	}}
	else
	{{
		MenuAdd(81, "Prismatic Jewel x 2 for {8}.")
	}}		

	if(ALLITEMWORK[ICON3D_MT_R4_GOLD] >= 3 && !FLAG[GF_OLDITEM_TRADE_05])	
    {{
		MenuAdd(90, "#2C Prismatic Jewel x 3 #0C for #2C {9}#0C .")
	}}
	else
	{{
		MenuAdd(91, "Prismatic Jewel x 3 for {9}.")
	}}

}}
"""
    item1 = dinasItems[0].itemName + ' x ' + str(dinasItems[0].quantity)
    item2 = dinasItems[1].itemName + ' x ' + str(dinasItems[1].quantity)
    item3 = dinasItems[2].itemName + ' x ' + str(dinasItems[2].quantity)
    item4 = dinasItems[3].itemName + ' x ' + str(dinasItems[3].quantity)
    item5 = dinasItems[4].itemName + ' x ' + str(dinasItems[4].quantity)
    item6 = dinasItems[5].itemName + ' x ' + str(dinasItems[5].quantity)
    item7 = dinasItems[6].itemName + ' x ' + str(dinasItems[6].quantity)
    item8 = dinasItems[7].itemName + ' x ' + str(dinasItems[7].quantity)
    item9 = dinasItems[8].itemName + ' x ' + str(dinasItems[8].quantity)
    item10 = dinasItems[9].itemName + ' x ' + str(dinasItems[9].quantity)
    return script.format(item1,item2,item3,item4,item5,item6,item7,item8,item9,item10)

#function to give hints for long checks, NPCs will tell you once the check is unlocked what is behind it
def talkHints(shuffledLocations):

    def formatHint(location):
        if location.skill:
            skillInfo = getSkillInfo(location.itemName)
            return skillInfo[2] + " Skill -" + skillInfo[1]
        elif location.quantity > 1:
            return location.itemName + ' x ' + str(location.quantity)
        else:
            return location.itemName
        
    dogiHints = 'function "interceptRewardPreview"\n{\n'
    ricottaHints = 'function "mkRewardsPreview"\n{\n'
    shoebillHints = 'function "fishRewardPreview"\n{\n'
    intReward = [None] * 5
    mkRewards = [None] * 7
    fishRewards = [None] * 6

    for location in shuffledLocations:
        if location.locName == 'Intercept':
            if location.mapCheckID == 'Stage 2':
                intReward[0] = formatHint(location)
            elif location.mapCheckID == 'Stage 3':
                intReward[1] = formatHint(location)
            elif location.mapCheckID == 'Stage 5':
                intReward[2] = formatHint(location)
            elif location.mapCheckID == 'Stage 7':
                intReward[3] = formatHint(location)
            elif location.mapCheckID == 'Stage 9':
                intReward[4] = formatHint(location)
        elif location.mapCheckID == 'Master Kong Skill Ricotta':
            mkRewards[0] = formatHint(location)
        elif location.mapCheckID == 'Master Kong Skill Sahad':
            mkRewards[1] = formatHint(location)
        elif location.mapCheckID == 'Master Kong Skill Dana':
            mkRewards[2] = formatHint(location)
        elif location.mapCheckID == 'Master Kong Skill Laxia':
            mkRewards[3] = formatHint(location)
        elif location.mapCheckID == 'Master Kong Skill Hummel':
            mkRewards[4] = formatHint(location)
        elif location.mapCheckID == 'Master Kong Skill Adol':
            mkRewards[5] = formatHint(location)
        elif location.mapCheckID == 'Master Kong Join':
            mkRewards[6] = formatHint(location)
        elif location.locName == 'Fish Trade':
            if location.mapCheckID == 'Fish 4':
                fishRewards[0] = formatHint(location)
            elif location.mapCheckID == 'Fish 8':
                fishRewards[1] = formatHint(location)
            elif location.mapCheckID == 'Fish 12':
                fishRewards[2] = formatHint(location)
            elif location.mapCheckID == 'Fish 16':
                fishRewards[3] = formatHint(location)
            elif location.mapCheckID == 'Fish 20':
                fishRewards[4] = formatHint(location)
            elif location.mapCheckID == 'Fish 24':
                fishRewards[5] = formatHint(location)
        

    dogiHints += """
    if(FLAG[GF_TBOX_DUMMY100] && !FLAG[GF_TBOX_DUMMY102])
    {{ 
        TalkPopup("Dogi",0,2,0,0,0)
        {{
            "Hey! Look what I got for you!"
            "If you clear stage 2: #2C {0}#0C"
            "If you clear stage 3: #2C {1}#0C"
            "If you clear stage 5: #2C {2}#0C"
            "If you clear stage 7: #2C {3}#0C"
        }}
        WaitPrompt()
        WaitCloseWindow()
        
        Wait(5)
    }}
    if(FLAG[GF_TBOX_DUMMY102])
    {{ 
        TalkPopup("Dogi",0,2,0,0,0)
        {{
            "Hey! Look what I got for you!"
            "If you clear stage 2: #2C {0}#0C"
            "If you clear stage 3: #2C {1}#0C"
            "If you clear stage 5: #2C {2}#0C"
            "If you clear stage 7: #2C {3}#0C"
            "If you clear stage 9: #2C {4}#0C"
        }}
        WaitPrompt()
        WaitCloseWindow()
        
        Wait(5)
    }}
}}
    """.format(intReward[0],intReward[1],intReward[2],intReward[3],intReward[4])

    ricottaHints += """
    TalkPopup("Ricotta",0,2,0,0,0)
    {{
        "Master says he can give the following:"
        "#2C {0}#0C for me!"
    }}
    WaitPrompt()
    WaitCloseWindow()

    if(FLAG[SF_SAHAD_JOINED])
    {{
        TalkPopup("Ricotta",0,2,0,0,0)
        {{
            "#2C {1}#0C for Sahad!"
        }}
        WaitPrompt()
        WaitCloseWindow()
    }}
    if(FLAG[SF_DANA_JOINED])
    {{
        TalkPopup("Ricotta",0,2,0,0,0)
        {{
            "#2C {2}#0C for Dana!"
        }}
        WaitPrompt()
        WaitCloseWindow()
    }}
    if(FLAG[SF_LAXIA_JOINED])
    {{
        TalkPopup("Ricotta",0,2,0,0,0)
        {{
            "#2C {3}#0C for Laxia!"
        }}
        WaitPrompt()
        WaitCloseWindow()
    }}
    if(FLAG[SF_HUMMEL_JOINED])
    {{
        TalkPopup("Ricotta",0,2,0,0,0)
        {{
            "#2C {4}#0C for Hummel!"
        }}
        WaitPrompt()
        WaitCloseWindow()
    }}
    if(FLAG[SF_ADOL_JOINED])
    {{
        TalkPopup("Ricotta",0,2,0,0,0)
        {{
            "#2C {5}#0C for Adol!"
        }}
        WaitPrompt()
        WaitCloseWindow()
    }}
    if(FLAG[SF_ADOL_JOINED] && FLAG[SF_SAHAD_JOINED] && FLAG[SF_DANA_JOINED] && FLAG[SF_LAXIA_JOINED] && FLAG[SF_HUMMEL_JOINED])
    {{
        TalkPopup("Ricotta",0,2,0,0,0)
        {{
            "#2C {6}#0C is for everyone!"
        }}
        WaitPrompt()
        WaitCloseWindow()
    }}
    Wait(5)
    
}}
    """.format(mkRewards[0],mkRewards[1],mkRewards[2],mkRewards[3],mkRewards[4],mkRewards[5],mkRewards[6])

    shoebillHints += """
        TalkPopup(UNDEF,0,3,STOPPER_PPOSX,STOPPER_PPOSY,0)
		{{
			"Skwaaaa!" 
            "(The Shoebill gestures broadly in a pantomime."
            "It seems to be signaling about the fishing rewards.)"
            ""
		}}

		WaitPrompt()
		WaitCloseWindow()

        TalkPopup(UNDEF,0,3,STOPPER_PPOSX,STOPPER_PPOSY,0)
		{{
			"(#2C {0}#0C)"
            "(#2C {1}#0C)"
            "(#2C {2}#0C)"
            "(#2C {3}#0C)"
            "(#2C {4}#0C)"
            "(#2C {5}#0C)"
		}}

		WaitPrompt()
		WaitCloseWindow()
}}
    """.format(fishRewards[0],fishRewards[1],fishRewards[2],fishRewards[3],fishRewards[4],fishRewards[5])
    return dogiHints + '\n' + ricottaHints + '\n' + shoebillHints

#the order intercepts unlock for finding T's Memos
def interceptUnlock():
    script = """
    if( !FLAG[GF_TBOX_DUMMY100])
    {
        SetFlag(GF_TBOX_DUMMY100,1)
    }
    else if( !FLAG[GF_TBOX_DUMMY101])
    {
        SetFlag(GF_TBOX_DUMMY094,1)
        SetFlag(GF_TBOX_DUMMY101,1)
    }
    else if( !FLAG[GF_TBOX_DUMMY102])
    {
        SetFlag(GF_TBOX_DUMMY102,1)
    }
    else if ( !FLAG[GF_TBOX_DUMMY103])
    {
        SetFlag(GF_TBOX_DUMMY103,1)
    }
"""
    return script

def buildFSCWarp():
    function = ''
    function = function + """
function "FSC_warp"
{
    SetStopFlag(STOPFLAG_TALK)
    SetFlag(TF_MENU_SELECT2, 0)
    MenuReset()
    MenuType(MENUTYPE_POPUP)

    if(FLAG[GF_TBOX_DUMMY156])
    {
        MenuAdd(10, "1F - Chamber of Braziers, Ent")	
    }
    else if(!FLAG[GF_TBOX_DUMMY156])
    {
        MenuAdd(11, "1F - Chamber of Braziers, Ent")	
    }


    if(FLAG[GF_TBOX_DUMMY157])
    {
        MenuAdd(20, "2F - Chamber of Stone, Ent")	
    }
    else if(!FLAG[GF_TBOX_DUMMY157])
    {
        MenuAdd(21, "2F - Chamber of Stone, Ent")	
    }

    if(FLAG[GF_TBOX_DUMMY158])
    {
        MenuAdd(30, "3F - Chamber of Clairvoyance, Ent")	
    }
    else if(!FLAG[GF_TBOX_DUMMY158])
    {
        MenuAdd(31, "3F - Chamber of Clairvoyance, Ent")	
    }

    if(FLAG[GF_TBOX_DUMMY159])
    {
        MenuAdd(40, "4F - Chamber of Frost, Ent")	
    }
    else if(!FLAG[GF_TBOX_DUMMY159])
    {
        MenuAdd(41, "4F - Chamber of Frost, Ent")	
    }

    if(FLAG[GF_TBOX_DUMMY160])
    {
        MenuAdd(50, "5F - Chamber of Magma, Ent")	
    }
    else if(!FLAG[GF_TBOX_DUMMY160])
    {
        MenuAdd(51, "5F - Chamber of Magma, Ent")	
    }

    MenuEnable( 11, 0)
    MenuEnable( 21, 0)
    MenuEnable( 31, 0)
    MenuEnable( 41, 0)
    MenuEnable( 51, 0)
    MenuOpen( TF_MENU_SELECT2 , 283 , ADOLMENU_PPOSY , -2 , -2 , 10 , 1)
    WaitMenu(0)
    CloseMessage(6,0)
    WaitCloseMessage(6)
    MenuClose(10, 0)
    
    if(FLAG[TF_MENU_SELECT2] == 10)
    {
        MenuClose(10, 0)
        LoadArg("map/mp6511/mp6511.arg")
        EventCue("mp6511:init")
        WaitFade()
    }
    else if(FLAG[TF_MENU_SELECT2] == 20)
    {
        MenuClose(20, 0)
        LoadArg("map/mp6521/mp6521.arg")
        EventCue("mp6521:init")
        WaitFade()
    }
    else if(FLAG[TF_MENU_SELECT2] == 30)
    {
        MenuClose(30, 0)
        LoadArg("map/mp6531/mp6531.arg")
        EventCue("mp6531:init")
        WaitFade()
    }
    else if(FLAG[TF_MENU_SELECT2] == 40)
    {
        MenuClose(40, 0)
        LoadArg("map/mp6541/mp6541.arg")
        EventCue("mp6541:init")
        WaitFade()
    }
            else if(FLAG[TF_MENU_SELECT2] == 50)
    {
        MenuClose(50, 0)
        LoadArg("map/mp6551/mp6551.arg")
        EventCue("mp6551:init")
        WaitFade()
    }
    ResetStopFlag(STOPFLAG_TALK)
}
"""
    return function
        



# we're doing away with this old method and simplifying everything. Max exp is a character stat in this game and the status file contains an editable version of it.
# so instead of the old method we're going to call a function to divide the character's max exp by our multiplier.
# this achives the same effect as a global exp multiplier in a far cleaner way than our old method.
# there is no growth rate anymore because honestly a lot of what it was going for is achieved through boss level scaling better
def expMult(parameters):
    newExpMult(parameters)








