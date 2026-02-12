from turtle import Turtle
import random


class Food(Turtle):  # will inherit attributes of Turtle class
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(
            stretch_len=0.5, stretch_wid=0.5
        )  # standard 20x20. if I want 10, then value 0.5
        self.color("blue")
        self.speed("fastest")
        # .speed("fastest") makes the turtle draw instantly when
        # moving to a new location. For food, we don’t want to see it "crawling"
        # from the old place to the new place when it relocates.
        # We want it to instantly appear at the new random spot.
        # Unlike the snake, the food only moves occasionally (when eaten),
        # and we don’t manually control it frame by frame with screen.tracer().
        # So .speed("fastest") ensures that when you call:
        # self.goto(x, y), the food jumps instantly without animation.
        self.refresh()

    def refresh(self):
        rand_x = random.randint(-265, 265)
        rand_y = random.randint(-265, 265)
        self.goto(rand_x, rand_y)
