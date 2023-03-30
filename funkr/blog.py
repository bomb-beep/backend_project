from flask import (
    Blueprint,g,request
)
from werkzeug.exceptions import abort
from funkr.db import get_db

def get_post(id,check_author = True):
	post = get_db().execute(
		"SELECT * FROM post JOIN user ON post_user_id = user_id"
		" WHERE post_id = ?",
		(id,)
	)

	if not post:
		return abort(404)
	if check_author and g.user["user_id"] is not post["user_id"]:
		return abort(403)
	
	return post