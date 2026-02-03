from flask import Flask, render_template, request
import wtforms_class
import os
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap5

load_dotenv()

app = Flask(__name__)
secret_key = os.environ["WTF_SECRET_KEY"]
app.config["SECRET_KEY"] = secret_key

bootstrap = Bootstrap5(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = wtforms_class.LoginForm()
    if request.method == "POST" and login_form.validate_on_submit():
        if (
            login_form.email.data == "admin@email.com"
            and login_form.password.data == "12345678"
        ):
            return render_template("success.html")
        else:
            return render_template("denied.html")
    return render_template("login.html", form=login_form)


if __name__ == "__main__":
    app.run(debug=True)
