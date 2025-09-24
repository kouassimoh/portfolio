#! C:\Python313\python.exe

import os
import urllib.parse

#**********Get the Query String Variables**********

query_string = os.environ['QUERY_STRING']  #assumes data is being sent GET
qs_values = urllib.parse.parse_qs(query_string, keep_blank_values=True)

fname = qs_values['fname'][0] 
lname = qs_values['lname'][0]


#**********Output HTML**********

print ("Content-type:text/html\r\n\r\n") #Must have this header
print ("<!DOCTYPE html>")
print ("<html>")
print ("<head>")
print ("<title>Hello Somebody</title>")
print ("</head>")
print ("<body>")

if lname == "Somebody":
  print("You are somebody!")

print ("<h2>Hello, %s %s!</h2>" % (fname, lname))
print ("</body>")
print ("</html>")


