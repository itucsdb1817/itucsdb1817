from flask import current_app, request, jsonify, session
import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from models import user

def logged_in():
	id = session.get("user_id","") or 0
	check = user.User(id)
	return check.get_user(id)
