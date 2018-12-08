import sys
from flask import Blueprint, render_template, request, jsonify, session, redirect, flash, current_app
from datetime import datetime
sys.path.append("../..") # Adds higher directory to python modules path.
from utils import logged_in as check

post_pages = Blueprint('post_pages', __name__,)

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

@post_pages.route('/post/<post_id>/<comment_id>')
def comment_permalink(post_id, comment_id):
    """
    This view is the permanant view for the comment chain starting from the supplied id.
    It only renders the post, given comment, and its children
    """
    NotImplementedError()

@post_pages.route('/post/submit')
def post_submit():
    """
    This view is for submitting posts. An account is required for submitting posts.
    """
    if not check.logged_in():
        error_context = {
            'error_name': "403 Forbidden",
            'error_info': "You many not post without an account. Please log in or create an account"
        }
        return render_template('error.html', **error_context)
    else:
        return render_template('error.html', error_type="OK", error_info="OK")