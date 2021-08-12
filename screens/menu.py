from PPlay.mouse import Mouse
from PPlay.sprite import Sprite
from PPlay.keyboard import Keyboard
import os
import json

class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.data = self.songsData()
        self.buttons = []
        self.createButtons()
    
    def songsData(self):
        tmp = []
        dir = os.listdir("songs")
        for file in dir:
            f = open("songs/" + file + "/info.json")
            data = json.load(f)
            tmp.append(data)
            f.close()
        return tmp
    
    def drawButtons(self):
        for i in range(len(self.buttons)):
            self.buttons[i].draw()
            self.screen.draw_text(self.data[i]["name"], self.buttons[i].x + 5, self.buttons[i].y + 5, 24, (255, 0, 0), "Arial")
    
    def downButtons(self):
        for i in range(len(self.buttons)):
            self.buttons[i].y -=  100 * self.screen.delta_time()
    def upButtons(self):
        for i in range(len(self.buttons)):
            self.buttons[i].y +=  100 * self.screen.delta_time()
    
    def createButtons(self):
        for i in range(len(self.data)):
            backbutton = Sprite("assets/backbutton.png")
            backbutton.x = self.screen.width - backbutton.width - 50
            if i == 0:
                backbutton.y = self.screen.height - 9 * backbutton.height - 10*10 - 10
            else:
                backbutton.y = self.buttons[i-1].y + 10 + backbutton.height
            self.buttons.append(backbutton)

    def run(self):
        if self.keyboard.key_pressed("DOWN"):
            self.downButtons()
        if self.keyboard.key_pressed("UP"):
            self.upButtons()
        self.drawButtons()