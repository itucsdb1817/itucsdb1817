from flask import Blueprint, render_template,request, jsonify, session, redirect, flash,current_app
from flask_bcrypt  import Bcrypt
import os
import sys
from datetime import datetime
sys.path.append("../..") # Adds higher directory to python modules path.
from utils import logged_in as check
from utils import admin_logged_in as admin_check
from models.user import User 
from models.post import Post 
from models.vote import Vote 
from models.tag import Tag 
from models.comment import Comment 
from models.report import Report 
from routes.user.forms import LoginForm
from routes.user.forms import RegistrationForm
from routes.user.forms import PasswordForm

user_page = Blueprint('user_page', __name__,)

#If user is not already logged in checks if
#password is correct.
@user_page.route('/', methods = ['GET', 'POST'])
def index():
    id = session.get("user_id","")
    return render_template("index.html", id = id, loggedin=check.logged_in(), tags=Tag.get_all(), pagination=Post.paginate(int(request.args.get('page') or 1)))
@user_page.route('/user/login', methods = ['GET', 'POST'])
def login():
    if check.logged_in():
        return redirect("/") 
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        user = User.get_from_username(username)	

        if user is not None:
            if user.is_banned is True:
                flash({'text': "You are banned from Accio, you can not sign in.", 'type': "error"}) 
                return redirect("/")
            password = form.data["password"]
            password_hash = user.password
            if current_app.config['bcrypt'].check_password_hash(password_hash, password):
                session['user_id'] = user.id
                flash({'text': "You have successfully logged in.", 'type': "success"}) 
                return redirect("/")
            else:
                return render_template("login.html", form=form,error = "Incorrect password.")
        else:
            return render_template("login.html", form=form,error = "Incorrect username or password.")
    return render_template("login.html", form=form)


@user_page.route('/user/logout')
def logout():
    session.pop("user_id",None)
    flash({'text': "You have successfully logged out.", 'type': "success"}) 
    return redirect("/")


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
                new_user.date = datetime.utcnow()
                new_user.save()
                flash({'text': "You have successfully signed up!", 'type': "success"}) 
                return redirect("/")
            else:
                return render_template('register.html', form=form, error = "This username or e-mail is already in use, please try another one.")
        else:
            if request.method == "POST":
                return render_template('register.html', form=form, error = ", field, please check again.")
            else:
                return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@user_page.route('/user/profile/<int:id>', methods = ['GET', 'POST'])
def profile_page(id):
    try:
        admin = False
        ban = False
        self_profile = False
        if check.logged_in():
            if id == session.get("user_id",""):
                self_profile = True
        if admin_check.admin_logged_in():
            admin = True
        user = User(id)
        if user.is_banned == True:
        	ban = True
       	
        parent_list = []
        for vote in Vote.get_user_total_votes(user.id):
        	if vote.is_comment == 1:
        		parent_list.append(Comment(vote.comment_id))
        	elif vote.is_comment == 0:
        		parent_list.append(Post(vote.post_id))


        return render_template('profile.html',id=user.id, username = user.username, first_name = user.first_name, last_name = user.last_name, birth_date = user.birth_date, creation_date = user.date, posts = Post.get_user_post(user.id),email= user.email, self_profile = self_profile, total_votes = Vote.get_user_total_votes(user.id), comments = Comment.get_user_total_comments(user.id), reports = Report.get_user_all_reports(user.id), parent_list = parent_list, admin=admin, ban= ban)

    except NotImplementedError as error:
        flash("Error: " + str(error))
        return redirect("/") 


@user_page.route('/user/change_password', methods = ['GET', 'POST'])
def change_password():
    if check.logged_in():
        form = PasswordForm()
        if form.validate_on_submit():
            user = User(session.get("user_id",""))
            password = form.data["old_password"]
            password_hash = user.password
            if current_app.config['bcrypt'].check_password_hash(password_hash, password):
                user.update_password(current_app.config['bcrypt'].generate_password_hash(form.data["new_password"]).decode('utf-8'))
                return render_template('change_password.html', form=form, success = "Your password has been updated.")
            else:
                return render_template('change_password.html', form=form, error = "Incorrect password.")
        else:
            if request.method == "POST":
                return render_template('change_password.html', form=form, error = "Invalid field, please check again.")
            else:
                return render_template('change_password.html', form=form)
    else:
        flash({'text': "You have to sign in to change your password.",'type':'is-warning'})
        return redirect("/user/login")


@user_page.route('/user/reports/<int:id>', methods = ['GET', 'POST'])
def show_reports(id):
    if check.logged_in():
        if id == session.get("user_id",""):
            return render_template('user_reports.html', report_list = Report.get_user_all_reports(id))
        else:
            flash({'text': "You can not view another user's reports", 'type': "error"}) 
            return redirect("../")
    else:
        flash({'text': "You have to sign in to view your reports.", 'type': "error"}) 
        return redirect("/")











