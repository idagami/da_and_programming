from turtle import Turtle, Screen
from paddle_class_24 import Paddle
from ball_class_24 import Ball
from scoreboard_class_24 import Scoreboard
import time

STEP = 10

my_screen = Screen()

my_screen.setup(800, 600)
my_screen.bgcolor("black")
my_screen.title("My pong game")
my_screen.tracer(0)  # turning animation off

right_paddle = Paddle(350)
left_paddle = Paddle(-350)
my_divider = Turtle()
my_ball = Ball()
my_score = Scoreboard()

my_divider.goto(0, -350)
my_divider.left(90)
# my_divider.hideturtle()

# for _ in range(int((my_screen.canvheight / STEP) / 2)):
for _ in range(30):
    my_divider.pencolor("white")
    my_divider.forward(STEP)
    my_divider.pencolor("black")
    my_divider.forward(STEP)

my_screen.listen()

my_screen.onkey(key="Up", fun=right_paddle.move_up)
my_screen.onkey(key="Down", fun=right_paddle.move_down)
my_screen.onkey(key="q", fun=left_paddle.move_up)
my_screen.onkey(key="z", fun=left_paddle.move_down)

game_on = True
while game_on:
    my_screen.update()  # manually update & refresh screen
    # time.sleep(0.1)
    time.sleep(my_ball.move_speed)
    my_ball.move()
    if my_ball.ycor() >= 280 or my_ball.ycor() <= -280:
        my_ball.bounce_top_bottom()
    # if my_ball.distance(left_paddle) < 10 or my_ball.distance(right_paddle) < 10: # wrong as .distance measures
    # distance between center of ball and center of paddle
    if (my_ball.distance(right_paddle) < 50 and my_ball.xcor() > 320) or (
        my_ball.distance(left_paddle) < 50 and my_ball.xcor() < -320
    ):
        my_ball.bounce_paddles()
    if my_ball.xcor() > 380:
        my_score.increase_score_left()
        my_ball.reset_position()
    if my_ball.xcor() < -380:
        my_score.increase_score_right()
        my_ball.reset_position()

    if my_score.score_left > 10 or my_score.score_right > 10:
        game_on = False
        my_score.game_over()

my_screen.exitonclick()
