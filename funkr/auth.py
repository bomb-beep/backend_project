import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from funkr.db import get_db
from random import randint

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
					"INSERT INTO user (username, password, token) VALUES (?,?,?)",
					(username,generate_password_hash(password),randint(0,9999999999))
				)
				db.commit()
			except db.IntegrityError:
				error = f"User {username} is already registered"
			else:
				# user = db.execute(
				# 	"SELECT * FROM user WHERE username = ?",(username,)
				# ).fetchone()
				session.clear()
				session["user_token"] = db.execute(
					"SELECT token FROM user WHERE username = ?",(username,)
				).fetchone()["token"]
				return redirect(url_for("index"))
		
		flash(error)
	return render_template("auth/register.html")

@bp.route("/login",methods=("GET","POST"))
def login():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]

		db = get_db()
		error = None

		user = db.execute(
			"SELECT * FROM user WHERE USERNAME = ?",
			(username,)
		).fetchone()

		if not user:
			error = "Incorrect username"

		if not error:

			if not check_password_hash(user["password"],password):
				error = "Incorrect password"
			else:
				session.clear()
				session["user_token"] = user["token"]
				
		if error:
			flash(error)
		else:
			return redirect(url_for("index"))

	return render_template("auth/login.html")

@bp.before_app_request
def load_logged_in_user():
	user_token = session.get("user_token")

	if user_token == None:
		g.user = None
	else:
		g.user = get_db().execute(
			"SELECT	* FROM user WHERE token = ?",
			(user_token,)
		).fetchone()

@bp.route("/logout")
def logout():
	session.clear()

	return redirect(url_for("index"))

def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return abort(401,"Login required")
			#return redirect(url_for("auth.login"))
		else:
			return view(**kwargs)
		
	return wrapped_view