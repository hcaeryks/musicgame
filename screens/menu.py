from PPlay.mouse import Mouse
import os
import json

class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.mouse = Mouse()
        self.list = self.songList()
        print(self.list)
        self.printNames()
    
    def songList(self):
        tmp = []
        dir = os.listdir("songs")
        for file in dir:
            f = open("songs/" + file + "/info.json")
            data = json.load(f)
            tmp.append(data)
            f.close()
        return tmp
    
    def printNames(self):
        for data in self.list:
            print(data["name"])
    
    def run(self):
        pass