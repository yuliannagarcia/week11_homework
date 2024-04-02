from flask import Flask
import os

# Creates a Flask application instance named app. The __name__ argument is a special Python variable that represents
# the name of the current module. It is used by Flask to locate resources such as templates and static files.
app = Flask(__name__)
app.secret_key = 'your_secret_key'
# Sets the secret key for the Flask application. The secret key is used to secure the session data and should be kept
# confidential. In this case, it is set directly in the code, which is not recommended for production applications.
SECRET_KEY = os.urandom(32)
#  Generates a random secret key using os.urandom(32), which generates 32 bytes of cryptographically secure random data.
#  This key is then stored in the SECRET_KEY variable.
app.config['SECRET_KEY'] = SECRET_KEY
# Sets the secret key for the Flask application configuration using the app.config dictionary. This is a more secure way
# of setting the secret key compared to directly assigning it.

from application import routes

