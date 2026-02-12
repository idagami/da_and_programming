from tkinter import *  # type: ignore
import os
from quiz_brain_class_36 import QuizBrain

THEME_COLOR = "#375362"
cur_file_dir = os.path.dirname(__file__)


class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()  # adding 'self. makes this window as property of this class
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score_label = Label(fg="white", text="Score: 0", pady=20, bg=THEME_COLOR)
        self.score_label.grid(row=0, column=1)

        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150,
            125,
            width=270,
            text="text here",
            font=("Arial", 18, "italic"),
            fill="black",
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        green_path = os.path.join(cur_file_dir, "images", "true.png")
        green_img = PhotoImage(
            file=green_path
        )  # no need for 'self.' as we wont use it anywhere in project other than here
        self.button_green = Button(
            image=green_img,
            highlightthickness=0,
            bg=THEME_COLOR,
            padx=20,
            pady=20,
            command=self.click_green,
        )
        self.button_green.grid(row=2, column=0)

        red_path = os.path.join(cur_file_dir, "images", "false.png")
        red_img = PhotoImage(file=red_path)
        self.button_red = Button(
            image=red_img,
            highlightthickness=0,
            bg=THEME_COLOR,
            padx=20,
            pady=20,
            command=self.click_red,
        )
        self.button_red.grid(row=2, column=1)

        self.get_next_question()

        self.window.mainloop()  # in essence it's a loop. it will get confused if it has another loop near it

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(
                self.question_text,
                text=f"You've completed the BrainQuiz!\nYour final score is: {self.quiz.score}/{self.quiz.question_number}",
            )
            self.button_green.config(state="disabled")
            self.button_red.config(state="disabled")

    def click_green(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def click_red(self):
        is_right = self.quiz.check_answer("False")
        self.give_feedback(is_right)  # option 2 of calling the f

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, self.get_next_question)
