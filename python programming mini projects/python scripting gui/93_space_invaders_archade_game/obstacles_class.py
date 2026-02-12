from turtle import Turtle
import random

start_x = -250
y_pos = range(-60, -60 + 6 * 30, 30)  # 6 here is the count of rows


class Obstacle(Turtle):
    def __init__(self, position):
        super().__init__("square")
        self.penup()
        self.shapesize(stretch_wid=0.5, stretch_len=0.1)
        self.shape("square")
        self.color("#8B4513")
        self.goto(position)


class ObstacleMgr:

    def __init__(self):
        self.obstacle_objects: list[Obstacle] = []

    def create(self):
        for y in y_pos:
            for i in range(35):
                x = start_x + i * 15
                obstacle = Obstacle((x, y))
                self.obstacle_objects.append(obstacle)
