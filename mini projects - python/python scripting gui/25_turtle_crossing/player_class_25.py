from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("black")
        self.penup()
        self.reset_position()
        self.left(90)
        self.FINISH_LINE_Y = (
            280  # dont need this line if use option 2 to detect cross finish line
        )

    def move_up(self):
        self.forward(MOVE_DISTANCE)

    # def is_at_finish_line(self): # option 2 to detect reaching finish line
    #     if self.ycor() > FINISH_LINE_Y:
    #         return True

    def reset_position(self):
        self.goto(STARTING_POSITION)
