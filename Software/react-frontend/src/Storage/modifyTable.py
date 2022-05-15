import createDatabase as db

def insertRow(mydb, mycursor, tableName, condition):
    mycursor.execute("INSERT INTO " + tableName + condition)
    mydb.commit()

def deleteRow(mydb, mycursor, tableName, condition):
    mycursor.execute("DELETE FROM " + tableName + " WHERE " + condition)
    mydb.commit()

def dropTable(mydb, mycursor, tableName):
	mycursor.execute("DROP TABLE " + tableName)
	mydb.commit()
	
