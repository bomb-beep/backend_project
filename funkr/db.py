import sqlite3
import click
from flask import current_app,g

def get_db():
	if "db" not in g:
		g.db = sqlite3.connect(
			current_app.config["DATABASE"],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row
		# g.db.row_factory = dict_factory

	return g.db

# def to_dict(row:sqlite3.Row):
# 	d = {}
# 	for key in row.keys():
# 		d[key] = row[key]

# def dict_factory(cursor,row):
# 	d = {}
# 	for idx, col in enumerate(cursor.description):
# 		d[col[0]] = row[idx]
# 	return d

def init_db():
	db = get_db()

	with current_app.open_resource("schema.sql") as f:
		db.executescript(f.read().decode("utf8"))

def test_db():
	init_db()
	db = get_db()

	with current_app.open_resource("data.sql") as f:
		db.executescript(f.read().decode("utf8"))

def close_db(e=None):
	db = g.pop("db",None)

	if db:
		db.close()


@click.command("test-db")
def test_db_command():
	test_db()
	click.echo("Established test database")
		
@click.command("init-db")
def init_db_command():
	init_db()
	click.echo("Initialized the database")

def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)
	app.cli.add_command(test_db_command)