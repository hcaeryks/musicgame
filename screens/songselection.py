from PPlay.keyboard import *
from PPlay.sprite import *
from PPlay.animation import *
from util.song import *
import globalVar as g
import os, json

class SongSelection():
    def __init__(self, screen):
        self.screen = screen
        self.keyboard = Keyboard()
        
        self.bottombar = Sprite("assets/ssbottom.png")
        self.bottombar.set_position(0, 1080-self.bottombar.height)
        self.selectedsongtexture = Animation("assets/songselectionselected-a.png", 10, True)
        self.selectedsongtexture.set_position(1920-1000, 1080/2-self.selectedsongtexture.height/2)
        self.selectedsongtexture.set_total_duration(1000)
        self.jacketdarken = Sprite("assets/ss.png")

        self.holdtime = 0
        self.moving = True
        self.sssoffset = 0
        self.totalmoved = 0
        self.loadSongData()
        self.loadSongsOnScreen()
        self.generateText()

    def loadSongData(self):
        self.songcount = 0
        self.songs = []
        self.infinitysonglist = []
        while len(self.songs) < 29:
            for dirs in os.walk("./songs/"):
                if os.path.isfile(dirs[0]+"/info.json"):
                    with open(dirs[0]+"/info.json") as s:
                        data = json.load(s)
                        self.songs.append(Song(data["name"], data["artist"], data["genre"], data["duration"], data["BPM"], data["difficulty"], data["image"], data["id"], data["wallpaper"]))

    def loadSongsOnScreen(self):
        self.infinitysonglist = self.list_range(self.sssoffset, 29, self.songs)
        for i in range(29):
            self.infinitysonglist[i].set_position(1080, i*54-27-54*5)

    def generateText(self):
        song = self.infinitysonglist[int(len(self.infinitysonglist)/2)+1]

        self.songart = Sprite(song.wallpaper)
        self.stitle = pygame.font.Font("assets/chopsic.otf", 70)
        self.stitle_surface = self.stitle.render(song.title, True, (255,255,255))
        self.sartist = pygame.font.Font("assets/chopsic.otf", 50)
        self.sartist_surface = self.sartist.render(song.artist, True, (255,255,255))

    def run(self):
        self.songart.draw()
        self.jacketdarken.draw()
        self.bottombar.draw()
        pUp = self.keyboard.key_pressed("up")
        pDw = self.keyboard.key_pressed("down")
        self.speed = 0
        if self.holdtime > 1:
            if pUp: self.speed = 900
            elif pDw: self.speed = -900
        elif self.holdtime > 0.5:
            if pUp: self.speed = 300
            elif pDw: self.speed = -300
        self.diff = self.screen.delta_time() * self.speed
        self.totalmoved += -self.diff
        for i in range(29):
            self.infinitysonglist[i].draw()
            self.infinitysonglist[i].draw_text(self.screen.screen)
            if self.keyboard.key_pressed("enter"):
                g.CURR_SONG = self.infinitysonglist[int(len(self.infinitysonglist)/2)+1].id
                g.GAME_STATE = 3

            self.infinitysonglist[i].y += self.diff
        if pUp and not self.moving:
            self.moving = True
            self.sssoffset -= 1
            self.loadSongsOnScreen()
            self.generateText()
        elif pDw and not self.moving:
            self.moving = True
            self.sssoffset += 1
            self.loadSongsOnScreen()
            self.generateText()
        elif self.moving and pUp or pDw:
            self.holdtime += self.screen.delta_time()
        elif self.moving and not pUp and not pDw:
            self.sssoffset += int(self.totalmoved/54)
            self.totalmoved = 0
            self.holdtime = 0
            self.moving = False
            self.loadSongsOnScreen()

        if self.totalmoved >= 54*4 or self.totalmoved <= -54*4:
            self.sssoffset += int(self.totalmoved/54)
            self.totalmoved = 0
            self.loadSongsOnScreen()
            self.generateText()
            

        self.selectedsongtexture.draw()
        self.selectedsongtexture.update()
        self.screen.screen.blit(self.stitle_surface, [1079/2-self.stitle_surface.get_size()[0]/2, 100])
        self.screen.screen.blit(self.sartist_surface, [1079/2-self.sartist_surface.get_size()[0]/2, 160])
    
    def list_range(self, offset, length, l):
        start = offset % len(l)
        end = (start + length) % len(l)
        if end > start:
            return l[start:end]
        return l[start:] + l[:end]