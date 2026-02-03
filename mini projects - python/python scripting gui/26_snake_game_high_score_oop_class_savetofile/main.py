## option 1, no oop
# import random
# from turtle import Turtle, Screen
# import time

# my_screen = Screen()
# my_screen.setup(600, 600)
# my_screen.bgcolor("black")
# my_screen.title("My snake game")
# my_screen.tracer(0)

# snake_body = ["a", "b", "c"]

# x_start = 0
# y_start = 0

# snake_obj = []

# for segment in snake_body:
#     segment = Turtle("square")
#     segment.color("white")
#     segment.penup()
#     segment.goto(x_start, y_start)
#     x_start -= 20
#     snake_obj.append(segment)

# a = snake_obj[0]
# a.color("yellow")


# game_on = True
# while game_on:
#     my_screen.update()  # we update screen everytime that ALL segments moved
#     time.sleep(0.1)  # will be delayed after ALL 3 segm moved
#     #     # my_screen.update() ## we see each single segment move in order 1 2 3 1 2 3, not simultaneously
#     #     # time.sleep(1)  ## adds 1 second delay after each segment moves
#     for seg_num in range(
#         len(snake_obj) - 1, 0, -1  # range(start, stop, step)
#     ):  # range from last piece whose index will be (len(obj) - 1)
#         new_x = snake_obj[seg_num - 1].xcor()
#         new_y = snake_obj[seg_num - 1].ycor()
#         snake_obj[seg_num].goto(new_x, new_y)
#     snake_obj[0].forward(20)
#     # snake_obj[0].left(90)

# my_screen.exitonclick()

## option 2, as oop
from turtle import Screen  # deleted Turtle class from here as we aren't using it below
from turtle import Turtle
import time
from snake_class_26 import Snake
from food_class_26 import Food
from score_class_26 import Scoreboard

my_screen = Screen()
my_screen.setup(600, 600)
my_screen.bgcolor("black")
my_screen.title("My snake game")
my_screen.tracer(0)

my_snake = Snake()
my_food = Food()
my_score = Scoreboard()

my_frame = Turtle()
my_frame.penup()
my_frame.hideturtle()
my_frame.pensize(20)
my_frame.goto(290, -290)
my_frame.pendown()
my_frame.pencolor("red")
for i in range(4):
    my_frame.left(90)
    my_frame.forward(590)

my_screen.listen()

my_screen.onkey(key="Up", fun=my_snake.move_up)
my_screen.onkey(key="Down", fun=my_snake.move_down)
my_screen.onkey(key="Left", fun=my_snake.move_left)
my_screen.onkey(key="Right", fun=my_snake.move_right)

game_on = True
score = 0
while game_on:
    my_screen.update()  # we update screen everytime that ALL segments moved
    time.sleep(0.3)  # will be delayed after ALL 3 segm moved
    # .sleep is also influencing snake's speed. changed from 0.1 to 0.3

    my_snake.move()

    # detect collision with food
    if my_snake.head.distance(my_food) < 15:
        # print("nom nom nom")
        my_snake.extend()
        my_food.refresh()
        my_score.increase_score()

    # detect collision with wall
    if (
        my_snake.head.xcor() >= 280
        or my_snake.head.xcor() < -280
        or my_snake.head.ycor() >= 280
        or my_snake.head.ycor() < -280
    ):
        my_score.reset_scoreboard()
        my_snake.reset()

    # detect collision with tail (all body segments except head)
    for segment in my_snake.body_segments_obj[1:]:
        if my_snake.head.distance(segment) < 10:
            my_score.reset_scoreboard()
            my_snake.reset()

my_screen.exitonclick()
