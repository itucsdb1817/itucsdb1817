from flask import Blueprint, render_template,request, jsonify, session, redirect, flash,current_app
from flask_bcrypt  import Bcrypt
import os
import sys
from datetime import datetime
sys.path.append("../..") # Adds higher directory to python modules path.
from utils import admin_logged_in as check
from models.user import User 
from models.post import Post 
from models.vote import Vote 
from routes.user.forms import LoginForm
from routes.user.forms import RegistrationForm
from routes.user.forms import PasswordForm

admin_user_page = Blueprint('admin_user_page', __name__,)
@admin_user_page.route('/admin/login', methods = ['GET', 'POST'])
def login():
	if check.admin_logged_in():
		return redirect("/") 
	form = LoginForm()
	if form.validate_on_submit():
		username = form.data["username"]
		user = User.get_from_username(username)			
		if user is not None:
			password = form.data["password"]
			password_hash = user.password
			if current_app.config['bcrypt'].check_password_hash(password_hash, password) and user.is_admin == True:
				session['admin_user_id'] = user.id
				flash({'text': "You have successfully logged in.", 'type': "success"}) 
				return redirect("/")
			else:
				return render_template("login.html", form=form,error = "Incorrect password.")
		else:
			return render_template("login.html", form=form,error = "Incorrect username or password.")
	return render_template("login.html", form=form)