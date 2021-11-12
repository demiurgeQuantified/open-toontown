from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.building import DoorTypes
from toontown.catalog import CatalogItemList, CatalogItem
from . import HouseGlobals, DistributedHouseDoorAI, DistributedHouseInteriorAI

class DistributedHouseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHouseAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.zoneId = 0

        self.housePosInd = 0
        self.houseType = HouseGlobals.HOUSE_DEFAULT
        self.gardenPos = 0
        self.ownerId = 0
        self.name = ''
        self.colorIndex = 0
        self.atticItems = CatalogItemList.CatalogItemList()
        self.interiorItems = CatalogItemList.CatalogItemList()
        self.atticWallpaper = CatalogItemList.CatalogItemList()
        self.interiorWallpaper = CatalogItemList.CatalogItemList()
        self.atticWindows = CatalogItemList.CatalogItemList()
        self.interiorWindows = CatalogItemList.CatalogItemList()
        self.deletedItems = CatalogItemList.CatalogItemList()
        self.cannonEnabled = 0

    def delete(self):
        self.ignoreAll()
        DistributedObjectAI.delete(self)

    def generateObjects(self):
        self.intZoneId = self.air.allocateZone()

        self.interior = DistributedHouseInteriorAI.DistributedHouseInteriorAI(self.air, self.intZoneId, self)
        self.interior.generateWithRequired(self.intZoneId)

        self.extDoor = DistributedHouseDoorAI.DistributedHouseDoorAI(self.air, self.doId, DoorTypes.EXT_STANDARD) # there's a DoorType called house, but it doesn't work?
        self.extDoor.zoneId = self.zoneId

        self.intDoor = DistributedHouseDoorAI.DistributedHouseDoorAI(self.air, self.doId, DoorTypes.INT_STANDARD)
        self.intDoor.zoneId = self.intZoneId

        self.extDoor.setOtherDoor(self.intDoor)
        self.intDoor.setOtherDoor(self.extDoor)
        self.extDoor.generateWithRequired(self.zoneId)
        self.intDoor.generateWithRequired(self.intZoneId)

        self.sendUpdate("setHouseReady", [])

    def b_setHousePos(self, pos):
        self.setHousePos(pos)
        self.d_setHousePos(pos)

    def d_setHousePos(self, pos):
        self.sendUpdate("setHousePos", [pos])

    def setHousePos(self, pos):
        self.housePosInd = pos

    def getHousePos(self):
        return self.housePosInd

    def setHouseType(self, houseType):
        self.houseType = houseType

    def getHouseType(self):
        return self.houseType

    def setGardenPos(self, gardenPos):
        self.gardenPos = gardenPos

    def getGardenPos(self):
        return self.gardenPos

    def b_setAvatarId(self, avId):
        self.setAvatarId(avId)
        self.d_setAvatarId(avId)

    def d_setAvatarId(self, avId):
        self.sendUpdate("setAvatarId", [avId])

    def setAvatarId(self, avId):
        self.ownerId = avId
        if avId != 0:
            try: self.air.doId2do[avId].b_setHouseId(self.getDoId())
            except: self.notify.info('could not setHouseId of toon %d' % avId)
            # this is called even when the toon is not in the dictionary (offline)

    def getAvatarId(self):
        return self.ownerId

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def d_setName(self, name):
        self.sendUpdate("setName", [name])

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def b_setColor(self, colorInd):
        self.setColor(colorInd)
        self.d_setColor(colorInd)

    def d_setColor(self, colorInd):
        self.sendUpdate("setColor", [colorInd])

    def setColor(self, color):
        self.colorIndex = color

    def getColor(self):
        return self.colorIndex

    def setAtticItems(self, items):
        self.atticItems = CatalogItemList.CatalogItemList(items, CatalogItem.Customization)

    def getAtticItems(self):
        return self.atticItems

    def setInteriorItems(self, items):
        self.interiorItems = CatalogItemList.CatalogItemList(items, CatalogItem.Customization)

    def getInteriorItems(self):
        return self.interiorItems

    def setAtticWallpaper(self, wallpaper):
        self.atticWallpaper = CatalogItemList.CatalogItemList(wallpaper, CatalogItem.Customization)

    def getAtticWallpaper(self):
        return self.atticWallpaper

    def setInteriorWallpaper(self, wallpaper):
        self.interiorWallpaper = CatalogItemList.CatalogItemList(wallpaper, CatalogItem.Customization)

    def getInteriorWallpaper(self):
        return self.interiorWallpaper

    def setAtticWindows(self, windows):
        self.atticWindows = CatalogItemList.CatalogItemList(windows, CatalogItem.Customization)

    def getAtticWindows(self):
        return self.atticWindows

    def setInteriorWindows(self, windows):
        self.interiorWindows = CatalogItemList.CatalogItemList(windows, CatalogItem.Customization)

    def getInteriorWindows(self):
        return self.interiorWindows

    def setDeletedItems(self, items):
        self.deletedItems = CatalogItemList.CatalogItemList(items, CatalogItem.Customization)

    def getDeletedItems(self):
        return self.deletedItems

    def setCannonEnabled(self, enabled):
        self.cannonEnabled = enabled

    def getCannonEnabled(self):
        return self.cannonEnabled
