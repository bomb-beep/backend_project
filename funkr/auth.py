from flask import Flask
from base64 import b64decode,b64encode

from funkr.db import get_db

def authenticate_user(user_token):
	token = user_token.split(" ")
	token = str(b64decode(token[token.index("Basic") + 1]),"utf8")
	
	#print(token)
	user = get_db().execute(
		"SELECT * FROM user WHERE user_token = ?",
		(token,)
	).fetchone()
	#print(user,user["user_id"])
	
	return user

def authorize_user(user_id,user_token):
	user = authenticate_user(user_token)
	return None if user is None or user["user_id"] != user_id else user