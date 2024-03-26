from tkinter import Canvas
from typing import Tuple

from memory_number_game.load_config import load_config
config = load_config()


class Circle:
    radius = config['circle_radius']

    def __init__(self, canvas: Canvas, center: Tuple[int, int], number: int):
        self.canvas = canvas
        self.center = center
        self.text = str(number)
        self.text_widget = None

    def render(self):
        x0 = self.center[0] - self.radius
        y0 = self.center[1] - self.radius
        x1 = self.center[0] + self.radius
        y1 = self.center[1] + self.radius
        self.canvas.create_oval(x0, y0, x1, y1, width=5, fill="white")

    def display_text(self):
        x = self.center[0]
        y = self.center[1] + 4
        self.text_widget = self.canvas.create_text((x, y), text=self.text, anchor="center", font=('Helvetica 27 bold'))

    def remove_text(self):
        self.canvas.delete(self.text_widget)

    def is_click_inside(self, click: Tuple[int, int]) -> bool:
        return sum([(click[i] - self.center[i])**2 for i in range(2)]) < self.radius**2
    
