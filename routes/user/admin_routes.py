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
from models.report import Report
from routes.user.forms import LoginForm
from routes.user.forms import RegistrationForm
from routes.user.forms import PasswordForm
from routes.user.forms import ReviewForm

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

@admin_user_page.route('/admin/logout')
def logout():
    session.pop("admin_user_id",None)
    flash({'text': "You have successfully logged out.", 'type': "success"}) 
    return redirect("/")


@admin_user_page.route('/admin/reports', methods = ['GET', 'POST'])
def show_reports():
    if check.admin_logged_in():
        return render_template('admin_reports.html', report_list = Report.get_reports())
    else:
        flash({'text': "You have to sign in to your admin account first.", 'type': "error"}) 
        return redirect("/admin/login")


@admin_user_page.route('/admin/reports/<int:id>', methods = ['GET', 'POST'])
def review_reports(id):
    if check.admin_logged_in():
        form = ReviewForm(request.form)
        
        if form.validate_on_submit():
            report = Report(id)
            action = form.data["action_taken"]
            is_dismissed = form.data["is_dismissed"]
            report.update_for_review(action,is_dismissed)
            return redirect("../")
        else:
            if request.method == "POST":
                return render_template('admin_review.html', form=form, error = "Invalid, field, please check again.")
            else:
                return render_template('admin_review.html', form=form)
    else:
        flash({'text': "You have to sign in to your admin account first.", 'type': "error"}) 
        return redirect("/admin/login")

@admin_user_page.route('/admin/ban/<int:id>', methods = ['GET', 'POST'])
def ban_user(id):
    try:
        user = User(id)
        if user.is_banned == False:
            user.is_banned = True
        else:
            user.is_banned = False
        user.save()
        return redirect("/user/profile/"+str(id))
    except NotImplementedError as error:
        flash({'text': "This account does not exist.", 'type': "Error:" + str(error)}) 
        return redirect("/")

@admin_user_page.route('/admin/view_users', methods = ['GET', 'POST'])
def view_users():
    if check.admin_logged_in():
        return render_template('user_review.html', list_of_users = User.get_all_user())
    else:
        return redirect("/admin/login")
