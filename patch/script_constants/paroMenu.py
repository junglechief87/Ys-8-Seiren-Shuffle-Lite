PARTY_MENU = """
function "Paro_Party"
{
	SetStopFlag(STOPFLAG_TALK)
	SetFlag(TF_MENU_SELECT, 1) // set to 1 so that we can start our while loop, it will get set to 0 before we get our actual character count
	SetFlag(TF_MENU_SELECT2, 0)
	while((FLAG[TF_MENU_SELECT2] != 90 && FLAG[TF_MENU_SELECT2] != -1) && // if close not selected or back button not pressed
            (FLAG[TF_MENU_SELECT] < 1 || FLAG[TF_MENU_SELECT] > 6)) // if too many or too few active members
	{
		SetFlag(TF_MENU_SELECT, 0) // counts active members
		MenuReset()
		MenuType(MENUTYPE_POPUP)
		//--------------------------------------------------------------------------------------
		
		if(FLAG[SF_ADOL_JOINOK]) {
			MenuAdd(10, "#2CAdol (Active)")
			SetFlag( TF_MENU_SELECT, (FLAG[TF_MENU_SELECT] + 1))
		}
		else if(FLAG[SF_ADOL_JOINOKBK]) {
			MenuAdd(11, "Adol (Inactive)")
		}

		if(FLAG[SF_LAXIA_JOINOK]) {
			MenuAdd(20, "#2CLaxia (Active)")
			SetFlag( TF_MENU_SELECT, (FLAG[TF_MENU_SELECT] + 1))
		}
		else if(FLAG[SF_LAXIA_JOINOKBK]) {
			MenuAdd(21, "Laxia (Inactive)")
		}

		if(FLAG[SF_SAHAD_JOINOK]) {
			MenuAdd(30, "#2CSahad (Active)")
			SetFlag( TF_MENU_SELECT, (FLAG[TF_MENU_SELECT] + 1))
		}
		else if(FLAG[SF_SAHAD_JOINOKBK]) {
			MenuAdd(31, "Sahad (Inactive)")
		}

		if(FLAG[SF_HUMMEL_JOINOK]) {
			MenuAdd(40, "#2CHummel (Active)")
			SetFlag( TF_MENU_SELECT, (FLAG[TF_MENU_SELECT] + 1))
		}
		else if(FLAG[SF_HUMMEL_JOINOKBK]) {
			MenuAdd(41, "Hummel (Inactive)")
		}

		if(FLAG[SF_RICOTTA_JOINOK])	{
			MenuAdd(50, "#2CRicotta (Active)")
			SetFlag( TF_MENU_SELECT, (FLAG[TF_MENU_SELECT] + 1))
		}
		else if(FLAG[SF_RICOTTA_JOINOKBK]) {
			MenuAdd(51, "Ricotta (Inactive)")
		}

		if(FLAG[SF_DANA_JOINOK]) {
			MenuAdd(60, "#2CDana (Active)")
			SetFlag( TF_MENU_SELECT, (FLAG[TF_MENU_SELECT] + 1))
		}
		else if(FLAG[SF_DANA_JOINOKBK]) {
			MenuAdd(61, "Dana (Inactive)")
		}
		
		if(FLAG[TF_MENU_SELECT] >= 6 && FLAG[SF_DANA2_JOINOK]) {
			SetFlag(SF_DANA2_JOINOK,0)
			SetFlag(SF_DANA2_JOINOKBK,1)
		}
		
		if(FLAG[SF_DANA2_JOINOK]) {
			MenuAdd(70, "#2CGratika (Active)")
			SetFlag( TF_MENU_SELECT, (FLAG[TF_MENU_SELECT] + 1))
		}
		else if(FLAG[SF_DANA2_JOINOKBK]) {
			MenuAdd(71, "Gratika (Inactive)")
		}
		
		if(FLAG[TF_MENU_SELECT] >= 6 && FLAG[SF_DANA3_JOINOK]) {
			SetFlag(SF_DANA3_JOINOK,0)
			SetFlag(SF_DANA3_JOINOKBK,1)
		}
		
		if(FLAG[SF_DANA3_JOINOK]) {
			MenuAdd(80, "#2CLuminous (Active)")
			SetFlag( TF_MENU_SELECT, (FLAG[TF_MENU_SELECT] + 1))
		}
		else if(FLAG[SF_DANA3_JOINOKBK]) {
			MenuAdd(81, "Luminous (Inactive)")
		}
		
		
		if (FLAG[TF_MENU_SELECT] < 0 || FLAG[TF_MENU_SELECT] > 6) {
			MenuAdd(90, "#0CClose")
		}
		else {
			MenuAdd(91, "Close")
		}
		//--------------------------------------------------------------------------------------
		
		// if 6 or more active, disable all inactive options, if 1 or fewer active, disable all active options, else enable all options
		if (FLAG[TF_MENU_SELECT] >= 6){
			MenuEnable(11,0)
			MenuEnable(21,0)
			MenuEnable(31,0)
			MenuEnable(41,0)
			MenuEnable(51,0)
			MenuEnable(61,0)
			MenuEnable(71,0)
			MenuEnable(81,0)
		}
		else if (FLAG[TF_MENU_SELECT] <= 1){
			MenuEnable(10,0)
			MenuEnable(20,0)
			MenuEnable(30,0)
			MenuEnable(40,0)
			MenuEnable(50,0)
			MenuEnable(60,0)
			MenuEnable(70,0)
			MenuEnable(80,0)
		}
		else{
			MenuEnable(11,1)
			MenuEnable(21,1)
			MenuEnable(31,1)
			MenuEnable(41,1)
			MenuEnable(51,1)
			MenuEnable(61,1)
			MenuEnable(71,1)
			MenuEnable(81,1)
			MenuEnable(10,1)
			MenuEnable(20,1)
			MenuEnable(30,1)
			MenuEnable(40,1)
			MenuEnable(50,1)
			MenuEnable(60,1)
			MenuEnable(70,1)
			MenuEnable(80,1)
		}
		
        // non-highlighted close option is always disabled
		MenuEnable(91,0)
		
		MenuOpen(TF_MENU_SELECT2, 283, ADOLMENU_PPOSY, -2, -2, 10, 1)
		WaitMenu(0)
		CloseMessage(0,0)
		WaitCloseMessage(0)
		MenuClose(0, 0)

        // set flags based on menu selected, it works as a toggle
		if(FLAG[TF_MENU_SELECT2] == 10){
			SetFlag(SF_ADOL_JOINOK,0)
			SetFlag(SF_ADOL_JOINOKBK,1)
		}
		else if(FLAG[TF_MENU_SELECT2] == 11){
			SetFlag(SF_ADOL_JOINOK,1)
			SetFlag(SF_ADOL_JOINOKBK,0)
		}
		else if(FLAG[TF_MENU_SELECT2] == 20){
			SetFlag(SF_LAXIA_JOINOK,0)
			SetFlag(SF_LAXIA_JOINOKBK,1)
		}
		else if(FLAG[TF_MENU_SELECT2] == 21){
			SetFlag(SF_LAXIA_JOINOK,1)
			SetFlag(SF_LAXIA_JOINOKBK,0)
		}
		else if(FLAG[TF_MENU_SELECT2] == 30){
			SetFlag(SF_SAHAD_JOINOK,0)
			SetFlag(SF_SAHAD_JOINOKBK,1)
		}
		else if(FLAG[TF_MENU_SELECT2] == 31){
			SetFlag(SF_SAHAD_JOINOK,1)
			SetFlag(SF_SAHAD_JOINOKBK,0)
		}
		else if(FLAG[TF_MENU_SELECT2] == 40){
			SetFlag(SF_HUMMEL_JOINOK,0)
			SetFlag(SF_HUMMEL_JOINOKBK,1)
		}
		else if(FLAG[TF_MENU_SELECT2] == 41){
			SetFlag(SF_HUMMEL_JOINOK,1)
			SetFlag(SF_HUMMEL_JOINOKBK,0)
		}
		else if(FLAG[TF_MENU_SELECT2] == 50){
			SetFlag(SF_RICOTTA_JOINOK,0)
			SetFlag(SF_RICOTTA_JOINOKBK,1)
		}
		else if(FLAG[TF_MENU_SELECT2] == 51){
			SetFlag(SF_RICOTTA_JOINOK,1)
			SetFlag(SF_RICOTTA_JOINOKBK,0)
		}
		else if(FLAG[TF_MENU_SELECT2] == 60){
			SetFlag(SF_DANA_JOINOK,0)
			SetFlag(SF_DANA_JOINOKBK,1)
		}
		else if(FLAG[TF_MENU_SELECT2] == 61){
			SetFlag(SF_DANA_JOINOK,1)
			SetFlag(SF_DANA_JOINOKBK,0)
		}
		else if(FLAG[TF_MENU_SELECT2] == 70){
			SetFlag(SF_DANA2_JOINOK,0)
			SetFlag(SF_DANA2_JOINOKBK,1)
		}
		else if(FLAG[TF_MENU_SELECT2] == 71){
			SetFlag(SF_DANA2_JOINOK,1)
			SetFlag(SF_DANA2_JOINOKBK,0)
		}
		else if(FLAG[TF_MENU_SELECT2] == 80){
			SetFlag(SF_DANA3_JOINOK,0)
			SetFlag(SF_DANA3_JOINOKBK,1)
		}
		else if(FLAG[TF_MENU_SELECT2] == 81){
			SetFlag(SF_DANA3_JOINOK,1)
			SetFlag(SF_DANA3_JOINOKBK,0)
		}
		
        // process party changes based on flags set above
		CallFunc("rng:processParty")
	}
	SetFlag(TF_MENU_SELECT, 0)
	SetFlag(TF_MENU_SELECT2, 0)
	
	ResetStopFlag(STOPFLAG_TALK)
}

function "processParty"
{
	if(!FLAG[SF_ADOL_JOINOK]){
		SeparateParty(PARTY_ADOL)
	}
	else{
		JoinParty(PARTY_ADOL)
	}
	
	if(!FLAG[SF_LAXIA_JOINOK]){
		SeparateParty(PARTY_LAXIA)
	}
	else{
		JoinParty(PARTY_LAXIA)
	}
	
	if(!FLAG[SF_SAHAD_JOINOK]){
		SeparateParty(PARTY_SAHAD)
	}
	else{
		JoinParty(PARTY_SAHAD)
	}
	
	if(!FLAG[SF_HUMMEL_JOINOK]){
		SeparateParty(PARTY_HUMMEL)
	}
	else{
		JoinParty(PARTY_HUMMEL)
	}
	
	if(!FLAG[SF_RICOTTA_JOINOK]){
		SeparateParty(PARTY_RICOTTA)
	}
	else{
		JoinParty(PARTY_RICOTTA)
	}
	
	if(!FLAG[SF_DANA_JOINOK]){
		SeparateParty(PARTY_DANA)
	}
	else{
		JoinParty(PARTY_DANA)
	}
	
	if(!FLAG[SF_DANA2_JOINOK]){
		SeparateParty(PARTY_DANA2)
	}
	else{
		JoinParty(PARTY_DANA2)
	}
	
	if(!FLAG[SF_DANA3_JOINOK]){
		SeparateParty(PARTY_DANA3)
	}
	else{
		JoinParty(PARTY_DANA3)
	}
}

function "count_party"
{
	SetFlag( TF_MENU_SELECT, 0 )
	// count current active party
	if(FLAG[SF_ADOL_JOINOK]) {
		SetFlag( TF_MENU_SELECT, (FLAG[TF_MENU_SELECT] + 1))
	}
	if(FLAG[SF_LAXIA_JOINOK]) {
		SetFlag( TF_MENU_SELECT, (FLAG[TF_MENU_SELECT] + 1))
	}
	if(FLAG[SF_SAHAD_JOINOK]) {
		SetFlag( TF_MENU_SELECT, (FLAG[TF_MENU_SELECT] + 1))
	}
	if(FLAG[SF_HUMMEL_JOINOK]) {
		SetFlag( TF_MENU_SELECT, (FLAG[TF_MENU_SELECT] + 1))
	}
	if(FLAG[SF_RICOTTA_JOINOK])	{
		SetFlag( TF_MENU_SELECT, (FLAG[TF_MENU_SELECT] + 1))
	}
	if(FLAG[SF_DANA_JOINOK]) {
		SetFlag( TF_MENU_SELECT, (FLAG[TF_MENU_SELECT] + 1))
	}
	if(FLAG[SF_DANA2_JOINOK]) {
		SetFlag( TF_MENU_SELECT, (FLAG[TF_MENU_SELECT] + 1))
	}
	if(FLAG[SF_DANA3_JOINOK]) {
		SetFlag( TF_MENU_SELECT, (FLAG[TF_MENU_SELECT] + 1))
	}
}

"""