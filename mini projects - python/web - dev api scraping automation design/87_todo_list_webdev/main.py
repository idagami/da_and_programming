from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

tasks = ["Buy groceries", "Complete coding tutorial", "Walk the dog"]


# Todo TABLE Configuration
class Todo(db.Model):
    task_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(200))
    complete: Mapped[bool] = mapped_column(Boolean)
    category: Mapped[str] = mapped_column(String(50))

    def to_dict(self):
        """Return model data as a dictionary"""
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


tasks = ["Buy groceries", "Complete coding tutorial", "Walk the dog"]

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/todo")
def todo():
    result = db.session.execute(db.select(Todo).where(Todo.category == "custom"))
    all_tasks = result.scalars().all()
    return render_template("todo.html", tasks=all_tasks)


@app.route("/add", methods=["POST"])
def add_task():
    new_task_text = request.form.get("newTask")
    if new_task_text:
        new_task = Todo(text=new_task_text, category="custom", complete=False)
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for("todo"))


@app.route("/checklists")
def checklists():
    return render_template("checklists.html", tasks=None, selected_category=None)


@app.route("/checklist/<category>")
def open_checklist(category):
    result = db.session.execute(db.select(Todo).where(Todo.category == category))
    tasks = result.scalars().all()
    return render_template("checklists.html", tasks=tasks, selected_category=category)


@app.route("/add/<category>", methods=["POST"])
def add_task_category(category):
    new_task_text = request.form.get("newTask")
    if new_task_text:
        new_task = Todo(text=new_task_text, category=category, complete=False)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for("open_checklist", category=category))


@app.route("/complete", methods=["POST"])
def complete_task():
    completed_task_id = request.form.getlist(
        "taskCheckbox"
    )  # always returns a list, even if 1 value
    for task_id in completed_task_id:
        task = db.session.get(Todo, int(task_id))
        if task:
            task.complete = True
            db.session.commit()
    return redirect(request.referrer)


@app.route("/delete", methods=["POST"])
def delete_task():
    task_id = request.form.get("task_id")
    if task_id:
        task = db.session.get(Todo, int(task_id))
        if task:
            db.session.delete(task)
            db.session.commit()
    return redirect(request.referrer)


@app.route("/calendar")
def calendar():
    return render_template("calendar.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
