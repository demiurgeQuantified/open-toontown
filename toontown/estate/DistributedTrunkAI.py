from direct.directnotify import DirectNotifyGlobal

from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI

class DistributedTrunkAI(DistributedFurnitureItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTrunkAI')
