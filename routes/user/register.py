from flask import request, jsonify, session, redirect
import os
import sys
sys.path.append("../..") # Adds higher directory to python modules path.
from utils import logged_in as check
from models import user as model
def register():
	if check.logged_in():
		return redirect("/") #If user is logged in redirect it to homepage.
	else:
		insertUser = model.User(None)
		insertUser.add_user('John', 'Doe', '1997-06-24 00:00:00', 'Johnny', 'xd', 'jdoe@hotmail.de') #User register
		return "Welcome " + insertUser.username
	req = request.json
	
