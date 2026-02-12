import time
from turtle import Screen
from player_class_25 import Player
from car_class_25 import CarManager
from scoreboard_class_25 import Scoreboard

my_screen = Screen()
my_screen.setup(width=600, height=600)
my_screen.tracer(0)

my_turtle = Player()
my_cars = CarManager()
my_score = Scoreboard()

my_screen.listen()
my_screen.onkey(key="Up", fun=my_turtle.move_up)

game_on = True
while game_on:
    time.sleep(0.1)
    my_screen.update()

    my_cars.create_car()  # on every car refresh
    my_cars.move_cars()
    my_cars.remove_cars()

    # detect collision with car
    for segment in my_cars.car_objects:
        if my_turtle.distance(segment) < 20:
            game_on = False
            my_score.game_over()

    # detect crossing finish line
    if my_turtle.ycor() > my_turtle.FINISH_LINE_Y:
        my_score.increase_score()
        my_turtle.reset_position()
        my_cars.increase_speed()

    # if my_turtle.is_at_finish_line():  # option 2 to detect reaching finish line
    #     my_score.increase_score()
    #     my_turtle.reset_position()
    #     my_cars.increase_speed()

my_screen.exitonclick()
