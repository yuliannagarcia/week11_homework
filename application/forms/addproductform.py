from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired


class AddToBasketForm(FlaskForm):
    # Define fields and validators
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
