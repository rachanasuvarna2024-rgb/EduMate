import mysql.connector
from mysql.connector import Error


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "learning_Sql#",
    "database": "edumate_db3_3"
}


# ============================================================
# FRESH DATABASE CONNECTION
# ============================================================

def get_db_connection():

    try:

        connection = mysql.connector.connect(
            **DB_CONFIG
        )

        if connection.is_connected():
            return connection

        return None

    except Error as err:

        print("Database Connection Failed")
        print(err)

        return None


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================
#
# Existing files such as auth.py still use:
#
#     from db import conn, cursor
#
# Keep these variables so those files continue working.
#
# Newer routes should use:
#
#     from db import get_db_connection
#
# ============================================================

try:

    conn = get_db_connection()

    if conn:

        cursor = conn.cursor(dictionary=True)

        print("Connected to EduMate Database")

    else:

        conn = None
        cursor = None

        print("Database Connection Failed")


except Error as err:

    conn = None
    cursor = None

    print("Database Connection Failed")
    print(err)