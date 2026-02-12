from tkinter import Tk, Canvas, PhotoImage, Button
import requests, os


data_json = {}
timer1 = None
cur_file_dir = os.path.dirname(__file__)


def next_joke():
    global data_json
    response = requests.get(url="https://v2.jokeapi.dev/joke/Any?type=twopart")
    response.raise_for_status()
    data_json = response.json()
    question = data_json["setup"]
    canvas.itemconfig(joke_text, text=question)


def get_answer():
    global timer1
    answer = data_json["delivery"]
    canvas.itemconfig(joke_text, text=answer)
    timer1 = window.after(2000, func=emoji_jump)


def emoji_jump():
    canvas.itemconfig(emoji_text, text="😁")


window = Tk()
window.title("Joke for you!")
window.config(padx=50, pady=50)

canvas = Canvas(width=300, height=414)
bg_img_path = os.path.join(cur_file_dir, "images", "background.png")
background_img = PhotoImage(file=bg_img_path)
canvas.create_image(150, 207, image=background_img)
joke_text = canvas.create_text(
    150, 207, width=250, font=("Arial", 20, "bold"), fill="white"
)
emoji_text = canvas.create_text(
    230, 50, text="", font=("Arial", 50, "bold"), fill="white"
)
canvas.grid(row=0, column=0, rowspan=2)

question_mark_path = os.path.join(cur_file_dir, "images", "download.png")
question_img = PhotoImage(file=question_mark_path)
question_button = Button(
    image=question_img, highlightthickness=0, command=get_answer, bg="white"
)
question_button.grid(row=0, column=1)

next_path = os.path.join(cur_file_dir, "images", "next.png")
next_img = PhotoImage(file=next_path)
next_button = Button(
    image=next_img, highlightthickness=0, command=next_joke, bg="white"
)
next_button.grid(row=1, column=1)

next_joke()

window.mainloop()
