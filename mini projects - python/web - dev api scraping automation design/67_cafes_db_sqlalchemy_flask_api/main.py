from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random as random

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        """Return model data as a dictionary"""
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record


@app.route("/random")
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    ## option 1
    # return jsonify(
    #     cafe={
    #         # "id": random_cafe.id,
    #         "name": random_cafe.name,
    #         "map_url": random_cafe.map_url,
    #         "img_url": random_cafe.img_url,
    #         "location": random_cafe.location,
    #         "amenities": {
    #             "seats": random_cafe.seats,
    #             "has_toilet": random_cafe.has_toilet,
    #             "has_wifi": random_cafe.has_wifi,
    #             "has_sockets": random_cafe.has_sockets,
    #             "can_take_calls": random_cafe.can_take_calls,
    #             "coffee_price": random_cafe.coffee_price,
    #         },
    #     }
    # )
    ## option 2
    # return jsonify(random_cafe.to_dict())
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def all_cafes():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    cafe_list = []
    for cafe in all_cafes:
        cafe_dict = cafe.to_dict()
        cafe_list.append(cafe_dict)
    return jsonify(cafes=cafe_list)


## option 1: path parameter - NOT preferred as is less flexible
# @app.route("/search/<location>")
# def search_cafe(location):
#     result = db.session.execute(db.select(Cafe).where(Cafe.location == location))
#     found_cafes = result.scalars().all()
#     if found_cafes:
#         return jsonify(results=[found_cafe.to_dict() for found_cafe in found_cafes])
#     else:
#         return (
#             jsonify(
#                 error={"Not Found": "Sorry, we don't have a cafe at that location."}
#             ),
#             404,
#         )


## option 2: query parameter - preferred in RESTful APIs
@app.route("/search")
def search_cafe():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    found_cafes = result.scalars().all()
    if found_cafes:
        return jsonify(results=[found_cafe.to_dict() for found_cafe in found_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, no cafe in such location."})


# HTTP POST - Create Record


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record


@app.route(
    "/update-name/<cafe_id>", methods=["PATCH", "GET"]
)  # this is the correct use of path parameters
def update_name(cafe_id):
    query_name = request.args.get("name")
    cafe_to_update = db.session.execute(
        db.select(Cafe).where(Cafe.id == cafe_id)
    ).scalar()
    if cafe_to_update is None:
        return jsonify(error={"Not Found": "No cafe with such id."}), 404
    else:
        cafe_to_update.name = query_name
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the name."}), 200


# HTTP DELETE - Delete Record


@app.route("/report-closed/<cafe_id>", methods=["DELETE", "GET"])
def delete_cafe(cafe_id):
    access_key = "MySecretKey"
    entered_key = request.args.get("key")
    cafe_to_delete = db.session.execute(
        db.select(Cafe).where(Cafe.id == cafe_id)
    ).scalar()
    if entered_key != access_key:
        return jsonify(error={"Access": "Invalid access key."}), 403
    if cafe_to_delete is None:
        return jsonify(error={"Not Found": "No cafe with such id."}), 404
    else:
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return (
            jsonify(response={"success": "Successfully deleted the cafe from db."}),
            200,
        )


if __name__ == "__main__":
    app.run(debug=True)
