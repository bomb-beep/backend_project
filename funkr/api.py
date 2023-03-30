from flask import (
    Blueprint,g,request
)
import json
from werkzeug.exceptions import abort
from funkr.db import get_db
from funkr.blog import get_post
from base64 import b64decode,b64encode

bp = Blueprint("api",__name__,url_prefix="/api")

@bp.route("/posts/<int:id>")
def show_post(id):
	post = get_post(id,check_author=False)

	return json.dump(post)