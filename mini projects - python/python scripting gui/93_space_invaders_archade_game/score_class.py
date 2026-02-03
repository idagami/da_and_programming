from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 19, "bold")


class Scoreboard(Turtle):
    def __init__(self, lives=5):
        super().__init__()
        self.score = 0
        self.lives = lives
        self.game_is_over = False
        self.color("white")
        self.penup()
        self.goto(0, 250)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(
            f"Lives: {self.lives}               Score: {self.score}",
            move=False,
            align=ALIGNMENT,
            font=FONT,
        )

    def increase_score(self, score):
        self.clear()
        self.score += score
        self.update_scoreboard()

    def decrease_score(self, score):
        self.clear()
        self.score -= score
        self.update_scoreboard()

    def decrease_lives(self):
        self.lives -= 1
        self.clear()
        if self.lives <= 0:
            self.game_over(result="lost")
        else:
            self.update_scoreboard()

    def game_over(self, result="lost"):
        self.goto(0, 0)
        self.write(
            f"GAME OVER\nYou {result}!\nScore: {self.score}",
            move=False,
            align=ALIGNMENT,
            font=("Courier", 40, "bold"),
        )
        self.game_is_over = True
