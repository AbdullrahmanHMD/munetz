from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return "Hello World"

api.add_resource(HelloWorld, '/hello_world')

if __name__ == '__main__':
    app.run(debug=False)