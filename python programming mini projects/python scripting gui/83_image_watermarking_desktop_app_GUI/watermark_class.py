from tkinter import *
from PIL import Image, ImageFont, ImageDraw
import os

curr_file_dir = os.path.dirname(__file__)


class Watermarking:
    def __init__(self, image, text):
        self.image = image.copy()
        self.image = self.image.convert("RGBA")
        self.text = text

    def add_mark(self):
        global final_img
        width, height = self.image.size

        font_size = int(width * 0.6 // 5)

        try:
            font_path = os.path.join(curr_file_dir, "BRUSHSCI.TTF")
            font = ImageFont.truetype(font_path, font_size)
        except OSError:
            font = ImageFont.load_default()

        transparent_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw_layer = ImageDraw.Draw(transparent_layer)

        bbox = draw_layer.textbbox((0, 0), self.text, font=font)  # measure text size
        left, top, right, bottom = bbox
        text_width = right - left
        text_height = bottom - top

        x_text = (width - text_width) // 2
        y_text = (height - text_height) // 2

        draw_layer.text(
            (x_text, y_text), self.text, font=font, fill=(255, 255, 255, 40)
        )

        self.final_img = Image.alpha_composite(self.image, transparent_layer)
        self.final_img = self.final_img.convert("RGB")

        return self.final_img

    def save_img(self, filename):
        downloads_dir = os.path.join(os.path.dirname(filename), "downloads")
        os.makedirs(downloads_dir, exist_ok=True)  # create folder if it doesn't exist
        root, ext = os.path.splitext(
            os.path.basename(filename)
        )  # to not get the full path name
        new_name = f"{root}-wm{ext}"
        save_path = os.path.join(downloads_dir, new_name)
        self.final_img.save(save_path)
        return save_path
