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
            elif name in self.userNameToAvId: # we have an estate, but it was already created by another toon
                avId = self.userNameToAvId[name]
                self.sendEstateZoneToAvId(senderId, avId)
            else:
                self.notify.warning('%d trying to enter non-existent estate belonging to %d' % (senderId, avId))
                return
        else:
            zoneId = self.ownerToZone[avId]
            self.sendEstateZoneToAvId(senderId, zoneId)
        
    def sendEstateZoneToAvId(self, avId, zoneId):
        self.air.doId2do[avId].startToonUp(30)
        # TODO: this will not find estates belonging to another account which were created on a different toon to the one being visited
        self.sendUpdateToAvatarId(avId, 'setEstateZone', [avId, zoneId])

    def createEstateZone(self, avId, name):
        callback = PythonUtil.Functor(self.returnEstate, avId, name)
        self.air.getEstate(self.air.doId2do[avId].getDISLid(), callback)

    def returnEstate(self, avId, name, estateId, houseToonIds):
        if estateId == 0: # the owner doesn't have an estate, so we need to create one
            self.createHouseInDatabase(avId, name, houseToonIds)
            return
        
        self.generateEstate(avId, name, houseToonIds, estateId)

    def generateEstate(self, avId, name, houseToonIds, estateId):
        zoneId = self.air.allocateZone()
        self.ownerToZone[avId] = zoneId
        self.userNameToAvId[name] = avId
        self.estateIdToAvId[estateId] = avId

        self.air.sendActivate(estateId, self.air.districtId, zoneId)
        estateGenerated = PythonUtil.Functor(self.gotEstate, houseToonIds)
        self.acceptOnce('generate-%d' % estateId, estateGenerated)

    def gotEstate(self, houseToonIds, estate):
        estate.avId = self.estateIdToAvId[estate.doId]
        estate.zoneId = self.ownerToZone[estate.avId]
        estate.createObjects(houseToonIds)
        self.sendEstateZoneToAvId(estate.avId, estate.zoneId)

    def createHouseInDatabase(self, avId, name, houseToonIds):
        newEstateCallback = PythonUtil.Functor(self.gotNewEstate, avId, name, houseToonIds)
        self.air.dbInterface.createObject(self.air.dbId,
                                          self.air.dclassesByName['DistributedEstateAI'],
                                          callback=newEstateCallback)

    def gotNewEstate(self, avId, name, houseToonIds, estate):
        self.air.dbInterface.updateObject(self.air.dbId,
                                          self.air.doId2do[avId].getDISLid(),
                                          self.air.dclassesByName['AstronAccountAI'],
                                          {'ESTATE_ID': estate})
        self.generateEstate(avId, name, houseToonIds, estate)

    def removeFriend(self, ownerId, avId):
        pass

    def exitEstate(self):
        pass

    def startAprilFools(self):
        self.sendUpdate("startAprilFools",[])

    def stopAprilFools(self):
        self.sendUpdate("stopAprilFools",[])