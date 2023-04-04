from flask import Flask
from flask_restful import Api,Resource
import os


def create_app(test_config=None):
	app = Flask(__name__,instance_relative_config=True)
	api = Api(app)
	app.config.from_mapping(
		SECRET_KEY = "dev",
		DATABASE = os.path.join(app.instance_path,"funkr.sqlite")
	)
	if test_config is None:
		app.config.from_pyfile("config.py",silent=True)
	else:
		app.config.from_mapping(test_config)
		
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	from . import db
	db.init_app(app)

	class Hello(Resource):
		def get(self):
			return {"data":"Hello!"}
		
	api.add_resource(Hello,"/hello/")

	from . import blog
	api.add_resource(blog.Post,"/posts/<int:post_id>/")
	api.add_resource(blog.Blog,"/posts/all/")
	api.add_resource(blog.Create,"/posts/create/")
	api.add_resource(blog.Update,"/posts/edit/<int:post_id>/")

	return app

if __name__ == "__main__":
    create_app().run(debug=True)