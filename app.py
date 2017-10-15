"""
	Entry point for flask app controlling /projects endpoint
	TODO: add a firebase config service? so we're not copy pasting all this stuff into every endpoint
		  figure out better auth flow...
		  setup trace route, debugging, logging, centralized documentation (can we publish to a wiki or something?)
"""
from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_cors import CORS, cross_origin
import pyrebase
import json

app = Flask(__name__)
CORS(app)

# Set up database connection.
config = {
    'apiKey': "AIzaSyDpFoAzfFzzcCmYkMwkAz61wUY_O5z9KM4", 
    'authDomain': "cloudide-3d6ca.firebaseapp.com", 
    'databaseURL': "https://cloudide-3d6ca.firebaseio.com", 
    'projectId': "cloudide-3d6ca", 
    'storageBucket': "cloudide-3d6ca.appspot.com", 
    'messagingSenderId': "42881595105"
}

firebase = pyrebase.initialize_app(config)

# Set up the user
auth = firebase.auth()
user = auth.sign_in_with_email_and_password('jmankhan1@gmail.com', 'password')

db = firebase.database()

@app.route("/projects")
def getProject():
	"""
		Gets a project by id, if provided
		Otherwise returns all project ids

		TODO: better error handling
	"""
	id = request.args.get('id')
	
	projects = db.child('projects').child(id).get(user['idToken']) if id != None else db.child('projects').get(user['idToken'])

	return jsonify(projects.val())

@app.route("/projects/", methods=["POST"])
def insertProject():
	"""
		Inserts a new project with a title attribtue
		Use the following curl command to test:
		curl -X POST -H "Content-Type: application/json" -d '{"id" : "5", "title" : "Jalal is the best"}' http://localhost:5000/projects/

		TODO: better error handling!
	"""
	project_json = request.get_json()

	try:
		db.child("projects").child(project_json['id']).set(project_json['title'], user['idToken'])
	except:
		return "Something went wrong inserting the project"
	
	return "Success"

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)

