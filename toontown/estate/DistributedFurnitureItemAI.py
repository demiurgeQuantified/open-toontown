from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI
from toontown.catalog import CatalogItem
from . import HouseGlobals

class DistributedFurnitureItemAI(DistributedSmoothNodeAI, DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFurnitureItemAI')

    def __init__(self, air, furnitureMgr, item):
        DistributedObjectAI.__init__(self, air)
        DistributedSmoothNodeAI.__init__(self, air)
        self.air = air
        self.furnitureMgr = furnitureMgr
        self.item = item
        self.posHpr = item.posHpr
        self.mode = HouseGlobals.FURNITURE_MODE_OFF
        self.avId = 0

    def getItem(self):
        return (self.furnitureMgr.doId, self.item.getBlob(CatalogItem.Customization))

    def b_setMode(self, mode, avId):
        self.setMode(mode, avId)
        self.d_setMode(mode, avId)

    def d_setMode(self, mode, avId):
        self.sendUpdate('setMode', [mode, avId])

    def setMode(self, mode, avId): # this is used to keep track of if the object is being moved, and who is moving it
        self.mode = mode
        self.avId = avId

    def getMode(self):
        return(self.mode, self.avId)

    def requestPosHpr(self, final, x, y, z, h, p, r, t):
        self.posHpr = (x,y,z,h,p,r)
        self.sendUpdate('setSmPosHpr', [x,y,z,h,p,r,t])