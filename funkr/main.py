from flask import Flask
from flask_restful import Api,Resource



app = Flask(__name__,instance_relative_config=True)
api = Api(app)

import db
db.init_app(app)

class Hello(Resource):
    def get(self):
        return {"data":"Hello!"}
    
api.add_resource(Hello,"/hello/")

if __name__ == "__main__":
    app.run(debug=True)