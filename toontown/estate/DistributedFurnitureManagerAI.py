from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.showbase import PythonUtil

from toontown.catalog import CatalogItem, CatalogItemList
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
        return self.house.getDeletedItems()

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
        self.dfitems.append(furnitureItem)
        furnitureItem.d_setPosHpr(*item.posHpr)
        return furnitureItem

    def saveFurniturePos(self, furnitureItem):
        furnitureItem in self.dfitems
        furnitureItem.item.posHpr = furnitureItem.posHpr
        self.house.interiorItems.markDirty() # we modified a property directly, so the CatalogItemList hasn't actually updated itself
        self.house.d_setInteriorItems(self.house.interiorItems)

    # client messages

    def moveItemToAtticMessage(self, item, context):
        senderId = self.air.getAvatarIdFromSender()
        item = self.air.doId2do[item]
        self.moveItemToAttic(item)
        self.sendUpdateToAvatarId(senderId, 'moveItemToAtticResponse', [1, context])

    def moveItemToAttic(self, furnitureItem):
        item = furnitureItem.item

        self.house.atticItems.append(item)
        self.house.d_setAtticItems(self.house.atticItems)
        self.d_setAtticItems(self.house.atticItems)

        for i in range(len(self.house.interiorItems)):
            if self.house.interiorItems[i] is item:
                del self.house.interiorItems[i]
                break
        self.house.d_setInteriorItems(self.house.interiorItems)

        self.dfitems.remove(furnitureItem)
        furnitureItem.requestDelete()

    def moveItemFromAtticMessage(self, index, x, y, z, h, p, r, context):
        senderId = self.air.getAvatarIdFromSender()
        objectId = self.moveItemFromAttic(index, (x, y, z, h, p, r), context)
        self.sendUpdateToAvatarId(senderId, 'moveItemFromAtticResponse', [1, objectId, context]) # this is causing crashes because the client looks up the id before it receives the object
        # if the client doesn't get the id, the furniture menu freezes until it is closed and opened again

    def moveItemFromAttic(self, index, posHpr, context):
        item = self.house.atticItems[index]
        del self.house.atticItems[index]

        item.posHpr = posHpr
        self.house.interiorItems.append(item)
        self.house.d_setInteriorItems(self.house.interiorItems)
        self.house.d_setAtticItems(self.house.atticItems)
        self.d_setAtticItems(self.house.atticItems)

        furnitureItem = self.createFurnitureItem(item)
        return furnitureItem.doId