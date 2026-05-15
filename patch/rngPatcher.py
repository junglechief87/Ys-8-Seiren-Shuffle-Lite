import random
import os
from shared.functions import *  
from patch.crew import getCrewFlags
from patch.gameStartFunctions import *
from patch.chestPatcher import *
from patch.miscPatches import randomizeOctoBosses, newExpMult
from patch.buildEntrances import *
import shared.config as config

#This is essentially the BnB for how this rando works. This script writes a big .scp file, the game's native scripting files, that we call for all randomized locations (as well as some other important functions for a rando)
#This takes in the game's shuffled list of loctions and then builds the scripts.
#We named our script file rng because we need something short, our script calls from the chests are limited to 8 characters so our standard format for script call is rng:(locID where locID is a 4 digit id).
#Plus rng.scp is a fitting filename for a rando.
patchFile = ''

WHITE = "#0C"
LIGHT_YELLOW = "#1C"
GOLD = "#2C"
ORANGE = "#3C"
GREEN = "#4C"
PINK = "#5C"
PURPLE = "#6C"
BLUE = "#7C"
DARK_RED = "#8C"
AP_ITEM = 149
LANDMARK_ITEM = 148
CASTAWAY_ITEM = 143
SKILL_ITEM = 144
PROGRESSIVE_SHOP_RANK_ITEM = 139

SCP_INCLUDE_LIST = ['#include "inc/mons.h"','#include "inc/def.h"','#include "inc/efx.h"','#include "inc/flag.h"','#include "inc/se.h"',
                  '#include "inc/scr_inc.h"','#include "inc/3dicon.h"','#include "inc/skilldef.h"','#include "inc/vo.h"','#include "inc/temp/rng.h"'] #standard set of header files used in most Ys 8 .scp files

ITEM_SOUND = 'ITEMMSG_SE_NORMAL'
SCRIPT_STOP_FLAG = 'STOPFLAG_SIMPLEEVENT2'

OBTAINED_ITEM_MESSAGE = " Obtained."
CREW_MESSAGE = " joined the Village."
PARTY_MESSAGE = " joined the Party."
SKILL_MESSAGE = f" has learned skill {GOLD}"

ITEM_TYPE_CONFIG = {
    'landmark': {'icon': -1, 'id': LANDMARK_ITEM, 'needs_skill_info': False},
    'castaway': {'icon': -1, 'id': CASTAWAY_ITEM, 'needs_skill_info': False},
    'skill': {'icon': -1, 'id': SKILL_ITEM, 'needs_skill_info': True},
}

LANDMARK_MESSAGE = ' discovered.'
LANDMARKS = {
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

TREASURE_SCRIPTS = {
"372":  "mp6561:EvOpenTBox",
"358":  "mp6554:EvOpenTBox",
"317":  "mp6531m:EvOpenTBox",
"291":  "mp6519:EvOpenTBox",
"288":  "mp6513:EvOpenTBox",
"239":  "mp6345:SubEV_05_Get_Bell_ED",
"19":   "mp0408:EV_M05S152_ED",
"18":   "mp0405:EV_M05S170_ED",
"13":   "mp0404:EV_M05S150_ED",
"9":    "mp0403:EV_M05S151_ED"
}

def rngPatcherMain(patch, progress_callback=None):
    global patchFile
    patchFile = ''
    rngScriptFile = getLocFile('rng','script')
    
    # If rng.scp file not found, construct path manually in script directory and ensure it exists
    if rngScriptFile is None:
        rng_script_dir = os.path.join(config.executable_directory, "script")
        os.makedirs(rng_script_dir, exist_ok=True)  # Create directory if it doesn't exist
        rngScriptFile = os.path.join(rng_script_dir, "rng.scp")
    
    # Build locations cache once to avoid rebuilding for every fillChest call
    locations = getLocations()
    locations_by_id = {loc.locID: loc for loc in locations}
    set_locations_cache(locations_by_id)

    # if patch_file == 'Past Dana':
    #     global PARTY_MESSAGE 
    #     PARTY_MESSAGE = " joined the Village."
    #     pastDanaFixes(True)  
    # else:
    #     pastDanaFixes(False)

    #if patch_file:
    #    randomize_bgmtbl()
    #else:
    #    restore_original_bgm()

    for inc in SCP_INCLUDE_LIST:
        patchFile = patchFile + inc + '\n'
    
    # opening cutscene
    patchFile = patchFile + buildStartParameters(patch) 
    patchFile = patchFile + manageEarlyGameParty(patch)
    patchFile = patchFile + soloStartingCharacterEvent(patch)

    duplicateChests = [47,48,49,179]
    for location in patch.item_map:
        loc_data = patch.item_map[location]
        loc_id = location
        if location not in duplicateChests: #no need to build out functions for the same location twice, these chests share flags with the not dawn version
            #cleanup the placeholders the game had for chests without scripts
            if location in TREASURE_SCRIPTS.keys():
                script = ('\tEventCue("' + TREASURE_SCRIPTS[location] + '")\n')
            else:
                script = ""

            if loc_data['item_type'] in ['Item', '']: # blank is mostly for offworld items
                patchFile = patchFile + genericItemMessage(loc_id, patch, script)
            elif loc_data['category'] == 'Crew':
                patchFile = patchFile + buildCrewLocation(loc_id, patch, script)
            elif 'Skill' in loc_data['category']: #skills contain the character name in the category
                patchFile = patchFile + buildSkillLocation(loc_id, patch, script)
            elif loc_data['category'] == 'Landmark':
                patchFile = patchFile + buildLandmarks(loc_id, patch, script)
        if progress_callback:
            progress_callback(f"Building location from item map: {location}")

    # Handling Options
    bossLevelsScript = bossLevels()
    patchFile = patchFile + bossLevelsScript

    if patch.settings['options']['final_boss_access'] == 2:
        patchFile = patchFile + buildPsyches(patch.settings)
    if patch.settings['options']['former_sanctuary_crypt'] == 1:
        patchFile = patchFile + buildFSCWarp()
    if patch.settings['options']['dungeon_entrance_shuffle'] == 1:
        patchFile = patchFile + buildEntrances(patch.dungeon_entrance_randomization, patch.settings['options'])
    if patch.settings['options']['octus_paths_opened'] == 1:
        patchFile = patchFile + octoBosses(patch.settings)
    else:
        #this is to restore the original values
        randomizeOctoBosses(patch.settings)
    if progress_callback:
        progress_callback("Handling options")

    patchFile = patchFile + interceptionHandler(patch.settings['options'])
    if progress_callback:
        progress_callback("Setting up interceptions")

    patchFile = patchFile + jewelTrade(patch.item_map)
    if progress_callback:
        progress_callback("Setting up Dina's shop")

    patchFile = patchFile + talkHints(patch.item_map)
    if progress_callback:
        progress_callback("Setting up NPC item hints")

    patchFile = patchFile + octusGoal(patch.settings['options'])
    if progress_callback:
        progress_callback("Setting up goal")

    patchFile = patchFile + goal(patch.settings['options'])
    if progress_callback:
        progress_callback("Setting up final boss")

    patchFile = patchFile + endingHandler(patch.settings['options'])
    expMult(patch.settings['options'])
    if progress_callback:
        progress_callback("Setting up ending")

    with open(rngScriptFile, 'w', encoding='Shift-JIS', errors='strip_accents') as fileToPatch: #build the entire rng file from one big string
        fileToPatch.write(patchFile)
        fileToPatch.close()

# ==========================================================================================================
# Functions appear in order called  
# ==========================================================================================================
# Generic Item Function
# ==========================================================================================================
#function used for all non-person item function generation
def genericItemMessage(location_id, patch, vanillaScript):
    options = patch.settings["options"]
    loc_data = patch.item_map[location_id]
    itemId = int(loc_data['item_id'])
    eventScripts = ""

    #'Maiden Journal','Blue Seal of Whirling Water','Green Seal of Roaring Stone','Golden Seal of Piercing Light','Treasure Chest Key','Frozen Flower','Shrine Maiden Amulate'
    danaPastEventsItems = [698,700,701,702,796,699,727]

    #unique item functions that will need additional scripting when the item is recieved
    if itemId == 739: # glow stone
        eventScripts += makeGlowStoneUseful()
    elif itemId in danaPastEventsItems:
        eventScripts += danaPastEvents(itemId)
    elif itemId in [9,146]: # mistilteinn
        eventScripts += sopEvent(options)
    elif itemId in [13,147]: # spirit ring
        eventScripts += spiritRingEvent(options)
    elif itemId == 770: #logbook from east coast cave
        eventScripts += f"\tSetFlag(GF_05MP7411_READ_NOTE1, 1)\n"

    elif itemId == 629: #fishing rod
        eventScripts += f"\tGetItem(ICON3D_FISHBAIT_WORM,30)\n"
    elif itemId == 779: #ship blueprints
        eventScripts += f"\tSetFlag(GF_SUBEV_06_1111_LOOK_BOAT,1)\n"
    elif itemId == 218:
        #Adding the other 2 medals to the slash medal check
        eventScripts += (
            f"\tGetItem(ICON3D_AC_068,1)\n"
            f"\tGetItem(ICON3D_AC_069,1)\n"
        )
    elif itemId == 206: #Jade pendant
        if options['former_sanctuary_crypt'] == 1:
            eventScripts += (
                f"\tSetFlag(SF_SYS_CLEARED, 1)\n"
                f"\tSetFlag(GF_SUBEV_PAST_07_CLEAR, 1)\n"
            )

    eventScripts += vanillaScript
    return formatGetItemScript(location_id, loc_data, eventScripts)

# ==========================================================================================================
# Crew Item Function
# ==========================================================================================================
#function used for all people function generations
def buildCrewLocation(location_id, patch, vanillaScript):
    loc_data = patch.item_map[location_id]

    crewFlags = getCrewFlags(loc_data['item_name'])
    eventScripts = crewFlags + vanillaScript
 
    return formatGetItemScript(location_id, loc_data, eventScripts, message_type="castaway", isParty=loc_data['party_flag'])

# ==========================================================================================================
# Skill Item Function
# ==========================================================================================================
#now skills are in the rando and they need a third special handler for their locations
def buildSkillLocation(location_id, patch, vanillaScript):
    loc_data = patch.item_map[location_id]
    eventScripts = vanillaScript

    return formatGetItemScript(location_id, loc_data, eventScripts, message_type='skill')

# ==========================================================================================================
# Landmark Function
# ==========================================================================================================
def buildLandmarks(location_id, patch, vanillaScript):
    loc_data = patch.item_map[location_id]
    
    landmarkFlag = "\tSetFlag(" + LANDMARKS.get(loc_data['item_name']) + ",1)\n"
    eventScripts = landmarkFlag + vanillaScript

    return formatGetItemScript(location_id, loc_data, eventScripts, message_type='landmark')
# ==========================================================================================================
# Boss Scaling Function
# ==========================================================================================================
def bossLevels():
    return "function \"bossLevels\"\n{\n\t//placeholder to keep existing build functioning until features are implemented\n}\n"
    bossLevels = [5,7,13,14,20,23,26,28,29,32,35,40,43,45,48,51,53,58,60,60,80]
    bossIDs = {'Byfteriza': 'M0111',
               'Avalodragil': 'B150',
               'Serpentus': 'B100',
               'Clareon': 'B000',
               'Lonbrigius': 'B101B',
               'Gargantula': 'B001',
               'Magamandra': 'B102',
               'Laspisus': 'B002',
               'Kiergaard Weissman': 'B152',
               'Avalodragil 2': 'B154',
               'Giasburn': 'B003',
               'Brachion': 'B006',
               'Exmetal': 'B104',
               'Carveros': 'B004',
               'Pirate Revenant': 'B103',
               'Coelacantos': 'B106',
               'Oceanus': 'B007',
               'Doxa Griel': 'B105',
               'Basileus': 'B005',
               'Mephorash': 'B153',
               'Silvia': 'B155',}
    remainingBosses = []
    finalBossLevels = []
    bossLevelsDictByRegion = {}
    HPmod = 0.5
    firstPostSecondCharacterBoss = ''
    partySize = 0
    secondCharacterSphere = 0
    soloPartyBoss = True
    secondCharacterFound = False

    if not parameters.goal == 'Untouchable' and parameters.formerSanctuaryCrypt: # Make sure Melaiduma's level and ID are in the pool if he's not the goal
        bossLevels.append(99) 
        bossIDs['Melaiduma'] = 'B170' 

    if not parameters.goal == 'Release the Psyches': # Make sure the Psyches' levels and IDs are in the pool if they aren't the goal
        bossLevels.extend([67,70,73,75])
        bossIDs['Psyche-Hydra'] = 'B112'
        bossIDs['Psyche-Minos'] = 'B110'
        bossIDs['Psyche-Nestor'] = 'B111'
        bossIDs['Psyche-Ura'] = 'B008'

    for location in playthroughAllProgression.locations:
        if location.party:
            partySize += 1
            if partySize >= 2:
                secondCharacterSphere = location.sphere
                secondCharacterFound = True
                print('Second character joins in sphere: ' + str(secondCharacterSphere))
                print(location.itemName)
                break

    for location in playthroughAllProgression.locations:
        if location.mapCheckID in bossIDs.keys() and location.sphere >= secondCharacterSphere and secondCharacterFound:
            firstPostSecondCharacterBoss = bossIDs.get(location.mapCheckID)
            break
                


    # build out a list of IDs for us to track what bosses aren't in the pool
    for boss in bossIDs.keys():
        remainingBosses.append(bossIDs.get(boss))

    random.seed(parameters.seed)
    spoilerLog.write(f'\n'
                     f'Boss Levels:\n')   
    # process bosses that are accessible before the goal in the seed and assign them levels in ascending order as the playthrough should have them in order
    for boss in playthroughAllProgression.bosses:
        if boss.mapCheckID in bossIDs.keys():
            bossID = bossIDs.get(boss.mapCheckID)
            bossLevel = bossLevels.pop(0)
            finalNonGoalBossLevel = random.randrange(bossLevel-2,bossLevel+2)
            finalBossLevels.append([remainingBosses.pop(remainingBosses.index(bossID)),random.randrange(bossLevel-2,bossLevel+2)])
            spoilerLog.write(f'\tBoss: {boss.mapCheckID} - Level {finalBossLevels[-1][1]}\n')

            if boss.mapCheckID in ['Clareon','Gargantula','Laspisus','Giasburn','Brachion','Carveros','Pirate Revenant','Oceanus','Basileus','Mephorash']:  #only bosses with psyches flags 
                bossLevelsDictByRegion[boss.locRegion] = finalBossLevels[-1][1] #storing this for use with psyches
        elif boss.mapCheckID == 'Gilkyra Encounter':
            finalBossLevels.append(['M0902', max(random.randrange(bossLevel-4,bossLevel+4), 5)])
    
    # bosses post goal have their levels shuffled from among the remaining levels in the boss level pool
    random.shuffle(bossLevels)
    for bossID in remainingBosses:
        bossLevel = bossLevels.pop(0)
        finalBossLevels.append([bossID,random.randrange(bossLevel-2,bossLevel+2)])
        bossName = [name for name, id in bossIDs.items() if id == bossID][0]
        spoilerLog.write(f'\tBoss: {bossName} - Level {finalBossLevels[-1][1]}\n')

    fscBosses = ''
    fscBossesHP = ''
    script = '\tfunction "bossScaling"\n\t{\n'
    for boss in finalBossLevels:
        script = script + '\t\tSetChrWorkGroup(' + boss[0] + ', CWK_LV, ' + str(boss[1]) + ')\n'

        #balance decision to lower boss HP if there are any bosses before party join, some fights are super tedious in early game if they show up and it's more punishing to lose them than we want for game pacing. 
        if firstPostSecondCharacterBoss == boss[0]:
            soloPartyBoss = False

        if soloPartyBoss and parameters.charMode != 'Past Dana':
            if boss[0] == 'M0111':
                script = script + '\t\tSetChrWork("tu_m0111_01", CWK_MAXHP, (tu_m0111_01.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
                script = script + '\t\tSetChrWork("tu_m0111_01", CWK_HP, (tu_m0111_01.CHRWORK[CWK_MAXHP]))\n'
            elif boss[0] == 'B101B':
                script = script + '\t\tSetChrWork("b101a", CWK_MAXHP, (b101a.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
                script = script + '\t\tSetChrWork("b101a", CWK_HP, (b101a.CHRWORK[CWK_MAXHP]))\n'
                script = script + '\t\tSetChrWork("b101b", CWK_MAXHP, (b101b.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
                script = script + '\t\tSetChrWork("b101b", CWK_HP, (b101b.CHRWORK[CWK_MAXHP]))\n'
                script = script + '\t\tSetChrWork("b101c", CWK_MAXHP, (b101c.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
                script = script + '\t\tSetChrWork("b101c", CWK_HP, (b101c.CHRWORK[CWK_MAXHP]))\n'
                script = script + '\t\tSetChrWork("b101d", CWK_MAXHP, (b101d.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
                script = script + '\t\tSetChrWork("b101d", CWK_HP, (b101d.CHRWORK[CWK_MAXHP]))\n'
                script = script + '\t\tSetChrWork("b101", CWK_MAXHP, (b101.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
                script = script + '\t\tSetChrWork("b101", CWK_HP, (b101.CHRWORK[CWK_MAXHP]))\n'
            elif boss[0] in ['B150','B100']:
                script = script + '\t\tSetChrWorkGroup(' + boss[0] + ', CWK_MAXHP, (' + boss[0] + '.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
                script = script + '\t\tSetChrWorkGroup(' + boss[0] + ', CWK_HP, (' + boss[0] + '.CHRWORK[CWK_MAXHP]))\n'
            else:
                script = script + '\t\tSetChrWork("' + boss[0].lower() + '", CWK_MAXHP, (' + boss[0].lower() + '.CHRWORK[CWK_MAXHP] * '+ str(HPmod) +'))\n'
                script = script + '\t\tSetChrWork("' + boss[0].lower() + '", CWK_HP, (' + boss[0].lower() + '.CHRWORK[CWK_MAXHP]))\n'
                

            #handling special cases for bosses with forms or minions
            if boss[0] == 'B005':
                script = script + '\t\tSetChrWorkGroup(M0644, CWK_MAXHP, (M0644.CHRWORK[CWK_MAXHP] *' + str(HPmod) + '))\n'
                script = script + '\t\tSetChrWorkGroup(M0644, CWK_HP, (M0644.CHRWORK[CWK_MAXHP]))\n'
                script = script + '\t\tSetChrWorkGroup(M0643, CWK_MAXHP, (M0643.CHRWORK[CWK_MAXHP] *' + str(HPmod) + '))\n' #if you can beat these enemies you can reach basileus so scale them too; this is the force garmr required to beat to reach basileus
                script = script + '\t\tSetChrWorkGroup(M0643, CWK_HP, (M0643.CHRWORK[CWK_MAXHP]))\n'
            if boss[0] == 'B170': 
                fscBossesHP = (
                            f'\t\tSetChrWorkGroup(B103,	CWK_MAXHP,	(B103.CHRWORK[CWK_MAXHP] * ' + str(HPmod) + '))\n'
                            f'\t\tSetChrWorkGroup(B103,	CWK_HP,	(B103.CHRWORK[CWK_MAXHP]))\n'
                            f'\t\tSetChrWorkGroup(B006,	CWK_MAXHP,	(B006.CHRWORK[CWK_MAXHP] * ' + str(HPmod) + '))\n'
                            f'\t\tSetChrWorkGroup(B006,	CWK_HP,	(B006.CHRWORK[CWK_MAXHP]))\n'
                            f'\t\tSetChrWorkGroup(B001,	CWK_MAXHP,	(B001.CHRWORK[CWK_MAXHP] * ' + str(HPmod) + '))\n'
                            f'\t\tSetChrWorkGroup(B001,	CWK_HP,	(B001.CHRWORK[CWK_MAXHP]))\n'
                            f'\t\tSetChrWorkGroup(B105,	CWK_MAXHP,	(B105.CHRWORK[CWK_MAXHP] * ' + str(HPmod) + '))\n'
                            f'\t\tSetChrWorkGroup(B105,	CWK_HP,	(B105.CHRWORK[CWK_MAXHP]))\n'
                            f'\t\tSetChrWorkGroup(B161,	CWK_MAXHP,	(B161.CHRWORK[CWK_MAXHP] * ' + str(HPmod) + '))\n'
                            f'\t\tSetChrWorkGroup(B161,	CWK_HP,	(B161.CHRWORK[CWK_MAXHP]))\n'
                            )
    
        #handling special cases for bosses with forms or minions
        if boss[0] == 'B005':
            script = script + '\t\tSetChrWorkGroup(M0644, CWK_LV, ' + str(boss[1]) + ')\n'
            script = script + '\t\tSetChrWorkGroup(M0643, CWK_LV, ' + str(boss[1]-1) + ')\n' #if you can beat these enemies you can reach basileus so scale them too
        if boss[0] == 'B101B':
            script = script + '\t\tSetChrWorkGroup(B101, CWK_LV, ' + str(boss[1]) + ')\n'
        if boss[0] == 'B170': # set FSC bosses relative to Melaiduma if Melaiduma is scaled
            fscBosses = (f'\n\tfunction "fscBosses"\n'
                         f'\t{{\n'
                         f'\t\tSetChrWorkGroup(B103,	CWK_LV,	' + str(max(1,boss[1]-10)) + ')\n'
                         f'\t\tSetChrWorkGroup(B006,	CWK_LV,	' + str(max(1,boss[1]-12)) + ')\n'
                         f'\t\tSetChrWorkGroup(B001,	CWK_LV,	' + str(max(1,boss[1]-14)) + ')\n'
                         f'\t\tSetChrWorkGroup(B105,	CWK_LV,	' + str(max(1,boss[1]-16)) + ')\n'
                         f'\t\tSetChrWorkGroup(B161,	CWK_LV,	' + str(max(1,boss[1]-18)) + ')\n'
                         f'\n' + fscBossesHP + '\n'
                         f'\t}}\n')
                        
    script = script + '\t}'

    return script + fscBosses, finalNonGoalBossLevel, bossLevelsDictByRegion

# ==========================================================================================================
#  Psyche Checkpoint Function
# ==========================================================================================================
#GF_TBOX_DUMMY112 is our flag for release the psyches so these won't get called outside this game mode.
#New version of this script hacks the checkpoint in Castaway Village and uses the boss flags for activation of the custom shop
#The boss menu is essentially a custom shop, it uses Dina's jewel trade menu as a base, there are two version of it depending on game mode
def buildPsyches(settings):
    bossCue = {
        "Psyche-Hydra Psyches": {
            'mapLoad': 'LoadArg("map/mp6305b/mp6305b.arg")',
            'eventCue': 'EventCue("mp6305b:EV_RetryBoss")',
            'mapID': 'MN_D_MP6305b',
            'characterID': 'B112'
        },
        "Psyche-Minos Psyches": {
            'mapLoad': 'LoadArg("map/mp6306b/mp6306b.arg")',
            'eventCue': 'EventCue("mp6306b:EV_RetryBoss")',
            'mapID': 'MN_D_MP6306b',
            'characterID': 'B110'
        },
        "Psyche-Nestor Psyches": {
            'mapLoad': 'LoadArg("map/mp6307b/mp6307b.arg")',
            'eventCue': 'EventCue("mp6307b:EV_RetryBoss")',
            'mapID': 'MN_D_MP6307b',
            'characterID': 'B111'
        },
        "Psyche-Ura Psyches": {
            'mapLoad': 'LoadArg("map/mp6308b/mp6308b.arg")',
            'eventCue': 'EventCue("mp6308b:EV_RetryBoss")',
            'mapID': 'MN_D_MP6308b',
            'characterID': 'B008'
        },
        "Le-Erythos Psyches": {
            'mapLoad': 'LoadArg("map/mp6409b/mp6409b.arg")',
            'eventCue': 'EventCue("mp6409b:EV_RetryBoss")',
            'mapID': 'MN_D_MP6409B',
            'characterID': 'B012'
        },
        "Grazios Psyches": {
            'mapLoad': 'LoadArg("map/mp6519m/mp6519m.arg")',
            'eventCue': 'EventCue("mp6519m:EV_RetryBoss")',
            'mapID': 'MN_D_MP6519M',
            'characterID': 'B161'
        },
        "Nebritia Psyches": {
            'mapLoad': 'LoadArg("map/mp6529m/mp6529m.arg")',
            'eventCue': 'EventCue("mp6529m:EV_RetryBoss")',
            'mapID': 'MN_D_MP6529M',
            'characterID': 'B162'
        },
        "Argura Psyches": {
            'mapLoad': 'LoadArg("map/mp6539m/mp6539m.arg")',
            'eventCue': 'EventCue("mp6539m:EV_RetryBoss")',
            'mapID': 'MN_D_MP6539M',
            'characterID': 'B163'
        },
        "Crusos Psyches": {
            'mapLoad': 'LoadArg("map/mp6549m/mp6549m.arg")',
            'eventCue': 'EventCue("mp6549m:EV_RetryBoss")',
            'mapID': 'MN_D_MP6549M',
            'characterID': 'B011'
        },
        "Blasphima Psyches": {
            'mapLoad': 'LoadArg("map/mp6559m/mp6559m.arg")',
            'eventCue': 'EventCue("mp6559m:EV_RetryBoss")',
            'mapID': 'MN_D_MP6559M',
            'characterID': 'B164'
        },
        "Le-Kyanos Psyches": {
            'mapLoad': 'LoadArg("map/mp6204m/mp6204m.arg")',
            'eventCue': 'EventCue("mp6204m:EV_Boss_Jump")',
            'mapID': 'MN_F_MP6204M',
            'characterID': 'B165'
        },
        "Melaiduma Psyches": {
            'mapLoad': 'LoadArg("map/mp6569/mp6569.arg")',
            'eventCue': 'EventCue("mp6569:EV_RetryBoss")',
            'mapID': 'MN_D_MP6569',
            'characterID': 'B170'
        }
    }
    
    bossFlagDict = {
        "Silent Tower Second Basement Mephorash Psyches": {'FLAG': 'FLAG[GF_SUBEV_06_6413_KILL_BOSS]', 'simpleName': 'Silent Tower Boss'},
        "Valley of Kings Boss Arena Basileus Psyches": {'FLAG': 'FLAG[GF_TBOX_DUMMY080]', 'simpleName': 'Valley of Kings Boss'},
        "Archeozoic Chasm Boss Arena Oceanus Psyches": {'FLAG': 'FLAG[GF_TBOX_DUMMY078]', 'simpleName': 'Archeozoic Chasm Boss'},
        "Pirate Ship Eleftheria Deck Pirate Revenant Psyches": {'FLAG': 'FLAG[GF_05MP0405_READ_REED]', 'simpleName': 'Pirate Ship Boss'},
        "Baja Tower Boss Arena Carveros Psyches": {'FLAG': 'FLAG[GF_05MP6329_KILL_BAHABOSS]', 'simpleName': 'Baja Tower Boss'},
        "Temple of the Great Tree Temple Boss Arena Brachion Psyches": {'FLAG': 'FLAG[GF_04MP6410_KILL_GUARDIAN]', 'simpleName': 'Temple of the Great Tree Boss'},
        "Mont Gendarme Boss Arena Giasburn Psyches": {'FLAG': 'FLAG[GF_03MP4341_KILL_ANCIENT]', 'simpleName': 'Mont Gendarme Boss'},
        "Schlamm Jungle Boss Arena Laspisus Psyches": {'FLAG': 'FLAG[GF_02MP2308_KILL_HIPPO]', 'simpleName': 'Schlamm Jungle Boss'},
        "Eroded Valley Boss Arena Gargantula Psyches": {'FLAG': 'FLAG[GF_TBOX_DUMMY074]', 'simpleName': 'Eroded Valley Boss'},
        "Towering Coral Forest Boss Arena Clareon Psyches": {'FLAG': 'FLAG[GF_02MP1308_KILL_CHAMELEON]', 'simpleName': 'Towering Coral Forest Boss'},
        "Former Sanctuary Crypt - Final Floor Boss Arena Melaiduma Psyches": {'FLAG': 'FLAG[GF_SUBEV_UNTOUCHABLE]', 'simpleName': 'Former Sanctuary Crypt Boss'}
    }
    
    psycheFlag = {
        "Psyches of the Sky Era": "GF_06MP6308_TALK_SARAI",
        "Psyches of the Insectoid Era": "GF_06MP6307_TALK_NESTOR",
        "Psyches of the Ocean Era": "GF_06MP6305_TALK_HYDRA",
        "Psyches of the Frozen Era": "GF_06MP6306_TALK_MINOS"
    }
    
    # Build warden scaling once
    wardenScaling = 'SetChrWork("b012", CWK_MAXHP, (b012.CHRWORK[CWK_MAXHP] * 3.0f))\nSetChrWork("b012", CWK_HP, (b012.CHRWORK[CWK_MAXHP]))\n'
    if settings['options']['former_sanctuary_crypt'] == 0:
        wardenScaling += 'SetChrWork(B170, CWK_LV, 65)\n'
    
    bossCheckpoint = (
        '\n'
        'function "bossCheckpoint"\n'
        '{\n'
        '\tSetStopFlag(STOPFLAG_TALK)\n'
        '\tSetFlag(TF_MENU_SELECT2, 0)\n'
        '\tMenuReset()\n'
        '\tMenuType(MENUTYPE_POPUP)\n'
        '\t//--------------------------------------------------------------------------------------\n'
    )
    bossLoad = ""
    bossReturn = ""
    menuEnableList = []
    
    rewards = settings['psyche_rewards']
    
    # Single pass: build all three script sections together
    for i, (psyche, accessBoss) in enumerate(settings['psyche_map'].items()):
        menuId = 10 + (i * 10)
        menuIdDisabled = menuId + 1
        condition = "if" if i == 0 else "else if"
        
        flagKey = psycheFlag[rewards[psyche]]
        simpleName = bossFlagDict[accessBoss]["simpleName"]
        bossName = psyche[:psyche.rfind(" ")]
        
        formattedPsyche = f"{simpleName}:{rewards[psyche]}({bossName})"
        enabledFormattedPsyche = f"{GOLD}{formattedPsyche}"
        
        # Build all three together
        bossCheckpoint += (
            f"\n"
            f"\tif({bossFlagDict[accessBoss]['FLAG']} && !FLAG[{flagKey}])\n"
            f"\t{{\n"
            f"\t\tMenuAdd({menuId}, \"{enabledFormattedPsyche}\")\n"
            f"\t}}\n"
            f"\telse if(!{bossFlagDict[accessBoss]['FLAG']} || FLAG[{flagKey}])\n"
            f"\t{{\n"
            f"\t\tMenuAdd({menuIdDisabled}, \"{formattedPsyche}\")\n"
            f"\t}}"
        )
        
        bossLoad += (
            f"\n"
            f"\t{condition}(FLAG[TF_MENU_SELECT2] == {menuId})\n"
            f"\t{{\n"
            f"\t\tMenuClose(10, 0)\n"
            f"\t\tSetFlag(GF_TBOX_DUMMY127,1)\n\t\tGetItem(ICON3D_831,1)\n"
            f"\t\t{bossCue[psyche]['mapLoad']}\n"
            f"\t\t{bossCue[psyche]['eventCue']}\n\t\tWaitFade()\n"
            f"\t}}"
        )
        
        bossReturn += (
            f"\n"
            f"\t{condition}(WORK[WK_MAPNAMENO] == {bossCue[psyche]['mapID']})\n"
            f"\t{{\n"
            f"\t\tSetFlag({flagKey},1)\n"
            f"\t}}"
        )
        
        menuEnableList.append(menuIdDisabled)
    
    # Finish building the full script
    bossCheckpoint += '\n\t//--------------------------------------------------------------------------------------\n'
    for menuId in menuEnableList:
        bossCheckpoint += f'\n\t\tMenuEnable({menuId}, 0)'
    
    bossCheckpoint += (
        '\n'
        '\n'
        '\tMenuOpen(TF_MENU_SELECT2, 283, ADOLMENU_PPOSY, -2, -2, 10, 1)\n'
        '\tWaitMenu(0)\n'
        '\tCloseMessage(6,0)\n'
        '\tWaitCloseMessage(6)\n'
        '\tMenuClose(10, 0)\n'
        '\n'
        + bossLoad + '\n'
        '\tResetStopFlag(STOPFLAG_TALK)\n'
        '}\n'
        '\n'
        'function "wardenScaling"\n'
        '{\n'
        f'\t{wardenScaling}\n'
        '}\n'
        '\n'
        'function "bossReturn"\n'
        '{\n'
        '\tSetFlag(SF_BOSS_BATTLE, 0)\n'
        + bossReturn + '\n'
        '\tLoadArg("map/mp1201/mp1201.arg")\n'
        '\tEventCue("mp1201:EV_M01S080_ED")\n'
        '}\n'
    )
    
    return bossCheckpoint

# ==========================================================================================================
#  FSC Checkpoint Function
# ==========================================================================================================
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
# ==========================================================================================================
#  Dina's Shop Function (Jewel Trade)
# ==========================================================================================================
def jewelTrade(locations):
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
    item_names = [locations[str(i)]['item_name'] + ("(!)" if 'PROGRESSION' in locations[str(i)]['item_classification'] else "") for i in range(461, 471)]
    return script.format(*item_names)

# ==========================================================================================================
#  Shop Self Hints: Dogi, Master Kong, Shoebill, Austin, Mishy, and Euron
# ==========================================================================================================
#function to give hints for long checks, NPCs will tell you once the check is unlocked what is behind it
def talkHints(locations):
    # Map location names to (array_index, item_index) for cleaner population
    location_map = {
        # Intercept Rewards
        "Calm Inlet Intercept Stage 2": (0, 0),
        "Calm Inlet Intercept Stage 3": (0, 1),
        "Calm Inlet Intercept Stage 5": (0, 2),
        "Calm Inlet Intercept Stage 7": (0, 3),
        "Calm Inlet Intercept Stage 9": (0, 4),
        # Master Kong Rewards
        "Roaring Seashore Parasequoia Master Kong Skill Ricotta": (1, 0),
        "Sunrise Beach Sunrise Beach Master Kong Skill Sahad": (1, 1),
        "Odd Rock Coast Odd Rock Coast Master Kong Skill Dana": (1, 2),
        "Mont Gendarme Mid-Boss Arena Master Kong Skill Laxia": (1, 3),
        "Pangaia Plains Ancient Tree Master Kong Skill Hummel": (1, 4),
        "Vista Ridge Vista Ridge Lower Master Kong Skill Adol": (1, 5),
        "Vista Ridge Vista Ridge Lower Master Kong Join": (1, 6),
        # Fish Rewards
        "Calm Inlet Fish Trade Fish 4": (2, 0),
        "Calm Inlet Fish Trade Fish 8": (2, 1),
        "Calm Inlet Fish Trade Fish 12": (2, 2),
        "Calm Inlet Fish Trade Fish 16": (2, 3),
        "Calm Inlet Fish Trade Fish 20": (2, 4),
        "Calm Inlet Fish Trade Fish 24": (2, 5),
        # Discovery Rewards
        "Calm Inlet Discovery Rewards Half": (3, 0),
        "Calm Inlet Discovery Rewards All": (3, 1),
        # Map Rewards
        "Calm Inlet Map Completion Percent 10": (4, 0),
        "Calm Inlet Map Completion Percent 20": (4, 1),
        "Calm Inlet Map Completion Percent 30": (4, 2),
        "Calm Inlet Map Completion Percent 40": (4, 3),
        "Calm Inlet Map Completion Percent 50": (4, 4),
        "Calm Inlet Map Completion Percent 60": (4, 5),
        "Calm Inlet Map Completion Percent 70": (4, 6),
        "Calm Inlet Map Completion Percent 80": (4, 7),
        "Calm Inlet Map Completion Percent 90": (4, 8),
        "Calm Inlet Map Completion Percent 100": (4, 9),
        # Food Rewards
        "Mont Gendarme Mishy Rewards Food 2": (5, 0),
        "Mont Gendarme Mishy Rewards Food 4": (5, 1),
        "Mont Gendarme Mishy Rewards Food 6": (5, 2),
        "Mont Gendarme Mishy Rewards Food 8": (5, 3),
        "Mont Gendarme Mishy Rewards Food 10": (5, 4),
        "Mont Gendarme Mishy Rewards Food 12": (5, 5),
    }
    
    # Create all reward arrays
    rewards = [
        [None] * 5,   # intReward
        [None] * 7,   # mkRewards
        [None] * 6,   # fishRewards
        [None] * 2,   # discoveryRewards
        [None] * 10,  # mapRewards
        [None] * 6,   # foodRewards
    ]
    
    # Populate from locations using the map
    for location in locations.values():
        if location['location_name'] in location_map:
            array_idx, item_idx = location_map[location['location_name']]
            rewards[array_idx][item_idx] = location['item_name'] + ("(!)" if 'PROGRESSION' in location['item_classification'] else "")
    
    intReward, mkRewards, fishRewards, discoveryRewards, mapRewards, foodRewards = rewards
    
    # Rest of the function (dogiHints, ricottaHints, etc.) remains the same...
    dogiHints = """
function "interceptRewardPreview"
{{
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
    """.format(*intReward)
    
    ricottaHints = """
function "mkRewardsPreview"
{{
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
    """.format(*mkRewards)
    
    shoebillHints = """
function "fishRewardPreview"
{{
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
    """.format(*fishRewards)

    austinHints = """
function "discoveryRewardPreview1"
{{
    TalkPopup("Austin",0,2,0,0,0)
    {{
        "Hmmmm...." 
        "I could really use some inspiration."
        "If you find something interesting, "
        "maybe you could share it with me?"
        "I'd be happy to offer the following in return."
    }}
    WaitPrompt()
    WaitCloseWindow()

    TalkPopup("Austin",0,2,0,0,0)
    {{
        "#2C {0}#0C for a little inspiration."
        "#2C {1}#0C for a lot of inspiration."
    }}

    WaitPrompt()
    WaitCloseWindow()
}}

function "discoveryRewardPreview2"
{{
    TalkPopup("Austin",0,2,0,0,0)
    {{
        "Splendid work!" 
        "Keep it up and I'll happily share this with you!"
    }}
    WaitPrompt()
    WaitCloseWindow()

    TalkPopup("Austin",0,2,0,0,0)
    {{
        "#2C {1}#0C for a lot of inspiration."
    }}

    WaitPrompt()
    WaitCloseWindow()
}}
    """.format(*discoveryRewards)

    euronHints = """
function "mapRewardPreview"
{{
    TalkPopup("Euron",0,2,0,0,0)
    {{
        "Hey there!" 
        "Show me that map as you explore and "
        "I'll offer you some of my collection."
        "Let's see here....."
    }}
    WaitPrompt()
    WaitCloseWindow()

    TalkPopup("Euron",0,2,0,0,0)
    {{
        "This is what I got for you!"
        "#2C {0}#0C for 10% map completion."
        "#2C {1}#0C for 20% map completion."
        "#2C {2}#0C for 30% map completion."
        "#2C {3}#0C for 40% map completion."
        "#2C {4}#0C for 50% map completion."
    }}
    WaitPrompt()
    WaitCloseWindow()

    TalkPopup(UNDEF,0,2,0,0,0)
    {{
        "#2C {5}#0C for 60% map completion."
        "#2C {6}#0C for 70% map completion."
        "#2C {7}#0C for 80% map completion."
        "#2C {8}#0C for 90% map completion."
        "#2C {9}#0C for 100% map completion."
    }}
    WaitPrompt()
    WaitCloseWindow()
}}
    """.format(*mapRewards)

    mishyHints = """
function "foodRewardPreview"
{{
    TalkPopup(UNDEF,0,3,STOPPER_PPOSX,STOPPER_PPOSY,0)
    {{
        "(Mishy shows you his stash, maybe he'll share" 
        "some of it if you keep bringing him food?)"
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
    """.format(*foodRewards)

    return dogiHints + '\n' + ricottaHints + '\n' + shoebillHints + '\n' + austinHints + '\n' + euronHints + '\n' + mishyHints

# ==========================================================================================================
#  Conditions for accessing the Octus Entrance from Temple of the Great Tree Garden
# ==========================================================================================================
#setting for when the great tree of origins entrance opens
def octusGoal(options):
    # Map mode to (template, param_key)
    scripts = {
        0: (
            '\n'
            'function "openTree"\n'
            '{\n'
            f'\tif(WORK[WK_NPCNUM] >= {str(options["octus_count_crew_mode"])} && !FLAG[GF_06MP6409_OPEN_GATE])\n'
            '\t{\n'
            '\t\tSetFlag(GF_06MP6409_OPEN_GATE, 1)\n'
            '\t\tCallFunc("mp6409:init")\n'
            '\t}\n'
            '}\n'
        ),
        1: (
            '\n'
            'function "openTree"\n'
            '{\n'
            '\tSetFlag(GF_06MP6409_OPEN_GATE, 1)\n'
            '\tCallFunc("mp6409:init")\n'
            '}\n'
        ),
        2: (
            '\n'
            'function "openTree"\n'
            '{\n'
            f'\tif(ALLITEMWORK[ICON3D_831] >= {str(options["octus_count_psyches_mode"])} && !FLAG[GF_06MP6409_OPEN_GATE])\n'
            '\t{\n'
            '\t\tSetFlag(GF_06MP6409_OPEN_GATE, 1)\n'
            '\t\tCallFunc("mp6409:init")\n'
            '\t}\n'
            '}\n'
        ),
        3: (
            '\n'
            'function "openTree"\n'
            '{\n'
            '\tSetFlag(GF_06MP6409_OPEN_GATE, 1)\n'
            '\tCallFunc("mp6409:init")\n'
            '}\n'
        ),
    }

    return scripts[options['final_boss_access']]

# ==========================================================================================================
#  Conditions for accessing the warp to the final boss from the Selection Sphere
# ==========================================================================================================
#Our goals for entering the selection sphere
def goal(options):
    goal_mode = options['final_boss_access']
    
    # Map mode to (condition, parameter_if_needed)
    scripts = {
        0: ('WORK[WK_NPCNUM] < ' + str(options['goal_count_crew_final_boss'])),
        1: ('!ALLITEMWORK[ICON3D_SHIP_PLAN] || !ALLITEMWORK[ICON3D_SEIREN_CHART] || !FLAG[GF_TBOX_DUMMY071]'),
        2: ('ALLITEMWORK[ICON3D_831] < ' + str(options['goal_count_psyches_final_boss'])),
        3: ('!FLAG[GF_SUBEV_UNTOUCHABLE]'),
    }
    
    condition = scripts[goal_mode]
    
    script = (
        '\n'
        'function "goal"\n'
        '{\n'
        f'\tif({condition})\n'
        '\t{\n'
        '\t\tSetChrWork("LP_warpin_mp6310b", CWK_CHECKOFF, 1)\n'
        '\t\tSetChrPos("b020",-100000.00f,0.00f,0.00f)\n'
        '\t}\n'
        '}\n'
    )
    
    return script

# ==========================================================================================================
#  Randomize Octus Bosses and levels, also make them more rewarding.
# ==========================================================================================================
def octoBosses(settings):
    random.seed(settings['seed'])
    octoBossAliases = ['"ev_mons01"','"ev_mons02"','"ev_mons03"','"ev_mons04"','"ev_mons05"','"ev_mons06"','"ev_mons07"','"ev_mons08"','"ev_mons09"','"ev_mons10"']
    #octus bosses exp and HP go up based on bosses leading into the end game. This is to help prep for the final boss.
    #the HP mod is just a percentage of a rough approcimation of the highest level the final boss could get to if unlucky.
    HPmod = 0.75
    EXPMod = 8.0
    script = 'function "setOctoBossLevels"\n\t{\n'
    for boss in octoBossAliases:
        bossLevel = random.randrange(65,75)
        script += (
            f'\t\tSetLevel({boss}, {bossLevel})\n'
            f'\t\tSetChrWork({boss}, CWK_MAXHP, ({boss}.CHRWORK[CWK_MAXHP] * {HPmod}))\n'
            f'\t\tSetChrWork({boss}, CWK_HP, ({boss}.CHRWORK[CWK_MAXHP]))\n'
            f'\t\tSetChrWorkGroup({boss}, CWK_EXPMUL, {EXPMod}f)\n'
        )
    script += '\t}\n'

    randomizeOctoBosses(settings)

    return script

# ==========================================================================================================
#  Handle the scripts for the final boss and ending cutscenes based on what phases and bosses we're doing.
# ==========================================================================================================
#This sorts out our final boss settings.
#First we figure out what phases we're doing then we run through our script that's called to start the final boss and what's used to call the ending cutscenes.
#if we're only doing theos then the theos start script calls theos and the ending script calls the ending cutscene.
#if we're doing both then the ending cutscene script instead calls origin.
#if we're only doing origin then the theos start script calls the origin boss fight.
#for Past Dana we only load the Io fight
def endingHandler(options):
    # if options.charMode == 'Past Dana':
    #     ioFightLoad = """
    # function "finalBoss"
    # {
    #     LoadArg("map/mp6569m/c.arg")
	#     EventCue("mp6569m:EV_RetryBoss")
    # }
    # """
    #     return ioFightLoad + finalBossLevelScript
    # leaving here in case we add something later and so we don't need to update the script for the selection sphere.

    # Phase mappings
    theos_phases = {
        1: '',
        2: 'SetFlag(GF_MP6310B_ENDROGRAM_STEP,1)',
        3: 'SetFlag(GF_MP6310B_ENDROGRAM_STEP,2)'
    }
    
    origin_phases = {
        1: '',
        2: 'SetFlag(GF_MP8323_2NDBATTLE,1)'
    }
    
    # Care package mappings
    packages = {
        0: "",
        1: (
            "GetItem(ICON3D_US_BERRY_S,5)\n"
            "GetItem(ICON3D_US_COCONUT_S,5)\n"
            "GetItem(ICON3D_US_MANGO_S,5)\n"
            "GetItem(ICON3D_US_DRAGONFRUIT_S,5)\n"
            "GetItem(ICON3D_USFD_FOOD15,1)\n"
            "GetItem(ICON3D_US_RESSURECT_02,1)\n"
            "GetItem(ICON3D_US_EXTRA_02,1)"
        ),
        2: (
            "GetItem(ICON3D_US_BERRY_S,9)\n"
            "GetItem(ICON3D_US_COCONUT_S,9)\n"
            "GetItem(ICON3D_US_MANGO_S,9)\n"
            "GetItem(ICON3D_US_DRAGONFRUIT_S,9)\n"
            "GetItem(ICON3D_USFD_FOOD15,9)\n"
            "GetItem(ICON3D_USFD_FOOD03,9)\n"
            "GetItem(ICON3D_US_RESSURECT_02,9)\n"
            "GetItem(ICON3D_US_EXTRA_02,2)"
        )
    }
    
    theos_phase = theos_phases[options['theos_start_phase']]
    origin_phase = origin_phases[options['origin_start_phase']]
    package = packages[options['origin_care_package']]
    
    # Final boss scripts
    boss_scripts = {
        0: (  # Theos only
            (
                '\n'
                'function "finalBoss"\n'
                '{\n'
                f'\t{theos_phase}\n'
                '\tLoadArg("map/mp6310b/mp6310b.arg")\n'
                '\tEventCue("mp6310b:EV_M06S240")\n'
                '}\n'
            ),
            (
                '\n'
                'function "ending"\n'
                '{\n'
                '\tLoadArg("map/mp0021/mp0021.arg")\n'
                '\tEventCue("mp0021:EV_M07S130")\n'
                '\tSetFlag(GF_TBOX_DUMMY120,1)\n'
                '}\n'
                'function "ending2"\n'
                '{\n'
                '\tLoadArg("map/mp0021/mp0021.arg")\n'
                '\tEventCue("mp0021:EV_M07S130")\n'
                '\tSetFlag(GF_TBOX_DUMMY120,1)\n'
                '}\n'
            )
        ),
        1: (  # Origin only
            (
                '\n'
                'function "finalBoss"\n'
                '{\n'
                f'\t{origin_phase}\n'
                '\tLoadArg("map/mp8323/mp8323.arg")\n'
                '\tEventCue("mp8323:init")\n'
                '}\n'
            ),
            (
                '\n'
                'function "ending"\n'
                '{\n'
                '\tLoadArg("map/mp0021/mp0021.arg")\n'
                '\tEventCue("mp0021:EV_M07S130")\n'
                '\tSetFlag(GF_TBOX_DUMMY120,1)\n'
                '}\n'
                'function "ending2"\n'
                '{\n'
                '\tLoadArg("map/mp0021/mp0021.arg")\n'
                '\tEventCue("mp0021:EV_M07S130")\n'
                '\tSetFlag(GF_TBOX_DUMMY120,1)\n'
                '}\n'
            )
        ),
        2: (  # Both (Theos -> Origin)
            (
                '\n'
                'function "finalBoss"\n'
                '{\n'
                f'\t{theos_phase}\n'
                '\tLoadArg("map/mp6310b/mp6310b.arg")\n'
                '\tEventCue("mp6310b:EV_M06S240")\n'
                '}\n'
            ),
            (
                '\n'
                'function "ending"\n'
                '{\n'
                f'\t{origin_phase}\n'
                f'\t{package}\n'
                '\tLoadArg("map/mp8323/mp8323.arg")\n'
                '\tEventCue("mp8323:init")\n'
                '}\n'
                'function "ending2"\n'
                '{\n'
                '\tLoadArg("map/mp0021/mp0021.arg")\n'
                '\tEventCue("mp0021:EV_M07S130")\n'
                '\tSetFlag(GF_TBOX_DUMMY120,1)\n'
                '}\n'
            )
        )
    }
    
    theos_script, ending_script = boss_scripts[options['final_boss']]
    
    finalBossLevelScript = (
        '\n'
        'function "finalBossLevel"\n'
        '{\n'
        '}\n'
    )
    
    return theos_script + ending_script + finalBossLevelScript

# ==========================================================================================================
#  Exp Muiltiplier handling and scaled exp items.
# ==========================================================================================================
# we're doing away with this old method and simplifying everything. Max exp is a character stat in this game and the status file contains an editable version of it.
# so instead of the old method we're going to call a function to divide the character's max exp by our multiplier.
# this achives the same effect as a global exp multiplier in a far cleaner way than our old method.
# there is no growth rate anymore because honestly a lot of what it was going for is achieved through boss level scaling better
def expMult(options):
    import re
    newExpMult(options['experience_multiplier'])

    if options['scale_exp_items'] == 1:
        item1 = 100//options['experience_multiplier']
        item2 = 1000//options['experience_multiplier']
        item3 = 10000//options['experience_multiplier']
    else:
        item1 = 100
        item2 = 1000
        item3 = 10000

    # Update scaled exp values in item.scp
    itemScpPath = os.path.join(config.executable_directory, 'script', 'item.scp')
    
    with open(itemScpPath, 'r', encoding='Shift-JIS', errors='surrogateescape') as itemFile:
        content = itemFile.read()
    
    # Find and replace GetExp values in each function
    # it_expup1 gets item1 value - pattern: function it_expup1 ... GetExp(100)
    content = re.sub(
        r'(function\s+it_expup1\s*\{.*?GetExp\()(\d+)(\))',
        r'\g<1>' + str(item1) + r'\g<3>',
        content,
        flags=re.DOTALL
    )
    
    # it_expup2 gets item2 value - pattern: function it_expup2 ... GetExp(1000)
    content = re.sub(
        r'(function\s+it_expup2\s*\{.*?GetExp\()(\d+)(\))',
        r'\g<1>' + str(item2) + r'\g<3>',
        content,
        flags=re.DOTALL
    )
    
    # it_expup3 gets item3 value - pattern: function it_expup3 ... GetExp(10000)
    content = re.sub(
        r'(function\s+it_expup3\s*\{.*?GetExp\()(\d+)(\))',
        r'\g<1>' + str(item3) + r'\g<3>',
        content,
        flags=re.DOTALL
    )
    
    with open(itemScpPath, 'w', encoding='Shift-JIS', errors='surrogateescape') as itemFile:
        itemFile.write(content)

# ==========================================================================================================
#  The remaining functions are called from other functions and used to help with item and flag management.
# ==========================================================================================================
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
    scripts = {
        698: (  # 'Maiden Journal'
            'if(!FLAG[GF_03MP1101_LEAVE_CAMP] ) //primordial passage access\n'
            '{\n'
            '\tSetFlag(GF_TBOX_DUMMY131, 1) // activate load zone to pinnacle from temple approach\n'
            '\tSetFlag(GF_03MP1101_LEAVE_CAMP,1)\n'
            '}\n'
        ),
        700: (  # 'Blue Seal of Whirling Water'
            'if(!FLAG[GF_04MP5101_OUT_CAMP]) //ruins of eternia access\n'
            '{\n'
            '\tSetFlag( GF_04MP5101_OUT_CAMP, 1 )\n'
            '\tSetFlag(GF_04MP6401M_GO_MP6101M,1)\n'
            '\tSetFlag( GF_04MP6101_MAKE_CAMP, 1 )\n'
            '\tSetFlag( GF_04MP6101_CRYSTAL_FLASH, 1 )\n'
            '\tSetFlag(GF_SUBEV_PAST_01_GIMMICK_A,1) // Past Part I: Achieved [Past Gimmick : Waterway Repair]\n'
            '\tSetFlag(GF_SUBEV_PAST_01_GIMMICK_C,1) // Past episode I: Viewed [Past gimmick: Reflection in modern version]\n'
            '\tSetFlag(GF_SUBEV_PAST_01_LP_1ST,1) // Past Part I: [LP: Bookshelf in Dana\'s Room] First time\n'
            '}\n'
        ),
        701: (  # 'Green Seal of Roaring Stone'
            'if(!FLAG[GF_04MP6201_DIS_OBSTACLE]) //temple of the great tree access\n'
            '{\n'
            '\tSetFlag(GF_04MP6201_DIS_OBSTACLE,1)\n'
            '\tSetFlag(GF_SUBEV_PAST_02_GIMMICK_A, 1) // Past Part II: Watched the event [Past Gimmick : Listen to the story of the key]\n'
            '\tSetFlag(GF_SUBEV_PAST_02_GIMMICK_B, 1)// Past Part II: [Past Gimmick : Listen to the story about the key] Opened the door\n'
            '\tSetFlag(GF_SUBEV_PAST_02_FIRECNT_A, 1)// Past Part II: [Past Quest E: Examine the light on the statue] Light the three candlesticks\n'
            '\tSetFlag(GF_SUBEV_PAST_02_FIRECNT_B, 1)// Past Part II: [Past Quest E: Examine the light on the statue] Light the three candlesticks\n'
            '\tSetFlag(GF_SUBEV_PAST_02_FIRECNT_C, 1)// Past Part II: [Past Quest E: Examine the light on the statue] Light the three candlesticks\n'
            '}\n'
        ),
        702: (  # 'Golden Seal of Piercing Light'
            'if(!FLAG[GF_05MP6201M_GOTO_BAHA]) //baja tower access\n'
            '{\n'
            '\tSetFlag(GF_05MP6201M_GOTO_BAHA,1)\n'
            '\tSetFlag(GF_SUBEV_PAST_03_GIMMICK_L,1) // Watched Past Edition III: [Past Gimmick : Helping Animals]\n'
            '\tSetFlag(GF_SUBEV_PAST_03_GIMMICK_A, 2) // Past Edition III: Achieved [Past Gimmick: Helping animals]\n'
            '\tSetFlag(GF_SUBEV_PAST_03_GIMMICK_B, 1) // Viewed past edition III: [Past gimmick : Reflection in modern edition]\n'
            '\tSetFlag(GF_GET_GRATICA, 1)\n'
            '}\n'
        ),
        699: (  # 'Frozen Flower'
            'if(!FLAG[GF_05MP6204_APPEAR_CASTLE]) //chasm access\n'
            '{\n'
            '\tSetFlag(GF_05MP6204_APPEAR_CASTLE,1)\n'
            '\tSetFlag(GF_SUBEV_PAST_04_GIMMICK_L, 1)// Watched Past Chapter IV: [Past Gimmick : Repairing the Great Monastery Door]\n'
            '\tSetFlag(GF_SUBEV_PAST_04_GIMMICK, 2)// Past Part IV: Achieved [Past Gimmick : Repairing the door of the Great Monastery]\n'
            '\tSetFlag(GF_OPEN_FLOOR_02,1) //I saw a prediction that the second floor would open.\n'
            '}\n'
        ),
        796: (  # 'Treasure Chest Key'
            'if(!FLAG[GF_05MP6105_GOTO_VALLAY]) //lodinia marsh back half access\n'
            '{\n'
            '\tSetFlag(GF_05MP6105_GOTO_VALLAY,1)\n'
            '\tSetFlag(GF_OPEN_FLOOR_03,1) //I saw a prediction that the third floor would open.\n'
            '\tSetFlag(GF_GET_LUMINOUS,1)\n'
            '}\n'
        ),
        727: (  # 'Shrine Maiden Amulate'
            'if(!FLAG[GF_SUBEV_PAST_06_GIMMICK_A]) //hill of eternity\n'
            '{\n'
            '\tSetFlag(GF_SUBEV_PAST_06_GIMMICK_A,1) // Watched Past Edition VI: [Past Gimmick : Discovered Poisonous Swamp]\n'
            '\tSetFlag(GF_SUBEV_PAST_06_GIMMICK_B,1)// Past Chapter VI: Moved the meteor fragment with [Past Gimmick : Purification of Poisonous Swamp]\n'
            '\tSetFlag(GF_SUBEV_PAST_06_GIMMICK_C,1) // Watched past edition VI: [Past gimmick : Reflection in modern edition]\n'
            '\tSetFlag(GF_OPEN_FLOOR_04, 1) //I saw a prediction that the 4th floor would open.\n'
            '\tSetFlag(GF_OPEN_FLOOR_05, 1) //I saw a prediction that the 5th floor would open.\n'
            '}\n'
        ),
    }
    
    return scripts.get(pastItem, '')

#Sword of Psyches event. Adol gets Mistletein(probably mispelled that)
#we make sure the weapon is equipped here when it is received, if progressive super items we just set the flag for haivng received it so Kathleen will know the upgrade can happen at shop rank max 
def sopEvent(options):
    if options["progressive_super_items"] == 1:
        script = "\tSetFlag(GF_TBOX_DUMMY071,1)\n"
    else:
        script = (
	        "\tGetItem(ICON3D_WP_ADOL_008,1)\n"
	        "\tEquipWeapon(ADOL,ICON3D_WP_ADOL_008)\n"
	        "\tSetFlag(GF_TBOX_DUMMY071,1)\n"
        )
    return script

#dana spirit ring
def spiritRingEvent(options):
    if options["progressive_super_items"] == 1:
        script = "\tSetFlag(GF_TBOX_DUMMY108,1)\n"
    else:
        script = (
	        "\tGetItem(ICON3D_WP_DANA_005,1)\n"
	        "\tEquipWeapon(DANA,ICON3D_WP_DANA_005)\n"
	        "\tSetFlag(GF_TBOX_DUMMY108,1)\n"
        )
    return script

#this builds out all our intercept rewards, it's called every time we return from an intercept in castaway village by checking the flags for last stage rank and stage clear
def interceptionHandler(options):

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

    if options['additional_intercept_rewards'] == 1:
        interceptionRewards = getIntRewards()
        for stage in interceptionRewards:
            stageCheck = """
            if (FLAG[GF_INTERCEPT_LASTSTAGEID] == {0})
            {{
                SetStopFlag(STOPFLAG_TALK)

    """
            script = script + stageCheck.format(stage.stage)

            if options['additional_intercept_rewards'] == 1:
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
                        script = script + rewardGet.format(item,itemNum,OBTAINED_ITEM_MESSAGE)
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

# ==========================================================================================================
# Helper functions
# ==========================================================================================================
def makeFileSafeItemName(itemName):
    replacements = {'#': ' ', '\\': '_', '/': '_', '"': "'"}
    for old, new in replacements.items():
        itemName = itemName.replace(old, new)
    return itemName

def buildMessage(itemId, itemName, classification, player, message_type=None, isParty=False, characterName=None):
    itemName = makeFileSafeItemName(itemName)
    
    if itemId == AP_ITEM:
        # Map classification to color
        color_map = {
            'PROGRESSION': PINK,
            'USEFUL': PURPLE,
            'TRAP': ORANGE,
        }
        color = color_map.get(classification, BLUE)
        return f"Sent {color}{itemName}{WHITE} to {GOLD}{player}."
    
    # Map message_type to message template
    message_map = {
        'landmark': f"{GOLD}{itemName}{GREEN}{LANDMARK_MESSAGE}",
        'castaway': f"{GOLD}{itemName}{GREEN}{'PARTY_MESSAGE' if isParty else CREW_MESSAGE}",
        'skill': f"{GREEN}{characterName}{SKILL_MESSAGE}{itemName}{GREEN}.",
    }
    
    return message_map.get(message_type, OBTAINED_ITEM_MESSAGE)

def formatGetItemScript(location_id, loc_data, eventScripts, message_type=None, isParty=False):
    itemName = loc_data['item_name']
    itemQuantity = loc_data['item_quantity']
    
    if message_type in ITEM_TYPE_CONFIG:
        config = ITEM_TYPE_CONFIG[message_type]
        itemIcon = config['icon']
        itemId = config['id']
        if config['needs_skill_info']:
            skillInfo = getSkillInfo(itemName)
            character, skillID, characterName = skillInfo
    else:
        itemId = int(loc_data['item_id'])
        itemIcon = getIcon(itemId) if itemId != AP_ITEM else -1

    requiresScript = itemId in [AP_ITEM, LANDMARK_ITEM, CASTAWAY_ITEM, SKILL_ITEM, PROGRESSIVE_SHOP_RANK_ITEM]

    # If there is no script and it's a chest location and isn't an AP Item then we return and small empty script to avoid errors.
    # Chests always point to a script because of the patcher so we need something and this will create a blank one.
    # We still need to fill the chest though.
    if (eventScripts == "" and location_id not in TREASURE_SCRIPTS.keys() 
        and loc_data['location_type'] in ['chest', 'fsc_chest'] and 
        not requiresScript): 
        fillChest(location_id,itemId,itemQuantity)
        return f"\nfunction \"{buildLocScripts(location_id,False)}\"\n{{\n}}\n"
    
    scriptName = buildLocScripts(location_id,False)
    player = loc_data['player'] if loc_data['player'] else ""
    classification = loc_data['item_classification'] if loc_data['item_classification'] else ""
    locationIsEvent = loc_data['location_type'] in ['event', 'landmark', 'fsc_event']

    message = buildMessage(itemId,itemName,classification,player,message_type,isParty,
                           characterName if message_type == 'skill' else None)

    if message_type == 'skill':
        getItem = f"\tGetSkill({character},{skillID},1)\n"
    elif itemId in [AP_ITEM, PROGRESSIVE_SHOP_RANK_ITEM] or not locationIsEvent:
        getItem = ""
    else:
        getItem = f"\tGetItem({itemIcon},{itemQuantity})\n"

    #overflow handling for progressive shop ranks.
    if itemId == PROGRESSIVE_SHOP_RANK_ITEM:
        getItemMessage = (
            f"\tif (ALLITEMWORK[{itemIcon}] >= 8)\n"
            f"\t{{\n"
            f"\t\tGetItem(ICON3D_MT_N4_STONE,5)\n"
            f"\t\tGetItemMessageExPlus(ICON3D_MT_N4_STONE,5,{ITEM_SOUND},\"{message}\",0,0)\n"
            f"\t\tDelteItem({itemIcon},{itemQuantity})\n" # We delete the shop rank so the shop rank trackers shows correctly
            f"\t\tWaitPrompt()\n"
            f"\t\tWaitCloseWindow()\n"
            f"\t}}\n"
            f"\telse\n"
            f"\t{{\n"
            f"\t\tGetItem({itemIcon},{itemQuantity})\n"
            f"\t\tGetItemMessageExPlus({itemIcon},{itemQuantity},{ITEM_SOUND},\"{message}\",0,0)\n"
            f"\t\tWaitPrompt()\n"
            f"\t\tWaitCloseWindow()\n"
            f"\t}}\n"
        )
    #if it's an event location or a landmark or castaway reward or skill reward we want the message to be in the event script instead of the chest script
    elif locationIsEvent or requiresScript: 
        getItemMessage = (
            f"\tGetItemMessageExPlus({itemIcon},{itemQuantity},{ITEM_SOUND},\"{message}\",0,0)\n"
            f"\tWaitPrompt()\n"
            f"\tWaitCloseWindow()\n"
        )
    else: 
        getItemMessage = ""

    if not locationIsEvent and (eventScripts != "" or getItemMessage != ""):
        setStopFlag = f"\tSetStopFlag({SCRIPT_STOP_FLAG})\n"
        resetStopFlag = f"\tResetStopFlag({SCRIPT_STOP_FLAG})\n"
    else: 
        setStopFlag = ""
        resetStopFlag = ""

    getItemFunction = ( 
        f"\n"
        f"function \"{scriptName}\"\n"
        f"{{\n"
        f"{setStopFlag}"
        f"{getItem}"
        f"{getItemMessage}"
        f"{eventScripts}"
        f"{resetStopFlag}"
        f"}}\n"
        f"\n"
    )

    if not locationIsEvent:
        fillChest(location_id,itemId,itemQuantity)
    
    return getItemFunction





