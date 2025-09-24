#! C:\Python313\python.exe

import os
import urllib.parse
import mysql.connector # must install mysql-connector-python then mysql-connector
from mysql.connector import errorcode
import bcrypt
from  DBConnection import HOST, USER, PASSWORD, DATABASE, AUTHPLUGIN

#**********Get the Query String Variables**********

query_string = os.environ['QUERY_STRING']  #assumes data is being sent GET
qs_values = urllib.parse.parse_qs(query_string, keep_blank_values=True)

id = qs_values['id2delete'][0] 

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

#**********Execute the SQL Statement to Delete the Record **********

sql = "Delete from user where id = %s"
val = (id,)
try:
  mycursor.execute(sql, val)
  mydb.commit()
  DBResponse = "User deleted successfully!"
except mysql.connector.Error as err:
  DBResponse = "Error on delete: {}".format(err)
mydb.close()

#**********Output HTM**********

print ("Content-type:text/html\r\n\r\n") #Must have this header
print ("<!DOCTYPE html>")
print ("<html>")
print ("<head>")
print ("<title>Python Crud Delete</title>")
print ("</head>")
print ("<body>")
print (DBResponse)
print ("<br><br><a href='read.py'>View List</a>")
print ("</body>")
print ("</html>")