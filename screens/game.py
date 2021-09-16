from util.hit import Hit
from PPlay.gameimage import GameImage
from PPlay import window
from PPlay.animation import Animation
from PPlay.keyboard import Keyboard
from PPlay.sprite import Sprite
from pygame.mixer import music
from pygame.mixer import Sound
from math import log10
import globalVar as g, pygame, util.settingsreader as settingsreader

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

class Game():
    def __init__(self, screen):
        self.screen = screen
        self.keyboard = Keyboard()

        settingsreader.read_settings()
        
        self.gameplay = Sprite("assets/gameplay.png")
        self.lifetxt = Sprite("assets/life.png")
        self.infomenu = Sprite("assets/infomenu.png")
        self.judgeline = Animation("assets/judgeline.png", 9, True)
        self.error = Sprite("assets/error.png")
        self.hpbar = Animation("assets/hpbar.png", 100, True)
        self.boostbar = Animation("assets/boostbar.png", 100, True)
        self.boosteffect = Animation("assets/boosteffect.png", 35, False)
        self.grading = Animation("assets/grades.png", 3, False)
        self.lanelights = [Animation("assets/lanelighta.png", 20, False) for x in range(6)]
        self.keylights = [Sprite("assets/keypress.png") for x in range(6)]
        self.explosions = [Animation("assets/explosion9.png", 9, False) for x in range(6)]
        self.keypresses = [g.NOTES[x] for x in range(6)]
        self.keypressesCurr = [False, False, False, False, False, False]

        self.oldpos = 0
        self.deltamus = 0
        self.velocity = g.NOTE_SPEED
        self.notes = self.loadNotes()
        self.allhits = []
        
        if self.diff == "shd": 
            self.dcolor = (151, 44, 222)
            self.diff = "SUPER HARD"
        if self.diff == "hd": 
            self.dcolor = (214, 50, 39)
            self.diff = "HARD"
        if self.diff == "nm": 
            self.dcolor = (39, 162, 214)
            self.diff = "NORMAL"
        if self.diff == "ez": 
            self.dcolor = (39, 214, 65)
            self.diff = "EASY"
        

        self.grading.set_position(373-self.grading.width/2, 1080/2)
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

        self.points = 0
        self.maxcombo = 0
        self.combo = 0
        self.hp = 100
        self.hpdiff = 0
        self.errortime = 200
        self.boost = 0
        self.boostdiff = 0
        self.boosttime = 0
        self.time_end = 0.1
        self.grade_disappear = 0
        self.continue_game = True

        self.hitP = 0
        self.hitA = 0
        self.hitT = 0
        self.hitM = 0

        self.sbig = pygame.font.Font("assets/chopsic.otf", 50)
        self.ssmall = pygame.font.Font("assets/chopsic.otf", 40)
        self.stitle = self.sbig.render(self.title, True, (255, 255, 255))
        self.sartist = self.ssmall.render(self.artist, True, (255, 255, 255))
        self.sdiff = self.sbig.render(self.diff, True, self.dcolor)

        self.hitsound = Sound("assets/hitsound.wav")
        self.hitsound.set_volume(0.3)
        self.music = music
        self.music.load("songs/"+str(g.CURR_SONG)+"/audio.mp3")
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
                elif self.notes[x][i-n].y >= 777+300:
                    if x < 6:
                        self.errortime = 1 - self.screen.delta_time()
                        self.hpdiff -= 15
                        self.combo = 0
                        self.hitM += 1
                        self.allhits.append(Hit(self.music.get_pos(), 0, -300))
                    self.notes[x].pop(i-n)
                    n += 1
        

        for x in range(6):
            if self.keyboard.key_pressed(self.keypresses[x]):
                self.lanelights[x].stop()
                self.lanelights[x].play()
                self.keylights[x].draw()
                if self.keypressesCurr[x] == False and self.notes[x] != []:
                    self.keypressesCurr[x] = True
                    if self.notes[x][0].y > 777-300:
                        self.hitsound.stop()
                        self.hitsound.play()
                        self.explosions[x].stop()
                        self.explosions[x].play()
                        self.hpdiff += 5
                        if self.boostdiff < 100: self.boostdiff += 1
                        self.combo += 1
                        self.grade_disappear = 0.5 
                        distance = self.notes[x][0].y - 777
                        tier, mult = 0, 1
                        if distance <= 40 and distance >= -40:
                            self.grading.set_curr_frame(0)
                            self.hitP += 1
                            tier = 3
                        elif distance <= 100 and distance >= -100:
                            self.grading.set_curr_frame(1)
                            self.hitA += 1
                            tier = 2
                        else:
                            self.grading.set_curr_frame(2)
                            self.hitT += 1
                            tier = 1
                        if self.boosttime > 0: mult = 5
                        self.points += tier * mult * log10(self.combo)
                        self.allhits.append(Hit(self.music.get_pos(), tier, 0-distance))
                        self.notes[x].pop(0)
                    else:
                        self.errortime = 1 -self.screen.delta_time()
                        self.combo = 0
                        self.hpdiff -= 15
                        self.allhits.append(Hit(self.music.get_pos(), 0, 300))
            elif self.keypressesCurr[x] == True:
                self.keypressesCurr[x] = False

        if self.keyboard.key_pressed("SPACE") and self.boost == 100:
            self.boostdiff = -300
            self.boosttime = 5
            self.boosteffect.play()

        if self.keyboard.key_pressed("ESC"):
            self.music.stop()
            g.GAME_STATE = 2

        if self.boosteffect.is_playing():
            self.boosteffect.update()
            self.boosteffect.draw()

        if self.judgeline.is_playing():
            self.judgeline.draw()
            self.judgeline.update()

        empty = 0
        if self.continue_game:
            for x in range(len(self.notes)-1):
                if len(self.notes[x]) == 0:
                    empty += 1

        if empty == 6:
            self.continue_game = False
            self.time_end = 2

        if not self.continue_game:
            self.time_end -= self.screen.delta_time()

        if self.boosttime > 0:
            self.boosttime -= self.screen.delta_time()

        if self.time_end <= 0 or self.hp <= 0:
            self.music.stop()
            total = self.hitP + self.hitA + self.hitT + self.hitM
            percentage = (self.hitP*10+self.hitA*7+self.hitT*3)/total
            g.SCORE_INFO[0] = self.allhits
            g.SCORE_INFO[2] = round(percentage*10, 2)
            g.SCORE_INFO[3] = self.maxcombo
            g.SCORE_INFO[4] = [self.hitP, self.hitA, self.hitT, self.hitM]
            g.SCORE_INFO[5] = round(self.points, 2)
            g.SCORE_INFO[6] = self.title
            g.GAME_STATE = 4

        [e.draw() for e in self.lanelights]
        [e.update() for e in self.lanelights]

        self.boostdiff, self.boost = self.diffCalc(self.boostdiff, self.boost)
        self.hpdiff, self.hp = self.diffCalc(self.hpdiff, self.hp)
        [e.update() for e in self.explosions]
        [e.draw() for e in self.explosions]

        if self.grade_disappear > 0:
            self.grade_disappear -= self.screen.delta_time()
            self.grading.draw()

        if self.combo > self.maxcombo:
            self.maxcombo = self.combo

        self.screen.screen.blit(self.stitle, [633+(1920-633)/2-self.stitle.get_width()/2,30])
        self.screen.screen.blit(self.sartist, [633+(1920-633)/2-self.sartist.get_width()/2,30+self.stitle.get_height()])
        self.screen.screen.blit(self.sdiff, [633+(1920-633)/2-self.sdiff.get_width()/2,1080-30-self.sdiff.get_height()])
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

    def loadNotes(self):
        notes = [[], [], [], [], [], [], []]
        i = False
        self.diff = ""
        if g.CURR_DIFF == 0: self.diff = "ez"
        if g.CURR_DIFF == 1: self.diff = "nm"
        if g.CURR_DIFF == 2: self.diff = "hd"
        if g.CURR_DIFF == 3: self.diff = "shd"
        self.bg = GameImage("songs/"+str(g.CURR_SONG)+"/bg.png")
        path = "songs/"+str(g.CURR_SONG)+"/"+self.diff+".sc"
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
        g.SCORE_INFO[1] = self.length * 1000
        for i in range(measures):
            note = Sprite("assets/bar.png")
            note.set_position(134, 1080-374-((timebmeas * 1000) * i) * self.velocity - 2)
            notes[6].append(note)

        return notes