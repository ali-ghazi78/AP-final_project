import mysql.connector

 
mydb = mysql.connector.connect(user="ali", password="root",
                                        host="localhost", database="clinic")