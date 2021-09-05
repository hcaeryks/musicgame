from PPlay.window import Window
from screens.game import Game
from screens.songselection import SongSelection
import globalVar

window = Window(1920, 1080)
scrGame = None
scrSongSelection = SongSelection(window)

# 0 - SongSelection
# 1 - Opções
# 2 - Seleção
# 3 - Jogo
# 4 - Resultados

while 1:
    #print(0 if window.delta_time() <= 0 else 1/window.delta_time())
    if globalVar.CURR_PLY == 0 and globalVar.GAME_STATE == 3:
        globalVar.CURR_PLY = 3
        scrGame = Game(window)
    elif globalVar.CURR_PLY == 3 and globalVar.GAME_STATE != 3:
        globalVar.CURR_PLY = 0
    window.set_background_color((0, 0, 0))
    if globalVar.GAME_STATE == 0:
        scrSongSelection.run()
    elif globalVar.GAME_STATE == 3:
        scrGame.draw()
    window.update()