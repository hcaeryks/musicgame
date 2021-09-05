from PPlay.sprite import Sprite
import pygame.font

class Song(Sprite):
    def __init__(self, title, artist, genre, duration, bpm, difficulty, image, idd, wall):
        Sprite.__init__(self, "assets/songselectionitem.png")
        self.title = title.replace('_', ' ')
        self.artist = artist
        self.genre = genre
        self.duration = duration
        self.bpm = bpm
        self.difficulty = difficulty
        self.image_jacket = image
        self.id = idd
        self.wallpaper = wall
        self.sfont = pygame.font.Font("assets/secrcode.ttf", 30)
        self.sfont_surface = self.sfont.render(self.title, True, (255,255,255))
        self.txtw = self.sfont_surface.get_size()[1]

    def draw_text(self, screen):
        screen.blit(self.sfont_surface, [self.x+40, self.y+self.height/2-self.txtw/2])