from patch.crew import *
import struct

#This functions was getting too big with so many flags so I split it into it's own file
#I also included the stuff for the starting character functions because they seemed logical to group together
def buildStartParameters(patch):
    gameSettingFlags = ''
    APScript = ''
    pastDanaFlags = '' #setting the past dana flags after loading castaway village was the only way I found to fix a problem where you spawn at a black map with either barbaros or katheew
    seed = struct.unpack('<I', struct.pack('<f', float(int(patch.settings["seed_name"]))))[0] # convert seed to float32 so it fits in the 32 bit flag space, will be stored in GF_TBOX_DUMMY117. It won't be the exact seed number but it'll be close enough for save marking.
    startingCharacter = CREW_FLAGS[patch.settings["starting_character"]] 

    APScript = """
    function "setSeed"
    {{
        SetFlag(GF_TBOX_DUMMY117, {0}) //AP Seed stored as a float32 so we lose some precision but it has to fit in 32 bits
        GetItem(ICON3D_502, 1) //AP Packages item used for obtaining some offworld items.
    }}

    """.format(seed)  

    # if parameters.charMode == "Past Dana":
    #     gameSettingFlags = gameSettingFlags + """
    #     SetFlag(SF_DANA_JOINED, 1)
    #     //SetFlag(SF_DANA_JOINOK, 1)
    #     //SetFlag(SF_PAST_MODE, 1)
    #     CallFunc("rng:soloEvent")
    #     //CallFunc("rng:earlyGameParty")
    #     SetFlag(GF_TBOX_DUMMY129,1) //Past Dana Mode
    # """
    #     pastDanaFlags = pastDanaFlags + """
    #     // 過去編
    #     SetFlag(SF_CHRSWITCH_MODE, 1)
    #     JoinParty(PARTY_DANA)
    #     JoinParty(PARTY_DANA2)
    #     SetFlag(SF_DANA2_JOINOK, 1)
    #     JoinParty(PARTY_DANA3)
    #     SetFlag(SF_DANA3_JOINOK, 1)
    #     SetFlag(SF_CANTLEARN_SKILL, 1)
    #     SetFlag(SF_DANA_WATERSTYLE_LV, 1)	// 水スタイル
    #     SetFlag(SF_DANA_EARTHSTYLE_LV, 1)	// 地スタイル
    #     SetFlag(SF_DANA_LIGHTSTYLE_LV, 1)
    #     GetItem(ICON3D_AC_069, 1)
    #     GetItem(ICON3D_AC_068, 1)
    #     GetSkill(PARTY_DANA, -1, -1)				// スキル全部忘れる
    #     //SetSkillShortCut(PARTY_DANA, -1, -1)		// スキルショートカットを全て外す
    #     //GetSkill(PARTY_DANA, -1, 3)					// 現在のレベルで習得できる物を全て習得する
    #     //SetSkillShortCut(PARTY_DANA, -1, 0)			// 現在のレベルに見合ったものに自動設定
    #     GetSkill(PARTY_DANA, SKILL_DANA_SP_C3, 1)
    #     GetSkill(PARTY_DANA, SKILL_DANA_SP_C4, 1)
    #     GetSkill(PARTY_DANA, SKILL_DANA_SP_B5, 1)
    #     GetSkill(PARTY_DANA, SKILL_DANA_SP_A2, 1)
    #     SetSkillShortCut(PARTY_DANA,	ATKSKILL_CIRCLE,	SKILL_DANA_SP_C3)	//ウォーターシュート
    #     SetSkillShortCut(PARTY_DANA,	ATKSKILL_CROSS,		SKILL_DANA_SP_B5)	//ミストラルエッジ
    #     SetSkillShortCut(PARTY_DANA,	ATKSKILL_SQUARE,	SKILL_DANA_SP_A2)	//蒼輪舞踏
    #     SetSkillShortCut(PARTY_DANA,	ATKSKILL_TRIANGLE,	SKILL_DANA_SP_C4)	//竜気
    # """

    if patch.settings["options"]["dungeon_entrance_shuffle"] == 1:
        gameSettingFlags = gameSettingFlags + """
    SetFlag(GF_TBOX_DUMMY114,1)
    """
    if patch.settings["options"]["progressive_super_items"] == 1:
        gameSettingFlags = gameSettingFlags + """
    SetFlag(GF_TBOX_DUMMY109,1)
    """
    if patch.settings["options"]["final_boss_access"] == 2: # Release the Psyches
        gameSettingFlags = gameSettingFlags + """
    SetFlag(GF_TBOX_DUMMY112,1)
    SetFlag (GF_06MP6301_RETURN_CENTER,1)
    SetFlag (GF_06MP6301_OPEN_INSECT,1)
    SetFlag (GF_06MP6301_OPEN_HEAVENS,1)
    """  
    if patch.settings["options"]["octus_paths_opened"] == 1:
        gameSettingFlags = gameSettingFlags + """
    SetFlag(GF_TBOX_DUMMY113,1)
    """
    if patch.settings["options"]["recipes_with_ingredients"] == 1: #The player starts with fish soup so we'll give some ingredients for it here
        gameSettingFlags = gameSettingFlags + """
    SetFlag(GF_TBOX_DUMMY115,1)
    """
        
    if patch.settings["options"]["north_side_open"] == 1: #Unlocking the crystal warp point to temple approach - camp
        gameSettingFlags = gameSettingFlags + """
    SetMapMarker( SMI_CHECKED_WARPPT, PAGE_F039, MARKER_CP_MP4111, -131, 587, 121, -131, 587, CP_MP4111, MN_F_MP4111, 0) 
    """

    if patch.settings["options"]["infinity_mode"] == 1:
        gameSettingFlags = gameSettingFlags + """
    SetFlag(SF_INFINITY, 1)
    """

    startParams = """
function "startParameters"
{{
    SetStopFlag(STOPFLAG_EVENT)
    SetFlag(SF_ADOL_JOINOK, 0)
    SetFlag(SF_ADOL_JOINED, 0)
    CallFunc("rng:earlyGameParty")
    SetLevel(ADOL,3)
    SetLevel(LAXIA,3)
    SetLevel(SAHAD,3)
    SetLevel(RICOTTA,3)
    SetLevel(HUMMEL,3)
    SetLevel(DANA,3)
    SetFlag(GF_TBOX_DUMMY121,3)
    GetItem(ICON3D_WP_ADOL_000,1)
    EquipWeapon(ADOL,ICON3D_WP_ADOL_000)
    GetItem(ICON3D_WP_LAXIA_000, 1)
    EquipWeapon(LAXIA,ICON3D_WP_LAXIA_000)
    GetItem(ICON3D_WP_SAHAD_000, 1)
    EquipWeapon(SAHAD,ICON3D_WP_SAHAD_000)
    GetItem(ICON3D_986, 1)
    EquipWeapon(DANA,ICON3D_986)
    GetItem(ICON3D_990, 1)
    EquipWeapon(RICOTTA,ICON3D_990)
    GetItem(ICON3D_992, 1)
    EquipWeapon(HUMMEL,ICON3D_992)
    SetFlag(SF_ITEMSLOT_NUM,1)
    // SetFlags for spirits, these might be itemized later but for now let's set them to put the spirit ring on mistilteinn's tier
    SetFlag(GF_TROPHY_ETERNIASPIRIT_START,1)
    SetFlag(GF_TROPHY_ETERNIASPIRIT_01,1)
    SetFlag(GF_TROPHY_ETERNIASPIRIT_02,1)
    SetFlag(GF_TROPHY_ETERNIASPIRIT_03,1)
    SetFlag(GF_TROPHY_ETERNIASPIRIT_04,1)
    SetFlag(GF_TROPHY_ETERNIASPIRIT_05,1)
    SetFlag(GF_TROPHY_ETERNIASPIRIT_06,1)
    SetFlag(GF_TROPHY_ETERNIASPIRIT_07,1)
    SetFlag(GF_TROPHY_ETERNIASPIRIT_08,1)
    SetFlag(GF_TROPHY_ETERNIASPIRIT_09,1)
    SetFlag(GF_TROPHY_ETERNIASPIRIT_10,1)
    SetFlag(GF_TROPHY_ETERNIASPIRIT_END,1)
    //Let's set the flags for checking a bunch of removeable obstacles so the players don't have to click on them twice
    SetFlag(GF_SUBEV_1111_CHECKED_ROCK,1)
    SetFlag(GF_SUBEV_2101_CHECKED_ROCK,1)
    SetFlag(GF_SUBEV_2101_SIEN03_LOOK, 1)
    SetFlag(GF_SUBEV_1131_CHECKED_ROCK,1)
    SetFlag(GF_SUBEV_1120_CHECKED_ROCK,1)
    SetFlag(GF_SUBEV_1117_CHECKED_ROCK,1)
    SetFlag(GF_SUBEV_2105_CHECKED_ROCK,1)
    SetFlag(GF_SUBEV_1116_CHECKED_ROCK,1)
    SetFlag(GF_SUBEV_1109_CHECKED_ROCK,1)
    SetFlag(GF_SUBEV_6102_CHECKED_ROCK,1)
    SetFlag(GF_SUBEV_1132_CHECKED_SAND,1)
    SetFlag(GF_SUBEV_4110_CHECKED_LADDER,1)
    SetFlag(GF_SUBEV_6107_CHECKED_SAND,1)
    SetFlag(GF_SUBEV_6362_CHECKED_PILLAR,1)
    SetFlag(GF_SUBEV_2104_CHECKED_SAND,1)
    SetFlag( GF_SUBEV_1107_CHECKED_BRIDGE , 1 )  //Checked broken bridge
    SetFlag( GF_03MP1107_REPAIR_ROPE , 1 )      //Had conversation with Ricotta about bridge
    //Place all map markers for the obstacle events
    SetMapMarker( SMI_COOPEVENT, PAGE_F002, REMOVE_OBJ_1107CE, -61.91f,-651.20f,72.13f, -61.91f,-651.20f, COOPEVID_MP1107, MN_F_MP1107,1)
    SetMapMarker(SMI_COOPEVENT, PAGE_F003, REMOVE_OBJ_1109CE, 458.66f,-634.03f,18.30f, 458.66f,-634.03f, COOPEVID_MP1109, MN_F_MP1109,0)
    SetMapMarker(SMI_COOPEVENT, PAGE_F001, REMOVE_OBJ_1111CE, 139.51f,-1190.52f,2.79f, 139.51f,-1190.52f, COOPEVID_MP1111, MN_F_SOUTHWEST_PLANE_MP1111,0)
    SetMapMarker(SMI_COOPEVENT, PAGE_F004, REMOVE_OBJ_1116CE, 1022.83f,-1209.00f,5.21f, 1022.83f,-1209.00f, COOPEVID_MP1116, MN_F_MP1116,0)
    SetMapMarker( SMI_COOPEVENT, PAGE_F008, REMOVE_OBJ_1117CE, -854.11f,-615.99f,21.02f, -854.11f,-615.99f, COOPEVID_MP1117, MN_F_MP1117,1)
    SetMapMarker(SMI_COOPEVENT, PAGE_F002, REMOVE_OBJ_1120CE, 408.91f,-664.52f,11.30f, 408.91f,-664.52f, COOPEVID_MP1120, MN_F_MP1120,1)
    SetMapMarker(SMI_COOPEVENT, PAGE_F001, REMOVE_OBJ_1131CE, -26.99f,-1292.62f,24.43f, -26.99f,-1292.62f, COOPEVID_MP1131, MN_F_SOUTHWEST_PLANE_MP1131,0)
    SetMapMarker(SMI_COOPEVENT, PAGE_F005, REMOVE_OBJ_1132CE, 351.66f,-1543.02f,-0.41f, 351.66f,-1543.02f, COOPEVID_MP1132, MN_F_MP1132,0)
    SetMapMarker(SMI_COOPEVENT, PAGE_F001, REMOVE_OBJ_2101CE, 53.73f, -919.31f, 13.52f, 53.73f, -919.31f, COOPEVID_MP2101, MN_F_SOUTHWEST_PLANE_MP2101,0)
    SetMapMarker(SMI_COOPEVENT, PAGE_F011, REMOVE_OBJ_2104CE, 1038.33f,-354.66f,76.45f, 1038.33f,-354.66f, COOPEVID_MP2104, MN_F_MP2104,0)
    SetMapMarker(SMI_COOPEVENT, PAGE_F011, REMOVE_OBJ_2105CE, 1020.21f,-810.00f,53.07f, 1020.21f,-810.00f, COOPEVID_MP2105, MN_F_MP2105,0)
    SetMapMarker(SMI_COOPEVENT, PAGE_F036, REMOVE_OBJ_4110CE, -482.02f,562.00f,122.59f, -482.02f,562.00f, COOPEVID_MP4110, MN_F_MP4110,0)
    SetMapMarker(SMI_COOPEVENT, PAGE_F034, REMOVE_OBJ_6102CE, 243.20f,1198.52f,43.72f, 243.20f,1198.52f, COOPEVID_MP6102, MN_F_MP6102,0)
    SetMapMarker(SMI_COOPEVENT, PAGE_F037, REMOVE_OBJ_6107CE, -791.34f,800.31f,41.7f, -791.34f,800.31f, COOPEVID_MP6107, MN_F_MP6107,-1)
    SetMapMarker(SMI_COOPEVENT, PAGE_MP636x, REMOVE_OBJ_6362CE, 123.92f,-201.60f,127.43f, 123.92f,-201.60f, COOPEVID_MP6362, MN_D_MP6362,1)
    //preset system flags for convenience 
    SetFlag(SF_CAMP_CANT_FORMATION,0)           // Formation menu prohibited
    SetFlag(SF_CAMP_CANT_MEMORYMENU,0)             // Disable memory menu
    SetFlag(SF_CAMP_CANT_DIARY,0)             // Adventure diary menu prohibited
    SetFlag(SF_CAMP_CANT_MAP,0)             // Map menu prohibited. If you stand on it while the map is open, it will not close.
    SetFlag(SF_CAMP_CANT_EQUIP,0)            // Equipment menu prohibited
    SetFlag(SF_CAMP_CANT_SKILL,0)
    SetFlag( SF_CANUSE_MAPWARP, 1 )
    SetFlag(SF_CANTUSE_MAP, 0)
    SetFlag(SF_CANTUSE_SKILL ,0)
    SetFlag(SF_CAN_EXSKILL, 1)
    //set a ton of story progress flags to try and make events more open, hopefully doesn't break anything, will need lots of testing
    SetFlag(GF_00MP0011_GO_CAPTAINROOM, 1)	// Head to the captain's room
    SetFlag(GF_00MP0012_START_PATROL, 1)	// start patrolling
    SetFlag(GF_00MP0012_GO_CAPTAINROOM2, 1)	// Head to the captain's room (second time)
    SetFlag(GF_00MP0016_HEAR_SCREAM, 1)		// I hear a scream
    SetFlag(GF_00MP0011b_DIVE_OCEAN, 1)		// jump into the sea
    SetFlag(GF_00MP1102_TALK_LAXIA,	1)	// Talked to Laxia
    SetFlag(GF_00MP1102_TALK_SAHAD,	1)	// Talked to Sahad
    SetFlag(GF_00MP1102_TALK_HUMMEL, 1)		// Talked to Hummel
    SetFlag(GF_00MP1102_TALK_DOGI, 1)		// Talked to Dogi
    SetFlag(GF_01MP1110_DRIFT,1)
    SetFlag(GF_01MP1110_GET_SWORD, 1)
    SetFlag(GF_01MP7301_GET_SKILL,1)
    SetFlag(GF_01MP7301_SET_SKILL,1)
    SetFlag(GF_01MP1110_BATTLE_WIN,1)
    SetFlag(GF_01MP1102_DRINK_WATER, 1)
    SetFlag(GF_01MP1201_IN_BASE, 1)
    SetFlag(GF_01MP1201_TALK_LAXIA, 1)
    SetFlag(GF_01MP1201_GET_DRIFT, 1)
    SetFlag(GF_01MP1202_IN_MP1202,1)
    SetFlag(GF_01MP1201_LOOK_MAN,1)
    SetFlag(GF_01MP7302_GET_ITEM, 1)
    SetFlag(GF_01MP7302_GET_ARMOR, 1)
    SetFlag(GF_01MP7302_GET_SWORD, 1)
    //SetFlag(GF_01MP1101_DRAW_MAP,1)
    SetFlag(GF_02MP1201_TALK_DOGISAHAD,	1)
	SetFlag(GF_02MP1203_START_FISHING,1)	
	SetFlag(GF_02MP1203_GET_FISH,1)	
    SetFlag(GF_02MP1201_TEST_SMITH, 1)
    SetFlag(GF_02MP1201_TEST_TRADE, 1)
    SetFlag(GF_02MP1201_TEST_DRUG, 1)
	SetFlag(GF_02MP1201_TAKE_BREAKFAST,	1)	
	SetFlag(GF_02MP1201_INFO_QUEST,1)			
	SetFlag(GF_GALL_EVIMG_01,1)			
	SetFlag(GF_GALL_EVIMG_02,1)		
	SetFlag(GF_GALL_EVIMG_03,1)	
    SetFlag(GF_02MP1110_REMOVE_OBSTACLE, 1)     // removed initial tree, lets the player see numbers required to move obstacles and makes sphere 0 more dynamic 
    SetFlag(GF_SUBEV_HELP_NUSHI,1)
    SetFlag( GF_02MP2102_LOOK_MONSTER , 1 )	
    SetFlag( GF_SUBEV_03_2102_SWAMP, 1 )
    //set flags fro arriving at the shoreline for great river valley
    SetFlag(GF_02MP1120_MEET_HUMMEL,1)
    SetFlag(GF_02MP1121_MAKE_CAMP,1)
    SetFlag( GF_02MP1201_TEST_RENSEI , 1 ) // Enables weapon enhancement, still requires kathleen
    SetFlag(GF_02MP1201_BEFORE_INTERCEPT,1) // Preparations for interception battle have begun.
    SetFlag(GF_02MP1201_START_INTERCEPT,1) // Started interception battle
    SetFlag(GF_02MP1201_AFTER_INTERCEPT,1) // The first interception battle is over.
    SetFlag(GF_02MP23xx_OCCUR_INTERCEPT3,1) // Interception 3 has occurred
    SetFlag(GF_02MP23xx_AFTER_INTERCEPT3,1) // Interception battle 3 has ended
    SetFlag(GF_03MP3109M_MOVE_CANYON,1) //Dana Edition Head to the Great Canyon
                                        //Dana Part 1: Declare the start of the tree-planting festival
                                        // Dana Edition Proceed deep into the valley
                                        //Dana Part 1: Start the tree-planting ceremony
    //SetFlag(GF_03MP1101_LEAVE_CAMP,1)  //Spawns tree that leads to primordial passage
    SetFlag(GF_03MP4202_IN_LODGE,1)
    SetFlag(GF_03MP4202_LOOK_LODGE,1)
    SetFlag(GF_03MP4202_LOOK_NOTE,1)
    SetFlag(GF_03MP4202_LOOK_FLOWER,1)
    SetFlag(GF_03MP4202_LOOK_BOOK,1)
    SetFlag(GF_03MP4202_TALK_LODGE,1)  //skip events at cabin on the initial way up gendarme
    SetFlag(GF_03MP433x_OCCUR_INTERCEPT5,1) // Interception battle 5 has occurred
    SetFlag(GF_03MP433x_AFTER_INTERCEPT5,1) // Intercept Battle 5 has ended
    SetFlag(GF_04MP5101_OCCUR_INTERCEPT7,1) // Intercept battle 7 has occurred
    SetFlag(GF_04MP5101_AFTER_INTERCEPT7,1) // Intercept Battle 7 has ended
    //Stop all the chasing of Thanatos
    SetFlag(GF_04MP6203_RUN_CENTER,1)
    SetFlag(GF_04MP6203_LOOK_BUILD,1)
    SetFlag(GF_04MP6203_IN_BUILD,1)
    SetFlag(GF_04MP6203_RUN_AWAY,1)
    SetFlag(GF_04MP6203_SEE_BUILD,1)
    SetFlag(GF_04MP6201_RUN_WEST,1)
    SetFlag(GF_04MP6201_LOOK_PAGOIDA,1)
    SetFlag(GF_04MP6203_RUN_CENTER,1)
    SetFlag(GF_04MP6202_SEE_FIGURE,1)
    SetFlag(GF_04MP6202_IN_EAST,1)
    SetFlag(GF_04MP6203_LOOK_BUILD,1)
    SetFlag(GF_04MP6214_GOTO_2F,1)
    SetFlag(GF_04MP6211_LOOK_STATUE,1)
    SetFlag(GF_04MP6211_RUN_PAGOIDA,1)
    SetFlag(GF_NPC_4_02_SEE_THANATOS,1)
    SetFlag(GF_04MP6204_IN_PAGOIDA,1)
    SetFlag(GF_04MP6201_TALK_THANATOS,1)
    SetFlag(GF_04MP6409_LOOKUP_ORITREE,1)
    //There are zero checks in temple of the great tree and the "puzzel" is simple to let's hurry the player along and open the doors for them.
    SetFlag(GF_04MP6402_CHECK_GIM,1)
    SetFlag(GF_MP6401_SWITCH_03,1)
    SetFlag(GF_MP6401_SWITCH_02,1)
    SetFlag(GF_MP6401_SWITCH_01R,1)
    SetFlag(GF_MP6401_SWITCH_01L,1)
    //SetFlag(GF_05MP1213_INTERCEPT_DANA,1) //Dana participates in the interception battle 2
    //SetFlag(GF_SUBEV_ST_6201_DOOR_OPEN,1)  //Door to Towal Highway is open if it can be reached, leaving this in as Dana can be a non-linear progression item for this
    //Towal entry cutscenes
    SetFlag(GF_05MP6204_SEE_RUIN,1)
    SetFlag(GF_05MP6201_IN_EAST,1)
    SetFlag(GF_05MP6203_SEE_BAHA,1)
    SetFlag(GF_05MP6115_SEE_HOLLOW,1)
    SetFlag(GF_05MP6110_OUT_CAMP,1)
    //Cutscenes before palace
    SetFlag(GF_05MP6204_FIND_CRYSTAL,1)
    SetFlag(GF_05MP6202_GOTO_SKYWAY,1)
    SetFlag(GF_05MP1201_OCCUR_INTERCEPT9,1) // Intercept battle 9 has occurred
    SetFlag(GF_05MP1201_AFTER_INTERCEPT9,1) // Intercept battle 9 has ended
    //Valley of Kings
    SetFlag(GF_05MP4105_PASS_TEM, 1)
    SetFlag(GF_05MP6108_MALK_CAMP,1)
    SetFlag(GF_06MP6305_IN_OCEAN,1)
    SetFlag(GF_SUBEV_ST_DOOR_1STTALK,1)
    SetFlag(GF_06MP6409_OCCUR_INTERCEPT12,1) // Interception 12 has occurred
    SetFlag(GF_06MP6409_AFTER_INTERCEPT12,1) // Interception Battle 12 has ended
    GetItem(ICON3D_MAP,1) //start with the map for faster exploration
    SetFlag( GF_06MP6301_OPEN_STAIRS , 1 ) // open selection sphere
	SetFlag( GF_06MP6301_OPEN_BOSSROOM , 1) // open selection sphere
	SetFlag( GF_06MP6310_ATTACK_BOSSROOM , 1 ) // open selection sphere
	SetFlag( GF_GALL_EV_06_05, 1 ) // open selection sphere
    //Remove all tutorials from the game
    SetFlag(    GF_HELP_A01,1 )
    SetFlag(	GF_HELP_A02,			1 )
    SetFlag(	GF_HELP_A03,			1 )
    SetFlag(	GF_HELP_A04,			1 )
    SetFlag(	GF_HELP_A05,			1 )
    SetFlag(	GF_HELP_A06,			1 )
    SetFlag(	GF_HELP_A07,			1 )
    SetFlag(	GF_HELP_A08,			1 )
    SetFlag(	GF_HELP_A09,			1 )
    SetFlag(	GF_HELP_A10,			1 )
    SetFlag(	GF_HELP_A11,			1 )
    SetFlag(	GF_HELP_A12,			1 )
    SetFlag(	GF_HELP_A13,			1 )
    SetFlag(	GF_HELP_A14,			1 )
    SetFlag(	GF_HELP_A15,			1 )
    SetFlag(	GF_HELP_A16,			1 )
    SetFlag(	GF_HELP_A17,			1 )
    SetFlag(	GF_HELP_A18,			1 )
    SetFlag(	GF_HELP_A19,			1 )
    SetFlag(	GF_HELP_A20,			1 )
    SetFlag(	GF_HELP_A21,			1 )
    SetFlag(	GF_HELP_A22,			1 )
    SetFlag(	GF_HELP_A23,			1 )
    SetFlag(	GF_HELP_A24,			1 )
    SetFlag(	GF_HELP_A25,			1 )
    SetFlag(	GF_HELP_A26,			1 )
    SetFlag(	GF_HELP_A27,			1 )
    SetFlag(	GF_HELP_A28,			1 )
    SetFlag(	GF_HELP_A29,			1 )
    SetFlag(	GF_HELP_A30,			1 )
    SetFlag(	GF_HELP_A31,			1 )
    SetFlag(	GF_HELP_A32,			1 )
    SetFlag(	GF_HELP_A33,			1 )
    SetFlag(	GF_HELP_A34,			1 )
    SetFlag(	GF_HELP_A35,			1 )
    SetFlag(	GF_HELP_A36,			1 )
    SetFlag(	GF_HELP_A37,			1 )
    SetFlag(	GF_HELP_A38,			1 )
    SetFlag(	GF_HELP_A39,			1 )
    SetFlag(	GF_HELP_A40,			1 )
    SetFlag(	GF_HELP_A41,			1 )
    SetFlag(	GF_HELP_A42,			1 )
    SetFlag(	GF_HELP_A43,			1 )
    SetFlag(	GF_HELP_A44,			1 )
    SetFlag(	GF_HELP_A45,			1 )
    SetFlag(	GF_HELP_B01,			1 )
    SetFlag(	GF_HELP_B02,			1 )
    SetFlag(	GF_HELP_B03,			1 )
    SetFlag(	GF_HELP_B04,			1 )
    SetFlag(	GF_HELP_B05,			1 )
    SetFlag(	GF_HELP_B06,			1 )
    SetFlag(	GF_HELP_B07,			1 )
    SetFlag(	GF_HELP_B08,			1 )
    SetFlag(	GF_HELP_B09,			1 )
    SetFlag(	GF_HELP_B10,			1 )
    SetFlag(	GF_HELP_B11,			1 )
    SetFlag(	GF_HELP_B12,			1 )
    SetFlag(	GF_HELP_B13,			1 )
    SetFlag(	GF_HELP_B13_B,			1 )
    SetFlag(	GF_HELP_B14,			1 )
    SetFlag(	GF_HELP_B15,			1 )
    SetFlag(	GF_HELP_B16,			1 )
    SetFlag(	GF_HELP_B17,			1 )
    SetFlag(	GF_HELP_B18,			1 )
    SetFlag(	GF_HELP_B19,			1 )
    SetFlag(	GF_HELP_B20,			1 )
    SetFlag(	GF_HELP_A46,			1 )
    SetFlag(	GF_HELP_A47,			1 )
    SetFlag(	GF_HELP_A48,			1 )
    SetFlag(	GF_HELP_A49,			1 )
    SetFlag(	GF_HELP_A50,			1 )
    SetFlag(	GF_HELP_A51,			1 )
    SetFlag(	GF_HELP_A52,			1 )
    SetFlag(	GF_HELP_A53,			1 )
    SetFlag(	GF_HELP_A54,			1 )
    SetFlag(	GF_HELP_A55,			1 )
    SetFlag(	GF_HELP_A56,			1 )
    SetFlag(	GF_HELP_A57,			1 )
    SetFlag(	GF_HELP_B21,			1 )
    SetFlag(	GF_HELP_B22,			1 )
    SetFlag(	GF_HELP_B23,			1 )
    SetFlag(	GF_HELP_B24,			1 )
    SetFlag(	GF_HELP_B25,			1 )
    SetFlag(	GF_HELP_B26,			1 )
    SetFlag(	GF_HELP_B27,			1 )
    SetFlag(	GF_HELP_B28,			1 )
    SetFlag(	GF_HELP_B29,			1 )
    SetFlag(	GF_HELP_B30,			1 )
    SetFlag(	GF_HELP_B31,			1 )
    SetFlag(	GF_HELP_A58,			1 )
    SetFlag(	GF_HELP_A59,			1 )
    SetFlag(	GF_HELP_A44_B,	1 )
    //Let's set every mission flag for a cleaner more stable looking diary and interface
    SetFlag(SF_MISSIONNO,MS_00_01)					
    SetFlag(SF_MISSIONNO,	MS_00_02)					
    SetFlag(SF_MISSIONNO,	MS_00_03)					
    SetFlag(SF_MISSIONNO,	MS_00_04)					
    SetFlag(SF_MISSIONNO,	MS_01_01)					
    SetFlag(SF_MISSIONNO,	MS_01_02)					
    SetFlag(SF_MISSIONNO,	MS_01_03)					
    SetFlag(SF_MISSIONNO,	MS_01_04)					
    SetFlag(SF_MISSIONNO,	MS_01_05)					
    SetFlag(SF_MISSIONNO,	MS_01_06)					
    SetFlag(SF_MISSIONNO,	MS_01_07)					
    SetFlag(SF_MISSIONNO,	MS_01_08)					
    SetFlag(SF_MISSIONNO,	MS_01_09)					
    SetFlag(SF_MISSIONNO,	MS_02_01)					
    SetFlag(SF_MISSIONNO,	MS_02_02)
    SetFlag(SF_MISSIONNO,	MS_02_02B)					
    SetFlag(SF_MISSIONNO,	MS_02_03)					
    SetFlag(SF_MISSIONNO,	MS_02_04)					
    SetFlag(SF_MISSIONNO,	MS_02_05)					
    SetFlag(SF_MISSIONNO,	MS_02_06)					
    SetFlag(SF_MISSIONNO,	MS_02_07)					
    SetFlag(SF_MISSIONNO,	MS_02_08)					
    SetFlag(SF_MISSIONNO,	MS_02_09)					
    SetFlag(SF_MISSIONNO,	MS_02_10)					
    SetFlag(SF_MISSIONNO,	MS_02_11)					
    SetFlag(SF_MISSIONNO,	MS_02_12)					
    SetFlag(SF_MISSIONNO,	MS_02_13)					
    SetFlag(SF_MISSIONNO,	MS_02_14)					
    SetFlag(SF_MISSIONNO,	MS_02_15)					
    SetFlag(SF_MISSIONNO,	MS_02_16)					
    SetFlag(SF_MISSIONNO,	MS_02_17)					
    SetFlag(SF_MISSIONNO,	MS_02_18)					
    SetFlag(SF_MISSIONNO,	MS_02_19)					
    SetFlag(SF_MISSIONNO,	MS_02_20)					
    SetFlag(SF_MISSIONNO,	MS_02_21)					
    SetFlag(SF_MISSIONNO,	MS_02_22)					
    SetFlag(SF_MISSIONNO,	MS_02_23)					
    SetFlag(SF_MISSIONNO,	MS_03_01)					
    SetFlag(SF_MISSIONNO,	MS_03_02)					
    SetFlag(SF_MISSIONNO,	MS_03_03)					
    SetFlag(SF_MISSIONNO,	MS_03_04)					
    SetFlag(SF_MISSIONNO,	MS_03_05)					
    SetFlag(SF_MISSIONNO,	MS_03_06)					
    SetFlag(SF_MISSIONNO,	MS_03_07)					
    SetFlag(SF_MISSIONNO,	MS_03_08)
    SetFlag(SF_MISSIONNO,	MS_03_08B)
    SetFlag(SF_MISSIONNO,	MS_03_08C)					
    SetFlag(SF_MISSIONNO,	MS_03_09)					
    SetFlag(SF_MISSIONNO,	MS_03_10)					
    SetFlag(SF_MISSIONNO,	MS_04_01)					
    SetFlag(SF_MISSIONNO,	MS_04_02)					
    SetFlag(SF_MISSIONNO,	MS_04_03)					
    SetFlag(SF_MISSIONNO,	MS_04_04)					
    SetFlag(SF_MISSIONNO,	MS_04_05)					
    SetFlag(SF_MISSIONNO,	MS_04_06)					
    SetFlag(SF_MISSIONNO,	MS_04_07)					
    SetFlag(SF_MISSIONNO,	MS_04_08)					
    SetFlag(SF_MISSIONNO,	MS_04_09)					
    SetFlag(SF_MISSIONNO,	MS_05_01)					
    SetFlag(SF_MISSIONNO,	MS_05_02)					
    SetFlag(SF_MISSIONNO,	MS_05_03)
    SetFlag(SF_MISSIONNO,	MS_05_03B)					
    SetFlag(SF_MISSIONNO,	MS_05_04)					
    SetFlag(SF_MISSIONNO,	MS_05_05)					
    SetFlag(SF_MISSIONNO,	MS_05_06)					
    SetFlag(SF_MISSIONNO,	MS_05_07)					
    SetFlag(SF_MISSIONNO,	MS_05_08)					
    SetFlag(SF_MISSIONNO,	MS_05_09)					
    SetFlag(SF_MISSIONNO,	MS_05_10)					
    SetFlag(SF_MISSIONNO,	MS_05_11)					
    SetFlag(SF_MISSIONNO,	MS_05_12)					
    SetFlag(SF_MISSIONNO,	MS_05_13)					
    SetFlag(SF_MISSIONNO,	MS_06_01)					
    SetFlag(SF_MISSIONNO,	MS_06_02)					
    SetFlag(SF_MISSIONNO,	MS_06_03)					
    SetFlag(SF_MISSIONNO,	MS_06_04)					
    SetFlag(SF_MISSIONNO,	MS_06_05)					
    SetFlag(SF_MISSIONNO,	MS_06_06)					
    SetFlag(SF_MISSIONNO,	MS_06_07)					
    SetFlag(SF_MISSIONNO,	MS_06_08)					
    SetFlag(SF_MISSIONNO,	MS_06_09)					
    SetFlag(SF_MISSIONNO,	MS_07_01)
    SetFlag(SF_MISSIONNO,	MS_07_01B)
    SetFlag(SF_MISSIONNO,	MS_07_01C)					
    SetFlag(SF_MISSIONNO,	MS_07_02)					
    SetFlag(SF_MISSIONNO,	MS_07_03)					
    SetFlag(SF_MISSIONNO,	MS_07_04)										
    SetFlag(SF_MISSIONNO,	MS_08_D1A)					
    SetFlag(SF_MISSIONNO,	MS_08_D1B)					
    SetFlag(SF_MISSIONNO,	MS_08_D1C)					
    SetFlag(SF_MISSIONNO,	MS_08_D3)					
    SetFlag(SF_MISSIONNO,	MS_08_D3B)					
    SetFlag(SF_MISSIONNO,	MS_08_01)					
    SetFlag(SF_MISSIONNO,	MS_08_01B)					
    SetFlag(SF_MISSIONNO,	MS_08_01C)					
    SetFlag(SF_MISSIONNO,	MS_08_02)					
    SetFlag(SF_MISSIONNO,	MS_08_02B)					
    SetFlag(SF_MISSIONNO,	MS_08_02C)					
    SetFlag(SF_MISSIONNO,	MS_08_02D)					
    SetFlag(SF_MISSIONNO,	MS_08_02E)					
    SetFlag(SF_MISSIONNO,	MS_08_02F)					
    SetFlag(SF_MISSIONNO,	MS_08_03)					
    SetFlag(SF_MISSIONNO,	MS_08_03B)					
    SetFlag(SF_MISSIONNO,	MS_08_03C)					
    SetFlag(SF_MISSIONNO,	MS_08_04)					
    SetFlag(SF_MISSIONNO,	MS_08_042)					
    SetFlag(SF_MISSIONNO,	MS_08_05)					
    SetFlag(SF_MISSIONNO,	MS_08_06)					
    SetFlag(SF_MISSIONNO,	MS_08_06B)					
    SetFlag(SF_MISSIONNO,	MS_08_06C)					
    SetFlag(SF_MISSIONNO,	MS_08_06D)					
    SetFlag(SF_MISSIONNO,	MS_08_07)					
    SetFlag(SF_MISSIONNO,	MS_08_07B)					
    SetFlag(SF_MISSIONNO,	MS_08_07C)					
    SetFlag(SF_MISSIONNO,	MS_08_07D)					
    SetFlag(GF_TBOX_DUMMY060,1) //enables first avolodragil fight from the start, this flag is replacing meeting barbaros
    SetFlag(GF_TBOX_DUMMY067,1) //Make ghostship available if it can be reached.
    SetFlag(GF_NPC_0_01_GO_CAPTAINROOM		, 1)
    SetFlag(	GF_NPC_0_02_START_PATROL		, 1)
    SetFlag(	GF_NPC_0_03_ATTACK_SHIP			, 1)
    SetFlag(	GF_NPC_1_01_IN_BASE				, 1)
    SetFlag(	GF_NPC_6_04_GET_MISTILTEINN		, 1)
    SetFlag( GF_CAMP_VILLAGE_LV, 7 )     //Same thing for the village build.
    //Set the captains quest to done, since he'll never be in the village.
    SetFlag(GF_QUEST_200, QUEST_END)
    SetFlag(GF_QUEST_201, QUEST_END)
    SetFlag(GF_QUEST_210, QUEST_END)
    SetFlag(GF_QUEST_220, QUEST_END)
    SetFlag(GF_QUEST_221, QUEST_END)
    SetFlag(GF_QUEST_222, QUEST_END)
    SetFlag(GF_QUEST_223, QUEST_END)
    SetFlag(GF_QUEST_230, QUEST_END)
    SetFlag(GF_QUEST_231, QUEST_END)
    SetFlag(GF_QUEST_300, QUEST_END)
    SetFlag(GF_QUEST_310, QUEST_END)
    SetFlag(GF_QUEST_301, QUEST_END)
    SetFlag(GF_QUEST_302, QUEST_END)
    SetFlag(GF_QUEST_310, QUEST_END)
    SetFlag(GF_QUEST_311, QUEST_END)
    SetFlag(GF_QUEST_401, QUEST_END)
    SetFlag(GF_QUEST_402, QUEST_END)
    SetFlag(GF_QUEST_500, QUEST_END)
    SetFlag(GF_QUEST_501, QUEST_END)
    SetFlag(GF_QUEST_502, QUEST_END)
    SetFlag(GF_QUEST_503, QUEST_END)
    SetFlag(GF_QUEST_510, QUEST_END)
    SetFlag(GF_QUEST_520, QUEST_END)
    SetFlag(GF_QUEST_521, QUEST_END)
    SetFlag(GF_QUEST_522, QUEST_END)
    SetFlag(GF_QUEST_530, QUEST_END)
    SetFlag(GF_QUEST_600, QUEST_END)
    SetFlag(GF_QUEST_601, QUEST_END)
    SetFlag(GF_QUEST_602, QUEST_END)
    SetFlag(GF_QUEST_610, QUEST_START)
    SetFlag(GF_QS610_LOOK_STELE, 1)
    SetFlag(GF_QUEST_611, QUEST_END)
    SetFlag(GF_QUEST_612, QUEST_END)
    SetFlag(GF_QUEST_613, QUEST_END)
	SetFlag(GF_QUEST_232, QUEST_END)			
	SetFlag(GF_QUEST_303, QUEST_END)				
	SetFlag(GF_QUEST_504, QUEST_END)				
	SetFlag(GF_QUEST_505, QUEST_END)				
    SetFlag(GF_SUBEV_JOIN_CURRAN2,1)
    SetFlag(GF_SUBEV_LOOK_NIA1,1) 
    SetFlag(GF_SUBEV_LOOK_SILVIA2,1)
    SetFlag(SF_CANTLEARN_SKILL,1)   //skill shuffle always on in AP
    SetFlag(GF_TBOX_DUMMY111,1)     //skill shuffle always on in AP
    // Open all diary entries for a cleaner interface
    SetFlag( GF_TBOX_DUMMY116, 1 ) //open diary
    // Diary Entry Unlock Flags - Complete Set
    // Sets DRCHA_FLAG_OPEN and all DRCHA_FLAG_INFO[1-N] flags for complete diary
    SetDiaryCharaFlag( DRCHA_ADOL, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_LAXIA, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_LAXIA, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_LAXIA, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_LAXIA, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_LAXIA, DRCHA_FLAG_INFO4, 1 )
    SetDiaryCharaFlag( DRCHA_SAHAD, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_SAHAD, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_SAHAD, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_SAHAD, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_SAHAD, DRCHA_FLAG_INFO4, 1 )
    SetDiaryCharaFlag( DRCHA_HUMMEL, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_HUMMEL, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_HUMMEL, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_HUMMEL, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_HUMMEL, DRCHA_FLAG_INFO4, 1 )
    SetDiaryCharaFlag( DRCHA_RICOTTA, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_RICOTTA, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_RICOTTA, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_RICOTTA, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_RICOTTA, DRCHA_FLAG_INFO4, 1 )
    SetDiaryCharaFlag( DRCHA_DOGI, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_DOGI, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_DOGI, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_DOGI, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_BARBAROSS, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_BARBAROSS, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_BARBAROSS, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_BARBAROSS, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_ALISON, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_ALISON, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_ALISON, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_ALISON, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_ED, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_ED, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_ED, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_ED, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_BABY, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_BABY, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_CURRAN, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_CURRAN, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_CURRAN, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_CURRAN, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_KIERGAARD, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_KIERGAARD, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_KIERGAARD, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_KATRIN, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_KATRIN, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_KATRIN, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_KATRIN, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_NIA, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_NIA, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_NIA, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_NIA, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_DINA, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_DINA, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_DINA, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_DINA, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_AARON, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_AARON, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_AARON, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_AARON, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_REJA, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_REJA, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_REJA, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_REJA, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_MIRALDA, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_MIRALDA, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_MIRALDA, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_MIRALDA, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_LICHT, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_LICHT, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_LICHT, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_LICHT, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_KUINA, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_KUINA, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_KUINA, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_KUINA, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_AUSTEN, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_AUSTEN, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_AUSTEN, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_AUSTEN, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_SILVIA, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_SILVIA, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_SILVIA, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_SILVIA, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_THANATOS, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_THANATOS, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_THANATOS, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_THANATOS, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_KASHU, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_KASHU, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_KASHU, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_KASHU, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_FRANZ, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_FRANZ, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_FRANZ, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_FRANZ, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_GRISELDA, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_GRISELDA, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_GRISELDA, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_GRISELDA, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_PARO, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_PARO, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_PARO, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_PARO, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_BALAENICEPS_REX, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_BALAENICEPS_REX, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_BALAENICEPS_REX, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_SKILLMONKY, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_SKILLMONKY, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_SKILLMONKY, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_DANA, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_DANA, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_DANA, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_DANA, DRCHA_FLAG_INFO3, 1 )
    SetDiaryCharaFlag( DRCHA_DANA, DRCHA_FLAG_INFO4, 1 )
    SetDiaryCharaFlag( DRCHA_OLGA, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_OLGA, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_OLGA, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_SARAI, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_SARAI, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_SARAI, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_RASTELL, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_RASTELL, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_RASTELL, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_IO, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_IO, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_IO, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_HUDDLA, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_HUDDLA, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_MINOS, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_MINOS, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_NESTOLE, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_NESTOLE, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_URRA, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_URRA, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_URRA, DRCHA_FLAG_INFO2, 1 )
    SetDiaryCharaFlag( DRCHA_MAIA, DRCHA_FLAG_OPEN, 1 )
    SetDiaryCharaFlag( DRCHA_MAIA, DRCHA_FLAG_INFO1, 1 )
    SetDiaryCharaFlag( DRCHA_MAIA, DRCHA_FLAG_INFO2, 1 )
    EquipCostume(ADOL, ICON3D_COS_ADOL_01, EQC_MAIN, EQC_MODE_EVDEFAULT)
    EquipCostume(ADOL, -1, EQC_MAIN, EQC_MODE_EQUIP)
    EquipCostume(ADOL, -1, EQC_MAIN, EQC_MODE_EVFORCE)
    {0}
    {1}
    LoadArg("map/mp1201/mp1201.arg")
    EventCue("mp1201:EV_M01S070_ED")
    {2}
    ResetStopFlag(STOPFLAG_EVENT)
}}
"""
    return APScript + startParams.format(gameSettingFlags,startingCharacter,pastDanaFlags)

def manageEarlyGameParty(patch):
    match patch.settings["starting_character"]:
        case 'Adol':
            party = "(PARTY_ADOL , -1 , -1)"
        case 'Laxia':
            party = "(PARTY_LAXIA , -1 , -1)"
        case 'Sahad':
            party = "(PARTY_SAHAD , -1 , -1)"
        case 'Hummel':
            party = "(PARTY_HUMMEL , -1 , -1)"
        case 'Ricotta':
            party = "(PARTY_RICOTTA , -1 , -1)"
        case 'Dana':
            party = "(PARTY_DANA , -1 , -1)"

    startParams = """
function "earlyGameParty"
{{
    SetPartyMember{0}
}}
"""
    return startParams.format(party)

def soloStartingCharacterEvent(patch):
    match patch.settings["starting_character"]:
        case 'Adol':
            flags = """
    SetFlag(SF_ADOL_JOINOK, 1)
    SetFlag(SF_LAXIA_JOINOK, 0)
    SetFlag(SF_SAHAD_JOINOK, 0)
    SetFlag(SF_HUMMEL_JOINOK, 0)
    SetFlag(SF_RICOTTA_JOINOK, 0)
    SetFlag(SF_DANA_JOINOK, 0)
"""
        case 'Laxia':
            flags = """
    SetFlag(SF_ADOL_JOINOK, 0)
    SetFlag(SF_LAXIA_JOINOK, 1)
    SetFlag(SF_SAHAD_JOINOK, 0)
    SetFlag(SF_HUMMEL_JOINOK, 0)
    SetFlag(SF_RICOTTA_JOINOK, 0)
    SetFlag(SF_DANA_JOINOK, 0)
"""
        case 'Sahad':
            flags = """
    SetFlag(SF_ADOL_JOINOK, 0)
    SetFlag(SF_LAXIA_JOINOK, 0)
    SetFlag(SF_SAHAD_JOINOK, 1)
    SetFlag(SF_HUMMEL_JOINOK, 0)
    SetFlag(SF_RICOTTA_JOINOK, 0)
    SetFlag(SF_DANA_JOINOK, 0)
"""
        case 'Hummel':
            flags = """
    SetFlag(SF_ADOL_JOINOK, 0)
    SetFlag(SF_LAXIA_JOINOK, 0)
    SetFlag(SF_SAHAD_JOINOK, 0)
    SetFlag(SF_HUMMEL_JOINOK, 1)
    SetFlag(SF_RICOTTA_JOINOK, 0)
    SetFlag(SF_DANA_JOINOK, 0)
"""
        case 'Ricotta':
            flags = """
    SetFlag(SF_ADOL_JOINOK, 0)
    SetFlag(SF_LAXIA_JOINOK, 0)
    SetFlag(SF_SAHAD_JOINOK, 0)
    SetFlag(SF_HUMMEL_JOINOK, 0)
    SetFlag(SF_RICOTTA_JOINOK, 1)
    SetFlag(SF_DANA_JOINOK, 0)
"""
        case 'Dana':
            flags = """
    SetFlag(SF_ADOL_JOINOK, 0)
    SetFlag(SF_LAXIA_JOINOK, 0)
    SetFlag(SF_SAHAD_JOINOK, 0)
    SetFlag(SF_HUMMEL_JOINOK, 0)
    SetFlag(SF_RICOTTA_JOINOK, 0)
    SetFlag(SF_DANA_JOINOK, 1)
"""
    partyFlags = """
function "soloEvent"
{{
{0}
}}
"""
    return partyFlags.format(flags)

