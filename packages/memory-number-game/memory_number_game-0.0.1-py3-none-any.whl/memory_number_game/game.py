from tkinter import Canvas, Button, Tk
import time
from memory_number_game.level import Level
from memory_number_game.load_config import load_config
config = load_config()


class Game:
    center_x = int(config['canvas_size']/2)
    center_y = center_x - int(config['header_height']/2)

    def __init__(self):
        self.level = config['initial_level']
        self.window = Tk()
        self.window.title("A little memory game...")
        self.window.geometry(f"{config['canvas_size']}x{config['canvas_size'] + config['header_height']}")
        self.window.configure(bg='white')

    def play(self):
        self.play_level()
        self.window.mainloop()

    def play_level(self):
        self.beginning_animation()
        level = Level(self)
        level.start()

    def get_canvas(self) -> Canvas:
        return Canvas(self.window, bg="white", height=config['canvas_size'], width=config['canvas_size'], highlightthickness=0)

    def beginning_animation(self):
        canvas = self.get_canvas()
        canvas.place(x=0, y=config['header_height'])
        for i in range(3):
            number = canvas.create_text((self.center_x, self.center_y), text=f'{3-i}', anchor="center", font=('Helvetica 50 bold'))
            canvas.update()
            time.sleep(1)
            canvas.delete(number)
        canvas.destroy()

    def level_won(self):
        self.level += 1
        canvas = self.get_canvas()
        canvas.place(x=0, y=config['header_height'])
        canvas.create_text((self.center_x, self.center_y), text='Bravo!', anchor="center", font=('Helvetica 50 bold'))
        canvas.update()
        time.sleep(1)
        canvas.destroy()
        self.play_level()

    def lost(self):
        button = Button(self.window, text='New Game', bg='green', font='Helvetica 27')
        button.bind("<Button-1>", self.new_game)
        button.place(x=self.center_x, y=50, anchor="center")

    def new_game(self, event):
        event.widget.destroy()
        self.level = config['initial_level']
        self.play_level()