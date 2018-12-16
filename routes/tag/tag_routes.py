import sys
from flask import Blueprint, render_template, request, jsonify, session, redirect, flash, current_app, url_for, flash
from datetime import datetime, date
sys.path.append('../..')
from utils import logged_in as check
from utils import md
from models.post import Post
from models.user import User
from models.tag import Tag, TagModerator
from routes.tag.tag_forms import TagCreationForm, TagEditForm

tag_pages = Blueprint('tag_pages', __name__,)

@tag_pages.route('/tag_create', methods = ['GET', 'POST'])
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

            # TODO: tag name sanitization
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

            flash('New tag created')
            # TODO: Redirect to tag page
            return render_template('tag_create.html', form=form)
        else:
            return render_template('tag_create.html', form=form)

@tag_pages.route('/t/<string:tag_name>', methods = ['GET'])
def tag_view(tag_name):
    tag = Tag(tag_name)
    # existance of the attributes _ORIGINAL_ATTR denotes the model instance
    # is not new and interfaces an entry in table
    if not hasattr(tag, '_ORIGINAL_ATTR'):
        error_context = {
            'error_name': "404 Not Found",
            'error_info': "The tag you tried to access does not exist, but you can create this tag."
        }
        return render_template('error.html', **error_context)
    
    # TODO: Implement tag page and pagination
    page_index = int(request.args.get('page'))
    if not isinstance(page_index, int):
        page_index = 1
    if page_index <= 0:
        page_index = 1
    
    context = { 
        'tag_info': {
            'title':        tag.title,
            'rules':        tag.rules,
            'description':  tag.description
        }
    }
    context['pagination'] = tag.paginate(page_index)
    return render_template('tag.html', **context)


@tag_pages.route('/t/<string:tag_name>/mod')
def tag_moderate():
    raise NotImplementedError()