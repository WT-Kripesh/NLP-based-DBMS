#for configuring the connection to the database

import mysql.connector

# Database configuration with credentials  :   change it if necessary
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin@123',                         
    'database': 'nlp'
}

# Establish database connection
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()