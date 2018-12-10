import sys
from flask import Blueprint, render_template, request, jsonify, session, redirect, flash, current_app, url_for, flash
from datetime import datetime
sys.path.append("../..") # Adds higher directory to python modules path.
from utils import logged_in as check
from utils import md
from models.post import Post
from models.user import User
from models.tag import Tag
from routes.post.post_forms import TextPostForm

post_pages = Blueprint('post_pages', __name__,)

@post_pages.route('/post/<int:post_id>')
def post_view(post_id):
    # get post info by id, 
    # render post block
    # TO DO AFTER:
    # expose comment input
    # get all comments
    # group comments (nesting)
    # sort comments by opt
    """
    Expand this DOCSTRING
    """
    try:
        post = Post(post_id)
    except:
        error_context = {
            'error_name': "404 Not Found",
            'error_info': "The post you tried to access does not exist"
        }
        return render_template('error.html', **error_context)

    context = {
        'meta': {
            'user':     User(post.user_id).username,
            'date':     post.date,
            'vote':     post.current_vote,
            'comment':  post.comment_count
        },
        'post': {
            'id':       post.id,
            'title':    post.title,
            'body':     post.content
        }
    }

    return render_template('post.html', **context)


@post_pages.route('/post/<post_id>/<comment_id>')
def comment_permalink_view(post_id, comment_id):
    """
    This view is the permanant view for the comment chain starting from the supplied id.
    It only renders the post, given comment, and its children
    """
    raise NotImplementedError()

# TODO: Implement different types of posts
@post_pages.route('/post/submit', methods = ['GET', 'POST'])
def post_submit():
    """
    This view is for submitting posts. An account is required for submitting posts.
    Get parameters supply the tag name, e.g. a link from the tag page to post with that tag.
    Post request receive the form submission
    """
    # Forbid submission of post if user is not logged in
    if not check.logged_in():
        error_context = {
            'error_name': "403 Forbidden",
            'error_info': "You many not post without an account. Please log in or create an account"
        }
        return render_template('error.html', **error_context)
    # User is logged in, show text submission form
    else:
        form = TextPostForm()

        if form.validate_on_submit():
            post = Post()
            post.user_id = int(session['user_id'])
            post.date = datetime.now()
            post.title = form.title.data
            post.content_type = 'text'
            post.content = md.render(form.content.data)
            # TODO: Implement external links
            post.is_external = False
            post.current_vote = 0
            post.rank_score = 0
            post.is_banned = False
            post.comment_count = 1
            # TODO: Implement tag existance check
            #       This should be done with custom validator after tags are created
            tag = Tag(form.tag.data)
            if hasattr(tag, _ORIGINAL_ATTR):
                post.tag_id = tag.id
            else:
                error_context = {
                    'error_name': "INVALID TAG",
                    'error_info': "the tag you entered is invalid"
                }
                return render_template('error.html', **error_context)

            post.save()

            flash('Post created sucessfully')
            return redirect(url_for('post_pages.post_view', post_id=post.id))
            
        else:
            return render_template('post_text_submit.html', form=form)