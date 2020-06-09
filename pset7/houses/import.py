from csv import reader, DictReader
from cs50 import SQL
from sys import argv
import sqlite3

# Check command line arguments
if len(argv) != 2:
    print("error")
    exit()

#                for input.py

# FOr each row parse name
# Insert each student into the students table of students.db

# HInts
# use split method for spliting name, middle & last names
# if student not have middle name, use none(NULL)
# use db.execute to insert row in the table

# Connect with the .db file and make a cursor
db = "students.db"
con = sqlite3.connect(db)

cursor = con.cursor()

# Open csv file given by command line argument
with open(argv[1], "r") as studentsFile:
    studentsList = DictReader(studentsFile)

    for studentRow in  studentsList:
        names = []

        for item in studentRow["name"].split(" "):
            names.append(item)

        names.append(studentRow["house"])
        names.append(studentRow["birth"])

        if (len(names) == 4):

            cursor.execute("INSERT INTO students(first, last, house, birth) VALUES(?,?,?,?)", names[:4])

        if (len(names) == 5):
            cursor.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?,?,?,?,?)", names[:5])

con.commit()
con.close()
