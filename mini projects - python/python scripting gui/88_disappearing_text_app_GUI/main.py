from tkinter import (
    Tk,
    Label,
    Canvas,
    PhotoImage,
    Button,
    LabelFrame,
    Scrollbar,
    Text,
)
from tkinter import messagebox
import os

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#dadd87"
FONT_NAME = "Courier"
wait_msec = 2000
countdown_sec = 10
countdown_timer = None
wait_timer = None

curr_file_dir = os.path.dirname(__file__)

##---------FUNCTIONS------------##


def countdown(count):
    global countdown_timer, wait_timer
    if count > 0:
        countdown_counter.config(text=count)
        countdown_timer = program_window.after(1000, countdown, count - 1)
        if count == 5:
            program_window.config(bg=YELLOW)
            window_canvas.config(bg=YELLOW)
            label_words.config(bg=YELLOW)
            words_counter.config(bg=YELLOW)
            label_countdown.config(bg=YELLOW)
            countdown_counter.config(bg=YELLOW)
            label_empty2.config(bg=YELLOW)
        if count == 3:
            program_window.config(bg=PINK)
            window_canvas.config(bg=PINK)
            label_words.config(bg=PINK)
            words_counter.config(bg=PINK)
            label_countdown.config(bg=PINK)
            countdown_counter.config(bg=PINK)
            label_empty2.config(bg=PINK)

    else:
        messagebox.showinfo(
            title="Your time ran out",
            message=f"Text is lost.",
        )
        program_window.config(bg=RED)
        entry_text.delete("1.0", "end")
        countdown_timer = None
        wait_timer = None
        program_window.config(bg=GREEN)
        window_canvas.config(bg=GREEN)
        label_words.config(bg=GREEN)
        words_counter.config(bg=GREEN)
        label_countdown.config(bg=GREEN)
        countdown_counter.config(bg=GREEN)
        label_empty2.config(bg=GREEN)


def key_release(event):  # must keep argument evenif not used
    global wait_timer, countdown_timer, words_counter
    my_text = entry_text.get("1.0", "end-1c")
    words = len([word for word in my_text.split() if word.strip() != ""])
    words_counter.config(text=words)
    if wait_timer:
        program_window.after_cancel(wait_timer)
        wait_timer = None
    if countdown_timer:
        program_window.after_cancel(countdown_timer)
        countdown_timer = None
    wait_timer = program_window.after(wait_msec, lambda: countdown(countdown_sec))


##-----------ELEMENTS----------##

program_window = Tk()
program_window.geometry("800x600")
program_window.title("Disappearing text program")
program_window.config(padx=50, pady=50, bg=GREEN)

window_canvas = Canvas(width=200, height=200, highlightthickness=0, bg=GREEN)
logo_path = os.path.join(curr_file_dir, "logo.png")
logo_img = PhotoImage(file=logo_path).subsample(3)
window_canvas.create_image(100, 100, image=logo_img)
window_canvas.grid(row=0, column=0)

entry_frame = LabelFrame(program_window, text="Type here")
entry_frame.grid(row=0, column=1, rowspan=6, sticky="nsew", padx=20)
entry_frame.grid_rowconfigure(0, weight=1)
entry_frame.grid_columnconfigure(0, weight=1)

entry_scroll = Scrollbar(entry_frame, orient="vertical")
entry_scroll.grid(row=0, column=1, sticky="ns")

entry_text = Text(
    entry_frame,
    font=(FONT_NAME, 12),
    yscrollcommand=entry_scroll.set,
    bg="white",
    padx=10,
    pady=10,
    wrap="word",
    height=26,
    width=44,
)

entry_text.grid(row=0, column=0, sticky="nsew")
entry_scroll.config(command=entry_text.yview)

label_words = Label(bg=GREEN, text="Words")
label_words.grid(row=1, column=0)

words_counter = Label(bg=GREEN, font=(FONT_NAME, 18, "bold"))
words_counter.grid(row=2, column=0)

label_empty2 = Label(bg=GREEN)
label_empty2.grid(row=3, column=0)

label_countdown = Label(bg=GREEN, text="Countdown")
label_countdown.grid(row=4, column=0)

countdown_counter = Label(bg=GREEN)
countdown_counter.grid(row=5, column=0)

##----------FUNCTIONALIITY-------##

entry_text.bind("<KeyRelease>", key_release)

entry_text.focus_set()

program_window.mainloop()
