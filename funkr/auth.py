from flask import Flask
from base64 import b64decode,b64encode

from funkr.db import get_db

def authenticate_user(user_token,authorize_id=None):
	token = user_token.split(" ")
	token = str(b64decode(token[token.index("Basic") + 1]),"utf8")
	
	user = get_db().execute(
		"SELECT * FROM user WHERE user_token = ?",
		(token,)
	).fetchone()
	if authorize_id is not None and authorize_id is not user["user_id"]:
		return None
	
	return user
