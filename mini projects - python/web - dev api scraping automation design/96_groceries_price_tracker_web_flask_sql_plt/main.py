from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Numeric, Date
import os
from datetime import date
from dotenv import load_dotenv
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from forms import MultiProductForm, GraphFilterForm, SHOPS, ITEMS, CATEGORIES


load_dotenv()


app = Flask(__name__, static_url_path="", static_folder="static")
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
Bootstrap(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///groceries_db.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Product(db.Model):
    __tablename__ = "groceries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date(), nullable=False)
    shop: Mapped[str] = mapped_column(String(50), nullable=False)
    item: Mapped[str] = mapped_column(String(100), nullable=False)
    descr: Mapped[str] = mapped_column(String(200), nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    weight: Mapped[float] = mapped_column(Numeric(6, 2), nullable=True)
    units: Mapped[int] = mapped_column(Integer, nullable=True)
    cost: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    price_kg: Mapped[str] = mapped_column(Numeric(10, 2), nullable=True)
    price_unit: Mapped[str] = mapped_column(Numeric(10, 2), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def add_new():
    form = MultiProductForm()
    if form.validate_on_submit():
        for row in form.products:
            if not row.cost.data:
                continue

            price_kg = None
            price_unit = None
            if row.weight.data:
                price_kg = round((row.cost.data / row.weight.data) * 1000, 2)
            elif row.units.data:
                price_unit = round(row.cost.data / row.units.data, 2)
            new_product = Product(
                date=form.date.data,
                shop=form.shop.data,
                item=row.item.data,
                descr=row.descr.data,
                category=row.category.data,
                weight=row.weight.data,
                units=row.units.data,
                cost=row.cost.data,
                price_kg=price_kg,
                price_unit=price_unit,
            )
            db.session.add(new_product)
        db.session.commit()
        return redirect(url_for("add_new"))
    return render_template("add_products.html", form=form)


def filter_dataframe():
    cur_dir = os.path.dirname(__file__)
    db_path = os.path.join(cur_dir, "instance", "groceries_db.db")

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM groceries", conn)

    df["shop"] = df["shop"].str.lower().str.strip().str.replace(" ", "_")
    df["category"] = df["category"].str.lower().str.strip().str.replace(" ", "_")
    df["item"] = df["item"].str.lower().str.strip().str.replace(" ", "_")

    conn.close()

    form = GraphFilterForm()

    selected_filter_type = form.filter_type.data or "shop"

    if selected_filter_type == "shop":
        form.filter_value.choices = [(s, s) for s in SHOPS]
    elif selected_filter_type == "category":
        form.filter_value.choices = [(c[0], c[1]) for c in CATEGORIES]
    elif selected_filter_type == "item":
        form.filter_value.choices = [(i[0], i[1]) for i in ITEMS]

    if form.validate_on_submit() and form.filter_value.data:
        df = df[df[selected_filter_type] == form.filter_value.data]

    return df, form, selected_filter_type


@app.route("/graphs", methods=["GET", "POST"])
def graphs():
    graphs_dir = os.path.join(app.static_folder, "graphs")
    os.makedirs(graphs_dir, exist_ok=True)

    df, form, _ = filter_dataframe()

    by_date = df.groupby("date", as_index=False)[["cost"]].sum()

    graph_file = "grocery_cost.png"
    graph_path = os.path.join(graphs_dir, graph_file)

    plt.figure(figsize=(8, 5))
    by_date.plot(x="date", y="cost", marker="o")
    plt.xlabel("Date")
    plt.ylabel("Total Spent")
    plt.title("Grocery Cost Over Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(graph_path)
    plt.close()

    return render_template("graphs.html", graph_file=graph_file, form=form)


@app.route("/table", methods=["GET", "POST"])
def table():
    df, form, _ = filter_dataframe()

    return render_template(
        "table.html",
        form=form,
        rows=df.to_dict(orient="records"),
        columns=df.columns,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
