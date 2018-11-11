from flask import Blueprint, render_template,request, jsonify, session, redirect
import os
import sys
sys.path.append("../..") # Adds higher directory to python modules path.
from utils import logged_in as check
from models import user as model

page = Blueprint('page', __name__,)

@page.route('/user/login')
def login():
	return "login"

@page.route('/user/logout')
def logout():
	return "logout"

@page.route('/user/register')
def register():
	if check.logged_in():
		return redirect("/") #If user is logged in redirect it to homepage.
	else:
		insertUser = model.User(None)
		insertUser.add_user('John', 'Doe', '1997-06-24 00:00:00', 'Johnny', 'xd', 'jdoe@hotmail.de') #User register
		return "Welcome " + insertUser.username
	req = request.json


#def show(page):	use for html connection
#   try:
#        return render_template('pages/%s.html' % page)
#    except TemplateNotFound:
#        abort(404)