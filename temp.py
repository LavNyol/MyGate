from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

# Create a engine for connecting to SQLite3.
# Assuming salaries.db is in your app root folder

e = create_engine('sqlite:///main.db')

app = Flask(__name__)
api = Api(app)


class Departments_Meta(Resource):
    def get(self):
        # Connect to databse
        conn = e.connect()
        # Perform query and return JSON data
        query = conn.execute("select distinct Applicant from trucks")
        return {'Applicants': [i[0] for i in query.cursor.fetchall()]}


class Applicant_Details(Resource):
    def get(self, applicant_name):
        conn = e.connect()
        query = conn.execute("select * from trucks where Applicant=?" , applicant_name)
        # Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return result
        # We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient
class Expiry_Details(Resource):
    def get(self, year):
        conn = e.connect()
        query = conn.execute("select * from trucks where permit = '%s'" %year)
        # print("select * from trucks where permit like ('?')" % (year))
        # Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return result


api.add_resource(Applicant_Details, '/applicants/<string:applicant_name>')
api.add_resource(Departments_Meta, '/applicants')
api.add_resource(Expiry_Details, '/license/<string:year>')

if __name__ == '__main__':
    app.run()