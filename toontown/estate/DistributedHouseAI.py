from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.catalog import CatalogItemList, CatalogItem
from . import HouseGlobals

class DistributedHouseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHouseAI')

    def __init__(self, air, zoneId, posIndex):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.zoneId = zoneId

        self.housePosInd = posIndex
        self.houseType = HouseGlobals.HOUSE_DEFAULT
        self.gardenPos = 0
        self.ownerId = 0
        self.name = ''
        self.colorIndex = posIndex
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
        #not dealing with this yet
        self.sendUpdate("setHouseReady", [])

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
        self.air.doId2do[avId].b_setHouseId(self.doId)

    def getAvatarId(self):
        return self.ownerId

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

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
