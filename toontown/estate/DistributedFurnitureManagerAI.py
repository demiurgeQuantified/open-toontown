from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.catalog import CatalogItem
from toontown.estate import DistributedFurnitureItemAI

class DistributedFurnitureManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFurnitureManagerAI')

    def __init__(self, air, house):
        self.house = house
        self.director = 0
        self.dfitems = []
        DistributedObjectAI.__init__(self, air)

    def getOwnerId(self):
        return self.house.ownerId

    def getOwnerName(self):
        return self.house.name

    def getInteriorId(self):
        return self.house.interior.doId

    def d_setAtticItems(self, items): # we don't need to store these as the DistributedHouseAI already has them
        self.sendUpdate("setAtticItems", [items.getBlob(CatalogItem.Customization)])

    def getAtticItems(self):
        return self.house.getAtticItems()

    def d_setAtticWallpaper(self, items):
        self.sendUpdate("setAtticWallpaper", [items.getBlob(CatalogItem.Customization)])

    def getAtticWallpaper(self):
        return self.house.getAtticWallpaper()

    def d_setAtticWindows(self, items):
        self.sendUpdate("setAtticWindows", [items.getBlob(CatalogItem.Customization)])

    def getAtticWindows(self):
        return self.house.getAtticWindows()

    def d_setDeletedItems(self, items):
        self.sendUpdate("setDeletedItems", [items.getBlob(CatalogItem.Customization)])

    def getDeletedItems(self):
        return self.house.deletedItems#.getBlob(CatalogItem.Customization)

    def suggestDirector(self, avId):
        senderId = self.air.getAvatarIdFromSender()
        if senderId == self.house.ownerId:
            self.b_setDirector(avId)

    def b_setDirector(self, avId):
        self.setDirector(avId)
        self.d_setDirector(avId)

    def d_setDirector(self, avId):
        self.sendUpdate('setDirector', [avId])

    def setDirector(self, avId):
        self.director = avId

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        self.air.doId2do.get(avId).b_setGhostMode(1) 

    def avatarExit(self):
        avId = self.air.getAvatarIdFromSender()
        self.air.doId2do.get(avId).b_setGhostMode(0)

    def createFurnitureItem(self, item):
        furnitureItem = DistributedFurnitureItemAI.DistributedFurnitureItemAI(self.air, self, item)
        furnitureItem.generateWithRequired(self.house.intZoneId)
        item.furnitureItem = furnitureItem
        self.dfitems.append(furnitureItem)
        furnitureItem.d_setPosHpr(*item.posHpr)

    def saveFurniturePos(self, furnitureItem):
        furnitureItem in self.dfitems
        furnitureItem.item.posHpr = furnitureItem.posHpr
        self.house.interiorItems.markDirty() # we modified a property directly, so the CatalogItemList hasn't actually updated itself
        self.house.d_setInteriorItems(self.house.interiorItems)