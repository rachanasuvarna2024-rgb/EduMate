import mysql.connector

# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------
try:

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="learning_Sql#",
        database="edumate_db3_3"
    )

    cursor = conn.cursor(dictionary=True)

    print("Connected to EduMate Database")

except mysql.connector.Error as err:

    print("Database Connection Failed")
    print(err)