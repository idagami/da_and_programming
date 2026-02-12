from turtle import Turtle

ALIGNMENT = "left"
FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 1
        self.color("black")
        self.penup()
        self.goto(-266, 250)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(
            f"Level: {self.score}",
            move=False,
            align=ALIGNMENT,
            font=FONT,
        )

    def increase_score(self):
        self.clear()
        self.score += 1
        self.update_scoreboard()

    def game_over(self):
        self.goto(-100, 0)
        self.write(
            "GAME OVER",
            move=False,
            align=ALIGNMENT,
            font=FONT,
        )
