from shared.functions import getCharacterJoinLv 

def getCrewFlags(name):
    flag = ''
    match name:
        case "Adol":
            flag = """
    if (FLAG[GF_TBOX_DUMMY129]) //Past Dana Mode
    {
        SetFlag(SF_RESERVE10_JOINOK,1)
    }
    else
    {
        SetFlag(SF_ADOL_JOINED, 1)
        SetFlag(SF_ADOL_JOINOK, 1)
        JoinParty(PARTY_ADOL)
    }

"""         
            flag = flag + getCharacterJoinLv("ADOL")

        case "Laxia": #vanilla function call on mp1101 script rng:0401
            flag = """
    if (FLAG[GF_TBOX_DUMMY129]) //Past Dana Mode
    {
        SetFlag(SF_RESERVE13_JOINOK,1)
    }
    else
    {
        SetFlag(SF_LAXIA_JOINED, 1)
        SetFlag(SF_LAXIA_JOINOK, 1)
        JoinParty(PARTY_LAXIA)
    }
 
    SetDiaryFlag( DF_JOIN_LAXIA, 1 )	

"""
            flag = flag + getCharacterJoinLv("LAXIA")

        case "Captain Barbaros": #vanilla function call on mp1201 script rng:0402
            flag = """
    SetDiaryFlag( DF_JOIN_BARBAROSS, 1 )	//Footprint memo: Reunited with Captain Barbaros.
    JoinNPC(NPC_BARBAROSS, JOIN_NPC_JOIN) // Captain Barbaros joins the interception battle
"""
        case "Little Paro": #vanilla function call on mp1201 script rng:0424
            flag = """
    SetFlag(SF_RESERVE15_JOINOK,1)
    JoinNPC( NPC_PARO, JOIN_NPC_JOIN ) // Little Paro has become a friend
"""
        case "Sahad": #vanilla function call on mp1103 script rng:0404
            flag = """
    if (FLAG[GF_TBOX_DUMMY129]) //Past Dana Mode
    {
        SetFlag(SF_RESERVE11_JOINOK,1)
    }
    else
    {
        SetFlag(SF_SAHAD_JOINED, 1)
        SetFlag(SF_SAHAD_JOINOK, 1)
        JoinParty(PARTY_SAHAD)
    }
 
    SetDiaryFlag( DF_JOIN_SAHAD, 1 )		

"""
            flag = flag + getCharacterJoinLv("SAHAD")

        case "Dogi": #vanilla function call on mp1201 script rng:0405
            flag = """
    SetDiaryFlag( DF_JOIN_DOGI, 1 )	
    JoinNPC(NPC_DOGI, JOIN_NPC_JOIN) // Participate in Dogi interception battle

"""
        case "Alison": #vanilla function call on mp1201 script rng:0406
            flag = """
    SetDiaryFlag( DF_JOIN_ALISON, 1 ) //Footprint memo: Rescued Alison.
    SetFlag(GF_02MP1202_OPEN_DRESS,1)
    SetFlag( GF_CAMP_TAILOR_LV, 1 )
    SetFlag( GF_02MP1201_JOIN_ALISON , 1 ) /// Rescued Alison
    SetFlag( GF_NPC_2A_03_JOIN_ALISON , 1)
    JoinNPC(NPC_ALISON, JOIN_NPC_JOIN) // Rescued Alison
"""
        case "Sir Carlan": #vanilla function call on mp1305 script rng:0407
            flag = """
    JoinNPC( NPC_CURRAN2, JOIN_NPC_JOIN ) //Rescued Lord Kahran.
    SetDiaryFlag( DF_JOIN_CURRAN, 1 ) //Footprint memo: Rescued Lord Kahran.
    SetDiaryFlag( DF_JOIN_CURRAN2, 1 )
"""
        case "Kiergaard": #vanilla function call on mp1305 script rng:0408
            flag = """
    SetFlag( GF_02MP1307_JOIN_KIERGAARD, 1 ) 
    JoinNPC( NPC_KIERGAARD, JOIN_NPC_JOIN ) //Rescued Killgor.
    SetFlag( GF_CAMP_BED_LV, 2 )
    SetDiaryFlag( DF_JOIN_KIERGAARD, 1 ) //Footprint memo: Rescued Killgor.
"""
        case "Kathleen": #vanilla function call on mp1201 script rng:0409
            flag = """
    SetDiaryFlag( DF_JOIN_KATRIN, 1 ) //Footprint memo: Rescued Katrin.
    JoinNPC( NPC_KATRIN, JOIN_NPC_JOIN ) // Katrin has joined
    SetFlag( GF_02MP1201_JOIN_KATRIN , 1 )
"""
        case "Sister Nia": #vanilla function call on mp7471 script rng:0410
            flag = """
    SetDiaryFlag( DF_JOIN_NIA, 1 ) //Footprint memo: Rescued Sister Nia.
    JoinNPC( NPC_NIA, JOIN_NPC_JOIN ) // Joined with Sister Nia
"""
        case "Dina": #vanilla function call on mp1119 script rng:0412
            flag = """
    SetFlag( GF_02MP1119_JOIN_DINA , 1 ) // Meet Dina
    SetFlag(GF_NPC_2_11_JOIN_DINA,1)
    SetDiaryFlag( DF_JOIN_DINA, 1 )  //Footprints memo: Dina was rescued.
    JoinNPC( NPC_DINA, JOIN_NPC_JOIN ) //Rescued Dina
    
    GetItem(ICON3D_US_PESTCIDE,99)
    GetItemMessageExPlus(ICON3D_US_PESTCIDE,99,ITEMMSG_SE_NORMAL," Obtained.",0,0)
    WaitPrompt()
    WaitCloseWindow()	
"""
        case "Reja": #vanilla function call on mp1114 script rng:0413
            flag = """
    SetFlag( GF_SUBEV_JOIN_REJA, 1 )
    SetDiaryFlag( DF_JOIN_REJA, 1 ) //Footprint memo: Reya was rescued.
    SetFlag( GF_CAMP_FARM_LV, 1 ) // Drifting village development settings: Farm LV1
    SetFlag( GF_CAMP_FARMFENCE_LV, 1 ) // Drifting village development settings: Farm fence LV1
    JoinNPC( NPC_REJA, JOIN_NPC_JOIN ) // Joined with Reya
"""
        case "Euron": #vanilla function call on mp2301 script rng:0414
            flag = """
    SetFlag( GF_02MP2301_JOIN_AARON , 1 )	
    SetDiaryFlag( DF_JOIN_AARON, 1 ) //Footprint memo: Aaron has joined the Drifting Village.
    JoinNPC( NPC_AARON, JOIN_NPC_JOIN ) //Joined with Aaron
"""
        case "Licht": #vanilla function call on mp1118 script rng:0415
            flag = """
    SetDiaryFlag( DF_JOIN_LICHT, 1 ) //Footprint memo: Rescued Licht.
    SetFlag( GF_CAMP_BED_LV, 2 ) // Drifting village development settings: Bed LV2
    JoinNPC( NPC_LICHT, JOIN_NPC_JOIN ) // Licht has become a friend
"""
        case "Quina": #vanilla function call on mp1201 script rng:0416
            flag = """
    SetDiaryFlag( DF_JOIN_KUINA, 1 ) //Footprint memo: Kuina was rescued.
    JoinNPC( NPC_KUINA, JOIN_NPC_JOIN ) //Rescued Kuina.
"""
        case "Ricotta": #vanilla function call on mp4202 script rng:0417
            flag = """
    if (FLAG[GF_TBOX_DUMMY129]) //Past Dana Mode
    {
        SetFlag(SF_RESERVE14_JOINOK,1)
    }
    else
    {
        SetFlag(SF_RICOTTA_JOINED, 1)
        SetFlag(SF_RICOTTA_JOINOK, 1)
        JoinParty(PARTY_RICOTTA)
    }

    SetDiaryFlag( DF_JOIN_RICOTTA, 1 )
    SetFlag( GF_QUEST_400, QUEST_START )
    SetDiaryFlag( DF_QS400_START, 1 )

"""
            flag = flag + getCharacterJoinLv("RICOTTA")

        case "Austin": #vanilla function call on mp3107 script rng:0418
            flag = """ 
    SetFlag( GF_SUBEV_JOIN_AUSTEN, 1 ) // Joined with Austin
    SetDiaryFlag( DF_JOIN_AUSTEN, 1 ) //Footprint memo: Rescued Austin.
    JoinNPC( NPC_AUSTEN2, JOIN_NPC_JOIN )// Austin has become a friend
"""
        case "Miralda": #vanilla function call on mp2106 script rng:0419
            flag = """
    SetFlag( GF_SUBEV_JOIN_MIRALDA, 1 )
    SetDiaryFlag( DF_JOIN_MIRALDA, 1 ) //Footprint memo: Rescued Miralda.
    JoinNPC( NPC_MIRALDA, JOIN_NPC_JOIN ) // Joined with Miralda
"""
        case "Thanatos": #vanilla function call on mp1201 script rng:0420
            flag = """

    SetDiaryFlag( DF_JOIN_THANATOS, 1 ) //Footprint memo: Thanatos has joined the Drifting Village.
    JoinNPC( NPC_THANATOS, JOIN_NPC_JOIN ) // Thanatos has become a friend
"""
        case "Hummel": #vanilla function call on mp1108 script rng:0411
            flag = """
    if (FLAG[GF_TBOX_DUMMY129]) //Past Dana Mode
    {
        SetFlag(SF_RESERVE12_JOINOK,1)
    }
    else
    {
        SetFlag(SF_HUMMEL_JOINED, 1)
        SetFlag(SF_HUMMEL_JOINOK, 1)
        JoinParty(PARTY_HUMMEL)
    }

    SetDiaryFlag( DF_JOIN_HUMMEL, 1 )

"""
            flag = flag + getCharacterJoinLv("HUMMEL")

        case "Silvia": #vanilla function call on mp6116 script rng:0421
            flag = """
    SetDiaryFlag( DF_JOIN_SILVIA, 1 ) //Footprint memo: Sylvia has joined the Drifting Village.
    JoinNPC( NPC_SILVIA, JOIN_NPC_JOIN ) // Sylvia has become a friend
"""
        case "Dana": #vanilla function call on mp1210 script rng:0422
            flag = """
    SetFlag(SF_DANA_JOINED, 1)
    SetFlag(SF_DANA_JOINOK, 1)
    SetDiaryFlag( DF_JOIN_DANA, 1 )
    JoinParty(PARTY_DANA)
    
"""
            flag = flag + getCharacterJoinLv("DANA")

        case "Katthew": #vanilla function call on mp6104 script rng:0423
            flag = """
    SetDiaryFlag( DF_JOIN_KASHU, 1 ) //Footprint memo: Rescued Cashu.
    SetFlag( GF_CAMP_SHIPYARD_LV, 7 )
    JoinNPC( NPC_KASHU, JOIN_NPC_JOIN ) // Joined with Cashu
"""
        case "Ed": #vanilla function call on mp1201 script rng:0424
            flag = """
    SetDiaryFlag( DF_JOIN_ED, 1 ) //Footprint memo: Rescued Ed.
    JoinNPC( NPC_ED, JOIN_NPC_JOIN ) // Joined with Ed
    SetFlag( GF_QS510_FIND_ED, 1 ) //Found Ed on your own (achieved hometown flower)
    SetFlag( GF_SUBEV_JOIN_ED, 1 ) //Rescued Ed
    SetDiaryFlag( DF_QS510_END, 1 ) // [QS510]At the same time as finding purple bellweed at Cape Bokkyo
"""
        case "Franz": #vanilla function call on mp4110 script rng:0425
            flag = """
    SetDiaryFlag( DF_JOIN_FRANZ, 1 ) //Footprint memo: Rescued Franz.
    JoinNPC( NPC_FRANZ, JOIN_NPC_JOIN ) // Joined with Franz
"""
        case "Shoebill": #vanilla function call on mp1201 script rng:0426
            flag = """
    JoinNPC( NPC_BALAENICEPS_REX, JOIN_NPC_JOIN ) // Shoebill has joined the party
    SetFlag(SF_RESERVE17_JOINOK,1)
"""
        case "Griselda": #vanilla function call on mp6109 script rng:0427
            flag = """
    SetDiaryFlag( DF_JOIN_GRISELDA, 1 ) //Footprint memo: Griselda has joined the Drifting Village.
    JoinNPC( NPC_GRISELDA, JOIN_NPC_JOIN ) // Joined up with Griselda
"""
        case "Master Kong": #vanilla function call on mp1201 script rng:0428
            flag = """
    JoinNPC( NPC_SKILLMONKY, JOIN_NPC_JOIN ) // Master Kong has become a friend
    SetFlag( SF_RESERVE16_JOINOKBK, 1 )

"""  
    return flag
    
