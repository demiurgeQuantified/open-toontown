from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.estate import DistributedEstateAI

class EstateManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('EstateManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.estateIds = {}

    def getEstateZone(self, avId, name):
        senderId = self.air.getAvatarIdFromSender()
        if avId not in self.estateIds:
            if avId == senderId:
                self.createEstateZone(avId)
            else:
                self.notify.warning('%d trying to enter non-existent estate belonging to %d', senderId, avId)
                return

        zoneId = self.estateIds[avId]
        self.sendUpdateToAvatarId(senderId, 'setEstateZone', [avId, zoneId])

    def createEstateZone(self, avId):
        zoneId = self.air.allocateZone()
        self.estateIds[avId] = zoneId
        estateAI = DistributedEstateAI.DistributedEstateAI(self.air, zoneId)
        estateAI.generateWithRequired(zoneId)
        estateAI.createObjects()

    def removeFriend(self, ownerId, avId):
        pass

    def exitEstate(self):
        pass

    def startAprilFools(self):
        self.sendUpdate("startAprilFools",[])

    def stopAprilFools(self):
        self.sendUpdate("stopAprilFools",[])