from turtle import Turtle


class Paddle(Turtle):

    def __init__(self, y_pos):
        super().__init__()
        self.create_paddle(y_pos)

    def create_paddle(self, y_pos):
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=5)
        self.color("white")
        self.penup()
        self.goto(0, y_pos)

    def move_right(self):
        new_x = self.xcor() + 20
        if new_x < 250:
            self.goto(new_x, self.ycor())

    def move_left(self):
        new_x = self.xcor() - 20
        if new_x > -250:
            self.goto(new_x, self.ycor())