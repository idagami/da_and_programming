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
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

with app.app_context():
    new_movie = Movie(
        title="Phone Booth",
        year=2002,
        description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
        rating=7.3,
        ranking=10,
        review="My favourite character was the caller.",
        img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg",
    )
    # db.session.add(new_movie) # commented after i ran it once
    # db.session.commit() # commented after i ran it once

with app.app_context():
    new_movie = Movie(
        title="Avatar The Way of Water",
        year=2022,
        description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
        rating=7.3,
        ranking=9,
        review="I liked the water.",
        img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg",
    )
    # db.session.add(new_movie)
    # db.session.commit()


class RateMovieForm(FlaskForm):
    new_rating = FloatField(label="New rating", validators=[DataRequired()])
    new_review = StringField(label="New review", validators=[DataRequired()])
    submit = SubmitField("Submit changes")


class AddMovieForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add movie")


@app.route("/")
def home():

    result = db.session.execute(db.select(Movie).order_by(Movie.rating.desc()))
    all_movies = result.scalars().all()
    for index, movie in enumerate(all_movies):
        movie.ranking = index + 1
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    with app.app_context():
        edit_form = RateMovieForm()
        movie_to_edit = db.get_or_404(Movie, movie_id)
        if request.method == "POST" and edit_form.validate_on_submit():
            new_rating = request.form["new_rating"]
            new_review = request.form["new_review"]
            movie_to_edit.rating = float(new_rating)
            movie_to_edit.review = new_review
            db.session.commit()
            return redirect(url_for("home"))

    return render_template("edit.html", movie=movie_to_edit, form=edit_form)


@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()

    return redirect(url_for("home"))


key = os.getenv("TMDB_ACCESS_TOKEN")
header = {"Authorization": f"Bearer {key}", "accept": "application/json"}

endpoint = "https://api.themoviedb.org/3/search/movie"
img_endpoint = "https://image.tmdb.org/t/p/original/"


@app.route("/add", methods=["GET", "POST"])
def add():
    add_form = AddMovieForm()
    if request.method == "POST" and add_form.validate_on_submit():
        title_entered = add_form.title.data.lower()
        response = requests.get(url=f"{endpoint}?query={title_entered}", headers=header)
        response.raise_for_status()
        data = response.json()["results"]
        movies_found = []
        for movie in data:
            movies_found.append(
                {
                    "tmdb_id": movie["id"],  # TMDB movie id
                    "title": movie["original_title"],
                    "year": movie.get("release_date", "")[
                        :4
                    ],  # included .get to avoid errors if they are missing.
                }
            )
            print(request.args.get("id"))
        return render_template("select.html", movies=movies_found)
    return render_template("add.html", add_form=add_form)


@app.route("/find")
def find_tmdb():
    tmdb_id = request.args.get("id")
    if not tmdb_id:
        return redirect(url_for("home"))

    endpoint3 = "https://api.themoviedb.org/3/movie/"
    response = requests.get(url=f"{endpoint3}/{tmdb_id}", headers=header)
    response.raise_for_status()
    data = response.json()

    year_tmdb = data["release_date"][:4]
    title_tmdb = data["original_title"]
    description_tmdb = data["overview"]
    img_url_tmdb = img_endpoint + data["poster_path"]

    new_movie = Movie(
        title=title_tmdb,
        year=year_tmdb,
        description=description_tmdb,
        rating=0.0,
        ranking=3,
        review="bla",
        img_url=img_url_tmdb,
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("edit", movie_id=new_movie.id))


if __name__ == "__main__":
    app.run(debug=True)
