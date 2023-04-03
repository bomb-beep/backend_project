from flask import Flask
from flask_restful import Api,Resource


def create_app(test_config=None):
	app = Flask(__name__,instance_relative_config=True)
	api = Api(app)

	from . import db
	db.init_app(app)

	class Hello(Resource):
		def get(self):
			return {"data":"Hello!"}
		
	api.add_resource(Hello,"/hello/")

	return app

if __name__ == "__main__":
    create_app().run(debug=True)