from turtle import Turtle, Screen
from paddle_class import Paddle
from ball_class import Ball
from blocks_class import Block
from scoreboard_class import Scoreboard
import time

my_screen = Screen()
my_screen.setup(578, 600)
my_screen.bgcolor("black")
my_screen.title("Breakout game")
my_screen.tracer(0)

COLORS = ["yellow", "yellow", "green", "green", "orange", "orange", "red", "red"]
start_x = -258
y_pos = range(140, 140 + 8 * 13, 13)
blocks = []

for row, y in enumerate(y_pos):
    for i in range(9):
        x = start_x + i * 64
        block = Block((x, y), COLORS[row])
        blocks.append(block)

paddle = Paddle(-270)
my_ball = Ball()
my_score = Scoreboard()

my_screen.listen()

my_screen.onkey(key="Right", fun=paddle.move_right)
my_screen.onkey(key="Left", fun=paddle.move_left)

game_on = True
while game_on:
    my_screen.update()
    time.sleep(my_ball.move_speed)
    my_ball.move()
    if my_score.game_is_over:
        my_ball.hideturtle()
        break
    if my_ball.xcor() >= 268 or my_ball.xcor() <= -268:
        my_ball.bounce_left_right()
    if my_ball.distance(paddle) < 50 and my_ball.ycor() <= -250:
        my_ball.bounce_paddle()
    for block in blocks:
        if my_ball.distance(block) < 50:
            block.hideturtle()
            blocks.remove(block)

            if (
                block.color()[0] == "yellow"
            ):  # .color() is a tuple of object color and object frame color.
                my_score.increase_score(1)
            elif block.color()[0] == "green":
                my_score.increase_score(3)
            elif block.color()[0] == "orange":
                my_score.increase_score(5)
                my_ball.move_speed *= 0.9
            elif block.color()[0] == "red":
                my_score.increase_score(7)
                my_ball.move_speed *= 0.9

            my_ball.bounce_top()
            break

    if my_ball.ycor() >= 280:
        my_ball.bounce_top()
    if my_ball.ycor() < -280:
        my_score.decrease_lives()
        my_ball.reset_position()
        paddle.goto(0, -270)
        my_ball.move()

my_screen.exitonclick()
