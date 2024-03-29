from flask import Flask,jsonify,Response,current_app
from flask_restful import Resource,Api,reqparse
from werkzeug.exceptions import abort

from funkr.db import get_db
from funkr.auth import authenticate_user#,authorize_user

post_args = reqparse.RequestParser()
post_args.add_argument("Authorization",type=str)
post_args.add_argument("post_body",type=str)

def get_post(post_id):
	post = get_db().execute(
			"SELECT post_id,post_user_id,post_body,user_name"
			" FROM post JOIN user ON post_user_id = user_id"
			" WHERE post_id = ?",
			(post_id,)
		).fetchone()
	return post

def check_args(post_id,args):
	post = get_post(post_id)
	if post is None:
		return {"message":"Post not found"},404
	if "Authorization" not in args:
		return {"message":"Login required"},401
	user = authenticate_user(args["Authorization"],post["post_user_id"])
	if user is None:
		return {"message":"Unauthorized user"},403
	return None

class Post(Resource):
	def get(self,post_id):
		post = get_post(post_id)
		if post is None:
			return {"message":"Post not found"},404
		else:
			return dict(post)
	
class Create(Resource):
	def post(self):
		args = post_args.parse_args()
		user = authenticate_user(args["Authorization"])
		if user is None:
			return {"message":"Login required"},401
		
		db = get_db()
		db.execute(
			"INSERT INTO post (post_body,post_user_id) VALUES (?,?)",
			(args["post_body"],user["user_id"])
		)
		db.commit()
		return {"message":"Created post"},201
	
class Update(Resource):
	def put(self,post_id):
		args = post_args.parse_args()
		error = check_args(post_id,args)
		if error is not None:
			return error
		
		db = get_db()
		db.execute(
			"UPDATE post SET post_body = ? WHERE post_id = ?",
			(args["post_body"],post_id)
		)
		db.commit()
		return {"message":"Updated post"},200
	
class Delete(Resource):
	def delete(self,post_id):
		args = post_args.parse_args()
		error = check_args(post_id,args)
		if error is not None:
			return error
		db = get_db()
		db.execute("DELETE FROM post WHERE post_id = ?",(post_id,))
		db.commit()
		return {"message":"Deleted post"},200
	
	def post(self,post_id):
		return self.delete(post_id)
	
class Blog(Resource):
	def get(self):
		posts = get_db().execute(
			"SELECT post_id,post_user_id,post_body,user_name"
			 " FROM post JOIN user ON user_id = post_user_id"
		).fetchall()
		index = []
		for post in posts:
			index.append(dict(post))
		return jsonify(index)