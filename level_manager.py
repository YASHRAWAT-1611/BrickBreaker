# level_manager.py
import json
import os
from objects.brick import Brick
from settings import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class LevelManager:
    def __init__(self):
        path = os.path.join(BASE_DIR, "data", "levels.json")
        with open(path, "r") as f:
            self.levels = json.load(f)["levels"]

    def load_level(self, level_index):
        bricks = []
        layout = self.levels[level_index]["rows"]
    
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == "1":
                    x = 50 + col_index * 80
                    y = 60 + row_index * 40
                    bricks.append(Brick(x, y, "normal"))
    
                elif cell == "2":
                    x = 50 + col_index * 80
                    y = 60 + row_index * 40
                    bricks.append(Brick(x, y, "strong"))
    
        return bricks


    def total_levels(self):
        return len(self.levels)
