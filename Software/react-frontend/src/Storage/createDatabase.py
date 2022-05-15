from setuptools import Command
import mysql.connector

class mysqlDatabase:
	# create database
	def __init__(self):
	  self.mydb = mysql.connector.connect(
	    host="localhost",
	    user="user_name",
	    password="Password!!!!!11111",
	    database = "mysql"
	  )
	  self.mycursor = self.mydb.cursor()
	  self.command = ""

	def __del__(self):
		  self.mydb.close()
		  self.mycursor.close()
	 	
	 # create table
	def createTable(self, TableName, column_lists):
		  self.command = "CREATE TABLE " + TableName + " ("
		  for elem in column_lists:
		    self.command += elem + " VARCHAR(255), "
		  self.command = self.command[:-2]
		  self.command += ")"
		  print(self.command)
		  try:
		  	self.mycursor.execute(self.command)
		  except mysql.connector.Error as err:
		  	print("Table already exists")
		  	return self.mydb, self.mycursor
		  return self.mydb, self.mycursor

