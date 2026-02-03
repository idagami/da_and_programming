from tkinter import Tk, Label, Button, Entry, Radiobutton, IntVar

window_program = Tk()
window_program.minsize(width=400, height=200)
window_program.title("Currency coverter")
window_program.config(padx=10, pady=10)


def calculate():
    if my_radio_state.get() == 1:
        result = round(float(entry_comp.get()) * 3.7, 2)
        label_original.config(text="USD")
        label_into.config(text="NIS")
    elif my_radio_state.get() == 2:
        result = round(float(entry_comp.get()) / 3.7, 2)
        label_original.config(text="NIS")
        label_into.config(text="USD")
    return label_result.config(text=result)


entry_comp = Entry()
entry_comp.grid(column=2, row=1, padx=10, pady=0)

label_original = Label()
label_original.config(text="USD", font=("Arial", 15, "normal"))
label_original.grid(column=3, row=1, padx=10, pady=10)

label_into = Label()
label_into.config(text="NIS", font=("Arial", 15, "normal"))
label_into.grid(column=3, row=2)

label_text = Label()
label_text.config(text="is equal to", font=("Arial", 10, "normal"))
label_text.grid(column=1, row=2)

label_result = Label()
label_result.config(text="0", font=("Arial", 15, "bold"))
label_result.grid(column=2, row=2, padx=10, pady=10)

button_calculate = Button()
button_calculate.config(
    text="Calculate",
    font=("Arial", 15, "italic"),
    activeforeground="green",
    command=calculate,
)

button_calculate.grid(column=2, row=3)


def radiobutton_selected():
    print(my_radio_state.get())


my_radio_state = IntVar()
my_radiobutton1 = Radiobutton(
    text="USD to NIS", value=1, variable=my_radio_state, command=radiobutton_selected
)
my_radiobutton2 = Radiobutton(
    text="NIS to USD", value=2, variable=my_radio_state, command=radiobutton_selected
)


my_radiobutton1.grid(column=0, row=0)
my_radiobutton2.grid(column=0, row=1)


window_program.mainloop()
