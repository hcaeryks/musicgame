from PPlay.window import Window
from screens.game import Game
from screens.songselection import SongSelection
from screens.home import Home
from screens.results import Results
from screens.options import Options
from PPlay.keyboard import *
from PPlay.sprite import *
import globalVar
import json

window = Window(1920, 1080)

scrRes = None
scrGame = None
scrHome = Home(window)
scrSongSelection = SongSelection(window)
scrOptions = Options(window)


#-1 - Exit
# 0 - Home
# 1 - Opções
# 2 - Seleção
# 3 - Jogo
# 4 - Resultados

#globalVar.GAME_STATE = 4

keyboard = Keyboard()
bg = Sprite("assets/bgresults.png")

file = open("config/controls.json", "r")
controls = json.load(file)
file.close()
for control in controls:
    key = controls[control]
    if control.startswith("Note"):
        note_number = control.split()
        note_number = int(note_number[1])-1
        globalVar.NOTES[note_number] = key

while globalVar.GAME_STATE != -1:
    #print(0 if window.delta_time() <= 0 else 1/window.delta_time())
    if globalVar.CURR_PLY == 0 and globalVar.GAME_STATE == 3:
        globalVar.CURR_PLY = 3
        scrGame = Game(window)
    elif globalVar.CURR_PLY == 3 and globalVar.GAME_STATE != 3:
        globalVar.CURR_PLY = 0

    if globalVar.CURR_PLY == 0 and globalVar.GAME_STATE == 4:
        globalVar.CURR_PLY = 4
        scrRes = Results(window)
    elif globalVar.CURR_PLY == 4 and globalVar.GAME_STATE != 4:
        globalVar.CURR_PLY = 0


    bg.draw()
    if globalVar.GAME_STATE == 0:
        scrHome.draw()
    elif globalVar.GAME_STATE == 1:
        scrOptions.draw()
    elif globalVar.GAME_STATE == 2:
        scrSongSelection.draw()
    elif globalVar.GAME_STATE == 3:
        scrGame.draw()
    elif globalVar.GAME_STATE == 4:
        scrRes.draw()
    window.update()