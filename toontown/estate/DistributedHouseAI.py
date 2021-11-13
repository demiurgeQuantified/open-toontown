from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
import random

from toontown.building import DoorTypes
from toontown.catalog import CatalogWallpaperItem, CatalogMouldingItem, CatalogFlooringItem, CatalogWainscotingItem
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
        self.atticItems = []
        self.interiorItems = []
        self.atticWallpaper = []
        self.interiorWallpaper = []
        self.atticWindows = []
        self.interiorWindows = []
        self.deletedItems = []
        self.cannonEnabled = 0
        self.interior = None

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

    def setupDefaults(self):
        self.interiorWindows = [[20, 2], [20, 4]]
        self.interior.b_setWindows(self.interiorWindows)
        self.b_setInteriorWindows(self.interiorWindows)

        wallpaper = random.choice(CatalogWallpaperItem.getWallpaperRange(1000, 1299))
        wallpaper = [wallpaper.patternIndex, wallpaper.colorIndex, wallpaper.borderIndex, wallpaper.borderColorIndex]

        moulding = random.choice(CatalogMouldingItem.getAllMouldings(1000, 1010))
        moulding = [moulding.patternIndex, moulding.colorIndex]

        flooring = random.choice(CatalogFlooringItem.getAllFloorings(1000, 1010))
        flooring = [flooring.patternIndex, flooring.colorIndex]

        wainscoting = random.choice(CatalogWainscotingItem.getAllWainscotings(1000, 1010))
        wainscoting = [wainscoting.patternIndex, wainscoting.colorIndex]

        self.interiorWallpaper = [[wallpaper,moulding,flooring,wainscoting],[wallpaper,moulding,flooring,wainscoting]]
        self.interior.b_setWallpaper(self.interiorWallpaper)
        self.b_setInteriorWallpaper(self.interiorWallpaper)

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
        self.atticItems = items

    def getAtticItems(self):
        return self.atticItems

    def setInteriorItems(self, items):
        self.interiorItems = items

    def getInteriorItems(self):
        return self.interiorItems

    def b_setInteriorWallpaper(self, wallpaper):
        self.setInteriorWallpaper(wallpaper)
        self.d_setInteriorWallpaper(wallpaper)

    def d_setInteriorWallpaper(self, wallpaper):
        self.sendUpdate("setInteriorWallpaper", [wallpaper])
        if self.interior:
            self.interior.b_setWallpaper(wallpaper)

    def setAtticWallpaper(self, wallpaper):
        self.atticWallpaper = wallpaper

    def getAtticWallpaper(self):
        return self.atticWallpaper

    def setInteriorWallpaper(self, wallpaper):
        self.interiorWallpaper = wallpaper

    def getInteriorWallpaper(self):
        return self.interiorWallpaper

    def setAtticWindows(self, windows):
        self.atticWindows = windows

    def getAtticWindows(self):
        return self.atticWindows

    def b_setInteriorWindows(self, windows):
        self.setInteriorWindows(windows)
        self.d_setInteriorWindows(windows)

    def d_setInteriorWindows(self, windows):
        self.sendUpdate("setInteriorWindows", [windows])
        if self.interior:
            self.interior.b_setWindows(windows)

    def setInteriorWindows(self, windows):
        self.interiorWindows = windows

    def getInteriorWindows(self):
        return self.interiorWindows

    def setDeletedItems(self, items):
        self.deletedItems = items

    def getDeletedItems(self):
        return self.deletedItems

    def setCannonEnabled(self, enabled):
        self.cannonEnabled = enabled

    def getCannonEnabled(self):
        return self.cannonEnabled
