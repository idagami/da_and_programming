import os, random
from tkinter import Tk, Button, Canvas, PhotoImage
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
current_file_directory = os.path.dirname(__file__)

##------------- file paths -------------- ##

front_img_path = os.path.join(
    current_file_directory,
    "images",
    "card_front.png",
)

back_img_path = os.path.join(
    current_file_directory,
    "images",
    "card_back.png",
)

right_img_path = os.path.join(
    current_file_directory,
    "images",
    "right.png",
)

wrong_img_path = os.path.join(
    current_file_directory,
    "images",
    "wrong.png",
)

try:
    cards_data_path = os.path.join(
        current_file_directory,
        "cards_to_learn.csv",
    )
    pd.read_csv(cards_data_path)
except FileNotFoundError:
    cards_data_path = os.path.join(
        current_file_directory,
        "he_en_cards_data.csv",
    )

new_file_path = os.path.join(
    current_file_directory,
    "cards_to_learn.csv",
)

cards_data = pd.read_csv(cards_data_path, encoding="utf-8", sep=",", header=0)
cards_data_df = pd.DataFrame(cards_data)
cards_data_df.rename(columns={"he_word": "Hebrew", "en_word": "English"}, inplace=True)
cards_list_of_dict = cards_data_df.to_dict(orient="records")

current_card = {}

##------------ functions ---------##


def new_card():
    global current_card, flip_timer
    window_program.after_cancel(flip_timer)  # type: ignore
    current_card = random.choice(cards_list_of_dict)
    my_canvas.itemconfig(canvas_img, image=front_img)
    my_canvas.itemconfig(title_text, text="Hebrew", fill="black")
    my_canvas.itemconfig(word_text, text=current_card["Hebrew"], fill="black")
    flip_timer = window_program.after(4000, func=flip_card)
    # print(len(cards_list_of_dict))


def flip_card():
    my_canvas.itemconfig(canvas_img, image=back_img)
    my_canvas.itemconfig(title_text, text="English", fill="white")
    my_canvas.itemconfig(word_text, text=current_card["English"], fill="white")


def press_known():
    cards_list_of_dict.remove(current_card)
    upd_cards_df = pd.DataFrame(cards_list_of_dict)
    upd_cards_df.to_csv(
        new_file_path, index=False, encoding="utf-8-sig"
    )  # index=False tells to not save indexes which are accumulating on every run
    new_card()


def press_unknown():
    new_card()


##------------- UI -------------- ##

window_program = Tk()
window_program.title("Flashy cards")
window_program.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window_program.after(4000, func=flip_card)

my_canvas = Canvas(width=800, height=526, highlightthickness=0)
front_img = PhotoImage(file=front_img_path)
back_img = PhotoImage(file=back_img_path)
canvas_img = my_canvas.create_image(400, 263, image=front_img)
my_canvas.config(bg=BACKGROUND_COLOR)

title_text = my_canvas.create_text(400, 150, fill="black", font=("Arial", 40, "italic"))
# # cards_data_df["he_correct"] = cards_data_df["he_word"].apply(lambda x: x[::-1]) # reversing order of letters
word_text = my_canvas.create_text(400, 263, fill="black", font=("Arial", 60, "bold"))
my_canvas.grid(column=0, row=1, columnspan=2)

right_img = PhotoImage(file=right_img_path)
wrong_img = PhotoImage(file=wrong_img_path)

button_right = Button(image=right_img)
button_right.config(bg=BACKGROUND_COLOR, command=press_known)
button_right.grid(column=1, row=2)

button_wrong = Button(image=wrong_img)
button_wrong.config(bg=BACKGROUND_COLOR, command=press_unknown)
button_wrong.grid(column=0, row=2)

new_card()

window_program.mainloop()
