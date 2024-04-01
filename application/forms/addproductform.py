from wtforms import Form, IntegerField
from wtforms.validators import DataRequired

def create_add_to_basket_form():
    return Form(
        product_id=IntegerField('Product ID', validators=[DataRequired()]),
        quantity=IntegerField('Quantity', validators=[DataRequired()])
    )