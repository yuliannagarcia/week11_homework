import mysql.connector
from flask import redirect, request, render_template
from application import routes

from application import app

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pa$$w0rd",
    database="product_db"
)


def get_db_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pa$$w0rd",
        database="product_db"
    )
    return mydb


def connect_to_database():
    return mysql.connector.connect(
        host="hostname",
        user="username",
        password="Pa$$w0rd",
        database="product_db"
    )


