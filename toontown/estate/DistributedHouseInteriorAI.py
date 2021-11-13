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
        self.windows = self.house.interiorWindows
        self.wallpaper = self.house.interiorWallpaper

        DistributedObjectAI.__init__(self, self.air)

    def generate(self):
        DistributedObjectAI.generate(self)

    def setHouseId(self, houseId):
        self.houseId = houseId

    def getHouseId(self):
        return self.houseId

    def setHouseIndex(self, index):
        self.houseIndex = index

    def getHouseIndex(self):
        return self.houseIndex

    def b_setWallpaper(self, wallpaper):
        self.setWallpaper(wallpaper)
        self.d_setWallpaper(wallpaper)

    def d_setWallpaper(self, wallpaper):
        self.sendUpdate("setWallpaper", [wallpaper])

    def setWallpaper(self, wallpaper):
        self.wallpaper = wallpaper

    def getWallpaper(self):
        return self.wallpaper

    def b_setWindows(self, windows):
        self.setWindows(windows)
        self.d_setWindows(windows)

    def d_setWindows(self, windows):
        self.sendUpdate("setWindows", [windows])

    def setWindows(self, windows):
        self.windows = windows

    def getWindows(self):
        return self.windows