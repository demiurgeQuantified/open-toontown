from direct.directnotify import DirectNotifyGlobal
from toontown.building import DistributedDoorAI

class DistributedHouseDoorAI(DistributedDoorAI.DistributedDoorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHouseDoorAI')

    def __init__(self, air, blockNumber, doorType):
        self.air = air
        self.blockNumber = blockNumber
        self.doorType = doorType
        DistributedDoorAI.DistributedDoorAI.__init__(self, self.air, self.blockNumber, self.doorType)