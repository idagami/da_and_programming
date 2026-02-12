from turtle import Turtle
import random


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.shapesize(stretch_len=1, stretch_wid=1)
        self.color("yellow")
        self.speed(8)
        # self.hideturtle()
        self.goto(0, -250)
        self.x_move = 10  # actually represent velocity, because they control
        # how far the ball travels each time move() is called.
        self.y_move = 10
        self.move_speed = 0.1  # option 2: way to speed up the ball after hitting paddle

    def move(self):
        # rand_x = random.randint(-350, 350) # not good. This teleported the ball to a random place
        # on the screen each frame. That’s why it looked jumpy. rand_y = random.randint(-250, 230)
        self.penup()
        new_x = (
            self.xcor() + self.x_move
        )  # vector-based movement. makes the ball move in a straight line with constant increments
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_top_bottom(self):
        self.y_move *= (
            -1
        )  # Only the vertical direction should change. So we flip y_move, because that controls up vs down.
        # x_move stays the same, so the ball keeps moving left or right.
        # Example: Before: (x_move=3, y_move=3) → going up-right.
        # After bouncing at the top: (x_move=3, y_move=-3) → now going down-right.

    def bounce_paddles(self):
        self.x_move *= -1
        self.x_move *= (
            1.1  # Suppose x_move = 10 → after hitting the paddle: 10 * 1.1 = 11
        )
        # That means the ball now moves 11 pixels per frame instead of 10.
        # So it’s “faster” because in the same loop iteration it travels further.
        self.y_move *= 1.1
        # self.move_speed *= 0.9  # option 2: way to speed up the ball after hitting paddle - reducing sleep time

    def reset_position(self):
        self.goto(0, -250)
        self.move_speed = (
            0.1  # option 2: way to speed up the ball after hitting paddle,
        )
        # we need to return the original speed if ball was missed
        self.x_move *= -1
