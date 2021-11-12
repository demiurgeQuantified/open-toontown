from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedHouseInteriorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHouseInteriorAI')

    def __init__(self, air, zoneId, house):
        self.air = air
        self.zoneId = zoneId
        self.house = house
        self.houseId = self.house.ownerId
        self.houseIndex = self.house.housePosInd
        self.wallpaper = self.house.interiorWallpaper
        self.windows = self.house.interiorWindows
        DistributedObjectAI.__init__(self, self.air)

    def setHouseId(self, houseId):
        self.houseId = houseId

    def getHouseId(self):
        return self.houseId

    def setHouseIndex(self, index):
        self.houseIndex = index

    def getHouseIndex(self):
        return self.houseIndex

    def setWallpaper(self, wallpaper):
        self.wallpaper = wallpaper

    def getWallpaper(self):
        return self.wallpaper

    def setWindows(self, windows):
        self.windows = windows

    def getWindows(self):
        return self.windows