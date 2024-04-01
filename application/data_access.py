import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pa$$w0rd",
    database="productDB"
)


def get_db_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pa$$w0rd",
        database="productDB"
    )
    return mydb
