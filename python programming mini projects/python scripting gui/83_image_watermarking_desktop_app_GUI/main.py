# A Desktop program where you can upload images and add a watermark.

from tkinter import Tk, Label, Canvas, PhotoImage, Entry, Button, filedialog
from tkinter import messagebox
from PIL import ImageTk
import os
from watermark_class import *

program_window = Tk()
program_window.minsize(width=500, height=400)
program_window.title("Image Watermark program")
program_window.config(padx=50, pady=50, bg="LightBlue1")
program_window.grid_rowconfigure(3, minsize=40)
program_window.grid_rowconfigure(4, minsize=40)

preview_width = 200
saved_img_path = None


## ---------------- FUNCTIONS -----------------------------------------
def reset():
    global saved_img_path, my_image
    entry_wmtext.delete(0, "end")
    entry_wmtext.insert(0, "Rainbow LTD")
    img_preview.config(image="")
    saved_img_path = None
    my_image = None


def upload_img(event=None):
    global my_image, img_preview, filename
    filename = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpeg *.jpg *.png *.gif")]
    )
    if filename:
        # global my_image
        my_image = Image.open(filename)
        print(f"Selected: {my_image}, Size: {my_image.size}")

        preview_image = my_image.copy()
        preview_image.thumbnail((preview_width, preview_image.height))
        preview = ImageTk.PhotoImage(preview_image)

        img_preview.config(image=preview)
        img_preview.image = preview

        return my_image


def add_wm():
    global saved_img_path
    if "my_image" not in globals():
        messagebox.showwarning("No image", "Please upload an image first.")
        return
    wm_img = Watermarking(image=my_image, text=entry_wmtext.get())
    wm_img.add_mark()
    saved_img_path = wm_img.save_img(filename)
    print("Saved as:", saved_img_path)
    messagebox.showinfo(
        title="Saved",
        message=f"Watermarked image saved at:\n{saved_img_path}",
    )
    return wm_img


def view_img():
    if not saved_img_path:
        messagebox.showwarning("No image", "Please upload an image first.")
        return
    try:
        img = Image.open(saved_img_path)
        img.show()
    except Exception as e:
        print("Error opening image:", e)


## -------------------------------- ELEMENTS --------------------------
label_empty = Label(bg="LightBlue1")
label_empty.grid(row=0, column=0)
label_empty = Label(bg="LightBlue1")
label_empty.grid(row=4, column=1)

window_canvas = Canvas(width=200, height=200, highlightthickness=0, bg="LightBlue1")

logo_path = os.path.join(curr_file_dir, "logo.png")
logo_img = PhotoImage(file=logo_path).subsample(3)  # scaling down by 3
window_canvas.create_image(100, 100, image=logo_img)
window_canvas.grid(row=0, column=1)

label_wmtext = Label(bg="LightBlue1")
label_wmtext.config(text="Watermark text:", padx=10, justify="right")
label_wmtext.grid(row=1, column=0, sticky="e", padx=10)
entry_wmtext = Entry()
entry_wmtext.config(width=35)
entry_wmtext.insert(0, "Rainbow LTD")
entry_wmtext.grid(row=1, column=1, sticky="ew")

label_empty = Label(bg="LightBlue1")
label_empty.grid(row=2, column=0)


button_reset = Button()
button_reset.config(
    text="Reset",
    activebackground="DodgerBlue3",
    activeforeground="white",
    justify="left",
    command=reset,
)
button_reset.grid(row=0, column=2, sticky="en")


button_upload = Button()
button_upload.config(
    text="Step 1: Upload image",
    activebackground="DodgerBlue3",
    activeforeground="white",
    command=upload_img,
)
button_upload.grid(row=1, column=2, sticky="ew")


button_add = Button()
button_add.config(
    text="Step 2: Add watermark",
    activebackground="DodgerBlue3",
    activeforeground="white",
    justify="left",
    command=add_wm,
)
button_add.grid(row=2, column=0, sticky="ew", ipady=15)


label_empty = Label(bg="LightBlue1")
label_empty.grid(row=3, column=0)


button_review = Button()
button_review.config(
    text="Step 3: Review image",
    activebackground="DodgerBlue3",
    activeforeground="white",
    command=view_img,
)
button_review.grid(row=4, column=0, sticky="ew", ipady=15)


img_frame = LabelFrame(program_window, text="Image preview")
img_frame.grid(row=2, column=1, rowspan=3, columnspan=2, sticky="nsew")

img_preview = Label(img_frame)
img_preview.config("", padx=10, justify="right")
img_preview.grid(sticky="nsew", padx=10, pady=10)


program_window.mainloop()
