from tkinter import *  # type: ignore
import os

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    global timer, reps
    window_program.after_cancel(timer)  # type: ignore # to cancel previously set timer
    label_title.config(text="Timer", fg=GREEN)
    my_canvas.itemconfig(timer_text, text="00:00")
    label_tick.config(text="")
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    global reps
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    reps += 1
    window_program.bell()  # making the sound once the timer resets to next rep
    # if reps in (1, 3, 5, 7):
    #     countdown(work_sec)
    # if reps in (2, 4, 6):
    #     countdown(short_break_sec)
    # if reps == 8:
    #     countdown(long_break_sec)
    # more proper way to calculate with %, as during the study day we will have more than
    # 8 reps, they will restart: after 8 will be 1 etc.
    if reps % 8 == 0:
        countdown(long_break_sec)
        label_title.config(text="Long break now", fg=RED)
    elif reps % 2 == 0:
        countdown(short_break_sec)
        label_title.config(text="Short break", fg=PINK)
    else:
        countdown(work_sec)
        label_title.config(text="Study hard!", fg=GREEN)
        current_text = label_tick.cget("text")
        label_tick.config(text=current_text + "✔")


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def countdown(count):
    count_min = int(count / 60)
    count_sec = count % 60
    my_canvas.itemconfig(
        timer_text,
        text=f"{count_min:02d}" + ":" + f"{count_sec:02d}",
    )  # special method to edit the canvas components (component name, parameter to change)
    # # option 2 to make countdown elements of 2 digits always
    # if count_min < 10:
    #     count_min = f"0{count_min}"
    # if count_sec < 10:
    #     count_sec = f"0{count_sec}"
    # my_canvas.itemconfig(timer_text, text = f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window_program.after(
            1000, countdown, count - 1
        )  # 1000 ms = 1 second. *args paramenter is argument for the function
    else:  # if countdown <= 0 restart timer again (adds reps and enters next session)
        start_timer()


# ---------------------------- UI SETUP ------------------------------- #

window_program = Tk()
window_program.title("Pomodoro")
# window_progam.minsize(width=400, height=400)
window_program.config(padx=100, pady=50, bg=YELLOW)


label_empty = Label()
label_empty.grid(column=0, row=0)

label_title = Label()
label_title.config(text="Timer", font=(FONT_NAME, 50), fg=GREEN, bg=YELLOW)
label_title.grid(column=1, row=0)

my_canvas = Canvas(
    width=200, height=224, highlightthickness=0
)  # we want to put tomato png on canvas, so size should be similar to png size, try keep even numbers
# highlightthickness gets rid of border

cur_file_dir = os.path.dirname(__file__)
tomato_path = os.path.join(cur_file_dir, "tomato.png")
tomato_img = PhotoImage(file=tomato_path)
my_canvas.create_image(100, 112, image=tomato_img)  # want my image to be in the middle
timer_text = my_canvas.create_text(
    100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold")
)  # fill is the color of text
my_canvas.config(bg=YELLOW)
my_canvas.grid(column=1, row=1)

button_start = Button()
button_start.config(
    text="Start", bg="white", command=start_timer
)  # Button command must be a callable with no arguments
button_start.grid(column=0, row=2)

button_reset = Button()
button_reset.config(text="Reset", bg="white", command=reset_timer)
button_reset.grid(column=2, row=2)

label_tick = Label()
label_tick.config(text="", fg=GREEN, bg=YELLOW, font=("Arial", 17, "bold"))
label_tick.grid(column=1, row=3)


window_program.mainloop()  # is listening, when user clicks start, start_timer runs
