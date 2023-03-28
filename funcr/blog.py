from flask import(
    Blueprint,flash,g,redirect,render_template,request,url_for
)
from werkzeug.exceptions import abort

from funcr.auth import login_required
from funcr.db import get_db

bp = Blueprint("blog",__name__)

@bp.route("/")
def index():
	db = get_db()
	posts = db.execute(
		"SELECT p.id, created, title, body, username, author_id"
		" FROM post p JOIN user u ON p.author_id = u.id"
		" ORDER BY p.created DESC"
	).fetchall()
    
	return render_template("blog/index.html",posts = posts)

@bp.route("/create",methods=("GET","POST"))
@login_required
def create():
	if request.method == "POST":
		db = get_db()
		title = request.form["title"]
		body = request.form["body"]
		error = None

		if not title:
			error = "Title is required"

		if not error:
			db.execute(
				"INSERT INTO post (title, body, author_id)"
				" VALUES (?, ?, ?)",
				(title,body,g.user["id"])
			)
			db.commit()

			return redirect(url_for("index"))
		else:
			flash(error)

	return render_template("blog/create.html")

def get_post(id,check_author = True):
	post = get_db().execute(
		"SELECT * "
		" FROM post p JOIN user u ON u.id = author_id"
		" WHERE p.id = ?",
		(id,)
	).fetchone()

	if not post:
		return abort(404,f"Post {id} does not exist")
	elif check_author and g.user["id"] != post["author_id"]:
		return abort(403)
	return post

@bp.route("/<int:id>/update",methods=("GET","POST"))
@login_required
def update(id):
	post = get_post(id)
	if request.method == "POST":
		title = request.form["title"]
		body = request.form["body"]
		error = None

		if not title:
			error = "Title is required"

		if not error:
			db = get_db()
			db.execute(
				"UPDATE post"
				" SET title = ?, body = ?"
				" WHERE id = ?",
				(title,body,id)
			)
			db.commit()
			return redirect(url_for("index"))
		else:
			flash(error)
	return render_template("blog/update.html",post=post)

@bp.route("/<int:id>/delete",methods=("GET","POST"))
@login_required
def delete(id):
	post = get_post(id)
	db = get_db()
	db.execute(
		"DELETE FROM post"
		" WHERE id = ?",
		(id,)
	)
	db.commit()

	return redirect(url_for("index"))


@bp.route("/<int:id>",methods=("GET",))
def show_post(id):
	post = get_post(id,check_author=False)

	return render_template("blog/show.html",post = post)