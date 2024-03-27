import time
from typing import Tuple
from memory_number_game.circle import Circle
from memory_number_game.coordinate_generator import CoordinateGenerator
from memory_number_game.load_config import load_config
config = load_config()


class Level:
    def __init__(self, game):

        self.number_of_circles = game.level
        self.game = game
        self.canvas = game.get_canvas()
        self.circles = []
        self.canvas.place(x=0, y=config['header_height'])


    def start(self):
        coordinate_generator = CoordinateGenerator()
        for i in range(self.number_of_circles):
            center = coordinate_generator.generate_circle()
            circle = Circle(canvas=self.canvas, center=center, number=i+1)
            self.circles.append(circle)
            circle.render()
            circle.display_text()

        self.canvas.update()
        time.sleep(config['observing_time'])

        for circle in self.circles:
            circle.remove_text()

        self.canvas.update()
        self.canvas.bind("<Button-1>", self.check)

    def check(self, event):
        click = (event.x, event.y)
        if self.correct_click(click):
            self.process_correct_click()
            if not self.circles:
                self.won()

        if self.wrong_click(click):
            self.lost()

    def correct_click(self, click: Tuple[int, int]) -> bool:
        return self.circles[0].is_click_inside(click)

    def wrong_click(self, click: Tuple[int, int]) -> bool:
        return any([circle.is_click_inside(click) for circle in self.circles])
    
    def process_correct_click(self):
        self.circles[0].display_text()
        del self.circles[0]

    def won(self):
        self.canvas.update()
        time.sleep(0.5)
        self.canvas.destroy()
        self.game.level_won()

    def lost(self):
        for circle in self.circles:
            circle.display_text()
        self.game.lost()