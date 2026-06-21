PARTY_MENU = """
function "Paro_Party"
{
	SetStopFlag(STOPFLAG_TALK)
	SetFlag(TF_MENU_SELECT2, 0)
	while(FLAG[TF_MENU_SELECT2] != 90 && FLAG[TF_MENU_SELECT2] != -1) // if close not selected or back button not pressed
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
		
		
		if (FLAG[TF_MENU_SELECT] < 1 || FLAG[TF_MENU_SELECT] > 6) {
			MenuAdd(91, "Close")
		}
		else {
			MenuAdd(90, "#0CClose")
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
        CallFunc("rng:checkLevel")
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

function "checkLevel"
{
	if(ADOL.CHRWORK[CWK_LV] == 0)
	{
		if(FLAG[GF_TBOX_DUMMY121] == 1){SetLevel(ADOL,1)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 2){SetLevel(ADOL,2)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 3){SetLevel(ADOL,3)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 4){SetLevel(ADOL,4)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 5){SetLevel(ADOL,5)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 6){SetLevel(ADOL,6)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 7){SetLevel(ADOL,7)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 8){SetLevel(ADOL,8)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 9){SetLevel(ADOL,9)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 10){SetLevel(ADOL,10)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 11){SetLevel(ADOL,11)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 12){SetLevel(ADOL,12)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 13){SetLevel(ADOL,13)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 14){SetLevel(ADOL,14)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 15){SetLevel(ADOL,15)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 16){SetLevel(ADOL,16)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 17){SetLevel(ADOL,17)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 18){SetLevel(ADOL,18)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 19){SetLevel(ADOL,19)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 20){SetLevel(ADOL,20)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 21){SetLevel(ADOL,21)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 22){SetLevel(ADOL,22)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 23){SetLevel(ADOL,23)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 24){SetLevel(ADOL,24)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 25){SetLevel(ADOL,25)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 26){SetLevel(ADOL,26)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 27){SetLevel(ADOL,27)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 28){SetLevel(ADOL,28)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 29){SetLevel(ADOL,29)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 30){SetLevel(ADOL,30)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 31){SetLevel(ADOL,31)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 32){SetLevel(ADOL,32)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 33){SetLevel(ADOL,33)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 34){SetLevel(ADOL,34)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 35){SetLevel(ADOL,35)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 36){SetLevel(ADOL,36)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 37){SetLevel(ADOL,37)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 38){SetLevel(ADOL,38)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 39){SetLevel(ADOL,39)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 40){SetLevel(ADOL,40)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 41){SetLevel(ADOL,41)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 42){SetLevel(ADOL,42)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 43){SetLevel(ADOL,43)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 44){SetLevel(ADOL,44)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 45){SetLevel(ADOL,45)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 46){SetLevel(ADOL,46)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 47){SetLevel(ADOL,47)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 48){SetLevel(ADOL,48)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 49){SetLevel(ADOL,49)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 50){SetLevel(ADOL,50)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 51){SetLevel(ADOL,51)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 52){SetLevel(ADOL,52)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 53){SetLevel(ADOL,53)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 54){SetLevel(ADOL,54)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 55){SetLevel(ADOL,55)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 56){SetLevel(ADOL,56)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 57){SetLevel(ADOL,57)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 58){SetLevel(ADOL,58)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 59){SetLevel(ADOL,59)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 60){SetLevel(ADOL,60)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 61){SetLevel(ADOL,61)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 62){SetLevel(ADOL,62)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 63){SetLevel(ADOL,63)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 64){SetLevel(ADOL,64)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 65){SetLevel(ADOL,65)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 66){SetLevel(ADOL,66)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 67){SetLevel(ADOL,67)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 68){SetLevel(ADOL,68)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 69){SetLevel(ADOL,69)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 70){SetLevel(ADOL,70)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 71){SetLevel(ADOL,71)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 72){SetLevel(ADOL,72)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 73){SetLevel(ADOL,73)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 74){SetLevel(ADOL,74)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 75){SetLevel(ADOL,75)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 76){SetLevel(ADOL,76)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 77){SetLevel(ADOL,77)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 78){SetLevel(ADOL,78)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 79){SetLevel(ADOL,79)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 80){SetLevel(ADOL,80)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 81){SetLevel(ADOL,81)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 82){SetLevel(ADOL,82)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 83){SetLevel(ADOL,83)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 84){SetLevel(ADOL,84)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 85){SetLevel(ADOL,85)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 86){SetLevel(ADOL,86)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 87){SetLevel(ADOL,87)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 88){SetLevel(ADOL,88)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 89){SetLevel(ADOL,89)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 90){SetLevel(ADOL,90)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 91){SetLevel(ADOL,91)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 92){SetLevel(ADOL,92)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 93){SetLevel(ADOL,93)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 94){SetLevel(ADOL,94)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 95){SetLevel(ADOL,95)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 96){SetLevel(ADOL,96)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 97){SetLevel(ADOL,97)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 98){SetLevel(ADOL,98)} 
		else{SetLevel(ADOL,99)}
	}
	if(LAXIA.CHRWORK[CWK_LV] == 0)
	{
		if(FLAG[GF_TBOX_DUMMY121] == 1){SetLevel(LAXIA,1)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 2){SetLevel(LAXIA,2)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 3){SetLevel(LAXIA,3)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 4){SetLevel(LAXIA,4)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 5){SetLevel(LAXIA,5)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 6){SetLevel(LAXIA,6)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 7){SetLevel(LAXIA,7)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 8){SetLevel(LAXIA,8)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 9){SetLevel(LAXIA,9)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 10){SetLevel(LAXIA,10)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 11){SetLevel(LAXIA,11)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 12){SetLevel(LAXIA,12)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 13){SetLevel(LAXIA,13)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 14){SetLevel(LAXIA,14)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 15){SetLevel(LAXIA,15)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 16){SetLevel(LAXIA,16)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 17){SetLevel(LAXIA,17)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 18){SetLevel(LAXIA,18)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 19){SetLevel(LAXIA,19)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 20){SetLevel(LAXIA,20)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 21){SetLevel(LAXIA,21)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 22){SetLevel(LAXIA,22)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 23){SetLevel(LAXIA,23)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 24){SetLevel(LAXIA,24)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 25){SetLevel(LAXIA,25)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 26){SetLevel(LAXIA,26)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 27){SetLevel(LAXIA,27)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 28){SetLevel(LAXIA,28)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 29){SetLevel(LAXIA,29)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 30){SetLevel(LAXIA,30)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 31){SetLevel(LAXIA,31)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 32){SetLevel(LAXIA,32)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 33){SetLevel(LAXIA,33)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 34){SetLevel(LAXIA,34)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 35){SetLevel(LAXIA,35)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 36){SetLevel(LAXIA,36)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 37){SetLevel(LAXIA,37)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 38){SetLevel(LAXIA,38)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 39){SetLevel(LAXIA,39)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 40){SetLevel(LAXIA,40)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 41){SetLevel(LAXIA,41)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 42){SetLevel(LAXIA,42)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 43){SetLevel(LAXIA,43)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 44){SetLevel(LAXIA,44)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 45){SetLevel(LAXIA,45)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 46){SetLevel(LAXIA,46)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 47){SetLevel(LAXIA,47)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 48){SetLevel(LAXIA,48)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 49){SetLevel(LAXIA,49)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 50){SetLevel(LAXIA,50)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 51){SetLevel(LAXIA,51)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 52){SetLevel(LAXIA,52)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 53){SetLevel(LAXIA,53)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 54){SetLevel(LAXIA,54)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 55){SetLevel(LAXIA,55)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 56){SetLevel(LAXIA,56)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 57){SetLevel(LAXIA,57)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 58){SetLevel(LAXIA,58)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 59){SetLevel(LAXIA,59)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 60){SetLevel(LAXIA,60)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 61){SetLevel(LAXIA,61)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 62){SetLevel(LAXIA,62)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 63){SetLevel(LAXIA,63)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 64){SetLevel(LAXIA,64)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 65){SetLevel(LAXIA,65)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 66){SetLevel(LAXIA,66)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 67){SetLevel(LAXIA,67)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 68){SetLevel(LAXIA,68)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 69){SetLevel(LAXIA,69)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 70){SetLevel(LAXIA,70)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 71){SetLevel(LAXIA,71)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 72){SetLevel(LAXIA,72)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 73){SetLevel(LAXIA,73)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 74){SetLevel(LAXIA,74)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 75){SetLevel(LAXIA,75)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 76){SetLevel(LAXIA,76)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 77){SetLevel(LAXIA,77)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 78){SetLevel(LAXIA,78)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 79){SetLevel(LAXIA,79)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 80){SetLevel(LAXIA,80)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 81){SetLevel(LAXIA,81)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 82){SetLevel(LAXIA,82)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 83){SetLevel(LAXIA,83)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 84){SetLevel(LAXIA,84)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 85){SetLevel(LAXIA,85)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 86){SetLevel(LAXIA,86)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 87){SetLevel(LAXIA,87)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 88){SetLevel(LAXIA,88)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 89){SetLevel(LAXIA,89)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 90){SetLevel(LAXIA,90)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 91){SetLevel(LAXIA,91)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 92){SetLevel(LAXIA,92)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 93){SetLevel(LAXIA,93)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 94){SetLevel(LAXIA,94)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 95){SetLevel(LAXIA,95)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 96){SetLevel(LAXIA,96)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 97){SetLevel(LAXIA,97)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 98){SetLevel(LAXIA,98)} 
		else{SetLevel(LAXIA,99)}
	}
	if(SAHAD.CHRWORK[CWK_LV] == 0)
	{
		if(FLAG[GF_TBOX_DUMMY121] == 1){SetLevel(SAHAD,1)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 2){SetLevel(SAHAD,2)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 3){SetLevel(SAHAD,3)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 4){SetLevel(SAHAD,4)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 5){SetLevel(SAHAD,5)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 6){SetLevel(SAHAD,6)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 7){SetLevel(SAHAD,7)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 8){SetLevel(SAHAD,8)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 9){SetLevel(SAHAD,9)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 10){SetLevel(SAHAD,10)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 11){SetLevel(SAHAD,11)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 12){SetLevel(SAHAD,12)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 13){SetLevel(SAHAD,13)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 14){SetLevel(SAHAD,14)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 15){SetLevel(SAHAD,15)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 16){SetLevel(SAHAD,16)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 17){SetLevel(SAHAD,17)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 18){SetLevel(SAHAD,18)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 19){SetLevel(SAHAD,19)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 20){SetLevel(SAHAD,20)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 21){SetLevel(SAHAD,21)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 22){SetLevel(SAHAD,22)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 23){SetLevel(SAHAD,23)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 24){SetLevel(SAHAD,24)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 25){SetLevel(SAHAD,25)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 26){SetLevel(SAHAD,26)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 27){SetLevel(SAHAD,27)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 28){SetLevel(SAHAD,28)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 29){SetLevel(SAHAD,29)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 30){SetLevel(SAHAD,30)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 31){SetLevel(SAHAD,31)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 32){SetLevel(SAHAD,32)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 33){SetLevel(SAHAD,33)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 34){SetLevel(SAHAD,34)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 35){SetLevel(SAHAD,35)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 36){SetLevel(SAHAD,36)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 37){SetLevel(SAHAD,37)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 38){SetLevel(SAHAD,38)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 39){SetLevel(SAHAD,39)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 40){SetLevel(SAHAD,40)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 41){SetLevel(SAHAD,41)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 42){SetLevel(SAHAD,42)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 43){SetLevel(SAHAD,43)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 44){SetLevel(SAHAD,44)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 45){SetLevel(SAHAD,45)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 46){SetLevel(SAHAD,46)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 47){SetLevel(SAHAD,47)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 48){SetLevel(SAHAD,48)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 49){SetLevel(SAHAD,49)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 50){SetLevel(SAHAD,50)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 51){SetLevel(SAHAD,51)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 52){SetLevel(SAHAD,52)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 53){SetLevel(SAHAD,53)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 54){SetLevel(SAHAD,54)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 55){SetLevel(SAHAD,55)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 56){SetLevel(SAHAD,56)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 57){SetLevel(SAHAD,57)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 58){SetLevel(SAHAD,58)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 59){SetLevel(SAHAD,59)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 60){SetLevel(SAHAD,60)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 61){SetLevel(SAHAD,61)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 62){SetLevel(SAHAD,62)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 63){SetLevel(SAHAD,63)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 64){SetLevel(SAHAD,64)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 65){SetLevel(SAHAD,65)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 66){SetLevel(SAHAD,66)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 67){SetLevel(SAHAD,67)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 68){SetLevel(SAHAD,68)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 69){SetLevel(SAHAD,69)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 70){SetLevel(SAHAD,70)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 71){SetLevel(SAHAD,71)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 72){SetLevel(SAHAD,72)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 73){SetLevel(SAHAD,73)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 74){SetLevel(SAHAD,74)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 75){SetLevel(SAHAD,75)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 76){SetLevel(SAHAD,76)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 77){SetLevel(SAHAD,77)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 78){SetLevel(SAHAD,78)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 79){SetLevel(SAHAD,79)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 80){SetLevel(SAHAD,80)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 81){SetLevel(SAHAD,81)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 82){SetLevel(SAHAD,82)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 83){SetLevel(SAHAD,83)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 84){SetLevel(SAHAD,84)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 85){SetLevel(SAHAD,85)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 86){SetLevel(SAHAD,86)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 87){SetLevel(SAHAD,87)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 88){SetLevel(SAHAD,88)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 89){SetLevel(SAHAD,89)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 90){SetLevel(SAHAD,90)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 91){SetLevel(SAHAD,91)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 92){SetLevel(SAHAD,92)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 93){SetLevel(SAHAD,93)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 94){SetLevel(SAHAD,94)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 95){SetLevel(SAHAD,95)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 96){SetLevel(SAHAD,96)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 97){SetLevel(SAHAD,97)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 98){SetLevel(SAHAD,98)} 
		else{SetLevel(SAHAD,99)}
	}
	if(HUMMEL.CHRWORK[CWK_LV] == 0)
	{
		if(FLAG[GF_TBOX_DUMMY121] == 1){SetLevel(HUMMEL,1)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 2){SetLevel(HUMMEL,2)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 3){SetLevel(HUMMEL,3)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 4){SetLevel(HUMMEL,4)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 5){SetLevel(HUMMEL,5)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 6){SetLevel(HUMMEL,6)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 7){SetLevel(HUMMEL,7)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 8){SetLevel(HUMMEL,8)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 9){SetLevel(HUMMEL,9)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 10){SetLevel(HUMMEL,10)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 11){SetLevel(HUMMEL,11)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 12){SetLevel(HUMMEL,12)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 13){SetLevel(HUMMEL,13)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 14){SetLevel(HUMMEL,14)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 15){SetLevel(HUMMEL,15)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 16){SetLevel(HUMMEL,16)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 17){SetLevel(HUMMEL,17)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 18){SetLevel(HUMMEL,18)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 19){SetLevel(HUMMEL,19)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 20){SetLevel(HUMMEL,20)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 21){SetLevel(HUMMEL,21)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 22){SetLevel(HUMMEL,22)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 23){SetLevel(HUMMEL,23)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 24){SetLevel(HUMMEL,24)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 25){SetLevel(HUMMEL,25)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 26){SetLevel(HUMMEL,26)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 27){SetLevel(HUMMEL,27)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 28){SetLevel(HUMMEL,28)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 29){SetLevel(HUMMEL,29)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 30){SetLevel(HUMMEL,30)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 31){SetLevel(HUMMEL,31)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 32){SetLevel(HUMMEL,32)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 33){SetLevel(HUMMEL,33)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 34){SetLevel(HUMMEL,34)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 35){SetLevel(HUMMEL,35)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 36){SetLevel(HUMMEL,36)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 37){SetLevel(HUMMEL,37)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 38){SetLevel(HUMMEL,38)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 39){SetLevel(HUMMEL,39)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 40){SetLevel(HUMMEL,40)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 41){SetLevel(HUMMEL,41)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 42){SetLevel(HUMMEL,42)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 43){SetLevel(HUMMEL,43)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 44){SetLevel(HUMMEL,44)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 45){SetLevel(HUMMEL,45)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 46){SetLevel(HUMMEL,46)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 47){SetLevel(HUMMEL,47)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 48){SetLevel(HUMMEL,48)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 49){SetLevel(HUMMEL,49)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 50){SetLevel(HUMMEL,50)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 51){SetLevel(HUMMEL,51)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 52){SetLevel(HUMMEL,52)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 53){SetLevel(HUMMEL,53)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 54){SetLevel(HUMMEL,54)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 55){SetLevel(HUMMEL,55)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 56){SetLevel(HUMMEL,56)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 57){SetLevel(HUMMEL,57)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 58){SetLevel(HUMMEL,58)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 59){SetLevel(HUMMEL,59)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 60){SetLevel(HUMMEL,60)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 61){SetLevel(HUMMEL,61)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 62){SetLevel(HUMMEL,62)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 63){SetLevel(HUMMEL,63)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 64){SetLevel(HUMMEL,64)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 65){SetLevel(HUMMEL,65)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 66){SetLevel(HUMMEL,66)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 67){SetLevel(HUMMEL,67)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 68){SetLevel(HUMMEL,68)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 69){SetLevel(HUMMEL,69)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 70){SetLevel(HUMMEL,70)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 71){SetLevel(HUMMEL,71)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 72){SetLevel(HUMMEL,72)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 73){SetLevel(HUMMEL,73)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 74){SetLevel(HUMMEL,74)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 75){SetLevel(HUMMEL,75)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 76){SetLevel(HUMMEL,76)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 77){SetLevel(HUMMEL,77)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 78){SetLevel(HUMMEL,78)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 79){SetLevel(HUMMEL,79)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 80){SetLevel(HUMMEL,80)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 81){SetLevel(HUMMEL,81)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 82){SetLevel(HUMMEL,82)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 83){SetLevel(HUMMEL,83)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 84){SetLevel(HUMMEL,84)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 85){SetLevel(HUMMEL,85)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 86){SetLevel(HUMMEL,86)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 87){SetLevel(HUMMEL,87)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 88){SetLevel(HUMMEL,88)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 89){SetLevel(HUMMEL,89)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 90){SetLevel(HUMMEL,90)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 91){SetLevel(HUMMEL,91)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 92){SetLevel(HUMMEL,92)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 93){SetLevel(HUMMEL,93)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 94){SetLevel(HUMMEL,94)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 95){SetLevel(HUMMEL,95)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 96){SetLevel(HUMMEL,96)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 97){SetLevel(HUMMEL,97)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 98){SetLevel(HUMMEL,98)} 
		else{SetLevel(HUMMEL,99)}
	}
	if(RICOTTA.CHRWORK[CWK_LV] == 0)
	{
		if(FLAG[GF_TBOX_DUMMY121] == 1){SetLevel(RICOTTA,1)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 2){SetLevel(RICOTTA,2)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 3){SetLevel(RICOTTA,3)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 4){SetLevel(RICOTTA,4)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 5){SetLevel(RICOTTA,5)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 6){SetLevel(RICOTTA,6)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 7){SetLevel(RICOTTA,7)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 8){SetLevel(RICOTTA,8)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 9){SetLevel(RICOTTA,9)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 10){SetLevel(RICOTTA,10)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 11){SetLevel(RICOTTA,11)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 12){SetLevel(RICOTTA,12)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 13){SetLevel(RICOTTA,13)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 14){SetLevel(RICOTTA,14)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 15){SetLevel(RICOTTA,15)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 16){SetLevel(RICOTTA,16)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 17){SetLevel(RICOTTA,17)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 18){SetLevel(RICOTTA,18)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 19){SetLevel(RICOTTA,19)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 20){SetLevel(RICOTTA,20)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 21){SetLevel(RICOTTA,21)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 22){SetLevel(RICOTTA,22)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 23){SetLevel(RICOTTA,23)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 24){SetLevel(RICOTTA,24)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 25){SetLevel(RICOTTA,25)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 26){SetLevel(RICOTTA,26)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 27){SetLevel(RICOTTA,27)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 28){SetLevel(RICOTTA,28)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 29){SetLevel(RICOTTA,29)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 30){SetLevel(RICOTTA,30)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 31){SetLevel(RICOTTA,31)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 32){SetLevel(RICOTTA,32)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 33){SetLevel(RICOTTA,33)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 34){SetLevel(RICOTTA,34)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 35){SetLevel(RICOTTA,35)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 36){SetLevel(RICOTTA,36)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 37){SetLevel(RICOTTA,37)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 38){SetLevel(RICOTTA,38)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 39){SetLevel(RICOTTA,39)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 40){SetLevel(RICOTTA,40)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 41){SetLevel(RICOTTA,41)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 42){SetLevel(RICOTTA,42)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 43){SetLevel(RICOTTA,43)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 44){SetLevel(RICOTTA,44)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 45){SetLevel(RICOTTA,45)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 46){SetLevel(RICOTTA,46)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 47){SetLevel(RICOTTA,47)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 48){SetLevel(RICOTTA,48)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 49){SetLevel(RICOTTA,49)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 50){SetLevel(RICOTTA,50)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 51){SetLevel(RICOTTA,51)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 52){SetLevel(RICOTTA,52)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 53){SetLevel(RICOTTA,53)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 54){SetLevel(RICOTTA,54)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 55){SetLevel(RICOTTA,55)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 56){SetLevel(RICOTTA,56)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 57){SetLevel(RICOTTA,57)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 58){SetLevel(RICOTTA,58)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 59){SetLevel(RICOTTA,59)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 60){SetLevel(RICOTTA,60)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 61){SetLevel(RICOTTA,61)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 62){SetLevel(RICOTTA,62)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 63){SetLevel(RICOTTA,63)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 64){SetLevel(RICOTTA,64)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 65){SetLevel(RICOTTA,65)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 66){SetLevel(RICOTTA,66)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 67){SetLevel(RICOTTA,67)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 68){SetLevel(RICOTTA,68)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 69){SetLevel(RICOTTA,69)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 70){SetLevel(RICOTTA,70)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 71){SetLevel(RICOTTA,71)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 72){SetLevel(RICOTTA,72)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 73){SetLevel(RICOTTA,73)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 74){SetLevel(RICOTTA,74)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 75){SetLevel(RICOTTA,75)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 76){SetLevel(RICOTTA,76)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 77){SetLevel(RICOTTA,77)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 78){SetLevel(RICOTTA,78)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 79){SetLevel(RICOTTA,79)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 80){SetLevel(RICOTTA,80)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 81){SetLevel(RICOTTA,81)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 82){SetLevel(RICOTTA,82)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 83){SetLevel(RICOTTA,83)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 84){SetLevel(RICOTTA,84)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 85){SetLevel(RICOTTA,85)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 86){SetLevel(RICOTTA,86)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 87){SetLevel(RICOTTA,87)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 88){SetLevel(RICOTTA,88)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 89){SetLevel(RICOTTA,89)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 90){SetLevel(RICOTTA,90)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 91){SetLevel(RICOTTA,91)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 92){SetLevel(RICOTTA,92)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 93){SetLevel(RICOTTA,93)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 94){SetLevel(RICOTTA,94)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 95){SetLevel(RICOTTA,95)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 96){SetLevel(RICOTTA,96)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 97){SetLevel(RICOTTA,97)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 98){SetLevel(RICOTTA,98)} 
		else{SetLevel(RICOTTA,99)}
	}
	if(DANA.CHRWORK[CWK_LV] == 0)
	{
		if(FLAG[GF_TBOX_DUMMY121] == 1){SetLevel(DANA,1)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 2){SetLevel(DANA,2)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 3){SetLevel(DANA,3)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 4){SetLevel(DANA,4)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 5){SetLevel(DANA,5)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 6){SetLevel(DANA,6)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 7){SetLevel(DANA,7)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 8){SetLevel(DANA,8)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 9){SetLevel(DANA,9)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 10){SetLevel(DANA,10)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 11){SetLevel(DANA,11)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 12){SetLevel(DANA,12)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 13){SetLevel(DANA,13)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 14){SetLevel(DANA,14)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 15){SetLevel(DANA,15)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 16){SetLevel(DANA,16)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 17){SetLevel(DANA,17)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 18){SetLevel(DANA,18)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 19){SetLevel(DANA,19)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 20){SetLevel(DANA,20)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 21){SetLevel(DANA,21)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 22){SetLevel(DANA,22)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 23){SetLevel(DANA,23)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 24){SetLevel(DANA,24)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 25){SetLevel(DANA,25)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 26){SetLevel(DANA,26)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 27){SetLevel(DANA,27)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 28){SetLevel(DANA,28)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 29){SetLevel(DANA,29)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 30){SetLevel(DANA,30)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 31){SetLevel(DANA,31)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 32){SetLevel(DANA,32)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 33){SetLevel(DANA,33)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 34){SetLevel(DANA,34)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 35){SetLevel(DANA,35)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 36){SetLevel(DANA,36)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 37){SetLevel(DANA,37)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 38){SetLevel(DANA,38)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 39){SetLevel(DANA,39)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 40){SetLevel(DANA,40)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 41){SetLevel(DANA,41)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 42){SetLevel(DANA,42)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 43){SetLevel(DANA,43)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 44){SetLevel(DANA,44)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 45){SetLevel(DANA,45)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 46){SetLevel(DANA,46)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 47){SetLevel(DANA,47)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 48){SetLevel(DANA,48)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 49){SetLevel(DANA,49)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 50){SetLevel(DANA,50)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 51){SetLevel(DANA,51)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 52){SetLevel(DANA,52)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 53){SetLevel(DANA,53)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 54){SetLevel(DANA,54)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 55){SetLevel(DANA,55)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 56){SetLevel(DANA,56)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 57){SetLevel(DANA,57)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 58){SetLevel(DANA,58)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 59){SetLevel(DANA,59)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 60){SetLevel(DANA,60)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 61){SetLevel(DANA,61)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 62){SetLevel(DANA,62)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 63){SetLevel(DANA,63)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 64){SetLevel(DANA,64)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 65){SetLevel(DANA,65)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 66){SetLevel(DANA,66)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 67){SetLevel(DANA,67)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 68){SetLevel(DANA,68)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 69){SetLevel(DANA,69)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 70){SetLevel(DANA,70)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 71){SetLevel(DANA,71)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 72){SetLevel(DANA,72)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 73){SetLevel(DANA,73)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 74){SetLevel(DANA,74)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 75){SetLevel(DANA,75)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 76){SetLevel(DANA,76)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 77){SetLevel(DANA,77)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 78){SetLevel(DANA,78)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 79){SetLevel(DANA,79)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 80){SetLevel(DANA,80)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 81){SetLevel(DANA,81)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 82){SetLevel(DANA,82)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 83){SetLevel(DANA,83)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 84){SetLevel(DANA,84)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 85){SetLevel(DANA,85)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 86){SetLevel(DANA,86)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 87){SetLevel(DANA,87)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 88){SetLevel(DANA,88)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 89){SetLevel(DANA,89)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 90){SetLevel(DANA,90)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 91){SetLevel(DANA,91)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 92){SetLevel(DANA,92)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 93){SetLevel(DANA,93)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 94){SetLevel(DANA,94)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 95){SetLevel(DANA,95)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 96){SetLevel(DANA,96)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 97){SetLevel(DANA,97)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 98){SetLevel(DANA,98)} 
		else{SetLevel(DANA,99)}
	}
	if(DANA2.CHRWORK[CWK_LV] == 0)
	{
		if(FLAG[GF_TBOX_DUMMY121] == 1){SetLevel(DANA2,1)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 2){SetLevel(DANA2,2)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 3){SetLevel(DANA2,3)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 4){SetLevel(DANA2,4)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 5){SetLevel(DANA2,5)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 6){SetLevel(DANA2,6)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 7){SetLevel(DANA2,7)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 8){SetLevel(DANA2,8)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 9){SetLevel(DANA2,9)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 10){SetLevel(DANA2,10)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 11){SetLevel(DANA2,11)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 12){SetLevel(DANA2,12)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 13){SetLevel(DANA2,13)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 14){SetLevel(DANA2,14)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 15){SetLevel(DANA2,15)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 16){SetLevel(DANA2,16)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 17){SetLevel(DANA2,17)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 18){SetLevel(DANA2,18)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 19){SetLevel(DANA2,19)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 20){SetLevel(DANA2,20)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 21){SetLevel(DANA2,21)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 22){SetLevel(DANA2,22)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 23){SetLevel(DANA2,23)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 24){SetLevel(DANA2,24)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 25){SetLevel(DANA2,25)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 26){SetLevel(DANA2,26)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 27){SetLevel(DANA2,27)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 28){SetLevel(DANA2,28)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 29){SetLevel(DANA2,29)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 30){SetLevel(DANA2,30)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 31){SetLevel(DANA2,31)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 32){SetLevel(DANA2,32)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 33){SetLevel(DANA2,33)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 34){SetLevel(DANA2,34)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 35){SetLevel(DANA2,35)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 36){SetLevel(DANA2,36)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 37){SetLevel(DANA2,37)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 38){SetLevel(DANA2,38)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 39){SetLevel(DANA2,39)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 40){SetLevel(DANA2,40)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 41){SetLevel(DANA2,41)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 42){SetLevel(DANA2,42)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 43){SetLevel(DANA2,43)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 44){SetLevel(DANA2,44)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 45){SetLevel(DANA2,45)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 46){SetLevel(DANA2,46)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 47){SetLevel(DANA2,47)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 48){SetLevel(DANA2,48)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 49){SetLevel(DANA2,49)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 50){SetLevel(DANA2,50)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 51){SetLevel(DANA2,51)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 52){SetLevel(DANA2,52)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 53){SetLevel(DANA2,53)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 54){SetLevel(DANA2,54)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 55){SetLevel(DANA2,55)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 56){SetLevel(DANA2,56)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 57){SetLevel(DANA2,57)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 58){SetLevel(DANA2,58)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 59){SetLevel(DANA2,59)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 60){SetLevel(DANA2,60)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 61){SetLevel(DANA2,61)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 62){SetLevel(DANA2,62)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 63){SetLevel(DANA2,63)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 64){SetLevel(DANA2,64)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 65){SetLevel(DANA2,65)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 66){SetLevel(DANA2,66)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 67){SetLevel(DANA2,67)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 68){SetLevel(DANA2,68)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 69){SetLevel(DANA2,69)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 70){SetLevel(DANA2,70)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 71){SetLevel(DANA2,71)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 72){SetLevel(DANA2,72)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 73){SetLevel(DANA2,73)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 74){SetLevel(DANA2,74)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 75){SetLevel(DANA2,75)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 76){SetLevel(DANA2,76)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 77){SetLevel(DANA2,77)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 78){SetLevel(DANA2,78)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 79){SetLevel(DANA2,79)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 80){SetLevel(DANA2,80)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 81){SetLevel(DANA2,81)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 82){SetLevel(DANA2,82)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 83){SetLevel(DANA2,83)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 84){SetLevel(DANA2,84)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 85){SetLevel(DANA2,85)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 86){SetLevel(DANA2,86)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 87){SetLevel(DANA2,87)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 88){SetLevel(DANA2,88)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 89){SetLevel(DANA2,89)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 90){SetLevel(DANA2,90)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 91){SetLevel(DANA2,91)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 92){SetLevel(DANA2,92)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 93){SetLevel(DANA2,93)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 94){SetLevel(DANA2,94)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 95){SetLevel(DANA2,95)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 96){SetLevel(DANA2,96)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 97){SetLevel(DANA2,97)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 98){SetLevel(DANA2,98)} 
		else{SetLevel(DANA2,99)}
	}
	if(DANA3.CHRWORK[CWK_LV] == 0)
	{
		if(FLAG[GF_TBOX_DUMMY121] == 1){SetLevel(DANA3,1)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 2){SetLevel(DANA3,2)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 3){SetLevel(DANA3,3)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 4){SetLevel(DANA3,4)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 5){SetLevel(DANA3,5)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 6){SetLevel(DANA3,6)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 7){SetLevel(DANA3,7)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 8){SetLevel(DANA3,8)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 9){SetLevel(DANA3,9)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 10){SetLevel(DANA3,10)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 11){SetLevel(DANA3,11)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 12){SetLevel(DANA3,12)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 13){SetLevel(DANA3,13)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 14){SetLevel(DANA3,14)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 15){SetLevel(DANA3,15)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 16){SetLevel(DANA3,16)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 17){SetLevel(DANA3,17)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 18){SetLevel(DANA3,18)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 19){SetLevel(DANA3,19)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 20){SetLevel(DANA3,20)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 21){SetLevel(DANA3,21)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 22){SetLevel(DANA3,22)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 23){SetLevel(DANA3,23)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 24){SetLevel(DANA3,24)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 25){SetLevel(DANA3,25)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 26){SetLevel(DANA3,26)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 27){SetLevel(DANA3,27)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 28){SetLevel(DANA3,28)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 29){SetLevel(DANA3,29)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 30){SetLevel(DANA3,30)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 31){SetLevel(DANA3,31)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 32){SetLevel(DANA3,32)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 33){SetLevel(DANA3,33)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 34){SetLevel(DANA3,34)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 35){SetLevel(DANA3,35)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 36){SetLevel(DANA3,36)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 37){SetLevel(DANA3,37)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 38){SetLevel(DANA3,38)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 39){SetLevel(DANA3,39)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 40){SetLevel(DANA3,40)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 41){SetLevel(DANA3,41)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 42){SetLevel(DANA3,42)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 43){SetLevel(DANA3,43)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 44){SetLevel(DANA3,44)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 45){SetLevel(DANA3,45)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 46){SetLevel(DANA3,46)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 47){SetLevel(DANA3,47)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 48){SetLevel(DANA3,48)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 49){SetLevel(DANA3,49)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 50){SetLevel(DANA3,50)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 51){SetLevel(DANA3,51)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 52){SetLevel(DANA3,52)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 53){SetLevel(DANA3,53)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 54){SetLevel(DANA3,54)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 55){SetLevel(DANA3,55)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 56){SetLevel(DANA3,56)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 57){SetLevel(DANA3,57)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 58){SetLevel(DANA3,58)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 59){SetLevel(DANA3,59)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 60){SetLevel(DANA3,60)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 61){SetLevel(DANA3,61)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 62){SetLevel(DANA3,62)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 63){SetLevel(DANA3,63)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 64){SetLevel(DANA3,64)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 65){SetLevel(DANA3,65)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 66){SetLevel(DANA3,66)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 67){SetLevel(DANA3,67)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 68){SetLevel(DANA3,68)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 69){SetLevel(DANA3,69)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 70){SetLevel(DANA3,70)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 71){SetLevel(DANA3,71)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 72){SetLevel(DANA3,72)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 73){SetLevel(DANA3,73)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 74){SetLevel(DANA3,74)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 75){SetLevel(DANA3,75)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 76){SetLevel(DANA3,76)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 77){SetLevel(DANA3,77)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 78){SetLevel(DANA3,78)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 79){SetLevel(DANA3,79)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 80){SetLevel(DANA3,80)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 81){SetLevel(DANA3,81)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 82){SetLevel(DANA3,82)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 83){SetLevel(DANA3,83)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 84){SetLevel(DANA3,84)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 85){SetLevel(DANA3,85)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 86){SetLevel(DANA3,86)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 87){SetLevel(DANA3,87)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 88){SetLevel(DANA3,88)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 89){SetLevel(DANA3,89)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 90){SetLevel(DANA3,90)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 91){SetLevel(DANA3,91)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 92){SetLevel(DANA3,92)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 93){SetLevel(DANA3,93)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 94){SetLevel(DANA3,94)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 95){SetLevel(DANA3,95)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 96){SetLevel(DANA3,96)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 97){SetLevel(DANA3,97)} 
		else if(FLAG[GF_TBOX_DUMMY121] == 98){SetLevel(DANA3,98)} 
		else{SetLevel(DANA3,99)}
	}
}

"""