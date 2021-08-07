import pygame
from PPlay.window import Window
from screens.game import Game
from screens.menu import Menu

GAME_STATE = 0
window = Window(1920, 1080)
scrGame = Game(window)
scrMenu = Menu(window)

# 0 - Menu
# 1 - Opções
# 2 - Seleção
# 3 - Jogo
# 4 - Resultados
switcher = {
    0: scrMenu.run,
    3: scrGame.draw
}

while 1:
    window.set_background_color((0, 0, 0))
    switcher.get(GAME_STATE)()
    window.update()