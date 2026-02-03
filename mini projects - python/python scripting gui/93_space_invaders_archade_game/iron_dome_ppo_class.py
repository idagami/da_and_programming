from turtle import Turtle
import random

starting_move_distance = 11  # speed
vertical_lanes = list(range(-240, 240, 40))
rand_x = random.choice(vertical_lanes)


class Ppo(Turtle):  # creating one bullet
    def __init__(self, cannon_position):
        super().__init__()
        self.shape("circle")
        self.shapesize(stretch_len=1.5, stretch_wid=0.1)
        self.color("white")
        self.penup()
        self.goto(cannon_position)
        self.setheading(90)
        self.speed = starting_move_distance

    def shoot(self):
        self.forward(self.speed)


class PpoManager:  # creating the whole laser
    def __init__(self):
        self.ppo_objects: list[Ppo] = []

    def create(self, cannon_xcor):
        new_ppo = Ppo((cannon_xcor, -210))
        self.ppo_objects.append(new_ppo)

    def move_all(self):
        for ppo in self.ppo_objects:
            ppo.shoot()

    def remove_ppo_offscreen(self):
        for ppo in self.ppo_objects[:]:
            if ppo.ycor() > 250:
                ppo.hideturtle()
                self.ppo_objects.remove(ppo)
