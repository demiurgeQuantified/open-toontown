from toontown.toonbase.ToontownGlobals import *
from . import RegenTreasurePlannerAI, DistributedETreasureAI

class ETreasurePlannerAI(RegenTreasurePlannerAI.RegenTreasurePlannerAI):

    def __init__(self, zoneId):
        self.healAmount = 2
        RegenTreasurePlannerAI.RegenTreasurePlannerAI.__init__(self, zoneId, DistributedETreasureAI.DistributedETreasureAI, 'ETreasurePlanner', 20, 1) # maxTreasures should be 5 but this will crash with the test value

    def initSpawnPoints(self):
        self.spawnPoints = [(-17.416, -19.757, 7.025),] # TODO: find correct values
        return self.spawnPoints