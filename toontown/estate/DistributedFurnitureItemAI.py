from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI
from toontown.catalog import CatalogItem
from . import HouseGlobals, DistributedHouseItemAI

class DistributedFurnitureItemAI(DistributedSmoothNodeAI, DistributedHouseItemAI.DistributedHouseItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFurnitureItemAI')

    def __init__(self, air, furnitureMgr, item):
        DistributedHouseItemAI.DistributedHouseItemAI.__init__(self, air)
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
        senderId = self.air.getAvatarIdFromSender()
        if senderId != self.avId:
            self.b_setMode(HouseGlobals.FURNITURE_MODE_START, senderId) # tells the client to start smoothing movement
        self.posHpr = (x,y,z,h,p,r)
        self.sendUpdate('setSmPosHpr', [x,y,z,h,p,r,t])
        if final:
            self.savePosition()
            self.b_setMode(HouseGlobals.FURNITURE_MODE_STOP, senderId) 
            self.b_setMode(HouseGlobals.FURNITURE_MODE_OFF, 0) # does this do anything?

    def savePosition(self):
        self.furnitureMgr.saveFurniturePos(self)