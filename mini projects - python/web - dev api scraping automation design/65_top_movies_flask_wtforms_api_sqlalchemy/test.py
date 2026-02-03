from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests, os, json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap5(app)


class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///best-movies.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


key = os.getenv("TMDB_ACCESS_TOKEN")
header = {"Authorization": f"Bearer {key}", "accept": "application/json"}

endpoint1 = "https://api.themoviedb.org/3/search/movie?query=Jack+Reacher"
endpoint2 = "https://api.themoviedb.org/3/search/movie"
img_endpoint = "https://image.tmdb.org/t/p/original/"

# searched_movie = input("enter movie title: ").lower()

# # response = requests.get(url=endpoint1, headers=header)
# response = requests.get(url=f"{endpoint2}?query={searched_movie}", headers=header)
# # print(response)
# # print(response.status_code)
# response.raise_for_status()
# data = response.json()["results"]
# movies_found = []
# for movie in data:
#     movies_found.append(
#         {
#             "tmdb_id": movie["id"],  # TMDB movie id
#             "title": movie["original_title"],
#             "year": movie.get("release_date", "")[:4],
#             "description": movie.get("overview", ""),
#             "img_url": (
#                 img_endpoint + movie["poster_path"] if movie.get("poster_path") else ""
#             ),
#         }
#     )
#     print(movie["id"])

tmdb_id = int(input("enter tmdb id: "))

endpoint3 = "https://api.themoviedb.org/3/movie/"
response = requests.get(url=f"{endpoint3}/{tmdb_id}", headers=header)
response.raise_for_status()
data = response.json()
print(data)
print(json.dumps(data, indent=4))

year_tmdb = data["release_date"][:4]
title_tmdb = data["original_title"]
description_tmdb = data["overview"]
img_url_tmdb = img_endpoint + data["poster_path"]

print(year_tmdb)

with app.app_context():
    new_movie = Movie(
        title=title_tmdb,
        year=year_tmdb,
        description=description_tmdb,
        rating=0.0,
        ranking=10,
        review="",
        img_url=img_url_tmdb,
    )
    db.session.add(new_movie)
    db.session.commit()


list1 = [1, 2, 3, 4]
print(list1.index(3))
