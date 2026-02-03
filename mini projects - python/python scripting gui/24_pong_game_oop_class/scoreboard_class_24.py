from turtle import Turtle

ALIGNMENT = "center"  # easier to change instead of scrolling the code
FONT = ("Courier", 19, "bold")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score_left = 0
        self.score_right = 0
        self.color("white")
        self.penup()
        self.goto(0, 230)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(
            f"  Score: \n{self.score_left}       {self.score_right}",
            move=False,
            align=ALIGNMENT,
            font=FONT,
        )

    def increase_score_right(self):
        self.clear()
        self.score_right += 1
        self.update_scoreboard()

    def increase_score_left(self):
        self.clear()
        self.score_left += 1
        self.update_scoreboard()

    def game_over(self):
        self.goto(0, 0)
        self.write(
            "GAME OVER",
            move=False,
            align=ALIGNMENT,
            font=FONT,
        )
