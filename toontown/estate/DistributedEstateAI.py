from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.showbase.PythonUtil import Functor

from toontown.safezone import ETreasurePlannerAI
from . import DistributedHouseAI

class DistributedEstateAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedEstateAI')

    def __init__(self, air, zoneId, avId):
        DistributedObjectAI.__init__(self, air)
        self.zoneId = zoneId
        self.avId = avId

        self.estateType = 0 # what is this supposed to represent?
        self.dawnTime = 0
        self.lastEpochTimeStamp = 0
        self.rentalTimeStamp = 0
        self.rentalType = 0

        self.houses = {}
        self.ownerToHouse = {None:0, None:1, None:2, None:3, None:4, None:5}

    def delete(self):
        self.ignoreAll()
        self.treasurePlanner.stop()
        self.treasurePlanner.deleteAllTreasuresNow()
        self.treasurePlanner = None
        for houseList in self.houses.values():
            for house in houseList:
                house.delete()
        DistributedObjectAI.delete(self)

    def createObjects(self):
        simbase.estate = self
        self.treasurePlanner = ETreasurePlannerAI.ETreasurePlannerAI(self.zoneId)
        self.treasurePlanner.start()

        self.air.getEstate(self.avId, Functor(self.handleGetEstate, self.avId))
        for houseIndex in range(0, 6):
            house = DistributedHouseAI.DistributedHouseAI(self.air, self.zoneId, houseIndex)
            house.generateWithRequired(self.zoneId)
            self.houses[houseIndex] = house
            house.generateObjects()

    def handleGetEstate(self, avId):
        pass

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