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
import os, random
import text_templates_class as templates

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
label_font = (FONT_NAME, 20, "bold")
label_fg = "green"
type_sec = 180
timer = None

curr_file_dir = os.path.dirname(__file__)

program_window = Tk()
program_window.geometry("1200x700")
program_window.state("zoomed")
program_window.title("Typing test program")
program_window.config(padx=50, pady=50, bg=YELLOW)

program_window.grid_columnconfigure(0, weight=0)
program_window.grid_columnconfigure(1, weight=1)
program_window.grid_columnconfigure(2, weight=1)
program_window.grid_columnconfigure(3, weight=1)

program_window.grid_rowconfigure(0, weight=0)
program_window.grid_rowconfigure(1, weight=0)
program_window.grid_rowconfigure(2, weight=0)
program_window.grid_rowconfigure(3, weight=0)

program_window.resizable(False, False)


def start():
    chosen_text = random.choice(templates.texts)
    text_preview.delete("1.0", "end")
    text_preview.insert("1.0", chosen_text)
    entry_text.delete("1.0", "end")  # from line 1, char 0 to the end
    countdown(type_sec)
    return text_preview


def reset():
    global label_wpm, label_accuracy
    entry_text.delete("1.0", "end")
    text_preview.delete("1.0", "end")
    text_preview.insert(
        "1.0", "Once you click start, you'll have 2 minutes to type the text."
    )
    label_wpm.config(text="WPM: 0")


def countdown(count):
    if count > 0:
        global timer
        timer = program_window.after(1000, countdown, count - 1)
    else:
        messagebox.showinfo(
            title="Your time ran out",
            message=f"Click OK for result.",
        )
        typed_text = entry_text.get(
            "1.0", "end-1c"
        )  # "1.0" = first line, char 0; "end-1c" = exclude final newline
        num_chars = len(typed_text)
        result_wpm = int((num_chars / 5) / (type_sec / 60))
        label_wpm.config(text=f"WPM result:\n{result_wpm} WPM")
        return result_wpm


label_empty = Label(bg=YELLOW)
label_empty.grid(row=0, column=0)

button_start = Button()
button_start.config(
    text="Start",
    bg="blue2",
    fg="white",
    activebackground="white",
    activeforeground="DodgerBlue3",
    justify="left",
    command=start,
    height=2,
    width=10,
)
button_start.grid(row=1, column=0, sticky="en", pady=(0, 20))

button_reset = Button()
button_reset.config(
    text="Reset",
    activebackground="DeepSkyBlue3",
    activeforeground="white",
    justify="left",
    command=reset,
)
button_reset.grid(row=2, column=0, sticky="ne", pady=(150, 0))

window_canvas = Canvas(width=200, height=200, highlightthickness=0, bg=YELLOW)
logo_path = os.path.join(curr_file_dir, "logo.png")
logo_img = PhotoImage(file=logo_path).subsample(3)  # scaling down by 3
window_canvas.create_image(100, 100, image=logo_img)
window_canvas.grid(row=0, column=1, padx=20)


text_frame = LabelFrame(program_window, text="Text preview")
text_frame.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=20)
text_frame.grid_rowconfigure(0, weight=1)
text_frame.grid_columnconfigure(0, weight=1)


text_scroll = Scrollbar(text_frame, orient="vertical")
text_scroll.grid(row=0, column=1, sticky="ns")

text_preview = Text(
    text_frame,
    wrap="word",
    font=(FONT_NAME, 12),
    yscrollcommand=text_scroll.set,
    bg="white",
    padx=10,
    pady=10,
    height=20,
    width=50,
)
text_preview.insert(
    "1.0", "Once you click START, you'll have 3 minutes to type the text."
)
text_preview.grid(row=0, column=0, sticky="nsew")
text_scroll.config(command=text_preview.yview)
# Every Tkinter widget that can scroll vertically (Text, Listbox, Canvas) includes a built-in method named .yview
# It returns the current vertical view area and allows the scrollbar to move the text up and down.


entry_frame = LabelFrame(program_window, text="Type here")
entry_frame.grid(row=1, column=2, rowspan=2, sticky="nsew", padx=20)
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
    height=20,
    width=50,
)

entry_text.grid(row=0, column=0, sticky="nsew")
entry_scroll.config(command=entry_text.yview)


result_frame = LabelFrame(program_window, text="Results")
result_frame.grid(row=0, column=2, sticky="ew", padx=20, pady=(0, 10))
result_frame.grid_columnconfigure(0, weight=1)
result_frame.grid_columnconfigure(1, weight=1)

label_wpm = Label(
    result_frame,
    text="WPM: 0",
    font=label_font,
    fg=label_fg,
    bg=YELLOW,
)
label_wpm.grid(row=0, column=0, sticky="w", padx=(0, 10))

program_window.mainloop()
