from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.showbase import PythonUtil
from toontown.estate import DistributedHouseAI
from toontown.ai import DatabaseObject
from toontown.toon import DistributedToonAI

from toontown.safezone import ETreasurePlannerAI

class DistributedEstateAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedEstateAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.zoneId = 0
        self.avId = 0

        self.estateType = 0 # i don't think this did anything
        self.dawnTime = 0 # beta time cycle stuff, not a focus
        self.lastEpochTimeStamp = 0
        self.rentalTimeStamp = 0
        self.rentalType = 0
        self.treasurePlanner = None

        self.houses = {}
        self.ownerList = []

    def delete(self):
        self.ignoreAll()
        self.treasurePlanner.stop()
        self.treasurePlanner.deleteAllTreasuresNow()
        self.treasurePlanner = None
        for houseList in self.houses.values():
            for house in houseList:
                house.delete()
        DistributedObjectAI.delete(self)

    def createObjects(self, houseToonIds): # houseToonIds is a list of toonIds on the account, ordered by house position
        simbase.estate = self
        self.ownerList = houseToonIds

        self.treasurePlanner = ETreasurePlannerAI.ETreasurePlannerAI(self.zoneId)
        self.treasurePlanner.start()

        for houseIndex in range(0, 6):
            houseId = 0
            toonId = self.ownerList[houseIndex]
            if not toonId == 0: # the house slot holds a toon
                if toonId == self.avId: # must be our online toon
                    toon = self.air.doId2do[toonId]
                    houseId = toon.getHouseId()
                    if houseId != 0: # they already have a house
                        self.createHouse(houseId, houseIndex)
                    else: # they don't have a house yet
                        self.createHouseInDatabase(houseIndex, toon.getName(), toonId)
                else: # toon is offline, we have to go through the database
                    readToonCallback = PythonUtil.Functor(self.returnToonHouse, houseIndex, toonId)
                    self.air.getToonHouse(toonId, readToonCallback)
            else: # this house doesn't belong to anyone, create a generic one
                house = DistributedHouseAI.DistributedHouseAI(self.air)
                house.housePosInd = houseIndex
                house.colorIndex = houseIndex
                house.generateWithRequired(self.zoneId)
                house.generateObjects()
                self.houses[houseIndex] = house

    def createHouseInDatabase(self, houseIndex, toonName, toonId):
        newHouseCallback = PythonUtil.Functor(self.returnNewHouseId, houseIndex, toonId)
        self.air.dbInterface.createObject(self.air.dbId,
                                          self.air.dclassesByName['DistributedHouseAI'],
                                          {'setAvatarId':[toonId],
                                          'setColor':[houseIndex],
                                          'setName':[toonName]},
                                          newHouseCallback)

    def returnNewHouseId(self, houseIndex, toonId, doId):
        self.createHouse(doId, houseIndex, toonId)

    def returnToonHouse(self, houseIndex, toonId, toonHouse, toonName):
        if toonHouse != 0: # they already have a house
            self.createHouse(toonHouse, houseIndex)
        else: # they don't have a house yet
            self.createHouseInDatabase(houseIndex, toonName, toonId)

    def createHouse(self, houseId, houseIndex, toonId=0):
        self.air.sendActivate(houseId, self.air.districtId, self.zoneId)
        self.acceptOnce('generate-%d' % houseId, PythonUtil.Functor(self.gotHouse, houseIndex, toonId))

    def gotHouse(self, houseIndex, toonId, house):
        self.houses[houseIndex] = house

        house.b_setHousePos(houseIndex)
        house.zoneId = self.zoneId
        house.generateObjects()
        
        if not toonId == 0: # this value is only set when the house is new, and must be saved
            if toonId == self.avId: #they must be our online toon
                house.b_setAvatarId(toonId)
            else: # we have to do weird stuff to modify offline toons
                toon = DistributedToonAI.DistributedToonAI(self.air)
                toon.doId = toonId
                db = DatabaseObject.DatabaseObject(self.air, toonId)
                toon.b_setHouseId(house.getDoId())
                db.storeObject(toon, ['setHouseId'])
                toon.deleteDummy()
            house.setupDefaults()

    def requestServerTime(self):
        self.sendUpdate('setServerTime', [0])

    def getEstateType(self):
        return self.estateType

    def setEstateType(self, estateType):
        self.estateType = estateType

    def getDawnTime(self):
        return self.dawnTime

    def setDawnTime(self, dawnTime):
        self.dawnTime = dawnTime

    def getDecorData(self):
        if hasattr(self, 'decorData'):
            return self.decorData
        else:
            return []

    def setDecorData(self, decorData):
        self.decorData = decorData

    def getLastEpochTimeStamp(self):
        return self.lastEpochTimeStamp

    def setLastEpochTimeStamp(self, timeStamp):
        self.lastEpochTimeStamp = timeStamp

    def getRentalTimeStamp(self):
        return self.rentalTimeStamp

    def setRentalTimeStamp(self, timeStamp):
        self.rentalTimeStamp = timeStamp
    
    def getRentalType(self):
        return self.rentalType

    def setRentalType(self, rentalType):
        self.rentalType = rentalType

    def setClouds(self, clouds):
        self.clouds = clouds

    def getClouds(self):
        if hasattr(self, 'clouds'):
            return self.clouds
        else:
            return 0

# gross
    
    def getToonId(self, slot):
        if slot == 0:
            return self.getSlot0ToonId()
        elif slot == 1:
            return self.getSlot1ToonId()
        elif slot == 2:
            return self.getSlot2ToonId()
        elif slot == 3:
            return self.getSlot3ToonId()
        elif slot == 4:
            return self.getSlot4ToonId()
        elif slot == 5:
            return self.getSlot5ToonId()

    def getItems(self, slot):
        if slot == 0:
            return self.getSlot0Items()
        elif slot == 1:
            return self.getSlot1Items()
        elif slot == 2:
            return self.getSlot2Items()
        elif slot == 3:
            return self.getSlot3Items()
        elif slot == 4:
            return self.getSlot4Items()
        elif slot == 5:
            return self.getSlot5Items()

    def getSlot0ToonId(self):
        if hasattr(self, "slot0ToonId"):
            return self.slot0ToonId
        else:
            return 0

    def getSlot1ToonId(self):
        if hasattr(self, "slot1ToonId"):
            return self.slot1ToonId
        else:
            return 0

    def getSlot2ToonId(self):
        if hasattr(self, "slot2ToonId"):
            return self.slot2ToonId
        else:
            return 0

    def getSlot3ToonId(self):
        if hasattr(self, "slot3ToonId"):
            return self.slot3ToonId
        else:
            return 0

    def getSlot4ToonId(self):
        if hasattr(self, "slot4ToonId"):
            return self.slot4ToonId
        else:
            return 0

    def getSlot5ToonId(self):
        if hasattr(self, "slot5ToonId"):
            return self.slot5ToonId
        else:
            return 0

    def getSlot0Items(self):
        if hasattr(self, "slot0Items"):
            return self.slot0Items
        else:
            return []

    def getSlot1Items(self):
        if hasattr(self, "slot1Items"):
            return self.slot1Items
        else:
            return []

    def getSlot2Items(self):
        if hasattr(self, "slot2Items"):
            return self.slot2Items
        else:
            return []

    def getSlot3Items(self):
        if hasattr(self, "slot3Items"):
            return self.slot3Items
        else:
            return []

    def getSlot4Items(self):
        if hasattr(self, "slot4Items"):
            return self.slot4Items
        else:
            return []

    def getSlot5Items(self):
        if hasattr(self, "slot5Items"):
            return self.slot5Items
        else:
            return []

    def setSlot0ToonId(self, avId):
        self.slot0ToonId = avId

    def setSlot0Items(self, items):
        self.slot0Items = items

    def setSlot1ToonId(self, avId):
        self.slot1ToonId = avId

    def setSlot1Items(self, items):
        self.slot1Items = items

    def setSlot2ToonId(self, avId):
        self.slot2ToonId = avId

    def setSlot2Items(self, items):
        self.slot2Items = items

    def setSlot3ToonId(self, avId):
        self.slot3ToonId = avId

    def setSlot3Items(self, items):
        self.slot3Items = items

    def setSlot4ToonId(self, avId):
        self.slot4ToonId = avId

    def setSlot4Items(self, items):
        self.slot4Items = items

    def setSlot5ToonId(self, avId):
        self.slot5ToonId = avId

    def setSlot5Items(self, items):
        self.slot5Items = items

    def completeFlowerSale(self, sell):
        pass