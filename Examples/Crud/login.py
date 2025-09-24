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

username = qs_values['username'][0] 
password = qs_values['password'][0]

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

#**********Execute the SQL Statement to See if User is Logged Int**********

sql = "Select username, password from user where UserName = %s"
val = (username, )
try:
  mycursor.execute(sql, val)
  myresult = mycursor.fetchall()
  if myresult:
    retrieved_password = myresult[0][1]
    if bcrypt.checkpw(password.encode('utf-8'), retrieved_password.encode('utf-8')):
      DBResponse = "User found with that username and password. <br> User logged in successfully!"
    else:
      DBResponse = "Password incorrect"
  else:
    DBResponse = "No user found with that username"
except mysql.connector.Error as err:
  DBResponse = "Error on insert: {}".format(err)
  
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