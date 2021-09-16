from PPlay.keyboard import Keyboard
from PPlay.sprite import Sprite
from PPlay.mouse import Mouse
import json
import globalVar
import pygame

class Options():
    def __init__(self, screen):
        self.mouse = Mouse()
        self.selection = -1
        self.file = open("config/controls.json", "r")
        self.controls = json.load(self.file)
        self.file.close()
        self.font = pygame.font.Font("assets/secrcode.ttf", 30)
        self.screen = screen
        self.keyboard = Keyboard()
        self.commands = []
        self.buttons = []
        self.text_surface = []
        self.createCommands()
        self.createButtons()
        for command in self.commands:
            self.text_surface.append(self.font.render(command, True, [0, 180, 255]))

    def createButtons(self):
        backbutton = Sprite("assets/backbutton.png")
        x = self.screen.width/2 - backbutton.width/2
        y_start = 200
        space = 10
        for i in range(len(self.commands)):
            backbutton = Sprite("assets/backbutton.png")
            backbutton.x = x
            backbutton.y = y_start + space*i + backbutton.height*i
            self.buttons.append(backbutton)

    def createCommands(self):
        for i in self.controls:
            self.commands.append(i)
    
    def updatejson(self):
        file = open("config/controls.json", "w")
        json.dump(self.controls, file)
        file.close()
    
    def drawButtons(self):
        for i in range(len(self.buttons)):
            self.buttons[i].draw()
            self.screen.screen.blit(self.text_surface[i], [50 + self.buttons[i].x + 10, self.buttons[i].y + self.buttons[i].height/2 - self.text_surface[i].get_height()/2])
            if self.selection == i:
                color = [0, 255, 0]
            else:
                color = [0, 180, 255]
            key_surface = self.font.render(str(self.controls[self.commands[i]]), True, color)
            self.screen.screen.blit(key_surface, [self.buttons[i].x + self.buttons[i].width - 10 - key_surface.get_width() - 50, self.buttons[i].y + self.buttons[i].height/2 - self.text_surface[i].get_height()/2])
    
    def draw(self):
        self.update()
        self.drawButtons()
    
    def update(self):
        if self.keyboard.key_pressed("ESC"):
            globalVar.GAME_STATE = 0        
        if self.selection > -1 and self.selection < len(self.commands):
            key = self.keyboard.return_keys_pressed()
            if len(key) > 0:
                self.controls[self.commands[self.selection]] = key[0]
                globalVar.NOTES[self.selection] = key[0]
                self.updatejson()
                self.selection = -1
        else:
            for i in range(len(self.buttons)):
                if self.mouse.is_over_object(self.buttons[i]) and self.mouse.is_button_pressed(1):
                    self.selection = i