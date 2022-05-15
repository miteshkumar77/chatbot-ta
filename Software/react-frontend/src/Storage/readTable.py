import createDatabase as db

def selectTable_all(mycursor, tableName):
    mycursor.execute("SELECT * FROM " + tableName)
    output = mycursor.fetchall()
    return output

def selectTable(mycursor, columns, tableName, condition):
    mycursor.execute("SELECT " + columns + " FROM " + tableName + " " + condition)
    output = mycursor.fetchall()
    return output
    

