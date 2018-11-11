from flask import current_app, request, jsonify, session
import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from models.user import User 
#This function returns true if the user is
#currently logged in.
def logged_in():
	id = session.get("user_id","") or -1
	return id != -1
