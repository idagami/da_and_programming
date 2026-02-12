from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    FloatField,
    IntegerField,
    SelectField,
)
from wtforms.validators import DataRequired, URL, Email, Length
from flask_ckeditor import CKEditorField


class NewProductForm(FlaskForm):
    name = StringField("Product Title", validators=[DataRequired()])
    description = CKEditorField("Description", validators=[DataRequired()])
    img_url = StringField("Product Image URL", validators=[DataRequired(), URL()])
    price_old = FloatField("Product Old Price", validators=[DataRequired()])
    price_new = FloatField("Product New Price", validators=[DataRequired()])
    stock = IntegerField("Available Stock", validators=[DataRequired()])
    submit = SubmitField("Submit Product")


class NewOrderForm(FlaskForm):
    shipping_address = CKEditorField("Shipping address", validators=[DataRequired()])
    payment_method = SelectField(
        "Payment Method", choices=[("card", "Card"), ("paypal", "PayPal")]
    )
    submit = SubmitField("Proceed to payment")


class NewUserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


# class CommentForm(FlaskForm):
#     body = CKEditorField("New comment", validators=[DataRequired()])
#     submit = SubmitField("Submit comment")
