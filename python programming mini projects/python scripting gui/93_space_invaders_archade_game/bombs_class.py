from turtle import Turtle
import random
from score_class import Scoreboard

starting_move_distance = 4  # speed
vertical_lanes = list(range(-240, 240, 40))
rand_x = random.choice(vertical_lanes)


class Bomb(Turtle):  # creating one bullet
    def __init__(self, invader_position):
        super().__init__()
        self.shape("circle")
        self.shapesize(stretch_len=1.5, stretch_wid=0.3)
        self.color("yellow")
        self.penup()
        self.goto(invader_position)
        self.setheading(270)
        self.speed = starting_move_distance

    def fall(self):
        self.forward(self.speed)


class BombManager:  # creating the whole laser
    def __init__(self, score):
        self.bomb_objects: list[Bomb] = []
        self.score = score

    def create(self, invader_position):
        new_bomb = Bomb(invader_position)
        self.bomb_objects.append(new_bomb)

    def move_all(self):
        for bomb in self.bomb_objects:
            bomb.fall()

    def remove_bomb_offscreen(self):
        for bomb in self.bomb_objects[:]:
            if bomb.ycor() < -240:
                bomb.hideturtle()
                self.bomb_objects.remove(bomb)
                self.score.decrease_score(1)
