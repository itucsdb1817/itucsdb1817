from flask import Blueprint, render_template, request, jsonify, session, redirect, flash, current_app
from datetime import datetime
sys.path.append("../..") # Adds higher directory to python modules path.

post_pages = Blueprint('post_pages', __name__, template_folder = 'templates')

@post_pages.route('/post/<post_id>')
def post_view(post_id):
    # get post info by id, 
    # render post block
    # TO DO AFTER:
    # expose comment input
    # get all comments
    # group comments (nesting)
    # sort comments by opt

    NotImplementedError()

@post_pages.route('/post/submit')
def post_submit():
    NotImplementedError()