from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, TimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField("Cafe name", validators=[DataRequired()])
    url = URLField(label="Location url", validators=[DataRequired(), URL()])
    open = TimeField(label="Opening time", validators=[DataRequired()])
    close = TimeField(label="Closing time", validators=[DataRequired()])
    coffee_rating = SelectField(
        label="Coffee rating",
        choices=["☕️☕️☕️☕️☕️", "☕️☕️☕️☕️", "☕️☕️☕️", "☕️☕️", "☕️", "✘"],
        validators=[DataRequired()],
    )
    wifi_rating = SelectField(
        label="Wifi strength rating",
        choices=["💪💪💪💪💪", "💪💪💪💪", "💪💪💪", "💪💪", "💪", "✘"],
        validators=[DataRequired()],
    )
    power_rating = SelectField(
        label="Power socket availability",
        choices=["🔌🔌🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌", "🔌🔌", "🔌", "✘"],
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cafes")
def cafes():
    with open("cafe-data.csv", newline="", encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=",")
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template("cafes.html", cafes=list_of_rows)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if request.method == "POST" and form.validate_on_submit():
        # print("True data")
        with open("cafe-data.csv", mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    form.cafe.data,
                    form.url.data,
                    form.open.data.strftime("%H:%M"),
                    form.close.data.strftime("%H:%M"),
                    form.coffee_rating.data,
                    form.wifi_rating.data,
                    form.power_rating.data,
                ]
            )
        return redirect(url_for("cafes"))
    return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
