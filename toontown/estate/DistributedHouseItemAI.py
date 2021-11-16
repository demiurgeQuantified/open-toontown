from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObjectAI

class DistributedHouseItemAI(DistributedObjectAI.DistributedObjectAI):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedHouseItemAI")

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
