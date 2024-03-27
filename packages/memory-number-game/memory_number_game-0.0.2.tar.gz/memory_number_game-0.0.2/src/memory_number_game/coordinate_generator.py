import random
from typing import Tuple

from memory_number_game.load_config import load_config
config = load_config()


class Spot:
    radius = config['circle_radius']
    min_circle_distance = 20

    def __init__(self, center: Tuple[int, int]):
        self.center = center

    def is_distant_enough(self, other_spot: "Spot") -> bool:
        return sum([(self.center[i] - other_spot.center[i])**2 for i in range(2)]) > (2*self.radius + self.min_circle_distance)**2


class CoordinateGenerator:
    def __init__(self):
        self.canvas_size = config['canvas_size']
        self.offset = config['circle_border_ditance']
        self.busy_spots = []

    def generate_circle(self) -> Tuple[int, int]:
        valid_candidate_found = False
        while not valid_candidate_found:
            center = (self.generate_candidate_1d(), self.generate_candidate_1d())
            candidate = Spot(center)
            if all([candidate.is_distant_enough(spot) for spot in self.busy_spots]):
                valid_candidate_found = True
        self.busy_spots.append(candidate)
        return center

    def generate_candidate_1d(self) -> int:
        return random.randint(self.offset, self.canvas_size - self.offset)
    


