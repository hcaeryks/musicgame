from PPlay.keyboard import Keyboard
from PPlay.sprite import Sprite
from pygame.mixer import music
import pygame

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

class Game():
    def __init__(self, screen):
        self.screen = screen
        self.keyboard = Keyboard()

        self.key1 = Sprite("assets/keylarge.png")
        self.key2 = Sprite("assets/keysmall.png")
        self.key3 = Sprite("assets/keysmall.png")
        self.key4 = Sprite("assets/keylarge.png")
        self.key1l = Sprite("assets/keypresswhite.png")
        self.key2l = Sprite("assets/keypressblue.png")
        self.key3l = Sprite("assets/keypressblue.png")
        self.key4l = Sprite("assets/keypresswhite.png")
        self.lane1l = Sprite("assets/lanelightwhite.png")
        self.lane2l = Sprite("assets/lanelightblue.png")
        self.lane3l = Sprite("assets/lanelightblue.png")
        self.lane4l = Sprite("assets/lanelightwhite.png")
        self.judgeline = Sprite("assets/judgeline.png")
        self.keys = [self.key1, self.key2, self.key3, self.key4]
        self.keysl = [self.key1l, self.key2l, self.key3l, self.key4l]
        self.lanel = [self.lane1l, self.lane2l, self.lane3l, self.lane4l]
        self.keypresses = ["D", "F", "J", "K"]
        self.keypressesCurr = [False, False, False, False]

        self.text2 = "NADA"
        self.key1.set_position(1920/6+100*0-10, 1080-125-130)
        self.key2.set_position(1920/6+100*1-10, 1080-125-130)
        self.key3.set_position(1920/6+100*2-10, 1080-125-130)
        self.key4.set_position(1920/6+100*3-10, 1080-125-130)
        self.key1l.set_position(1920/6+100*0-10, 1080-125-130)
        self.key2l.set_position(1920/6+100*1-10, 1080-125-130)
        self.key3l.set_position(1920/6+100*2-10, 1080-125-130)
        self.key4l.set_position(1920/6+100*3-10, 1080-125-130)
        self.lane1l.set_position(1920/6+100*0, 1080-125-130-10-5-331)
        self.lane2l.set_position(1920/6+100*1, 1080-125-130-10-5-331)
        self.lane3l.set_position(1920/6+100*2, 1080-125-130-10-5-331)
        self.lane4l.set_position(1920/6+100*3, 1080-125-130-10-5-331)
        self.judgeline.set_position(1920/6+100*0, 1080-125-130-30)

        self.oldpos = 0
        self.deltamus = 0
        self.notes = self.loadNotes()
        self.music = music
        self.music.load("songs/0/audio.ogg")
        self.music.play()
        pass

    def draw(self):
        self.deltamus = (self.music.get_pos() - self.oldpos) / 1000
        self.oldpos = self.music.get_pos()

        self.key1.draw()
        self.key2.draw()
        self.key3.draw()
        self.key4.draw()

        self.text2 = str(self.music.get_pos())
        

        for x in range(len(self.notes)):
            n = 0
            for i in range(len(self.notes[x])):
                self.notes[x][i-n].y += 1800 * self.deltamus
                if self.notes[x][i-n].y + self.notes[x][i-n].height >= 0 and self.notes[x][i-n].y < 1080-150-125:
                    self.notes[x][i-n].draw()
                elif self.notes[x][i-n].y >= 1080-150-130:
                    self.notes[x].pop(i-n)
                    n += 1
        
        self.judgeline.draw()
        for x in range(len(self.keys)):
            if self.keyboard.key_pressed(self.keypresses[x]):
                self.lanel[x].draw()
                self.keysl[x].draw()
                if self.keypressesCurr[x] == False and self.notes[x] != []:
                    self.keypressesCurr[x] = True
                    if self.notes[x][0].y > 1080-150-130-70-75:
                        self.notes[x].pop(0)
            elif self.keypressesCurr[x] == True:
                self.keypressesCurr[x] = False


        self.screen.draw_text(self.text2, 1000, 700, 50, (255,255,255))
        pass

    def play(self):
        pass

    def stop(self):
        pass

    def loadNotes(self, path="songs/0/nm.sc"):
        notes = [[], [], [], []]
        i = False
        with open(path, 'r') as f:
            for line in f:
                if i and line.startswith("#"):
                    data = line[1:]
                    data = data.split(":")
                    note = None
                    if data[1] == "0":
                        note = Sprite("assets/notegreen.png")
                    elif data[1] == "1":
                        note = Sprite("assets/noteblue.png")
                    elif data[1] == "2":
                        note = Sprite("assets/noteblue.png")
                    elif data[1] == "3":
                        note = Sprite("assets/notegreen.png")
                    note.set_position(1920/6+100*int(data[1]), 815-(int(data[0]) * 1.8))
                    notes[int(data[1])].append(note)
                if "#SONGDATA#" in line:
                    i = True
        return notes