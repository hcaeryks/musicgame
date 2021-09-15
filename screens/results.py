from pygame.display import Info
from PPlay.sprite import Sprite
from PPlay.keyboard import Keyboard
import globalVar as g
import pygame


class Results():
    def __init__(self, screen):
        self.screen = screen
        self.keyboard = Keyboard()

        title = g.SCORE_INFO[6]
        self.rank = g.SCORE_INFO[2]
        if self.rank > 95:
            self.rank = Sprite("assets/srank.png")
        elif self.rank > 85:
            self.rank = Sprite("assets/arank.png")
        elif self.rank > 75:
            self.rank = Sprite("assets/brank.png")
        elif self.rank > 65:
            self.rank = Sprite("assets/crank.png")
        elif self.rank > 50:
            self.rank = Sprite("assets/drank.png")
        else:
            self.rank = Sprite("assets/frank.png")

        self.graph = Sprite("assets/graph.png")
        self.results = Sprite("assets/results.png")
        self.bgresults = Sprite("assets/bgresults.png")
        self.graphtext = Sprite("assets/graphtext.png")
        self.infoboard = Sprite("assets/infoboard.png")
        self.esctoleave = Sprite("assets/esctoleave.png")

        self.graph.set_position(1920/2-self.graph.width/2, 1080*0.6)
        self.results.set_position(10, 30)
        self.rank.set_position(10, 20+self.results.height)
        self.graphtext.set_position(1920/2-self.graph.width/2, 1080*0.6-self.graphtext.height)
        self.infoboard.set_position(1920/2-self.infoboard.width/2, 200)
        self.esctoleave.set_position(30, 1080-30-self.esctoleave.height)

        self.hits_translated = g.SCORE_INFO[0]
        for i in range(len(self.hits_translated)):
            self.hits_translated[i].set_position(1920/2-self.graph.width/2+1+(self.hits_translated[i].time/g.SCORE_INFO[1])*950, 1080*0.6+151-self.hits_translated[i].vpos/2)

        self.title = pygame.font.Font("assets/chopsic.otf", 60)
        self.maxcombo = pygame.font.Font("assets/secrcode.ttf", 40)
        self.perfects = pygame.font.Font("assets/secrcode.ttf", 40)
        self.averages = pygame.font.Font("assets/secrcode.ttf", 40)
        self.terribles = pygame.font.Font("assets/secrcode.ttf", 40)
        self.misses = pygame.font.Font("assets/secrcode.ttf", 40)
        self.accuracy = pygame.font.Font("assets/secrcode.ttf", 40)
        self.points = pygame.font.Font("assets/secrcode.ttf", 60)

        self.title_surface = self.title.render(title, True, (255, 255, 255))
        self.maxcombo_surface = self.maxcombo.render(str(g.SCORE_INFO[3])+"x", True, (255, 255, 255))
        self.perfects_surface = self.perfects.render("PERFECTS: "+str(g.SCORE_INFO[4][0]), True, (255, 255, 255))
        self.averages_surface = self.averages.render("AVERAGES: "+str(g.SCORE_INFO[4][1]), True, (255, 255, 255))
        self.terribles_surface = self.terribles.render("TERRIBLES: "+str(g.SCORE_INFO[4][2]), True, (255, 255, 255))
        self.misses_surface = self.misses.render("MISSES: "+str(g.SCORE_INFO[4][3]), True, (255, 255, 255))
        self.accuracy_surface = self.accuracy.render(str(g.SCORE_INFO[2])+"%", True, (255, 255, 255))
        self.points_surface = self.points.render("SCORE: "+str(g.SCORE_INFO[5]), True, (255, 255, 255))


    def draw(self):
        self.bgresults.draw()
        self.graph.draw()
        self.graphtext.draw()
        self.results.draw()
        self.rank.draw()
        self.infoboard.draw()
        self.esctoleave.draw()
        
        for hit in self.hits_translated:
            hit.draw()

        if self.keyboard.key_pressed("ESC"):
            g.GAME_STATE = 2

        self.screen.screen.blit(self.title_surface, [1920/2-self.title_surface.get_width()/2, 30])
        self.screen.screen.blit(self.maxcombo_surface, [self.infoboard.x+20, self.infoboard.y+20])
        self.screen.screen.blit(self.perfects_surface, [self.infoboard.x+20,self.infoboard.y+self.infoboard.height/2-self.perfects_surface.get_height()])
        self.screen.screen.blit(self.averages_surface, [self.infoboard.x+20,self.infoboard.y+self.infoboard.height/2])
        self.screen.screen.blit(self.terribles_surface, [self.infoboard.x+self.infoboard.width-20-self.terribles_surface.get_width(),self.infoboard.y+self.infoboard.height/2-self.perfects_surface.get_height()])
        self.screen.screen.blit(self.misses_surface, [self.infoboard.x+self.infoboard.width-20-self.misses_surface.get_width(),self.infoboard.y+self.infoboard.height/2])
        self.screen.screen.blit(self.accuracy_surface, [self.infoboard.x+self.infoboard.width-20-self.accuracy_surface.get_width(), self.infoboard.y+20])
        self.screen.screen.blit(self.points_surface, [self.infoboard.x+self.infoboard.width/2-self.points_surface.get_width()/2, self.infoboard.y+self.infoboard.height-self.points_surface.get_height()-20])