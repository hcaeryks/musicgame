from PPlay.window import Window
from screens.game import Game
from screens.menu import Menu

GAME_STATE = 3
CURR_PLY = 0
window = Window(1920, 1080)
scrGame = None
scrMenu = Menu(window)

# 0 - Menu 
# 1 - Opções
# 2 - Seleção
# 3 - Jogo
# 4 - Resultados

while 1:
    print(0 if window.delta_time() <= 0 else 1/window.delta_time())
    if CURR_PLY == 0 and GAME_STATE == 3:
        CURR_PLY = 3
        scrGame = Game(window)
    elif CURR_PLY == 3 and GAME_STATE != 3:
        CURR_PLY = 0
    window.set_background_color((0, 0, 0))
    if GAME_STATE == 0:
        scrMenu.run()
    elif GAME_STATE == 3:
        scrGame.draw()
    window.update()