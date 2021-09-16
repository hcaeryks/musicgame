from PPlay.sprite import *
from PPlay.mouse import *
import pygame
import globalVar as g

class Home():
    def __init__(self, screen):
        self.mouse = Mouse()
        self.screen = screen
        self.font = pygame.font.Font("assets/secrcode.ttf", 40)
        self.texts = [["Song Selection", [0, 0, 255], 2], ["Settings", [0, 0, 255], 1], ["Exit", [0, 0, 255], -1]]
        self.buttons = []
        self.surfaces = []
        self.createButtons()
        for i in range(len(self.buttons)):
            self.surfaces.append(self.font.render(self.texts[i][0], True, self.texts[i][1]))

    def createButtons(self):
        backbutton = Sprite("assets/backbutton.png")
        x_start = self.screen.width/2-backbutton.width/2
        y_start = self.screen.height/2
        space = 20
        for i in range(3):
            backbutton = Sprite("assets/backbutton.png")
            backbutton.x = x_start
            backbutton.y = y_start + i*space + i*backbutton.height
            self.buttons.append(backbutton)


    def drawButtons(self):
        for i in range(len(self.buttons)):
            text_surface = self.font.render(self.texts[i][0], True, self.texts[i][1])
            self.buttons[i].draw()
            self.screen.screen.blit(text_surface, [self.buttons[i].x + self.buttons[i].width/2 - text_surface.get_width()/2, self.buttons[i].y + self.buttons[i].height/2 - text_surface.get_height()/2])
            

    def draw(self):
        self.update()
        self.drawButtons()

    def update(self):
        for i in range(len(self.buttons)):
            self.texts[i][1] = [0, 0, 255]
            if self.mouse.is_over_object(self.buttons[i]):
                self.texts[i][1] = [0, 255, 0]
                if self.mouse.is_button_pressed(1):
                    g.GAME_STATE = self.texts[i][2]