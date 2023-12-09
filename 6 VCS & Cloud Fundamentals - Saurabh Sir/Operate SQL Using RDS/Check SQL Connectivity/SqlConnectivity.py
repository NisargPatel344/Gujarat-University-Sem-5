import mysql.connector

mydb = mysql.connector.connect(
  host="database-2.ctifqxiyrkpp.eu-north-1.rds.amazonaws.com",
  user="admin",
  password="11111111"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for x in mycursor:
     print(x)
