from turtle import Turtle

STARTING_POSITION = (0, -250)
MOVE_DISTANCE = (
    15  # must be matching to obstancles distance otherwise wont be able to hit all
)
FLOOR_WALL = 280


class Cannon(Turtle):
    def __init__(self, shape):
        super().__init__()
        self.shape(shape)
        self.penup()
        self.hideturtle()

        self.tiltangle(90)
        self.goto(STARTING_POSITION)
        self.showturtle()

    def move_left(self):
        new_x = self.xcor() - MOVE_DISTANCE
        if new_x < -FLOOR_WALL:
            new_x = -FLOOR_WALL
        self.setx(new_x)

    def move_right(self):
        new_x = self.xcor() + MOVE_DISTANCE
        if new_x > FLOOR_WALL:
            new_x = FLOOR_WALL
        self.setx(new_x)

    def reset_position(self):
        self.goto(STARTING_POSITION)
