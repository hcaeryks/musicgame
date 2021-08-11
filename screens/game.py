from PPlay.gameimage import GameImage
from PPlay import window
from PPlay.animation import Animation
from PPlay.keyboard import Keyboard
from PPlay.sprite import Sprite
from pygame.mixer import music
from pygame.mixer import Sound
import pygame

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

class Game():
    def __init__(self, screen):
        self.velocity = 1.5
        self.screen = screen
        self.diff = "HARD"
        self.keyboard = Keyboard()

        if self.diff == "HARD": self.dcolor = (214, 50, 39)
        if self.diff == "NORMAL": self.dcolor = (39, 162, 214)
        if self.diff == "EASY": self.dcolor = (39, 214, 65)
        

        self.gameplay = Sprite("assets/gameplay.png")
        self.lifetxt = Sprite("assets/life.png")
        self.infomenu = Sprite("assets/infomenu.png")
        self.judgeline = Animation("assets/judgeline.png", 9, True)
        self.error = Sprite("assets/error.png")
        self.hpbar = Animation("assets/hpbar.png", 100, True)
        self.boostbar = Animation("assets/boostbar.png", 100, True)
        self.boosteffect = Animation("assets/boosteffect.png", 35, False)
        self.lanelights = [Animation("assets/lanelighta.png", 20, False) for x in range(6)]
        self.keylights = [Sprite("assets/keypress.png") for x in range(6)]
        self.explosions = [Animation("assets/explosion9.png", 9, False) for x in range(6)]
        self.keypresses = ["S", "D", "F", "J", "K", "L"]
        self.keypressesCurr = [False, False, False, False, False, False]

        self.oldpos = 0
        self.deltamus = 0
        self.notes = self.loadNotes()

        self.lifetxt.set_position(21, 5)
        self.infomenu.set_position(620, self.screen.height/2)
        self.error.set_position(877-850, 142)
        self.boostbar.set_position(643, 395)
        self.boostbar.set_total_duration(200)
        self.boostbar.stop()
        self.hpbar.set_position(21, 0)
        self.hpbar.set_total_duration(200)
        self.hpbar.stop()
        self.boosteffect.set_position(134, 1080-304-600)
        self.boosteffect.set_total_duration(350)
        self.boosteffect.stop()
        self.judgeline.set_position(20, 1080-303-40)
        self.judgeline.set_total_duration(self.bpm*2)
        self.judgeline.stop()
        self.judgeline.play()
        [e.stop() for e in self.explosions]
        [e.set_total_duration(200) for e in self.explosions]
        [self.explosions[e].set_position(134+40-150+80*e, 1080-304+20-150) for e in range(len(self.explosions))]
        [e.stop() for e in self.lanelights]
        [e.set_total_duration(25) for e in self.lanelights]
        [self.lanelights[e].set_position(135+78*e+2*e, 1080-304-self.lanelights[e].height) for e in range(len(self.lanelights))]
        [self.keylights[e].set_position(134+80*e, 1080-304+20) for e in range(len(self.keylights))]

        self.combo = 0
        self.hp = 100
        self.hpdiff = 0
        self.errortime = 200
        self.boost = 0
        self.boostdiff = 0

        self.hitsound = Sound("assets/hitsound.wav")
        self.hitsound.set_volume(0.3)
        self.music = music
        self.music.load("songs/2/audio.mp3")
        self.music.set_volume(0.8)
        self.music.play()
        pass

    def draw(self):
        self.deltamus = (self.music.get_pos() - self.oldpos) / 1000
        self.oldpos = self.music.get_pos()

        self.bg.draw()
        if self.errortime < 1 and self.errortime > 0:
            self.errortime -= self.screen.delta_time()
            self.error.draw()
        elif self.errortime <= 0:
            self.errortime = 1
        self.boostbar.set_curr_frame(self.boost-1)
        self.boostbar.draw()
        self.gameplay.draw()
        self.hpbar.set_curr_frame(self.hp-1)
        self.hpbar.draw()
        self.lifetxt.draw()
        #self.infomenu.draw()

        for x in range(len(self.notes)):
            n = 0
            for i in range(len(self.notes[x])):
                self.notes[x][i-n].y += (self.velocity * 1000) * self.deltamus
                if self.notes[x][i-n].y + self.notes[x][i-n].height >= 0 and self.notes[x][i-n].y < 1080-304-20:
                    self.notes[x][i-n].draw()
                elif self.notes[x][i-n].y >= 1080-304-20+200:
                    if x < 6:
                        self.errortime = 1 -self.screen.delta_time()
                        self.hpdiff -= 15
                        self.combo = 0
                    self.notes[x].pop(i-n)
                    n += 1
        

        for x in range(6):
            if self.keyboard.key_pressed(self.keypresses[x]):
                self.lanelights[x].stop()
                self.lanelights[x].play()
                self.keylights[x].draw()
                if self.keypressesCurr[x] == False and self.notes[x] != []:
                    self.keypressesCurr[x] = True
                    if self.notes[x][0].y > 1080-304-20-400:
                        self.hitsound.stop()
                        self.hitsound.play()
                        self.explosions[x].stop()
                        self.explosions[x].play()
                        self.notes[x].pop(0)
                        self.hpdiff += 5
                        if self.boostdiff < 100: self.boostdiff += 1
                        self.combo += 1
                    else:
                        self.errortime = 1 -self.screen.delta_time()
                        self.combo = 0
                        self.hpdiff -= 15
            elif self.keypressesCurr[x] == True:
                self.keypressesCurr[x] = False

        if self.keyboard.key_pressed("SPACE") and self.boost == 100:
            self.boostdiff = -300
            self.boosteffect.play()

        if self.boosteffect.is_playing():
            self.boosteffect.update()
            self.boosteffect.draw()

        if self.judgeline.is_playing():
            self.judgeline.draw()
            self.judgeline.update()

        [e.draw() for e in self.lanelights]
        [e.update() for e in self.lanelights]

        self.boostdiff, self.boost = self.diffCalc(self.boostdiff, self.boost)
        self.hpdiff, self.hp = self.diffCalc(self.hpdiff, self.hp)
        [e.update() for e in self.explosions]
        [e.draw() for e in self.explosions]

        self.screen.draw_text(self.diff, 862+828/2-((len(self.diff)*45)/2), self.screen.height - 70 - 30, 70, self.dcolor, "Arial")
        self.screen.draw_text(self.title, 862+828/2-((len(self.title)*40)/2), 20, 70, (200, 200, 200), "Arial")
        self.screen.draw_text(self.artist, 862+828/2-((len(self.artist)*18)/2), 20+70, 30, (200, 200, 200), "Arial")
        self.screen.draw_text(str(self.combo), 374-(len(str(self.combo))*50+(len(str(self.combo))-1)*3)//2, 200, 100, (200,200,200), "Impact")
        pass

    def play(self):
        pass

    def stop(self):
        pass

    def diffCalc(self, diff, real):
        if diff != 0:
            if real > 1 or real < 100: real += diff * self.screen.delta_time()
            diff -= diff * self.screen.delta_time() * 2
        if real < 0: real = 0
        elif real > 100: real = 100

        return diff, real

    def loadNotes(self, path="songs/2/hd.sc"):
        notes = [[], [], [], [], [], [], []]
        i = False
        self.bg = GameImage("songs/2/bg.png")
        self.bg.set_position(877, 142)
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
                        note = Sprite("assets/notegreen.png")
                    elif data[1] == "3":
                        note = Sprite("assets/notegreen.png")
                    elif data[1] == "4":
                        note = Sprite("assets/noteblue.png")
                    elif data[1] == "5":
                        note = Sprite("assets/notegreen.png")
                    note.set_position(134+80*int(data[1]), 1080-304-20-(int(data[0]) * self.velocity))
                    notes[int(data[1])].append(note)
                if "#SONGDATA#" in line:
                    i = True
                if "#BPM" in line:
                    self.bpm = int(line[5:])
                if "#LENGTH" in line:
                    self.length = int(line[7:])
                if "#TITLE" in line:
                    self.title = line[7:]
                    self.title = self.title.replace("_", " ")[:-1]
                if "#ARTIST" in line:
                    self.artist = line[8:]
                    self.artist = self.artist.replace("_", " ")[:-1]
        measures = int((self.bpm/4) * (self.length/60))
        timebmeas = int(self.length/measures)
        for i in range(measures):
            note = Sprite("assets/bar.png")
            note.set_position(134, 1080-304-((timebmeas * 1000) * i) * self.velocity - 2)
            notes[6].append(note)

        return notes