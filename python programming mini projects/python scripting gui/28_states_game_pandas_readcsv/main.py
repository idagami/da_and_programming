from turtle import Turtle, Screen
from scoreboard_class_28 import Scoreboard
from cursor_class_28 import Cursor
import time, os
from timer_class_28 import Timer
import pandas as pd


my_screen = Screen()
my_screen.title("US states game")

cur_file_dir = os.path.dirname(__file__)
states_img_path = os.path.join(cur_file_dir, "blank_states_img.gif")

my_screen.bgpic(states_img_path)
my_screen.setup(750, 520)
my_screen.tracer(0)


my_timer = Timer()
my_cursor = Cursor()
# my_cursor.hideturtle()
my_score = Scoreboard()

states_list_path = os.path.join(cur_file_dir, "50_states.csv")

data = pd.read_csv(states_list_path)

states_list = data.state.to_list()

my_screen.update()
my_timer.countdown()
guessed_states_list = []
while len(guessed_states_list) < 50 and my_timer.timer1 > 0:
    user_guess = my_screen.textinput(
        f"Guessed so far: {my_score.score}/50",
        "  Enter state name: ",
    )
    time.sleep(0.1)
    if user_guess is None or my_timer.timer1 <= 0:
        break  # user clicked Cancel button

    user_guess = user_guess.title().strip()

    if user_guess in states_list and user_guess not in guessed_states_list:
        # row_list = data[data.state == user_guess].values  # it's a 2D numpy array
        # state = row_list[0][0]
        # guessed_states_list.append(state)
        # coord_tuple = (row_list[0][1], row_list[0][2])
        # option 2 for above to get state and coordinates:
        row = data[data.state == user_guess]  # DataFrame with 1 row
        state = row.state.item()  # state name
        x_coord = row.x.item()  # x coordinate
        y_coord = row.y.item()  # y coordinate
        coord_tuple = (x_coord, y_coord)
        my_cursor.move(state, coord_tuple)
        guessed_states_list.append(state)
        my_score.increase_score()


states_to_learn = [i for i in states_list if i not in guessed_states_list]
print(len(states_to_learn))

# states_to_learn = list(set(states_list) - set(guessed_states_list)) # option 2 for above
# print(len(states_to_learn))

study = pd.Series(states_to_learn)

states_to_learn_path = os.path.join(cur_file_dir, "study_me.csv")

study.to_csv(states_to_learn_path)

my_score.game_over()

# my_screen.exitonclick()
my_screen.mainloop()  # keeps screen open after code execution, doesnt depend on click
