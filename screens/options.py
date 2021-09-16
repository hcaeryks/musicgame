from PPlay.keyboard import Keyboard
from PPlay.sprite import Sprite
from PPlay.mouse import Mouse
import json
import globalVar
import pygame

class Options():
    def __init__(self, screen):
        self.start_cooldown = True
        self.start_cooldown_time = 0.1
        self.start_time = 0
        
        self.exit_cooldown = False
        self.exit_cooldown_time = 0.1
        self.exit_time = 0

        self.cooldown = False
        self.volume_cooldown_time = 0.1
        self.cooldown_time = 0.3
        self.hold = 0
        
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
        y_start = 150
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
        if self.start_cooldown:
            self.start_time += self.screen.delta_time()
            if self.start_time >= self.start_cooldown_time:
                self.start_cooldown = False
                self.start_time = 0
        else:
            if self.exit_cooldown:
                self.exit_time += self.screen.delta_time()
                if self.exit_time >= self.exit_time:
                    self.exit_cooldown = False
                    self.exit_time = 0
            if self.keyboard.key_pressed("ESC") and self.selection == -1 and not self.exit_cooldown:
                globalVar.GAME_STATE = 0
                self.start_cooldown = True
            if self.selection > -1 and self.selection < len(self.commands):
                if self.commands[self.selection].startswith("Note"):
                    if not self.commands[self.selection].endswith("Speed"):
                        key = self.keyboard.return_keys_pressed()
                        if len(key) > 0:
                            self.controls[self.commands[self.selection]] = key[0]
                            globalVar.NOTES[self.selection] = key[0]
                            self.updatejson()
                            self.selection = -1
                            self.exit_cooldown = True
                    else:
                        if self.keyboard.key_pressed("ENTER"):
                            self.selection = -1
                        else:
                            if not self.keyboard.key_pressed("UP") and not self.keyboard.key_pressed("DOWN"):
                                self.hold = 0
                                self.cooldown = False
                            else:
                                if self.hold >= self.cooldown_time:
                                    self.hold = 0
                                    self.cooldown = False
                                if self.keyboard.key_pressed("UP") and float(self.controls[self.commands[self.selection]]) < 2:
                                    if self.cooldown:
                                        self.hold += self.screen.delta_time()
                                    else:
                                        self.controls[self.commands[self.selection]] = str(round(float(self.controls[self.commands[self.selection]]) + 0.1, 1))
                                        self.updatejson()
                                        self.cooldown = True
                                    
                                if self.keyboard.key_pressed("DOWN") and float(self.controls[self.commands[self.selection]]) > 1:
                                    if self.cooldown:
                                        self.hold += self.screen.delta_time()
                                    else:
                                        self.controls[self.commands[self.selection]] = str(round(float(self.controls[self.commands[self.selection]]) - 0.1, 1))
                                        self.updatejson()
                                        self.cooldown = True
                if self.commands[self.selection].startswith("Volume"):
                    if self.hold >= self.volume_cooldown_time:
                                    self.hold = 0
                                    self.cooldown = False
                    if not self.keyboard.key_pressed("UP") and not self.keyboard.key_pressed("DOWN") and self.cooldown:
                                self.hold = 0
                                self.cooldown = False
                                
                    if self.keyboard.key_pressed("ENTER"):
                            self.selection = -1
                            
                    elif self.keyboard.key_pressed("UP") and int(self.controls[self.commands[self.selection]]) < 100:
                        if self.cooldown:
                            self.hold += self.screen.delta_time()
                        else:
                            self.controls[self.commands[self.selection]] = str(int(self.controls[self.commands[self.selection]]) + 1)
                            self.updatejson()
                            self.cooldown = True
                        
                    elif self.keyboard.key_pressed("DOWN") and int(self.controls[self.commands[self.selection]]) > 1:
                        if self.cooldown:
                            self.hold += self.screen.delta_time()
                        else:
                            self.controls[self.commands[self.selection]] = str(int(self.controls[self.commands[self.selection]]) - 1)
                            self.updatejson()
                            self.cooldown = True
            else:
                for i in range(len(self.buttons)):
                    if self.mouse.is_over_object(self.buttons[i]) and self.mouse.is_button_pressed(1):
                        self.selection = i