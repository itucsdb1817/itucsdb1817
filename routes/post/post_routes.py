from flask import Blueprint, render_template, request, jsonify, session, redirect, flash, current_app
from datetime import datetime
sys.path.append("../..") # Adds higher directory to python modules path.

post_pages = Blueprint('post_pages', __name__, template_folder = 'templates')

@post_pages.route('/post/<post_id>')
def post_view(post_id):
    # get post info by id, 
    # render post main
    NotImplementedError()

@post_pages.route('/post/submit')
def post_submit():
    NotImplementedError()