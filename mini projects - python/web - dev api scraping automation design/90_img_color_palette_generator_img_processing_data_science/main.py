from flask import Flask, render_template, request, send_from_directory
import colorgram, os
from matplotlib.colors import to_hex

app = Flask(__name__)

cur_file_dir = os.path.dirname(__file__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/uploads/<filename>")
def send_uploaded_img(filename=""):
    app.config["uploads"] = os.path.join(cur_file_dir, "uploads")
    return send_from_directory(app.config["uploads"], filename)


@app.route("/run", methods=["POST", "GET"])
def run():
    file = request.files.get("uplImage")
    num_colors = int(request.form.get("numColors"))
    if file:
        uploaded_img_path = os.path.join(cur_file_dir, "uploads", file.filename)
        os.makedirs(os.path.dirname(uploaded_img_path), exist_ok=True)
        file.save(uploaded_img_path)

        colors = colorgram.extract(uploaded_img_path, num_colors)
        color_palette = []

        for i in range(len(colors)):
            r = float(colors[i].rgb.r)
            g = float(colors[i].rgb.g)
            b = float(colors[i].rgb.b)
            rgb_tuple = (r, g, b)
            hex_color = to_hex([r / 255, g / 255, b / 255])
            color_proportion = round((colors[i].proportion * 100), 2)
            color_palette.append(
                {"rgb": rgb_tuple, "hex": hex_color, "proportion": color_proportion}
            )

        return render_template("index.html", c_palette=color_palette, img=file.filename)
    return "No file uploaded"


if __name__ == "__main__":
    app.run(debug=True)
