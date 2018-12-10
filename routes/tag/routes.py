import sys
from flask import Blueprint, render_template, request, jsonify, session, redirect, flash, current_app, url_for, flash
from datetime import datetime, date
sys.path.append('../..')
from utils import logged_in as check
from utils import md
from models.post import Post
from models.user import User
from forms import TagCreationForm, TagEditForm

tag_pages = Blueprint('tag_pages', __name__,)

@tag_pages.route('/tag_create')
def tag_create():
    raise NotImplementedError()

@tag_pages.route('/t/<string:tag_name>')
def tag_view():
    raise NotImplementedError()

@tag_pages.route('/t/<string:tag_name>/mod')
def tag_moderate():
    raise NotImplementedError()