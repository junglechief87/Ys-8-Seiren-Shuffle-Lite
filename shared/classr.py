class location:
  def __init__(self,locID,mapID,mapCheckID,item):
    self.locID = locID
    self.mapID = mapID
    self.mapCheckID = mapCheckID
    self.item = item
  
class interceptReward:
  def __init__(self,stage,rewards):
    self.stage = stage
    self.rewards = rewards
