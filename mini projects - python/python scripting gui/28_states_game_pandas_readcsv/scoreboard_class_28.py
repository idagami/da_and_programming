from turtle import Turtle

ALIGNMENT = "right"
FONT = ("Courier", 30, "bold")

# all commented code below can be uncommented if i need score to be displayed on screen along the timer


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        # self.color("black")
        # self.penup()
        # self.goto(200, 170)
        self.hideturtle()
        # self.update_scoreboard()

    def update_scoreboard(self):
        # self.write(
        #     f"Score:\n {self.score}/50",
        #     move=False,
        #     align=ALIGNMENT,
        #     font=FONT,
        # )
        pass

    def increase_score(self):
        self.clear()
        self.score += 1
        # self.update_scoreboard()

    def game_over(self):
        self.goto(0, 0)
        self.write(
            f"Time's up!\n GAME OVER\n Guessed so far: {self.score}/50",
            move=False,
            align="center",
            font=FONT,
        )
