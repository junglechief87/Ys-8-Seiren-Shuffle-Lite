FSC_WARP = """
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