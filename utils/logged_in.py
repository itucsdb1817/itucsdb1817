from flask import current_app, request, jsonify, session, redirect
import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from models.user import User 
#This function returns true if the user is
#currently logged in.
def logged_in():
    try:
        id = session.get("user_id","") or -1
        xduser = User(id)
        return id != -1
    except NotImplementedError as e:
        session.pop("user_id", None)
        return False 
