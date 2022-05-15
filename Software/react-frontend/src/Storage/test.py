import createDatabase as db
import readTable as db_read
import modifyTable as db_modify
from NLP import BertClassify as bert 

DataMessage = [
	"SVN update working folder",
	"status report",
	"class schedule"
]
DataMessageRest = [
	"upload new file in working directory",
	"update current folder",
	"delete files in working directory",
	"make appointment",
	"due dates for class",
	"Grading criteria"
]
database1 = db.mysqlDatabase()
dbName = "ChatLogs"
mydb, mycursor = database1.createTable(dbName , ["Time", "Message"])
db_modify.insertRow(mydb, mycursor, dbName , " VALUES('a', 'c')")
db_modify.insertRow(mydb, mycursor, dbName , " VALUES('a', 'b')")
db_modify.insertRow(mydb, mycursor, dbName , " VALUES('e', 'c')")
database1.createTable("GroupedChats", ["GroupNo", "Message"])

grouped_messages = bert.classifyMessages(DataMessage, DataMessageRest)
goup_number = 0
#for groups in grouped_messages:
#	group_number += 1
#	for elem in groups:
#		db_modify.insertRow(mydb, mycursor, "GroupedChats", " VALUES('%d', %s)" %(group_number, elem))
#				
#print(db_read.selectTable_all(mycursor, "GroupedChats"))
with open('display.txt', 'w') as file1:
	for line in grouped_messages:
		for elem in line:
			file1.write(elem + '\n')
		file1.write('\n')
#db_modify.dropTable(mydb, mycursor, dbName)
