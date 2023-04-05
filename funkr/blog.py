from flask import Flask,jsonify,Response,current_app
from flask_restful import Resource,Api,reqparse
from werkzeug.exceptions import abort

from funkr.db import get_db
from funkr.auth import authenticate_user,authorize_user

post_args = reqparse.RequestParser()
#create_post_args.add_argument("post_title",type=str)
post_args.add_argument("Authorization",type=str)
post_args.add_argument("post_body",type=str)

def get_post(post_id):
	post = get_db().execute(
			"SELECT * FROM post WHERE post_id = ?",
			(post_id,)
		).fetchone()
	return post

class Post(Resource):
	def get(self,post_id):
		post = get_post(post_id)
		return dict(post) if post is not None else 404
	
class Create(Resource):
	def post(self):
		args = post_args.parse_args()
		user = authenticate_user(args["Authorization"])
		if user is None:
			return 401
		
		db = get_db()
		db.execute(
			"INSERT INTO post (post_body,post_user_id) VALUES (?,?)",
			(args["post_body"],user["user_id"])
		)
		db.commit()
		#print(args)
		#return Response("Created post",status=201)
		return {"message":"Created post"},201
	
class Update(Resource):
	def put(self,post_id):
		args = post_args.parse_args()
		if args["Authorization"] is None:
			return 401
		db = get_db()
		post = get_post(post_id)
		if post is None:
			return 404
		
		user = authorize_user(post["post_user_id"],args["Authorization"])
		if user is None:
			return 403
		db.execute(
			"UPDATE post SET post_body = ? WHERE post_id = ?",
			(args["post_body"],post_id)
		)
		db.commit()
		return {"message":"Updated post"},200
	
class Delete(Resource):
	def delete(self,post_id):
		post = get_post(post_id)
		if post is None:
			return 404
		
		args = post_args.parse_args()
		if "Authorization" not in args:
			return 401
		
		user = authorize_user(post["post_user_id"],args["Authorization"])

		if user is None:
			return 403
		
		db = get_db()
		db.execute("DELETE FROM post WHERE post_id = ?",(post_id,))
		db.commit()
		return {"message":"Deleted post"},200
	
	def post(self,post_id):
		post = get_post(post_id)
		if post is None:
			return 404
		
		args = post_args.parse_args()
		if "Authorization" not in args or args["Authorization"] is None:
			return 401
		
		user = authorize_user(post["post_user_id"],args["Authorization"])

		if user is None:
			return 403
		
		db = get_db()
		db.execute("DELETE FROM post WHERE post_id = ?",(post_id,))
		db.commit()
		return {"message":"Deleted post"},200
	
class Blog(Resource):
	def get(self):
		posts = get_db().execute(
			"SELECT * FROM post"
		).fetchall()
		index = []
		for post in posts:
			index.append(dict(post))
		return jsonify(index)