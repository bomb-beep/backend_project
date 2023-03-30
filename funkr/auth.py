from flask import(
    Blueprint,g,request
)
from werkzeug.exceptions import abort
from funkr.db import get_db
from base64 import b64decode

bp = Blueprint("auth",__name__,url_prefix="/auth")

@bp.before_app_request
def load_user():
	if "Authorization" in request.headers:
		token = request.headers["Authorization"].split(" ")
		token = b64decode(token[token.index("Basic") + 1])
		
		db = get_db()
		user = db.execute(
			"SELECT * FROM user WHERE user_token = ?",
			(token,)
		).fetchone()

		assert user is not None
		g.user = user

	else:
		g.user = None