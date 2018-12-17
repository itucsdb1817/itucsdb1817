from flask import current_app, request, jsonify, session, redirect
import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from models.user import User 
#This function returns true if the admin is
#currently logged in.
def admin_logged_in():
    try:
        user = User(session.get("user_id", "") or -1)
        return user.is_admin
    except NotImplementedError as e:
        session.pop("user_id", None)
        return False
    
    

