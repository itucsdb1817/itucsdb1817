from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', [validators.required()])
