from wtforms import Form, IntegerField  # This is a field type representing an integer input.
from wtforms.validators import DataRequired  # This is a validator that checks if the field is not empty.


#  Creates and returns an instance of a form using the Form class.
def create_add_to_basket_form():
    return Form(
        product_id=IntegerField('Product ID', validators=[DataRequired()]),
        quantity=IntegerField('Quantity', validators=[DataRequired()])
    )
# Inside the Form constructor, two IntegerField instances are defined:
# product_id: Represents the product ID field. It's labelled "Product ID" and has a DataRequired validator,
# which means it's required and cannot be empty. quantity: Represents the quantity field. It's labelled
# "Quantity" and also has a DataRequired validator.
