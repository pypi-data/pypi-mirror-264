from tkinter import TclError
from memory_number_game.game import Game


def play_number_game():
    try:
        game = Game()
        game.play()
    except TclError:
        pass
