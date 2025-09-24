#! C:\Python313\python.exe

import os
import urllib.parse
import mysql.connector 
from mysql.connector import errorcode
import bcrypt
from  DBConnection import HOST, USER, PASSWORD, DATABASE, AUTHPLUGIN

#**********Get the Query String Variables**********

query_string = os.environ['QUERY_STRING']  #assumes data is being sent GET
qs_values = urllib.parse.parse_qs(query_string, keep_blank_values=True)

id = qs_values['id2update'][0]
username = qs_values['username'][0] 
password = qs_values['password'][0]
email = qs_values['email'][0]

#********** Hash the password**********
password_bytes = password.encode('utf-8')
hashedpassword = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

#**********Connect to Database**********

DBResponse = ""
try:
  mydb = mysql.connector.connect(host=HOST,user=USER,password=PASSWORD, database=DATABASE, auth_plugin= AUTHPLUGIN)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    DBResponse = "Something is wrong with the user name or password"
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    DBResponse = "Database does not exist"
  else:
    DBResponse = err

mycursor = mydb.cursor()

#**********Execute the SQL Statement to Update the Record **********

sql = "UPDATE user set UserName = %s, Email = %s, Password=%s where ID = %s"
val = (username, email, hashedpassword, id)
try:
  mycursor.execute(sql, val)
  mydb.commit()
  DBResponse = "User updated successfully!"
except mysql.connector.Error as err:
  DBResponse = "Error on update: {}".format(err)
mydb.close()

#**********Output HTML**********

print ("Content-type:text/html\r\n\r\n") 
print ("<!DOCTYPE html>")
print ("<html>")
print ("<head>")
print ("<title>Python Crud Update</title>")
print ("</head>")
print ("<body>")
print (DBResponse)
print ("<br><br><a href='read.py'>View List</a>")
print ("<br><br><a href='index.html'>Crud Home</a>")
print ("</body>")
print ("</html>")