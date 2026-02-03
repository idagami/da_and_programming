from turtle import Turtle
import os

ALIGNMENT = "center"  # easier to change instead of scrolling the code
FONT = ("Courier", 19, "normal")
cur_file_dir = os.path.dirname(__file__)
score_data_path = os.path.join(cur_file_dir, "data.txt")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        with open(score_data_path) as score_file:
            self.high_score = int(score_file.read())
        self.color("white")  # must be BEFORE .write()
        self.goto(0, 266)  # must be BEFORE .write()
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(
            f"Score: {self.score}    High score: {self.high_score}",
            move=False,
            align=ALIGNMENT,
            font=FONT,
        )

    def increase_score(self):
        self.score += 1
        self.update_scoreboard()

    def reset_scoreboard(self):
        if self.score > self.high_score:
            with open(score_data_path, mode="w") as score_file:
                score_file.write(str(self.score))
        self.score = 0
        self.update_scoreboard()
