#from funkr import db
import sqlite3
import os

DATABASE = "C:\\Users\\bo\\Desktop\\dev_proj\\instance\\funkr.sqlite"

def connect_db():
	return sqlite3.connect(DATABASE,detect_types=sqlite3.PARSE_DECLTYPES)

print(DATABASE)
db = connect_db()
#db.execute("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)")
#db.execute
#db.row_factory = sqlite3.Row
#print(db.execute("SELECT * FROM user").fetchall())
#print(db.execute("SELECT * FROM post").fetchall())

query = db.execute(
	"SELECT * FROM post p JOIN user u ON u.id = author_id"
).fetchone()

print(query)