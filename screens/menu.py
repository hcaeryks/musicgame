from PPlay.mouse import Mouse
from PPlay.sprite import Sprite
from PPlay.keyboard import Keyboard
import os
import json
import globalVar

class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.data = self.songsData()
        self.buttons = []
        self.backmenu = Sprite("assets/backmenu.png")
        self.background = Sprite("assets/background.png")
        self.createButtons()
        self.maxheight = self.screen.height - 6 * self.buttons[0].height - 6*10 - 10
        self.posButtons()
    
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
            self.screen.draw_text(self.data[i]["name"], self.buttons[i].x + 5, self.buttons[i].y + 5, 24, (0, 255, 255), "Arial")
    
    def downButtons(self):
        for i in range(len(self.buttons)):
            self.buttons[i].y -=  100 * self.screen.delta_time()

    def upButtons(self):
        for i in range(len(self.buttons)):
            self.buttons[i].y +=  100 * self.screen.delta_time()
    
    def posButtons(self):
        for i in range(len(self.buttons)):
            self.buttons[i].x = self.screen.width - self.buttons[i].width - 50
            if i == 0:
                self.buttons[i].y = self.maxheight
            else:
                self.buttons[i].y = self.buttons[i-1].y + 10 + self.buttons[i].height
    
    def createButtons(self):
        for i in range(len(self.data)):
            backbutton = Sprite("assets/backbutton.png")
            self.buttons.append(backbutton)

    def showSelection(self, data):
        songicon = Sprite(data["image"])
        songicon.x = 100
        songicon.y = 150
        songicon.draw()
        self.screen.draw_text("Name: " + data["name"], songicon.x + 50, songicon.y + 50, 32, (0, 0, 255), "Arial")
        self.screen.draw_text("Artist: " + data["artist"], songicon.x + 50, songicon.y + 90, 32, (0, 0, 255), "Arial")
        self.screen.draw_text("Difficulty: " + data["difficulty"], songicon.x + 50, songicon.y + 130, 32, (0, 0, 255), "Arial")
        if self.mouse.is_button_pressed(1):
            globalVar.CURR_PLY = data["id"]
            globalVar.GAME_STATE = 3

    def run(self):
        if self.keyboard.key_pressed("DOWN"):
            self.downButtons()
        if self.keyboard.key_pressed("UP"):
            self.upButtons()
        
        self.background.draw()
        self.drawButtons()
        self.backmenu.draw()
        self.screen.draw_text("Song Selection", 1260, 360, 32, (0, 0, 255), "Arial")
        
        for i in range(len(self.buttons)):
            if self.mouse.is_over_object(self.buttons[i]) and self.mouse.is_over_area([self.screen.width - 10 - self.buttons[i].width, self.maxheight], [self.screen.width - 10, self.screen.height - 10]):
                self.showSelection(self.data[i])