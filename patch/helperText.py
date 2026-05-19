helpTextMessageDict = {
    139:    "Village shops and forge upgraded.",
    206:    "The stairs to the Crypt in the Stupa are lowered.",
    698:    "The way up the Mont Gendarme is open.",
    699:    "The Palace and Monastery are open.",
    700:    "Pangai Plains to Eternia is open and the waterway is repaired.",
    701:    "Eternia to the Palace is open and the secret room is unlocked.",
    702:    "Baja Tower can be reached. Breath Fountain is revealed.",
    727:    "The way to Eternal Hill is open.",
    739:    "Night exploration can now be undertaken.",
    764:    "Raid list updated.",
    770:    "The gangway to the Eleftheria is down.",
    779:    "The damaged boat on the Nameless Coast Shore has been repaired.",
    796:    "Lodinia Marsh is open and the chest in Eternia can be opened.",
    90600:  "The tailor is now open.",
    91100:  "Jewel trades can be made and insect repellent can be used.",
    91300:  "The map can be shown for rewards.",
    91400:  "Medicine can now be brewed.",
    91600:  "Master Kong can now be challenged.",
    92000:  "Silvia can now be fought in the village.",
    92100:  "Essence doors can be opened.",
}


def getHelperText(itemId):
    if itemId in helpTextMessageDict:
        return (
                f"\tMessage(\"{helpTextMessageDict[itemId]}\")\n"
                f"\tWaitPrompt()\n"
                f"\tWaitCloseWindow()\n"
                )
    else:
        return ""
