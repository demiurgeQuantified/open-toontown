from direct.directnotify import DirectNotifyGlobal

from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI

class DistributedPhoneAI(DistributedFurnitureItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPhoneAI')
