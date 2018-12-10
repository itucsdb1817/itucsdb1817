from flask import Blueprint, render_template,request, jsonify, session, redirect, flash,current_app
from flask_bcrypt  import Bcrypt
import os
import sys
from datetime import datetime
sys.path.append("../..") # Adds higher directory to python modules path.
from utils import logged_in as check
from models.user import User 
from models.post import Post 
from routes.user.forms import LoginForm
from routes.user.forms import RegistrationForm

user_page = Blueprint('user_page', __name__,)

#If user is not already logged in checks if
#password is correct.
@user_page.route('/user/login', methods = ['GET', 'POST'])
def login():
	if check.logged_in():
		return redirect("/") 
	form = LoginForm()
	if form.validate_on_submit():
		username = form.data["username"]
		user = User.get_from_username(username)
		if user is not None:
			password = form.data["password"]
			password_hash = user.password
			if current_app.config['bcrypt'].check_password_hash(password_hash, password):
				session['user_id'] = user.id
				return "User logged in successfully."
			else:
				return render_template("login.html", form=form,error = "Incorrect password.")
		else:
			return render_template("login.html", form=form,error = "Incorrect username or password.")
	return render_template("login.html", form=form)


@user_page.route('/user/logout')
def logout():
	session.pop("user_id",None)
	return "User logged out successfully."


#If user is logged in page is redirected it to homepage.
#User can register if there is no other acccount with same username or email.
@user_page.route('/user/register', methods = ['GET', 'POST'])
def register():
	if check.logged_in():
		return redirect("/") 
	else:
		form = RegistrationForm(request.form)		
		if form.validate() == False:
			print(form.errors) 

		if form.validate_on_submit():
			username = form.data["username"]
			email = form.data["email"]
			unique_check = User.unique_user_check(username,email)

			if unique_check:
				new_user = User()
				new_user.first_name = form.data["firstname"]
				new_user.last_name = form.data["lastname"]
				new_user.username = form.data["username"]
				new_user.birth_date = form.data["birth_date"]
				new_user.email = form.data["email"]
				password_hash = current_app.config['bcrypt'].generate_password_hash(form.data["password"]).decode('utf-8')
				new_user.password = password_hash
				new_user.is_admin = False
				new_user.is_banned = False
				new_user.creation_date = datetime.utcnow()
				new_user.save()
				return "User has successfully signed up."
			else:
				return "This username or email address is already in use."
		else:
			return render_template('register.html', form=form, error = "Invalid field, please check again.")

	return render_template('register.html', form=form)


@user_page.route('/user/profile/<int:id>', methods = ['GET', 'POST'])
def profile_page(id):
	try:
		user = User(id)
		return render_template('profile.html', username = user.username, first_name = user.first_name, last_name = user.last_name, birth_date = user.birth_date, creation_date = user.creation_date, posts = Post.get_user_post(user.id))

	except (NotImplementedError) as error:
		flash('Error: ' + error)
		return redirect("/") 




