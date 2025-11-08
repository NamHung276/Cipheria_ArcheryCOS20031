import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Blue@Sky2706",
    database="archery_db"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM employees")  # replace with your table
rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()