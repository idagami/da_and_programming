from turtle import Turtle


class Paddle(Turtle):

    def __init__(self, x_pos):  # when using this class, must pass 1 argument
        super().__init__()
        self.create_paddle(x_pos)

    def create_paddle(self, x_pos):
        self.shape("square")
        self.shapesize(stretch_wid=5, stretch_len=1)  # start 20x20, so 20x100 is 5x1
        self.color("white")
        self.penup()
        self.goto(x_pos, 0)

    def move_up(self):
        new_y = self.ycor() + 20
        if new_y < 250:
            self.goto(self.xcor(), new_y)
        # self.forward(20)

    def move_down(self):
        new_y = self.ycor() - 20
        if new_y > -250:
            self.goto(self.xcor(), new_y)
        # self.forward(20)
