from datetime import date
from flask import (
    Flask,
    abort,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request,
)
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import NewPostForm, NewUser, LoginForm, CommentForm
from flask_ckeditor.utils import cleanify
import smtplib, os
from dotenv import load_dotenv
from typing import List
from datetime import datetime as dt

load_dotenv()
my_email = os.getenv("GMAIL_APP_MAIL")
my_password = os.getenv("GMAIL_APP_PASSWORD")
smtp_address = os.getenv("GMAIL_SMTP_ADDRESS")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap5(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI", "sqlite:///posts.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


# CONFIGURE TABLES
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    posts = relationship(
        "BlogPost", back_populates="author"
    )  # creating relationship One-to-Many, one author-many posts
    comments = relationship("Comment", back_populates="comment_author")


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    author = relationship(
        "User", back_populates="posts"
    )  # It’s a Python property that automatically retrieves the User object for this blog post.
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comments = relationship("Comment", back_populates="post")


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    comment_author = relationship("User", back_populates="comments")
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog_posts.id"))
    post = relationship("BlogPost", back_populates="comments")


# we didn't create 'author' column becuz we can access this info by post.author.name.
# Otherwise it's a duplicate.

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)  # use this line if db has users
    # return User.query.get(int(user_id))  # use this line if db has no users


def admin_only(function):  # creating my own decorator
    @wraps(function)
    def wrapper_f(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)
        return function(*args, **kwargs)

    return wrapper_f


gravatar = Gravatar(  # creating profile picture - a random small img
    app=app,
    size=100,
    rating="g",
    default="retro",
    force_default=False,
    use_ssl=True,
    base_url=None,
)


@app.context_processor
def inject_now_year():
    return {"now_year": dt.today().year}


@app.route("/")
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route("/register", methods=["POST", "GET"])
def register():
    new_user_form = NewUser()
    if new_user_form.validate_on_submit():
        existing_user = db.session.execute(
            db.select(User).where(User.email == new_user_form.email.data)
        ).scalar()
        if existing_user:
            flash("User already exists. Please log in")
            return redirect(url_for("login"))
        else:
            hash_salt_password = generate_password_hash(
                new_user_form.password.data, method="pbkdf2", salt_length=8
            )
            new_user = User(
                email=new_user_form.email.data,
                name=new_user_form.name.data,
                password=hash_salt_password,
            )
            db.session.add(new_user)
            db.session.commit()
            session["name"] = new_user_form.name.data
            login_user(new_user)
            return redirect(url_for("get_all_posts"))
    return render_template("register.html", reg_form=new_user_form)


@app.route("/login", methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        result = db.session.execute(
            db.select(User).where(User.email == login_form.email.data)
        )
        user = result.scalar()
        if user:
            if check_password_hash(user.password, login_form.password.data):
                login_user(user)
                return redirect(url_for("get_all_posts"))
            else:
                flash("Wrong password. Please check correctness.")
                return redirect(url_for("login"))
        else:
            flash("Invalid email. Please check correctness or hit 'Register'.")
            return redirect(url_for("login"))
    return render_template("login.html", login_form=login_form)


@app.route("/logout")
def logout():
    logout_user()
    print("Logged out")
    return redirect(url_for("get_all_posts"))


@app.route("/post/<int:post_id>", methods=["POST", "GET"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    comment_form = None
    if current_user.is_authenticated:
        comment_form = CommentForm()
        if comment_form.validate_on_submit():
            new_comment = Comment(
                text=comment_form.body.data,
                comment_author=current_user,
                post=requested_post,
            )
            db.session.add(new_comment)
            db.session.commit()
            # return redirect(url_for("get_all_posts"))
            # return reload()
            return render_template("post.html", post=requested_post, form=comment_form)
    return render_template(
        "post.html", post=requested_post, current_user=current_user, form=comment_form
    )


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y"),
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = NewPostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body,
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact_section():
    if request.method == "GET":
        return render_template("contact.html", form_submitted=False)
    elif request.method == "POST":
        name_sent = request.form["input_name"]
        email_sent = request.form["input_email"]
        phone_sent = request.form["input_phone"]
        msg_sent = request.form["input_msg"]
        print(email_sent)
        # return f"<h1>Successfully sent your message</h1>" ## opens a new page with this msg

        with smtplib.SMTP(smtp_address, 587) as my_connection:
            my_connection.starttls()
            my_connection.login(user=my_email, password=my_password)
            my_connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=f"Subject: You've got new message!\n\nNew messaage received from your blog contact page:\nName: {name_sent}\nEmail: {email_sent}\nPhone: {phone_sent}\nMessage: {msg_sent}",
            )
            print("email sent")

        return render_template("contact.html", form_submitted=True)


# if __name__ == "__main__":
#     app.run(debug=True, port=5000)

if __name__ == "__main__":
    app.run(debug=False)
