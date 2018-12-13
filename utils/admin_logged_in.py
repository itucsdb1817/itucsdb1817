from flask import current_app, request, jsonify, session
import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from models.user import User 
#This function returns true if the admin is
#currently logged in.
def admin_logged_in():
	id = session.get("admin_user_id","") or -1
	return id != -1
