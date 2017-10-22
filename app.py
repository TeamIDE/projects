"""
	Entry point for flask app controlling /projects endpoint
	TODO: add a firebase config service? so we're not copy pasting all this stuff into every endpoint
		  figure out better auth flow...
		  setup trace route, debugging, logging, centralized documentation (can we publish to a wiki or something?)
"""
from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import pyrebase
import json
import os

app = Flask(__name__)
CORS(app)

# Set up database connection.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

# Set up the user
auth = firebase.auth()
user = auth.sign_in_with_email_and_password('jmankhan1@gmail.com', 'password')

class ProjectException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.route("/projects/", methods=["GET", "POST"])
def handleRoute():
	if request.method == "POST":
		return insertProject(request)
	elif request.method == "GET":
		return getProject(request)
	else:
		raise ProjectException("There was an error processing your request" , status_code=400)

def getProject(request):
	"""
		Gets a project by id, if provided
		Otherwise returns all project ids

		TODO: return as array!
	"""
	id = request.args.get('id')
	
	projects = db.child('projects').child(id).get(user['idToken']) if id != None else db.child('projects').order_by_key().get(user['idToken'])

	return jsonify(projects.val())

def insertProject(request):
	"""
		Inserts a new project with a title attribtue
		Use the following curl command to test:
		curl -X POST -H "Content-Type: application/json" -d '{"id" : "5", "title" : "Jalal is the best"}' http://localhost:5000/projects/

		TODO: better error handling!
	"""
	data = request.get_json()
	id = db.generate_key()
	data['id'] = id
	print(data)
	try:
		db.child("projects").push(data, user['idToken'])
	except:
		return jsonify('{ status : "error", message : "Something went wrong inserting the project" }')
	print('returning success')
	return jsonify('{ status : "Success" }')

@app.errorhandler(ProjectException)
def err(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5001, debug=True)

