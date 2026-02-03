import requests
import json
from flask import Flask, render_template
from dotenv import load_dotenv
import os
import random
import smtplib
from datetime import datetime as dt

## -------------- CONSTANTS ------------ ##

load_dotenv()
# loads variables from .env into os.environ (instead of loading them into my shell / cmd)

email = os.environ.get("my_email")
email_password = os.environ.get("my_password")

app = Flask(__name__)

## ------------ API set up ------------ ##

BOOKS_ENDPOINT = "https://api.potterdb.com/v1/books"
MOVIES_ENDPOINT = "https://api.potterdb.com/v1/movies"
SPELLS_ENDPOINT = "https://potterhead-api.vercel.app/api/spells"

response_books = requests.get(url=BOOKS_ENDPOINT)
response_mov = requests.get(url=MOVIES_ENDPOINT)
response_spel = requests.get(url=SPELLS_ENDPOINT)

# print(response.status_code)
response_books.raise_for_status()
response_mov.raise_for_status()
response_spel.raise_for_status()
data_books = response_books.json()
data_movies = response_mov.json()
data_spel = response_spel.json()

json_books = json.dumps(data_books, indent=2, ensure_ascii=False)
json_mov = json.dumps(data_movies, indent=2, ensure_ascii=False)
json_spel = json.dumps(data_spel, indent=2, ensure_ascii=False)

# print(json_spel)

## --------------- ROUTES --------------- ##


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/titles")
def titles():
    books = [
        {
            "title": "("
            + book["attributes"]["release_date"][:4]
            + ") "
            + book["attributes"]["title"],
            "cover": book["attributes"]["cover"],
        }
        for book in data_books["data"]
    ]
    movies = [
        {
            "title": "("
            + movie["attributes"]["release_date"][:4]
            + ") "
            + movie["attributes"]["title"],
            "cover": movie["attributes"]["poster"],
        }
        for movie in data_movies["data"]
    ]
    return render_template("titles.html", books=books, movies=movies)


@app.route("/spell")
def spell():
    spells_list = [
        spell["name"] + ":" + " " + spell["description"] for spell in data_spel
    ]
    random_spell = random.choice(spells_list)
    return render_template("spell.html", spell=random_spell)


def get_today_anniversaries():
    today = dt.now().date()
    matches = []

    for book in data_books["data"]:
        release_str = book["attributes"].get("release_date")
        if not release_str:
            continue

        release_date = dt.strptime(release_str, "%Y-%m-%d").date()

        if release_date.month == today.month and release_date.day == today.day:
            matches.append(book["attributes"]["title"])

    return matches


@app.route("/anniversary")
def anniversary():
    matches = get_today_anniversaries()
    return render_template("anniversary.html", matches=matches)


@app.route("/anniversary/send", methods=["POST"])
def send_anniversary_emails():
    matches = get_today_anniversaries()

    if not matches:
        return "No releases today. No emails sent."

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email, password=email_password)

        for title in matches:
            message = f"Happy anniversary! Today is the release of {title}!"
            connection.sendmail(
                from_addr=email,
                to_addrs=email,
                msg=f"Subject: Harry Potter Release Anniversary!\n\n{message}",
            )

    return f"Emails sent for: {matches}"


if __name__ == "__main__":
    app.run(debug=True)
