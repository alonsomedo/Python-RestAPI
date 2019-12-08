from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)

class Student(Resource):
    def get(self, name):
        return {'student': name}

api.add_resource(Student, '/student/<string:name>')

app.run(debug=True, port=5000)