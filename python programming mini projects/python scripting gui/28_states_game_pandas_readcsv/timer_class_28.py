import time
from turtle import Turtle

ALIGNMENT = "right"
FONT = ("Courier", 30, "bold")


class Timer(Turtle):
    def __init__(self):
        super().__init__()
        self.timer1 = 15 * 60
        self.color("black")
        self.penup()
        self.goto(350, 170)
        self.hideturtle()
        self.countdown()

    def countdown(self):
        if self.timer1 > 0:
            self.clear()
            self.getscreen().ontimer(
                self.countdown, 1000
            )  # schedule countdown() after 1000 ms
            mins, secs = divmod(self.timer1, 60)
            timer_text = f"{mins:02d}:{secs:02d}"
            self.write(
                f"Timer:\n {timer_text}",
                move=False,
                align=ALIGNMENT,
                font=FONT,
            )
            self.timer1 -= 1
