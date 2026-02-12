from turtle import Turtle


class Cursor(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.color("black")
        self.penup()
        self.speed(
            "fastest"
        )  # to avoid seeing the turtle “move” to each coordinate slowly.

    def move(self, state_name, coord):
        self.goto(coord)
        self.write(state_name, move=False, align="center", font=("Arial", 10, "normal"))
