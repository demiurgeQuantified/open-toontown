from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.estate import DistributedEstateAI

class EstateManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('EstateManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.ownerToZone = {}
        self.userNameToAvId = {}

    def getEstateZone(self, avId, name):
        senderId = self.air.getAvatarIdFromSender()
        if avId not in self.ownerToZone:
            if avId == senderId:
                self.createEstateZone(avId, name)
            else:
                self.notify.warning('%d trying to enter non-existent estate belonging to %d', senderId, avId)
                return
        # there is no handling for visiting another toon's estate yet, or if the estate was created by another toon on the same account

        self.air.doId2do[avId].startToonUp(30)
        
        zoneId = self.ownerToZone[avId]
        self.sendUpdateToAvatarId(senderId, 'setEstateZone', [avId, zoneId])

    def createEstateZone(self, avId, name):
        zoneId = self.air.allocateZone()
        self.ownerToZone[avId] = zoneId
        self.userNameToAvId[name] = avId
        estateAI = DistributedEstateAI.DistributedEstateAI(self.air, zoneId, avId)
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