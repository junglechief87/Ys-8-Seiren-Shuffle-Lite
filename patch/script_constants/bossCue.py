BOSS_CUE = {
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
            'characterID': 'B161',
            'pastMode': True
        },
        "Nebritia Psyches": {
            'mapLoad': 'LoadArg("map/mp6529m/mp6529m.arg")',
            'eventCue': 'EventCue("mp6529m:EV_RetryBoss")',
            'mapID': 'MN_D_MP6529M',
            'characterID': 'B162',
            'pastMode': True
        },
        "Argura Psyches": {
            'mapLoad': 'LoadArg("map/mp6539m/mp6539m.arg")',
            'eventCue': 'EventCue("mp6539m:EV_RetryBoss")',
            'mapID': 'MN_D_MP6539M',
            'characterID': 'B163',
            'pastMode': True
        },
        "Crusos Psyches": {
            'mapLoad': 'LoadArg("map/mp6549m/mp6549m.arg")',
            'eventCue': 'EventCue("mp6549m:EV_RetryBoss")',
            'mapID': 'MN_D_MP6549M',
            'characterID': 'B011',
            'pastMode': True
        },
        "Blasphima Psyches": {
            'mapLoad': 'LoadArg("map/mp6559m/mp6559m.arg")',
            'eventCue': 'EventCue("mp6559m:EV_RetryBoss")',
            'mapID': 'MN_D_MP6559M',
            'characterID': 'B164',
            'pastMode': True
        },
        "Le-Kyanos Psyches": {
            'mapLoad': 'LoadArg("map/mp6204m/mp6204m.arg")',
            'eventCue': 'EventCue("mp6204m:EV_Boss_Jump")',
            'mapID': 'MN_F_MP6204M',
            'characterID': 'B165',
            'pastMode': True
        },
        "Melaiduma Psyches": {
            'mapLoad': 'LoadArg("map/mp6569/mp6569.arg")',
            'eventCue': 'EventCue("mp6569:EV_RetryBoss")',
            'mapID': 'MN_D_MP6569',
            'characterID': 'B170',
        },
        "Theos":
        {
            'mapLoad': 'LoadArg("map/mp6310b/mp6310b.arg")',
            'eventCue': 'EventCue("mp6310b:EV_M06S240")',
            'mapID': 'MN_D_MP6310',
            'characterID': 'B020',
            'pastMode': False
        },
        "Origin":
        {
            'mapLoad': 'LoadArg("map/mp8323/mp8323.arg")',
            'eventCue': 'EventCue("mp8323:init")',
            'mapID': 'MN_D_MP8323',
            'characterID': 'B020',
            'pastMode': False
        },
        "Io":
        {
            'mapLoad': 'LoadArg("map/mp6569m/mp6569m.arg")',
            'eventCue': 'EventCue("mp6569m:EV_RetryBoss")',
            'mapID': 'MN_D_MP6569M',
            'characterID': 'B020',
            'pastMode': True
        },
    }

def pastModeToggle(boss):
        if BOSS_CUE[boss].get('pastMode', False):
            return 'SetFlag(SF_PAST_MODE, 1)', 'SetFlag(SF_PAST_MODE, 0)'
        else:
            return '', ''
        
def getBossCue(boss):    
     return f"{BOSS_CUE[boss]['mapLoad']}",  f"{BOSS_CUE[boss]['eventCue']}"