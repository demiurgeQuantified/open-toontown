from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.showbase import PythonUtil

class EstateManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('EstateManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.ownerToZone = {}
        self.userNameToAvId = {}
        self.estateIdToAvId = {}

    def getEstateZone(self, avId, name):
        senderId = self.air.getAvatarIdFromSender()
        if avId not in self.ownerToZone: # 
            if avId == senderId: # we are the owner of the estate, and it has not been created yet
                self.createEstateZone(avId, name)
            if name in self.userNameToAvId: # we have an estate, but it was already created by another toon
                avId = self.userNameToAvId[name]
            else:
                self.notify.warning('%d trying to enter non-existent estate belonging to %d', senderId, avId)
                return

        self.air.doId2do[avId].startToonUp(30)
        
        zoneId = self.ownerToZone[avId]
        # TODO: this will not find estates belonging to another account which were created on a different toon to the one being visited
        self.sendUpdateToAvatarId(senderId, 'setEstateZone', [avId, zoneId])

    def createEstateZone(self, avId, name):
        zoneId = self.air.allocateZone()
        self.ownerToZone[avId] = zoneId
        self.userNameToAvId[name] = avId

        callback = PythonUtil.Functor(self.returnEstate, zoneId, avId)
        self.air.getEstate(self.air.doId2do[avId].getDISLid(), callback)

    def returnEstate(self, zoneId, avId, estateId, houseToonIds):
        if not estateId:
            self.notify.warning('failed to find an estateId for %d' % avId)
            return
        
        self.estateIdToAvId[estateId] = avId

        self.air.sendActivate(estateId, self.air.districtId, zoneId)
        estateGenerated = PythonUtil.Functor(self.gotEstate, houseToonIds)
        self.acceptOnce('generate-%d' % estateId, estateGenerated)

    def gotEstate(self, houseToonIds, estate):
        estate.avId = self.estateIdToAvId[estate.doId]
        estate.zoneId = self.ownerToZone[estate.avId]
        estate.createObjects(houseToonIds)

    def removeFriend(self, ownerId, avId):
        pass

    def exitEstate(self):
        pass

    def startAprilFools(self):
        self.sendUpdate("startAprilFools",[])

    def stopAprilFools(self):
        self.sendUpdate("stopAprilFools",[])