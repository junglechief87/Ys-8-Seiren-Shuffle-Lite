helpTextMessageDict = {
    "Progressive Shop Rank":            "Village shops and forge upgraded.",
    "Jade Pendant":                     "The stairs to the Crypt in the Stupa are lowered.",
    "Maiden Journal":                   "The way up the Mont Gendarme is open.",
    "Frozen Flower":                    "The Palace and Monastery are open.",
    "Blue Seal of Whirling Water":      "Pangai Plains to Eternia is open and the waterway is repaired.",
    "Green Seal of Roaring Stone":      "Eternia to the Palace is open and the secret room is unlocked.",
    "Golden Seal of Piercing Light":    "Baja Tower can be reached. Breath Fountain is revealed.",
    "Shrine Maiden Amulet":             "The way to Eternal Hill is open.",
    "Glow Stone":                       "Night exploration can now be undertaken.",
    "Progressive Raid List":            "Raid list updated.",
    "Ship's Log 1":                     "The gangway to the Eleftheria is down.",
    "Ship Blueprints":                  "The damaged boat on the Nameless Coast Shore has been repaired.",
    "Treasure Chest Key":               "Lodinia Marsh is open and the chest in Eternia can be opened.",
    "Alison":                           "The tailor is now open.",
    "Dina":                             "Jewel trades can be made and insect repellent can be used.",
    "Euron":                            "The map can be shown for rewards.",
    "Licht":                            "Medicine can now be brewed.",
    "Ricotta":                          "Master Kong can now be challenged.",
    "Silvia":                           "Silvia can now be fought in the village.",
    "Dana":                             "Essence doors can be opened.",
    "Broken Glasses":                   "Turn this into Euron at max shop rank.",
    "Broken Necklace":                  "Turn this into Euron at max shop rank.",
    "Broken Lure":                      "Turn this into Euron at max shop rank.",
    "Odd Rock":                         "Turn this into Euron at max shop rank.",
    "Broken Mistilteinn":               "Turn this into Kathleen at max shop rank.",
    "Broken Spirit Ring":               "Turn this into Kathleen at max shop rank.",
}


def getHelperText(itemName):
    if itemName in helpTextMessageDict:
        return (
                f"\tMessage(\"{helpTextMessageDict[itemName]}\")\n"
                f"\tWaitPrompt()\n"
                f"\tWaitCloseWindow()\n"
                )
    else:
        return ""
