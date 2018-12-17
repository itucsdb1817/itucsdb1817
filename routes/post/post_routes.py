import sys
from flask import Blueprint, render_template, request, jsonify, session, redirect, flash, current_app, url_for, flash
from datetime import datetime
sys.path.append("../..") # Adds higher directory to python modules path.
from utils import logged_in as check
from utils import md
from models.post import Post
from models.user import User
from models.tag import Tag, TagModerator
from models.comment import Comment
from routes.post.post_forms import TextPostForm, TextPostEditForm, DeleteForm
from routes.post.comment_forms import CommentForm

post_pages = Blueprint('post_pages', __name__,)

@post_pages.route('/post/<int:post_id>', methods=['GET', 'POST'])
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
        # get post object with all comments
        post = Post(post_id, True)
    except:
        error_context = {
            'error_name': "404 Not Found",
            'error_info': "The post you tried to access does not exist"
        }
        return render_template('error.html', **error_context)
    
    form = CommentForm()
    if form.validate_on_submit():
        if not check.logged_in():
            error_context = {
                'error_name': "403 Forbidden",
                'error_info': "You may not comment without an account. Please log in or create an account"
            }
            return render_template('error.html', **error_context)
        # create comment
        comment = Comment()
        comment.user_id = session['user_id']
        comment.post_id = post_id
        comment.content_type = 'text'
        comment.content = form.content.data
        comment.content_html = md.render(form.content.data)
        comment.is_external = False
        comment.rank_score = 0
        comment.date = datetime.now()
        comment.current_vote = 0
        
        comment.save()

        post.comment_count += 1
        post.save()

        flash('Comment created successfuly')
        # reload page with the new comment
        return redirect(url_for('post_pages.post_view', post_id=post_id))

    context = post.generate_context()
    # sets flag if viewer is logged in
    context['is_logged_in'] = check.logged_in()
    # sets flag if viewer is the original poster (a.k.a OP)
    context['is_op'] = context['is_logged_in'] and (post.user_id == session['user_id'])
    if not context['is_op']:
        context['is_op'] = context['is_logged_in'] and TagModerator.is_mod(session['user_id'], post.tag_id)

    return render_template('post.html', **context, form=form)


# TODO: Implement different types of posts
@post_pages.route('/post/submit', methods=['GET', 'POST'])
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
            'error_info': "You may not post without an account. Please log in or create an account"
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
            post.content_type = form.content_type.data
            post.content = form.content.data
            post.content_html = md.render(form.content.data)
            # TODO: Implement external links
            post.is_external = False
            post.current_vote = 0
            post.rank_score = 0
            post.is_banned = False
            post.comment_count = 0
            # TODO: Implement tag existance check
            #       This should be done with custom validator after tags are created
            try:
                tag = Tag(form.tag.data)
                print(form.tag.data)
                post.tag_id = tag.id
            except NotImplementedError as error:
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

@post_pages.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def post_edit(post_id):
    # check if post exists
    try:
        post = Post(post_id, False)
    except:
        error_context = {
            'error_name': "404 Not Found",
            'error_info': "The post you tried to access does not exist"
        }
        return render_template('error.html', **error_context)
    
    # check if user is logged in
    if not check.logged_in():
        error_context = {
            'error_name': "Unauthorized",
            'error_info': "You must log in first"
        }
        return render_template('error.html', **error_context)

    # check if user is OP
    if not (post.user_id == session['user_id']):
        error_context = {
            'error_name': "Unauthorized",
            'error_info': "You are not the original poster"
        }
        return render_template('error.html', **error_context)

    # get POST input
    form = TextPostEditForm(content=post.content)
    if form.validate_on_submit():
        post.content = form.content.data
        post.content_html = md.render(form.content.data)
        post.save()

        flash("Post edited successfully")
        return redirect(url_for('post_pages.post_view', post_id=post_id))

    return render_template('post_text_edit.html', form=form, body=post.content, name="Post")

@post_pages.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
def post_delete(post_id):
    try:
        post = Post(post_id, False)
    except:
        error_context = {
            'error_name': "404 Not Found",
            'error_info': "The post you tried to access does not exist"
        }
        return render_template('error.html', **error_context)
    
    # check if user is logged in
    if not check.logged_in():
        error_context = {
            'error_name': "Unauthorized",
            'error_info': "You must log in first"
        }
        return render_template('error.html', **error_context)

    # check if user is OP
    if not (post.user_id == session['user_id']):
        error_context = {
            'error_name': "Unauthorized",
            'error_info': "You are not the original poster"
        }
        return render_template('error.html', **error_context)
    
    form = DeleteForm()
    if form.validate_on_submit():
        if form.yes.data:
            post.delete()
            flash("Post deleted succesfully")
            return redirect('/')
        else:
            flash("Post deletion cancelled")
            return redirect(url_for('post_pages.post_view', post_id=post_id))

    return render_template('post_delete.html', form=form, name="Post")

@post_pages.route('/comment/<int:comment_id>/edit', methods=['GET', 'POST'])
def comment_edit(comment_id):
    # check if post exists
    try:
        comment = Comment(comment_id)
    except:
        error_context = {
            'error_name': "404 Not Found",
            'error_info': "The comment you tried to access does not exist"
        }
        return render_template('error.html', **error_context)
    
    # check if user is logged in
    if not check.logged_in():
        error_context = {
            'error_name': "Unauthorized",
            'error_info': "You must log in first"
        }
        return render_template('error.html', **error_context)

    # check if user is OP
    if not (comment.user_id == session['user_id']):
        error_context = {
            'error_name': "Unauthorized",
            'error_info': "You are not the original poster of this comment"
        }
        return render_template('error.html', **error_context)

    # get POST input
    form = CommentForm(content=comment.content)
    if form.validate_on_submit():
        comment.content = form.content.data
        comment.content_html = md.render(form.content.data)
        comment.save()

        flash("Comment edited successfully")
        return redirect(url_for('post_pages.post_view', post_id=comment.post_id))

    return render_template('post_text_edit.html', form=form, body=comment.content, name="Comment")

@post_pages.route('/comment/<int:comment_id>/delete', methods=['GET', 'POST'])
def comment_delete(comment_id):
    try:
        comment = Comment(comment_id)
    except:
        error_context = {
            'error_name': "404 Not Found",
            'error_info': "The comment you tried to access does not exist"
        }
        return render_template('error.html', **error_context)
    
    # check if user is logged in
    if not check.logged_in():
        error_context = {
            'error_name': "Unauthorized",
            'error_info': "You must log in first"
        }
        return render_template('error.html', **error_context)

    # check if user is OP
    if not (comment.user_id == session['user_id']):
        error_context = {
            'error_name': "Unauthorized",
            'error_info': "You are not the original poster"
        }
        return render_template('error.html', **error_context)
    
    form = DeleteForm()
    if form.validate_on_submit():
        if form.yes.data:
            comment.delete()
            flash("Comment deleted succesfully")
            return redirect('/')
        else:
            flash("Comment deletion cancelled")
            return redirect(url_for('post_pages.post_view', post_id=comment.post_id))

    return render_template('post_delete.html', form=form, name="Comment")
