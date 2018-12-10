import sys
from flask import Blueprint, render_template, request, jsonify, session, redirect, flash, current_app, url_for, flash
from datetime import datetime, date
sys.path.append('../..')
from utils import logged_in as check
from utils import md
from models.post import Post
from models.user import User
from models.tag import Tag, TagModerator
from forms import TagCreationForm, TagEditForm

tag_pages = Blueprint('tag_pages', __name__,)

@tag_pages.route('/tag_create')
def tag_create():
    if not check.logged_in():
        error_context = {
            'error_name': "403 Forbidden",
            'error_info': "You may not create a tag without an account. Please log in or create an account"
        }
        return render_template('error.html', **error_context)
    else:
        form = TagCreationForm()
        if form.validate_on_submit():
            tag = Tag()
            mod = TagModerator()

            tag.title = form.title.data
            tag.date = datetime.now()
            tag.subscriber_amount = 0
            tag.is_banned = False
            tag.description = form.description.data
            tag.rules = form.rules.data

            tag.save()

            # exact same date of creation denotes original creator
            mod.date = tag.date
            mod.user_id = int(session['user_id'])
            mod.tag_id = tag.id

            mod.save()

            # TODO: Redirect to tag page

        else:
            # TODO: Render form
            raise NotImplementedError()

@tag_pages.route('/t/<string:tag_name>')
def tag_view():
    raise NotImplementedError()

@tag_pages.route('/t/<string:tag_name>/mod')
def tag_moderate():
    raise NotImplementedError()