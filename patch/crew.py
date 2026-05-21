from shared.functions import getCharacterJoinLv 

CREW_FLAGS = {

"Adol":(
"""
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
""" + getCharacterJoinLv("ADOL")),

"Laxia":(#vanilla function call on mp1101 script rng:0401
"""
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
""" + getCharacterJoinLv("LAXIA")),

"Sahad":( #vanilla function call on mp1103 script rng:0404
"""
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
""" + getCharacterJoinLv("SAHAD")),

"Ricotta":( #vanilla function call on mp4202 script rng:0417
"""
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
""" + getCharacterJoinLv("RICOTTA")),

"Hummel":( #vanilla function call on mp1108 script rng:0411
"""
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
""" + getCharacterJoinLv("HUMMEL")),
        
"Dana":( #vanilla function call on mp1210 script rng:0422
"""
    SetFlag(SF_DANA_JOINED, 1)
    SetFlag(SF_DANA_JOINOK, 1)
    SetDiaryFlag( DF_JOIN_DANA, 1 )
    JoinParty(PARTY_DANA)
""" + getCharacterJoinLv("DANA")),

"Captain Barbaros":( #vanilla function call on mp1201 script rng:0402
"""
    SetDiaryFlag( DF_JOIN_BARBAROSS, 1 )	//Footprint memo: Reunited with Captain Barbaros.
    JoinNPC(NPC_BARBAROSS, JOIN_NPC_JOIN) // Captain Barbaros joins the interception battle
"""),

"Little Paro":( #vanilla function call on mp1201 script rng:0424
"""
    SetFlag(SF_RESERVE15_JOINOK,1)
    JoinNPC( NPC_PARO, JOIN_NPC_JOIN ) // Little Paro has become a friend
"""),

"Dogi":( #vanilla function call on mp1201 script rng:0405
"""
    SetDiaryFlag( DF_JOIN_DOGI, 1 )	
    JoinNPC(NPC_DOGI, JOIN_NPC_JOIN) // Participate in Dogi interception battle
"""),

"Alison":( #vanilla function call on mp1201 script rng:0406
"""
    SetDiaryFlag( DF_JOIN_ALISON, 1 ) //Footprint memo: Rescued Alison.
    SetFlag(GF_02MP1202_OPEN_DRESS,1)
    SetFlag( GF_CAMP_TAILOR_LV, 1 )
    SetFlag( GF_02MP1201_JOIN_ALISON , 1 ) /// Rescued Alison
    SetFlag( GF_NPC_2A_03_JOIN_ALISON , 1)
    JoinNPC(NPC_ALISON, JOIN_NPC_JOIN) // Rescued Alison
"""),

"Sir Carlan":( #vanilla function call on mp1305 script rng:0407
"""
    JoinNPC( NPC_CURRAN2, JOIN_NPC_JOIN ) //Rescued Lord Kahran.
    SetDiaryFlag( DF_JOIN_CURRAN, 1 ) //Footprint memo: Rescued Lord Kahran.
    SetDiaryFlag( DF_JOIN_CURRAN2, 1 )
"""),

"Kiergaard":( #vanilla function call on mp1305 script rng:0408
"""
    SetFlag( GF_02MP1307_JOIN_KIERGAARD, 1 ) 
    JoinNPC( NPC_KIERGAARD, JOIN_NPC_JOIN ) //Rescued Killgor.
    SetFlag( GF_CAMP_BED_LV, 2 )
    SetDiaryFlag( DF_JOIN_KIERGAARD, 1 ) //Footprint memo: Rescued Killgor.
"""),

"Kathleen":( #vanilla function call on mp1201 script rng:0409
"""
    SetDiaryFlag( DF_JOIN_KATRIN, 1 ) //Footprint memo: Rescued Katrin.
    JoinNPC( NPC_KATRIN, JOIN_NPC_JOIN ) // Katrin has joined
    SetFlag( GF_02MP1201_JOIN_KATRIN , 1 )
"""),

"Sister Nia":( #vanilla function call on mp7471 script rng:0410
"""
    SetDiaryFlag( DF_JOIN_NIA, 1 ) //Footprint memo: Rescued Sister Nia.
    JoinNPC( NPC_NIA, JOIN_NPC_JOIN ) // Joined with Sister Nia
"""),

"Dina":( #vanilla function call on mp1119 script rng:0412
"""
    SetFlag( GF_02MP1119_JOIN_DINA , 1 ) // Meet Dina
    SetFlag(GF_NPC_2_11_JOIN_DINA,1)
    SetDiaryFlag( DF_JOIN_DINA, 1 )  //Footprints memo: Dina was rescued.
    JoinNPC( NPC_DINA, JOIN_NPC_JOIN ) //Rescued Dina
    
    GetItem(ICON3D_US_PESTCIDE,1)
    GetItemMessageExPlus(ICON3D_US_PESTCIDE,1,ITEMMSG_SE_NORMAL," Obtained.",0,0)
    WaitPrompt()
    WaitCloseWindow()	
"""),

"Reja":( #vanilla function call on mp1114 script rng:0413
"""
    SetFlag( GF_SUBEV_JOIN_REJA, 1 )
    SetDiaryFlag( DF_JOIN_REJA, 1 ) //Footprint memo: Reya was rescued.
    SetFlag( GF_CAMP_FARM_LV, 1 ) // Drifting village development settings: Farm LV1
    SetFlag( GF_CAMP_FARMFENCE_LV, 1 ) // Drifting village development settings: Farm fence LV1
    JoinNPC( NPC_REJA, JOIN_NPC_JOIN ) // Joined with Reya
"""),

"Euron":( #vanilla function call on mp2301 script rng:0414
"""
    SetFlag( GF_02MP2301_JOIN_AARON , 1 )	
    SetDiaryFlag( DF_JOIN_AARON, 1 ) //Footprint memo: Aaron has joined the Drifting Village.
    JoinNPC( NPC_AARON, JOIN_NPC_JOIN ) //Joined with Aaron
"""),

"Licht":( #vanilla function call on mp1118 script rng:0415
"""
    SetDiaryFlag( DF_JOIN_LICHT, 1 ) //Footprint memo: Rescued Licht.
    SetFlag( GF_CAMP_BED_LV, 2 ) // Drifting village development settings: Bed LV2
    JoinNPC( NPC_LICHT, JOIN_NPC_JOIN ) // Licht has become a friend
"""),

"Quina":( #vanilla function call on mp1201 script rng:0416
"""
    SetDiaryFlag( DF_JOIN_KUINA, 1 ) //Footprint memo: Kuina was rescued.
    JoinNPC( NPC_KUINA, JOIN_NPC_JOIN ) //Rescued Kuina.
"""),

"Austin":( #vanilla function call on mp3107 script rng:0418
"""
    SetFlag( GF_SUBEV_JOIN_AUSTEN, 1 ) // Joined with Austin
    SetDiaryFlag( DF_JOIN_AUSTEN, 1 ) //Footprint memo: Rescued Austin.
    JoinNPC( NPC_AUSTEN2, JOIN_NPC_JOIN )// Austin has become a friend
"""),

"Miralda":( #vanilla function call on mp2106 script rng:0419
"""
    SetFlag( GF_SUBEV_JOIN_MIRALDA, 1 )
    SetDiaryFlag( DF_JOIN_MIRALDA, 1 ) //Footprint memo: Rescued Miralda.
    JoinNPC( NPC_MIRALDA, JOIN_NPC_JOIN ) // Joined with Miralda
"""),
    
"Thanatos":( #vanilla function call on mp1201 script rng:0420
"""
    SetDiaryFlag( DF_JOIN_THANATOS, 1 ) //Footprint memo: Thanatos has joined the Drifting Village.
    JoinNPC( NPC_THANATOS, JOIN_NPC_JOIN ) // Thanatos has become a friend
"""),

"Silvia":( #vanilla function call on mp6116 script rng:0421
"""
    SetDiaryFlag( DF_JOIN_SILVIA, 1 ) //Footprint memo: Sylvia has joined the Drifting Village.
    JoinNPC( NPC_SILVIA, JOIN_NPC_JOIN ) // Sylvia has become a friend
"""),

"Katthew":( #vanilla function call on mp6104 script rng:0423
"""
    SetDiaryFlag( DF_JOIN_KASHU, 1 ) //Footprint memo: Rescued Cashu.
    SetFlag( GF_CAMP_SHIPYARD_LV, 7 )
    JoinNPC( NPC_KASHU, JOIN_NPC_JOIN ) // Joined with Cashu
"""),

"Ed":( #vanilla function call on mp1201 script rng:0424
"""
    SetDiaryFlag( DF_JOIN_ED, 1 ) //Footprint memo: Rescued Ed.
    JoinNPC( NPC_ED, JOIN_NPC_JOIN ) // Joined with Ed
    SetFlag( GF_QS510_FIND_ED, 1 ) //Found Ed on your own (achieved hometown flower)
    SetFlag( GF_SUBEV_JOIN_ED, 1 ) //Rescued Ed
    SetDiaryFlag( DF_QS510_END, 1 ) // [QS510]At the same time as finding purple bellweed at Cape Bokkyo
"""),

"Franz":( #vanilla function call on mp4110 script rng:0425
"""
    SetDiaryFlag( DF_JOIN_FRANZ, 1 ) //Footprint memo: Rescued Franz.
    JoinNPC( NPC_FRANZ, JOIN_NPC_JOIN ) // Joined with Franz
"""),

"Shoebill":( #vanilla function call on mp1201 script rng:0426
"""
    JoinNPC( NPC_BALAENICEPS_REX, JOIN_NPC_JOIN ) // Shoebill has joined the party
    SetFlag(SF_RESERVE17_JOINOK,1)
"""),

"Griselda":( #vanilla function call on mp6109 script rng:0427
"""
    SetDiaryFlag( DF_JOIN_GRISELDA, 1 ) //Footprint memo: Griselda has joined the Drifting Village.
    JoinNPC( NPC_GRISELDA, JOIN_NPC_JOIN ) // Joined up with Griselda
"""),

"Master Kong":( #vanilla function call on mp1201 script rng:0428
"""
    JoinNPC( NPC_SKILLMONKY, JOIN_NPC_JOIN ) // Master Kong has become a friend
    SetFlag( SF_RESERVE16_JOINOK, 1 )
""")
}
    
