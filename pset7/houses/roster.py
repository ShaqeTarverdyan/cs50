from csv import reader, DictReader
from cs50 import SQL
from sys import argv
import sqlite3

# Check command line arguments
if (len(argv) != 2):
    print("error")
    exit()

# Connect with the .db file and make a cursor
db = "students.db"
connect = sqlite3.connect(db)
cursor = connect.cursor()
houseName = argv[1].lower()

# Query database for all students in house
cursor.execute('SELECT DISTINCT(first), middle, last, birth FROM students WHERE lower(house)="{}" ORDER BY last, first;'.format(houseName))


houseRoster = cursor.fetchall()

for item in houseRoster:
    if not item[1]:
         print("{} {}, born {}".format(item[0], item[2], item[3]))
    else:
         print("{} {} {}, born {}".format(item[0], item[1], item[2], item[3]))

connect.close()



# Hints
# use db.execute("Select")
# Return value will be a list of python dict, where each dict represents a row in the table
# Remember to check for NULL values for middle names

# sqlite3 students.db

