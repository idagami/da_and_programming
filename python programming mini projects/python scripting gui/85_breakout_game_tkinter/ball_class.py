from turtle import Turtle
import random


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.shapesize(stretch_len=1, stretch_wid=1)
        self.color("white")
        self.speed(8)
        self.penup()
        self.goto(0, -230)
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.1

    def move(self):
        self.penup()
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_left_right(self):
        self.x_move *= -1

    def bounce_top(self):
        self.y_move *= -1
        self.x_move = random.choice([-10, 10])

    def bounce_paddle(self):
        self.y_move *= -1
        self.y_move *= 1.1
        self.x_move *= 1.1

    def reset_position(self):
        self.goto(0, -230)
        self.x_move = 10
        self.y_move = random.choice([-10, 10])
