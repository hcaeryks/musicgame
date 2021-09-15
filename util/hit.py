from PPlay.sprite import Sprite

class Hit(Sprite):
    def __init__(self, time, tier, vpos):
        self.time = time
        self.tier = tier
        self.vpos = vpos

        if tier == 0:
            Sprite.__init__(self, "assets/hitM.png")
        elif tier == 1:
            Sprite.__init__(self, "assets/hitT.png")
        elif tier == 2:
            Sprite.__init__(self, "assets/hitA.png")
        elif tier == 3:
            Sprite.__init__(self, "assets/hitP.png")