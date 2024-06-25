import base64
import json
import os

from flask import Flask, Response
from flask_restful import Resource, Api, reqparse, inputs

from scraping import Scraping

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return "Hello World"


class Details(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str)
        args = parser.parse_args()
        print(args)
        return {"test": "test"}, 200


class Scraper(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, required=True, location='json')
        args = parser.parse_args()
        try:
            url = inputs.url(args['url'])
        except ValueError:
            return {"msg": "No valid URL"}, 400
        scraping = Scraping()
        scraping.setup_driver()
        details = scraping.get_page(args['url'])
        print(details)
        scraping.shutdown_driver()
        with open(f'{os.getcwd()}/temp/output.zip', 'rb') as zipfile:
            file_data = zipfile.read()
            file_encoded = base64.b64encode(file_data)
        os.remove(f'{os.getcwd()}/temp/output.zip')
        return Response(file_encoded, mimetype='application/zip')


api.add_resource(HelloWorld, '/hello_world')
api.add_resource(Details, '/details')
api.add_resource(Scraper, '/scraper')

if __name__ == '__main__':
    app.run(debug=False)