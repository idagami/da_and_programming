from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
cars = ["a", "b", "c", "d"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 2  # by this amount speed increases, its pace
LANES = list(range(-230, 250, 40))  # so cars arent stacked on top of another
# print(LANES)


class CarManager:
    def __init__(self):
        self.car_objects = []
        # self.create_car() # not needed here. You create all cars in __init__
        # (or create multiple upfront). Better: spawn cars occasionally (random) so traffic looks natural.
        self.car_speed = STARTING_MOVE_DISTANCE

    def create_car(
        self,
    ):  # could have added an additional check: distance between each car, so they dont stack horizontally.
        # decided not to. So some cars seem longer
        # 1 in 6 chance per frame (adjust number for more/less traffic)
        if random.randint(1, 6) == 1:
            car = Turtle("square")
            car.shapesize(stretch_wid=1, stretch_len=2)
            car.color(random.choice(COLORS))
            car.penup()
            rand_y = random.choice(LANES)
            car.goto(300, rand_y)
            car.setheading(180)
            self.car_objects.append(car)

    def move_cars(self):
        for car in self.car_objects:
            car.forward(self.car_speed)

    def remove_cars(self):
        for car in self.car_objects[:]:
            if car.xcor() < -260:
                car.hideturtle()
                self.car_objects.remove(car)

    def increase_speed(self):
        self.car_speed += MOVE_INCREMENT
