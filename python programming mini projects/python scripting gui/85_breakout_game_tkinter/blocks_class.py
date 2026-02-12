from turtle import Turtle


class Block(Turtle):
    def __init__(self, position, color):
        super().__init__("square")
        self.penup()
        self.shapesize(stretch_wid=0.5, stretch_len=3)
        self.color(color)
        self.goto(position)
