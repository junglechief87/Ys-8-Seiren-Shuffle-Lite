from shared.functions import * 

class playthrough:
  def __init__(self):
    self.locations = []
    self.locIDList = []
    self.regions = []
    self.bosses = []

  def build(self,location,sphere):
    location.sphere = sphere
    location.isHinted = False
    self.locations.append(location)
    self.locIDList.append(location.locID)

    if location.locRegion not in self.regions:
      self.regions.append(location.locRegion)

    if 'Defeated' in location.itemName:
      self.bosses.append(location)

class location:
  def __init__(self,locID,mapID,locRegion,locName,mapCheckID,event,itemID,itemName,quantity,progression,nice,party,crew,item,script,skill,landmark,entrance,exit):
    self.locID = locID
    self.mapID = mapID
    self.locRegion = locRegion
    self.locName = locName
    self.mapCheckID = mapCheckID
    self.event = event
    self.itemID = itemID
    self.itemName = itemName
    self.quantity = quantity
    self.progression = progression
    self.nice = nice
    self.party = party
    self.crew = crew
    self.item = item
    self.script = script
    self.skill = skill
    self.landmark = landmark
    self.entrance = entrance
    self.exit = exit

  def printSpoiler(self):
    print("\t" + self.locRegion + '-' + self.locName + '(' + self.mapCheckID + '): ' + self.itemName + '(' + str(self.itemID) + ')x' + str(self.quantity))

  def writeSpoiler(self,file):
    if self.skill:
      skillName = getSkillInfo(self.itemName)
      file.write("\t" + self.locRegion + '-' + self.locName + '(' + self.mapCheckID + '): ' + skillName[2] + ':' + skillName[1] + '\n')
    elif self.quantity == 1:
      file.write("\t" + self.locRegion + '-' + self.locName + '(' + self.mapCheckID + '): ' + self.itemName + '\n')
    else:
      file.write("\t" + self.locRegion + '-' + self.locName + '(' + self.mapCheckID + '): ' + self.itemName + ' x ' + str(self.quantity) + '\n')

class shuffledLocation(location):
  def __init__(self,location):
    self.locID = location.locID
    self.mapID = location.mapID
    self.locRegion = location.locRegion
    self.locName = location.locName
    self.mapCheckID = location.mapCheckID
    self.event = location.event
    self.script = location.script

class inventory(location):
  def __init__(self,location):
    self.itemID = location.itemID
    self.itemName = location.itemName
    self.quantity = location.quantity
    self.progression = location.progression
    self.nice = location.nice
    self.party = location.party
    self.crew = location.crew
    self.item = location.item
    self.skill = location.skill
    self.landmark = location.landmark
    self.entrance = location.entrance
    self.exit = location.exit
  
class interceptReward:
  def __init__(self,stage,rewards):
    self.stage = stage
    self.rewards = rewards
