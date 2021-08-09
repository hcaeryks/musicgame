from PPlay.window import Window
from screens.game import Game

GAME_STATE = 4
window = Window(1920, 1080)
scrGame = Game(window)
    
switcher = {
    4: scrGame.draw
}

while 1:
    window.set_background_color((0, 0, 0))
    switcher.get(GAME_STATE)()
    window.update()