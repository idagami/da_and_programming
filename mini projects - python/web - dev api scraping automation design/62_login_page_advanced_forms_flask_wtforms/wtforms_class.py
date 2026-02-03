from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField(
        label="Email", validators=[DataRequired(), Email(message="email field error")]
    )
    password = PasswordField(
        label="Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long."),
        ],
    )
    remember = BooleanField(label="Remember Me")
    submit = SubmitField("Log In")
