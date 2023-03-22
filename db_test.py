#from funcr import db
import sqlite3
import os

DATABASE = "C:\\Users\\bo\\Desktop\\dev_proj\\instance\\funcr.sqlite"

def connect_db():
	return sqlite3.connect(DATABASE,detect_types=sqlite3.PARSE_DECLTYPES)

print(DATABASE)
db = connect_db()
#db.execute("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)")
db.execute
print(db.execute("SELECT * FROM user").fetchall())