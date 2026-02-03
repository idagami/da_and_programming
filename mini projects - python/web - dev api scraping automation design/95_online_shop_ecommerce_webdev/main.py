from datetime import datetime, timezone
from flask import (
    Flask,
    abort,
    render_template,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
    session,
    request,
)

from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Numeric, DateTime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import NewProductForm, NewUserForm, LoginForm, NewOrderForm
from flask_ckeditor.utils import cleanify
import smtplib, os
from dotenv import load_dotenv
from slugify import slugify
from email.mime.text import MIMEText
import bleach
import stripe


load_dotenv()
my_email = os.getenv("GMAIL_APP_MAIL")
my_password = os.getenv("GMAIL_APP_PASSWORD")
smtp_address = os.getenv("GMAIL_SMTP_ADDRESS")

app = Flask(__name__, static_url_path="", static_folder="public")
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

PAYMENT_ENDPOINT = "https://api.stripe.com"
stripe.api_key = os.getenv("stripe_ak")
YOUR_DOMAIN = "http://127.0.0.1:5000"


## ----------------- CONFIGURE TABLES ------------------ ##
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(250))
    name: Mapped[str] = mapped_column(String(50))
    orders = relationship(
        "Order", back_populates="user"
    )  # creating relationship One-to-Many, one author-many orders


class Product(db.Model):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    price_old: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    price_new: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


class OrderItem(db.Model):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    # if 'relationship', use '=', if MApped, use ':'
    order = relationship("Order", back_populates="items")
    product = relationship("Product")


class Order(db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    shipping_address: Mapped[str] = mapped_column(String(250), nullable=False)
    total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(50))


with app.app_context():
    db.create_all()

## --------------- FUNCTIONS and ROUTES ------------ ##


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def admin_only(function):  # creating my own decorator
    @wraps(function)
    def wrapper_f(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)
        return function(*args, **kwargs)

    return wrapper_f


@app.route("/")
def home():
    result = db.session.execute(db.select(Product))
    products = result.scalars().all()
    return render_template("index.html", all_products=products)


@app.route("/register", methods=["POST", "GET"])
def register():
    new_user_form = NewUserForm()
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
            return redirect(url_for("home"))
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
                return redirect(url_for("home"))
            else:
                flash("Wrong password. Please check correctness.")
                return redirect(url_for("login"))
        else:
            flash("Invalid email. Please check correctness or hit 'Register'.")
            return redirect(url_for("login"))
    return render_template("login.html", login_form=login_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("cart", None)  # clearing session cart on logout
    list(get_flashed_messages())  # emptying msg list if any stored
    return redirect(url_for("home"))


@app.route("/contact", methods=["GET", "POST"])
def contact_section():
    if request.method == "POST":
        name_sent = request.form.get("input_name")
        email_sent = request.form.get("input_email")
        phone_sent = request.form.get("input_phone")
        msg_sent = request.form.get("input_msg")

        try:
            with smtplib.SMTP(smtp_address, 587) as connection:
                connection.starttls()
                connection.login(my_email, my_password)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=my_email,
                    msg=(
                        "Subject: New Contact Message\n\n"
                        f"Name: {name_sent}\n"
                        f"Email: {email_sent}\n"
                        f"Phone: {phone_sent}\n"
                        f"Message:\n{msg_sent}"
                    ),
                )
        except Exception as e:
            flash("Failed to send message. Please try again later.")
            return redirect(url_for("contact_section"))

        return render_template("contact.html", form_submitted=True)

    return render_template("contact.html", form_submitted=False)


@app.route("/new-product", methods=["GET", "POST"])
@admin_only
def add_new_product():
    form = NewProductForm()
    if form.validate_on_submit():
        slug_value = slugify(form.name.data)
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            img_url=form.img_url.data,
            slug=slug_value,
            stock=form.stock.data,
            price_old=form.price_old.data,
            price_new=form.price_new.data,
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add-product.html", form=form)


@app.route("/adding_to_cart/<int:product_id>", methods=["POST"])
def adding_to_cart(product_id):
    quantity = int(request.form.get("quantity", 1))
    cart = session.get("cart", [])  # Cart = temporary (session)
    # check if product already in cart
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            break
    else:
        cart.append({"product_id": product_id, "quantity": quantity})
    session["cart"] = cart
    flash("Product added to cart!")
    return redirect(url_for("home"))


@app.route("/remove-from-cart/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", [])
    cart = [item for item in cart if item["product_id"] != product_id]
    session["cart"] = cart
    flash("Item removed from cart.")
    return redirect(url_for("show_cart"))


@app.route("/cart")
def show_cart():
    cart = session.get("cart", [])
    products_in_cart = []
    total = 0
    for item in cart:
        product = Product.query.get(item["product_id"])
        if product:
            subtotal = float(product.price_new) * item["quantity"]
            total += subtotal
            products_in_cart.append(
                {"product": product, "quantity": item["quantity"], "subtotal": subtotal}
            )
    return render_template("show-cart.html", products=products_in_cart, total=total)


@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    form = NewOrderForm()
    cart = session.get("cart", [])
    if not cart:
        flash("Your cart is empty!")
        return redirect(url_for("home"))

    if form.validate_on_submit():
        plain_address = bleach.clean(
            form.shipping_address.data, tags=[], strip=True
        )  # removes html tags that address text come embedded in
        total = 0
        new_order = Order(
            user_id=current_user.id,
            shipping_address=plain_address,
            status="Pending",  # mark as pending until Stripe confirms
            total=0,
        )
        db.session.add(new_order)
        db.session.flush()

        for item in cart:
            product = Product.query.get(item["product_id"])
            if item["quantity"] > product.stock:
                flash(f"Not enough stock for {product.name}")
                return redirect(url_for("show_cart"))

            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=item["quantity"],
                price=float(product.price_new),
            )
            product.stock -= item["quantity"]
            total += float(product.price_new) * item["quantity"]
            db.session.add(order_item)

        new_order.total = total
        db.session.commit()
        session["cart"] = []

        # Create Stripe session
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "ils",
                            "product_data": {"name": f"Order #{new_order.id}"},
                            "unit_amount": int(new_order.total * 100),
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                metadata={"order_id": str(new_order.id)},
                success_url=YOUR_DOMAIN + f"/order-confirmation/{new_order.id}",
                cancel_url=YOUR_DOMAIN + f"/checkout",
            )
        except Exception as e:
            flash(f"Stripe error: {e}")
            return redirect(url_for("checkout"))

        return redirect(checkout_session.url, code=303)

    return render_template("checkout.html", form=form)


@app.route("/create-checkout-session/<int:order_id>")
@login_required
def create_checkout_session(order_id):  # handling Stripe system
    order = Order.query.get_or_404(order_id)

    if order.user_id != current_user.id:
        abort(403)

    if order.status != "Pending":
        flash("Order already paid.")
        return redirect(url_for("home"))

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "ils",
                        "product_data": {"name": f"Order #{order.id}"},
                        "unit_amount": int(
                            order.total * 100
                        ),  # * 100 becuz currency 'ils' is counted in agorot
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            metadata={"order_id": str(order.id)},
            success_url=YOUR_DOMAIN + f"/order-confirmation/{order.id}",
            cancel_url=YOUR_DOMAIN + f"/my-orders",
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url)


def send_order_confirmation_email(order):
    user = order.user
    plain_address = bleach.clean(
        order.shipping_address, tags=[], strip=True
    )  # removes html tags that address text come embedded in

    subject = f"Order #{order.id} Confirmation"
    body = f"Hi {user.name},\nThank you for your order!\nOrder ID: #{order.id}\nTotal: ILS {order.total}\nShipping address: {plain_address}\nStatus: {order.status}."

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = my_email
    msg["To"] = user.email
    msg["Bcc"] = my_email

    try:
        with smtplib.SMTP(smtp_address, 587) as connection:
            connection.starttls()
            connection.login(my_email, my_password)
            connection.send_message(msg)
    except Exception as e:
        print(f"Email error: {e}")


@app.route("/order-confirmation/<int:order_id>")
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        abort(403)

    if order.status != "Fake-paid":
        order.status = "Fake-paid"
        db.session.commit()
        send_order_confirmation_email(order)

    return render_template("order_confirmation.html", order=order)


@app.route("/my-orders")
@login_required
def my_orders():
    orders = (
        Order.query.filter_by(user_id=current_user.id).order_by(Order.date.desc()).all()
    )
    return render_template("my_orders.html", orders=orders)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
