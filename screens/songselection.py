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
        self.diffchooser = Animation("assets/diffchoose.png", 4, False)
        self.diffchooser.set_position(1079/2-self.diffchooser.width/2, 600)
        self.charterror = Animation("assets/charterror.png", 2, False)
        self.charterror.set_position(1079/2-self.charterror.width/2, 600-self.charterror.height-10)
        self.selectedsongtexture = Animation("assets/songselectionselected-a.png", 10, True)
        self.selectedsongtexture.set_position(1920-1000, 1080/2-self.selectedsongtexture.height/2)
        self.selectedsongtexture.set_total_duration(500)
        self.jacketdarken = Sprite("assets/ss.png")

        self.lpress = False
        self.rpress = False

        self.charterrortime = 0
        self.currdiff = 0
        self.holdtime = 0
        self.moving = True
        self.sssoffset = 0
        self.totalmoved = 0
        self.loadSongData()
        self.loadSongsOnScreen()
        self.generateText()
        self.ssoundscape = pygame.font.Font("assets/chopsic.otf", 20)
        self.ssoundscape_surface = self.ssoundscape.render("Soundscape", True, (255,255,255))

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
            self.infinitysonglist[i].set_position(1080, i*54-27-54*4)

    def generateText(self):
        song = self.infinitysonglist[int(len(self.infinitysonglist)/2)]

        self.songart = Sprite(song.wallpaper)
        self.stitle = pygame.font.Font("assets/chopsic.otf", 70)
        self.stitle_surface = self.stitle.render(song.title, True, (255,255,255))
        self.sartist = pygame.font.Font("assets/chopsic.otf", 50)
        self.sartist_surface = self.sartist.render(song.artist, True, (255,255,255))
        self.sbpm = pygame.font.Font("assets/secrcode.ttf", 30)
        self.sbpm_surface = self.sbpm.render("BPM: "+str(song.bpm), True, (255,255,255))
        self.sduration = pygame.font.Font("assets/secrcode.ttf", 30)
        self.sduration_surface = self.sduration.render("LENGTH: "+str(song.duration//60)+"m:"+str(song.duration%60)+"s", True, (255,255,255))
        self.sgenre = pygame.font.Font("assets/secrcode.ttf", 30)
        self.sgenre_surface = self.sgenre.render("GENRE: "+song.genre, True, (255,255,255))

    def draw(self):
        self.songart.draw()
        self.jacketdarken.draw()
        self.bottombar.draw()
        self.charterror.draw()
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
                diff = ""
                if g.CURR_DIFF == 0: diff = "ez"
                if g.CURR_DIFF == 1: diff = "nm"
                if g.CURR_DIFF == 2: diff = "hd"
                if g.CURR_DIFF == 3: diff = "shd"
                g.CURR_SONG = self.infinitysonglist[int(len(self.infinitysonglist)/2)].id
                g.CURR_DIFF = self.currdiff
                if os.path.isfile("songs/"+str(g.CURR_SONG)+"/"+diff+".sc"):
                    g.GAME_STATE = 3
                else:
                    self.charterror.set_curr_frame(1)
                    self.charterrortime = 2

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

        if self.charterrortime > 0:
            self.charterrortime -= self.screen.delta_time()
            if self.charterrortime <= 0: self.charterror.set_curr_frame(0)

        if self.keyboard.key_pressed("ESC"):
            g.GAME_STATE = 0

        if self.keyboard.key_pressed("left") and not self.lpress:
            self.lpress = True
            self.currdiff -= 1
            if self.currdiff < 0: self.currdiff = 3
            self.diffchooser.set_curr_frame(self.currdiff)
        elif not self.keyboard.key_pressed("left") and self.lpress: self.lpress = False

        if self.keyboard.key_pressed("right") and not self.rpress:
            self.rpress = True
            self.currdiff += 1
            if self.currdiff > 3: self.currdiff = 0
            self.diffchooser.set_curr_frame(self.currdiff)
        elif not self.keyboard.key_pressed("right") and self.rpress: self.rpress = False
        
        self.diffchooser.draw()
        self.selectedsongtexture.draw()
        self.selectedsongtexture.update()
        self.screen.screen.blit(self.ssoundscape_surface, [10, 10])
        self.screen.screen.blit(self.stitle_surface, [1079/2-self.stitle_surface.get_size()[0]/2, 100])
        self.screen.screen.blit(self.sartist_surface, [1079/2-self.sartist_surface.get_size()[0]/2, 160])
        self.screen.screen.blit(self.sbpm_surface, [150, 1010])
        self.screen.screen.blit(self.sduration_surface, [150+50+self.sbpm_surface.get_width(), 1010])
        self.screen.screen.blit(self.sgenre_surface, [150+100+self.sbpm_surface.get_width()+self.sduration_surface.get_width(), 1010])
    
    def list_range(self, offset, length, l):
        start = offset % len(l)
        end = (start + length) % len(l)
        if end > start:
            return l[start:end]
        return l[start:] + l[:end]