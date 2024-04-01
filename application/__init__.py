# from flask import Flask
# from application import routes
# import os
#
# app = Flask(__name__)
# app.secret_key = 'your_secret_key'
#
# SECRET_KEY = os.urandom(32)
# app.config['SECRET_KEY'] = SECRET_KEY

from flask import Flask

app = Flask(__name__)

from application import routes
