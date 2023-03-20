import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from funcr.db import get_db

bp = Blueprint("auth",__name__,url_prefix="/auth")

@bp.route("/register",methods=("GET","POST"))
def register():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		
		db = get_db()
		error = None

		if not username:
			error = "Username is required"
		elif not password:
			error = "Password is required"

		if not error:
			try:
				db.execute(
					"INSERT INTO user (username, password) VALUES (?,?)",
					(username,generate_password_hash(password))
				)
				db.commit()
			except db.IntegrityError:
				error = f"User {username} is already registered"
			else:
				redirect(url_for("auth.login"))
		
		if error:
			flash(error)
	return render_template("auth/register.html")

@bp.route("/login",methods=("GET","POST"))
def login():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]

		db = get_db()
		error = None

		if not username:
			error = "Username is required"
		elif not password:
			error = "Password is required"

		if not error:
			user = db.execute(
				"SELECT * FROM user WHERE USERNAME = ?",
				(username,)
			)
			if not user["password"] == check_password_hash(password):
				error = "Incorrect password"
			else:
				session.clear()
				session["user_id"] = user["id"]
				
		if error:
			flash(error)

	render_template("auth/login.html")