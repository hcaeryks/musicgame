from PPlay.keyboard import Keyboard
from PPlay.sprite import Sprite
from random import randint

class Game():
    def __init__(self, screen):
        self.screen = screen
        self.keyboard = Keyboard()

        self.key1 = Sprite("assets/key.png")
        self.key2 = Sprite("assets/key.png")
        self.key3 = Sprite("assets/key.png")
        self.key4 = Sprite("assets/key.png")
        self.key1l = Sprite("assets/keypresswhite.png")
        self.key2l = Sprite("assets/keypressblue.png")
        self.key3l = Sprite("assets/keypressblue.png")
        self.key4l = Sprite("assets/keypresswhite.png")
        self.lane1l = Sprite("assets/lanelight.png")
        self.lane2l = Sprite("assets/lanelight.png")
        self.lane3l = Sprite("assets/lanelight.png")
        self.lane4l = Sprite("assets/lanelight.png")
        self.expl1 = Sprite("assets/explosion.png")
        self.expl2 = Sprite("assets/explosion.png")
        self.expl3 = Sprite("assets/explosion.png")
        self.expl4 = Sprite("assets/explosion.png")
        self.judgeline = Sprite("assets/judgeline.png")
        self.keys = [self.key1, self.key2, self.key3, self.key4]
        self.keysl = [self.key1l, self.key2l, self.key3l, self.key4l]
        self.lanel = [self.lane1l, self.lane2l, self.lane3l, self.lane4l]
        self.expls = [self.expl1, self.expl2, self.expl3, self.expl4]
        self.keypresses = ["D", "F", "J", "K"]
        self.keypressesCurr = [False, False, False, False]
        self.notes = [[Sprite("assets/notepurple.png"), Sprite("assets/notepurple.png"), Sprite("assets/notepurple.png")],[Sprite("assets/notepurple.png"), Sprite("assets/notepurple.png"), Sprite("assets/notepurple.png")],[Sprite("assets/notepurple.png"), Sprite("assets/notepurple.png"), Sprite("assets/notepurple.png")],[Sprite("assets/notepurple.png"), Sprite("assets/notepurple.png"), Sprite("assets/notepurple.png")]]
        for x in self.notes: 
            for i in x: i.set_position(1920/6+130*randint(0,3),1080-150-130-150*randint(5,50))

        self.text = "NADA"
        self.key1.set_position(1920/6+130*0, 1080-150-130)
        self.key2.set_position(1920/6+130*1, 1080-150-130)
        self.key3.set_position(1920/6+130*2, 1080-150-130)
        self.key4.set_position(1920/6+130*3, 1080-150-130)
        self.key1l.set_position(1920/6+130*0, 1080-150-130)
        self.key2l.set_position(1920/6+130*1, 1080-150-130)
        self.key3l.set_position(1920/6+130*2, 1080-150-130)
        self.key4l.set_position(1920/6+130*3, 1080-150-130)
        self.lane1l.set_position(1920/6+130*0, 1080-150-130-471)
        self.lane2l.set_position(1920/6+130*1, 1080-150-130-471)
        self.lane3l.set_position(1920/6+130*2, 1080-150-130-471)
        self.lane4l.set_position(1920/6+130*3, 1080-150-130-471)
        self.judgeline.set_position(1920/6-1, 1080-150-130-70)
        pass

    def draw(self):
        self.key1.draw()
        self.key2.draw()
        self.key3.draw()
        self.key4.draw()
        
        for x in range(len(self.keys)):
            if self.keyboard.key_pressed(self.keypresses[x]):
                self.lanel[x].draw()
                self.keysl[x].draw()
                if self.keypressesCurr[x] == False and self.notes[x] != []:
                    self.keypressesCurr[x] = True
                    print(x)
                    if self.notes[x][0].y > 1080-150-130-70-300:
                        self.notes[x].pop(0)
                        self.text = "hit "+ self.keypresses[x]
            elif self.keypressesCurr[x] == True:
                self.keypressesCurr[x] = False

        for x in range(len(self.notes)):
            n = 0
            for i in range(len(self.notes[x])):
                self.notes[x][i-n].y += 200 * self.screen.delta_time()
                if self.notes[x][i-n].y >= 0 and self.notes[x][i-n].y < 1080-150-130-70-300:
                    self.notes[x][i-n].draw()
                elif self.notes[x][i-n].y >= 1080-150-130-30:
                    self.notes[x].pop(i-n)
                    n += 1

        self.judgeline.draw()
        self.screen.draw_text(self.text, 1000, 500, 50, (255,255,255))
        pass

    def play(self):
        pass

    def stop(self):
        pass