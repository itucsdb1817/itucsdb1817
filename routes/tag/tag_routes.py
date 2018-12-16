import sys
from flask import Blueprint, render_template, request, jsonify, session, redirect, flash, current_app, url_for, flash
from datetime import datetime, date
sys.path.append('../..')
from utils import logged_in as check
from utils import md
from models.post import Post
from models.user import User
from models.tag import Tag, TagModerator
from routes.tag.tag_forms import TagCreationForm, TagEditForm, TagModForm

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

@tag_pages.route('/t/<string:tag_name>', methods=['GET'])
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
def tag_moderate(tag_name):
    """Main moderation view for tags"""
    if not check.logged_in():
        error_context = {
            'error_name': "Forbidden",
            'error_info': "You may not access this page without logging in"
        }
        return render_template('error.html', **error_context)

    try:
        tag = Tag(tag_name)
    except:
        error_context = {
            'error_name': "404 Not Found",
            'error_info': "The tag you tried to access does not exist, but you can create this tag."
        }
        return render_template('error.html', **error_context)

    if not TagModerator.is_mod(session['user_id'], tag.id):
        error_context = {
            'error_name': "Access Denied",
            'error_info': "You are not a moderator of this tag"
        }
        return render_template('error.html', **error_context)

    add_mod_form = TagModForm()
    remove_mod_form = TagModForm()
    edit_tag_form = TagEditForm(description=tag.description, rules=tag.rules)

    return render_template(
        'tag_mod.html',
        add_mod_form=add_mod_form,
        remove_mod_form=remove_mod_form,
        edit_tag_form=edit_tag_form
        # CONTEXT
    )


@tag_pages.route('/t/<string:tag_name>/mod/add', methods=['GET', 'POST'])
def tag_moderate_add_mod(tag_name):
    """Form processor for adding new moderators
    """
    try:
        tag = Tag(tag_name)
    except:
        error_context = {
            'error_name': "404 Not Found",
            'error_info': "The tag you tried to access does not exist, but you can create this tag."
        }
        return render_template('error.html', **error_context)

    if not check.logged_in():
        error_context = {
            'error_name': "Forbidden",
            'error_info': "You may not access this page without logging in"
        }
        return render_template('error.html', **error_context)

    if not TagModerator.is_mod(session['user_id'], tag.id):
        error_context = {
            'error_name': "Access Denied",
            'error_info': "You are not a moderator of this tag"
        }
        return render_template('error.html', **error_context)

    form = TagModForm()
    if form.validate_on_submit():
        username_to_add = form.user.data
        if username_to_add:
            try:
                user = User.get_from_username(username_to_add)
            except:
                flash('User does not exist')
                return redirect(url_for('tag_pages.tag_moderate', tag_name=tag_name))
            if TagModerator.is_mod(user.id, tag.id):
                flash('User is already a mod')
                return redirect(url_for('tag_pages.tag_moderate', tag_name=tag_name))
            if user.id == session['user_id']:
                flash('You are already a mod')
                return redirect(url_for('tag_pages.tag_moderate', tag_name=tag_name))
            if user.is_banned:
                flash('You may not add a banned user as mod')
                return redirect(url_for('tag_pages.tag_moderate', tag_name=tag_name))
            tag.mod_add_user(user.id)
            flash('User added as mod successfully')
            return redirect(url_for('tag_pages.tag_moderate', tag_name=tag_name))
        else:
            flash('Invalid Input')
            return redirect(url_for('tag_pages.tag_moderate', tag_name=tag_name))
    
    # empty access, return
    return redirect(url_for('tag_pages.tag_moderate', tag_name=tag_name))

@tag_pages.route('/t/<string:tag_name>/mod/remove', methods=['GET', 'POST'])
def tag_moderate_remove_mod(tag_name):
    """Form processor for removing existing moderators
    """
    try:
        tag = Tag(tag_name)
    except:
        error_context = {
            'error_name': "404 Not Found",
            'error_info': "The tag you tried to access does not exist, but you can create this tag."
        }
        return render_template('error.html', **error_context)

    if not check.logged_in():
        error_context = {
            'error_name': "Forbidden",
            'error_info': "You may not access this page without logging in"
        }
        return render_template('error.html', **error_context)

    if not TagModerator.is_mod(session['user_id'], tag.id):
        error_context = {
            'error_name': "Access Denied",
            'error_info': "You are not a moderator of this tag"
        }
        return render_template('error.html', **error_context)

    form = TagModForm()
    if form.validate_on_submit():
        username_to_remove = form.user.data
        if username_to_remove:
            try:
                user = User.get_from_username(username_to_remove)
            except:
                flash('User does not exist')
                return redirect(url_for('tag_pages.tag_moderate', tag_name=tag_name))
            if not TagModerator.is_mod(user.id, tag.id):
                flash('Specified user is not a mod')
                return redirect(url_for('tag_pages.tag_moderate', tag_name=tag_name))
            if user.id == session['user_id']:
                flash('You may not delete yourself as a mod')
                return redirect(url_for('tag_pages.tag_moderate', tag_name=tag_name))
            tag.mod_remove_user(user.id)
            flash('User removed as mod successfully')
            return redirect(url_for('tag_pages.tag_moderate', tag_name=tag_name))
        else:
            flash('Invalid Input')
            return redirect(url_for('tag_pages.tag_moderate', tag_name=tag_name))

    return redirect(url_for('tag_pages.tag_moderate', tag_name=tag_name))

@tag_pages.route('/t/<string:tag_name>/mod/edit_info', methods=['GET', 'POST'])
def tag_moderate_edit_info(tag_name):
    try:
        tag = Tag(tag_name)
    except:
        error_context = {
            'error_name': "404 Not Found",
            'error_info': "The tag you tried to access does not exist, but you can create this tag."
        }
        return render_template('error.html', **error_context)

    if not check.logged_in():
        error_context = {
            'error_name': "Forbidden",
            'error_info': "You may not access this page without logging in"
        }
        return render_template('error.html', **error_context)

    if not TagModerator.is_mod(session['user_id'], tag.id):
        error_context = {
            'error_name': "Access Denied",
            'error_info': "You are not a moderator of this tag"
        }
        return render_template('error.html', **error_context)
    
    form = TagEditForm()
    if form.validate_on_submit():
        tag.description = form.description.data
        tag.rules = form.rules.data
        tag.save()
        flash('Tag info saved')

    return redirect(url_for('tag_pages.tag_moderate', tag_name=tag_name))
    

