from tkinter import Tk, Label, Canvas, PhotoImage, Entry, Button
from tkinter import messagebox  # is a module, not class
import random, os
from data_for_password import *

# # ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    global letters, cap_letter, numbers, symbols
    part1 = random.choices(letters, k=5)
    part2 = random.choices(cap_letter, k=2)
    part3 = random.choices(numbers, k=3)
    part4 = random.choices(symbols, k=1)
    list_password = part1 + part2 + part3 + part4
    random.shuffle(list_password)  # do not assign to a variable
    password = "".join(list_password)
    entry_password.delete(0, "end")
    entry_password.insert(0, password)


# # ---------------------------- SAVE PASSWORD ------------------------------- #

curr_file_dir = os.path.dirname(__file__)
hasla_path = os.path.join(curr_file_dir, "hasla.txt")


def save_info():
    global secure_password
    website = entry_web.get()
    secure_password = entry_password.get()
    email_user = entry_user.get()
    text_to_write = f"{website} | {secure_password} | {email_user}"
    if (
        not website or not secure_password or not email_user
    ):  # checks for string = "". if website is None doesnt check for ""
        messagebox.showwarning(title="Error", message="Some fields are empty")
        return  # when Python hits return, it jumps out of the function and never executes the code below it.
        # Or alternatively could have added else statement and indented all below text under it
    if len(entry_password.get()) < 10:
        label_status.config(
            text="Not saved ✘. Enter more secure password.\nUse 'Generate password' button for help.",
            fg="red",
        )
    else:
        is_ok = messagebox.askokcancel(
            title=website,
            message=f"Details enetered:\nwebsite: {website},\nemail: {email_user},\nPassword: {secure_password}\nIs it OK to save?",
        )
        if is_ok == True:
            with open(hasla_path, mode="a") as passwords_file:
                passwords_file.write(f"{str(text_to_write)}\n")
            label_status.config(
                text="Saved ✔. Password copied to clipboard", fg="green"
            )
            copy_entry_to_clipboard(entry_password)
            entry_web.delete(0, "end")
            entry_user.delete(0, "end")
            entry_password.delete(0, "end")
            entry_web.focus()
            entry_user.insert(0, "irena@gmail.com")


def copy_entry_to_clipboard(entry_password):
    text_to_copy = entry_password.get()
    window_program.clipboard_clear()  # Clear any existing content in the clipboard
    window_program.clipboard_append(
        text_to_copy
    )  # Append the Entry's text to the clipboard
    window_program.update()  # Update the clipboard to ensure the content is available


# # ---------------------------- UI SETUP ------------------------------- #

window_program = Tk()
# window_program.minsize(width=240, height=240)
window_program.title("Password Manager")
window_program.config(padx=50, pady=50)

# --- configure grid ---
window_program.grid_columnconfigure(0, weight=0)  # labels
window_program.grid_columnconfigure(
    1, weight=1
)  # Column 1 (the entry column) expands (weight=1), so all entries take the same width.
window_program.grid_columnconfigure(
    2, weight=0
)  # The Add button spans columns 1 and 2, so its width = exactly the combined width of the entries + generate button.

label_empty = Label()
label_empty.grid(row=0, column=0)

label_empty = Label()
label_empty.grid(row=4, column=1)

my_canvas = Canvas(width=200, height=200, highlightthickness=0)

logo_path = os.path.join(curr_file_dir, "logo.png")
logo_img = PhotoImage(file=logo_path)
my_canvas.create_image(100, 100, image=logo_img)
# my_canvas.config(bg="white")
my_canvas.grid(column=1, row=0)

label_web = Label()
label_web.config(text="Website:")
label_web.grid(row=1, column=0, sticky="e", padx=10)

label_user = Label()
label_user.config(text="Email / Username:", padx=10, justify="right")
label_user.grid(row=2, column=0, sticky="e", padx=10)

label_password = Label()
label_password.config(text="Password:", padx=10, justify="right")
label_password.grid(row=3, column=0, sticky="e", padx=10)

label_status = Label()
label_status.config(text="")
label_status.grid(row=5, column=1, columnspan=2, sticky="w")

entry_web = Entry()
entry_web.config(justify="left")
entry_web.focus()  # cursor on the entry from the start
entry_web.grid(
    row=1, column=1, columnspan=2, sticky="ew"
)  # "ew" → stick to both left and right, so the widget expands horizontally to fill the cell

entry_user = Entry()
entry_user.config(width=35)
entry_user.insert(
    0, "irena@gmail.com"
)  # 0 => insert piece of text at 0th character (very beginning)
entry_user.grid(row=2, column=1, columnspan=2, sticky="ew")

entry_password = Entry()
entry_password.config(justify="left")  # Entry.width = number of characters that fit
entry_password.grid(
    row=3, column=1, sticky="ew", padx=(0, 5)
)  # padx is the horizontal padding inside the grid cell.
# You can give it a single number, e.g. padx=5, which adds 5 pixels both left and right.
# Or you can give a tuple (left, right) to pad each side differently.

button_generate = Button()
button_generate.config(
    text="Generate password",
    activebackground="grey",
    activeforeground="white",
    command=generate_password,
)
button_generate.grid(row=3, column=2, sticky="ew")

button_add = Button()
button_add.config(
    text="Add",
    # Button.width = number of text units
    activebackground="grey",
    activeforeground="white",
    justify="left",
    command=save_info,
)
button_add.grid(row=4, column=1, columnspan=2, sticky="ew")

window_program.mainloop()
