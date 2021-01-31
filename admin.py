import mysql.connector

mydb = mysql.connector.connect(user='ali', password='root',
                              host='127.0.0.1',database="patient")

print(mydb)
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM patient")


# mycursor.execute("INSERT INTO customers (name,address) VALUES (%s,%s) ",("amin","iran"))
# mycursor.execute("use mydatabase")

# mydb.commit()
for x in mycursor:
  print(x)