from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    FloatField,
    IntegerField,
    DateField,
    SubmitField,
    FieldList,
    FormField,
    ValidationError,
)
from wtforms.validators import DataRequired, Optional, ValidationError
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    FloatField,
    IntegerField,
    SelectField,
)
from wtforms.validators import DataRequired
from lists import SHOPS, ITEMS, CATEGORIES


class ProductRowForm(FlaskForm):
    class Meta:
        csrf = False

    item = SelectField(
        choices=[("", "---")] + ITEMS,
        validators=[Optional()],
    )
    descr = StringField("Description", validators=[Optional()])
    category = SelectField(
        choices=[("", "---")] + CATEGORIES,
        validators=[Optional()],
    )  # SelectField choices = [(submitted_value, displayed_text)]
    weight = IntegerField("Weight, gr", validators=[Optional()])
    units = IntegerField("Pieces / units", validators=[Optional()])
    cost = FloatField("Price", validators=[Optional()])

    def validate_cost(
        self, field
    ):  # default: def validate_<fieldname>(self, field): . WTForms reads 'validate_cost' and knows taht field = form.cost
        filled = [
            field.data,
            self.category.data,
        ]

        if any(filled) and not all(filled):
            raise ValidationError(
                "If you enter a product, price and category are required"
            )


class MultiProductForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    shop = SelectField(
        label="Shop",
        choices=SHOPS,
        validators=[DataRequired()],
    )
    products = FieldList(
        FormField(ProductRowForm), min_entries=15  # number of rows shown by default
    )
    submit = SubmitField("Submit")


class GraphFilterForm(FlaskForm):
    filter_type = SelectField(
        "Filter by",
        choices=[("shop", "Shop"), ("category", "Category"), ("item", "Item")],
        validators=[DataRequired()],
    )
    filter_value = SelectField("Choose value", choices=[], validators=[DataRequired()])
    submit = SubmitField("Refresh filter & Show Graph")
